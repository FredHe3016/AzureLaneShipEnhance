import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Any, Callable

from ortools.linear_solver import pywraplp 

from algorithm.ship import Ship, EnhanceMaterial, EnhanceStats
from algorithm.utils import adapt_ship_data
from data.static import STAT_TRANS, ENHANCE_SHIP_NAME, REQ_ENHANCE, REC_MATERIAL, TOTAL_ENHANCE, EQ_RESOURCE, COIN, MEDAL, SPECIAL_CORE, TOTAL_WE
from data.data_loader import load_ships_data

@dataclass
class EnhanceSolverConfig: 
    medal_weight: float = 1000      #勋章相对物资权重
    sc_weight: float = 0            #特装原型相对物资权重

    @classmethod
    def get_ships_data(cls, ships: Dict[str, int]): 
        sd = load_ships_data()
        if _ := set(ships.keys()).difference(set(sd.keys())): 
            raise ValueError(f"缺少舰船强化值数据：{_}")
        return [adapt_ship_data(n, sd[n], num) for n, num in ships.items()]

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
        sum_enhance = EnhanceStats(*sum((m.nutrition.array * m.res_num for m in used_materials), start=np.array([0,0,0,0]).astype(object)))
        return {
            ENHANCE_SHIP_NAME: self.target_ship.name, 
            REQ_ENHANCE: {v: getattr(self.target_ship.nutri_requirements, k) for k, v in STAT_TRANS.items()}, 
            REC_MATERIAL: {
                m.name: m.res_num for m in used_materials
            }, 
            TOTAL_ENHANCE: {v: getattr(sum_enhance, k) for k, v in STAT_TRANS.items()}, 
            EQ_RESOURCE: (equal_rec := {
                COIN: sum(m.retire_coins * m.res_num for m in used_materials), 
                MEDAL: sum(m.medal * m.res_num for m in used_materials),
                SPECIAL_CORE: sum(m.sc * m.res_num for m in used_materials)
            }), 
            TOTAL_WE: equal_rec[COIN] + equal_rec[MEDAL] * self.config.medal_weight + equal_rec[SPECIAL_CORE] * self.config.sc_weight,
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
