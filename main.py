import traceback
import json
from typing import Dict, Any

from algorithm.wrapped import minimize_cost

def main_func(input_data: Dict[str, Any]):
    try: 
        res = minimize_cost(**input_data) 
        success = True
    except Exception as e: 
        res = traceback.format_exc()
        success = False
    return json.dumps({
        "success": success, 
        "result": res
    })

# def minimize_cost(
#     target_ship: Dict[str, Any], 
#     material_ships: Dict[str, int], 
#     medal_weight: int, 
#     sc_weight: int
# ): 
    
#     solver_config = EnhanceSolverConfig(medal_weight=medal_weight, sc_weight=sc_weight)
#     solver = EnhanceCostMinimizer(target_ship=target_ship, material_ships=material_ships, config=solver_config)
#     res = solver.run()
#     return json.dumps(res, indent=4, ensure_ascii=False)
