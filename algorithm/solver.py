import numpy as np
from dataclasses import replace, asdict
from typing import TYPE_CHECKING, List, Dict, Any, Callable

from ortools.linear_solver import pywraplp 

from .ship import Ship, EnhanceMaterial, EnhanceStats
from .utils import join_names, EnhanceSolverConfig
from data.static import STAT_TRANS

class EnhanceCostMinimizer: 
    solver: pywraplp.Solver

    def __init__(
        self, 
        target_ship: Dict[str, Any], 
        material_ships: Dict[str, int], 
        config: EnhanceSolverConfig
    ):
        self.solver = pywraplp.Solver.CreateSolver("SCIP")
        self.config = config
        self.target_ship = Ship.target_ship(target_ship)
        materials = list(map(Ship.from_dict, config.get_ships_data(material_ships)))
        self.materials = EnhanceMaterial.from_ships(self.target_ship, materials)

    def run(self): 
        self._create_variables()
        self._set_constraints()
        status = self._do_solve()
        if status == pywraplp.Solver.OPTIMAL: 
            self._apply_res()
        else: 
            raise Exception("failed to calculate the result")
        return self._output()
    
    def _output(self): 
        res_num: Callable[[EnhanceMaterial], int] = lambda m: m.res_num
        used_materials = list(filter(res_num, self.materials))
        used_materials.sort(key=res_num, reverse=True)
        for m in used_materials: 
            print((m.nutrition.array, m.res_num))
        sum_enhance = EnhanceStats(*sum((m.nutrition.array * m.res_num for m in used_materials), start=np.array([0,0,0,0]).astype(object)))
        return {
            "强化舰船": self.target_ship.name, 
            "所需强化值": {k: getattr(self.target_ship.nutri_requirements, v) for k, v in STAT_TRANS.items()}, 
            "推荐强化素材": {
                join_names([s.name for s in m.ships]): m.res_num for m in used_materials
            }, 
            "总计强化值": {k: getattr(sum_enhance, v) for k, v in STAT_TRANS.items()}, 
            "等价消耗资源": {
                "物资": sum(m.retire_coins * m.res_num for m in used_materials), 
                "勋章": sum(m.medal * m.res_num for m in used_materials),
                "特装原型": sum(m.sc * m.res_num for m in used_materials)
            }
        }

    def _create_variables(self):
        #创建强化素材的数量所对应变量
        for _  in self.materials: 
            if (max_num := _.max_num) < 0: 
                max_num = 2**32
            _.var_num = self.solver.IntVar(0, max_num, name=f"{_.ships[0].name}, ...")

    def _set_constraints(self): 
        #所需强化值
        nutri_req = self.target_ship.nutri_requirements
        #溢出强化值
        nutri_overflow = EnhanceStats(
            *(sum(m.nutrition.array * m.var_num for m in self.materials) - nutri_req.array)
        )
        #添加溢出强化值大于等于0的约束
        for k in EnhanceStats.__annotations__: 
            no = getattr(nutri_overflow, k)
            self.solver.Add(no >= -0.5, name=f"{k}_overflow")

    def _do_solve(self): 
        def cost(m: EnhanceMaterial): 
            return m.retire_coins + m.medal * self.config.medal_weight + m.sc * self.config.sc_weight
        #总计等价物资消耗
        total_cost = sum(cost(m) * m.var_num for m in self.materials)
        self.solver.Minimize(total_cost)
        return self.solver.Solve()

    def _apply_res(self): 
        for m in self.materials: 
            m.res_num = int(m.var_num.solution_value())
