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

if __name__ == "__main__": 
    ...