# import json
from typing import Dict, Any

from algorithm.solver import EnhanceCostMinimizer
from algorithm.utils import EnhanceSolverConfig

def minimize_cost(
    target_ship: Dict[str, Any], 
    material_ships: Dict[str, int], 
    medal_weight: int, 
    sc_weight: int
): 
    
    solver_config = EnhanceSolverConfig(medal_weight=medal_weight, sc_weight=sc_weight)
    solver = EnhanceCostMinimizer(target_ship=target_ship, material_ships=material_ships, config=solver_config)
    res = solver.run()
    return res
    # return json.dumps(res, indent=4, ensure_ascii=False)
