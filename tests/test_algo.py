
import os
import json

from algorithm.wrapped import minimize_cost

class TestAlgo: 
    @staticmethod
    def run(input_params): 
        print(json.dumps(minimize_cost(**input_params), ensure_ascii=False, indent=4))

if __name__ == "__main__": 
    pth = os.path.join(os.path.dirname(__file__), "input_example.json")
    with open(pth, "r", encoding="utf-8") as f: 
        input_params = json.load(f)
    TestAlgo.run(input_params)