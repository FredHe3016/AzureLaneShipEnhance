
import os
import json

from algorithm.wrapped import minimize_cost
from algorithm.utils import adapt_material_input

class TestAlgo: 
    @staticmethod
    def run(input_params): 
        print(json.dumps(minimize_cost(**input_params), ensure_ascii=False, indent=4))

    def adapt_input(materials: str): 
        print(adapt_material_input(materials))

if __name__ == "__main__": 
    pth = os.path.join(os.path.dirname(__file__), "input_example.json")
    with open(pth, "r", encoding="utf-8") as f: 
        input_params = json.load(f)
    TestAlgo.run(input_params)
    # TestAlgo.adapt_input("卡辛 唐斯 克雷文 麦考尔 奥利克 富特 斯彭斯 奥马哈 罗利 彭萨科拉 盐湖城 内华达 俄克拉荷马 博格 兰利 突击者 小猎兔犬 大斗犬 彗星 新月 小天鹅 狐提 利安得 竞技神 不知火 长良 阿武隈 古鹰 加古 青叶 衣笠 柯尼斯堡 卡尔斯鲁厄 科隆 Z20 Z21 睦月 10 如月 卯月 水无月 三日月 里士满")
    ...