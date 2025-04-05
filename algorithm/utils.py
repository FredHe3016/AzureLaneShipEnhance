import pandas as pd
from dataclasses import dataclass
from functools import cache
from typing import Type, List, Dict, Any

from config import SHIP_DATA_PATH
from data.static import SHIP_CLS_COIN_MAP, RARITY_MEDAL_SC_MAP, STAT_TRANS, SHIP_CLS, RARITY

@cache
def cls_annots(cls: Type): 
    annots_list = [_.__annotations__.copy() for _ in cls.mro()[-2::-1]]
    annots = annots_list[0]
    for _ in annots_list[1:]: 
        annots.update(_)
    return annots

def adapt_ship_data(n: str, d: Dict[str, Any], num: int = -1): 
    d = d.copy()
    d["name"] = n
    d["max_num"] = num
    d["retire_coins"] = SHIP_CLS_COIN_MAP[d.pop(SHIP_CLS)]
    d.update(RARITY_MEDAL_SC_MAP[d.pop(RARITY)])
    nutri = {v: d.pop(k) for k, v in STAT_TRANS.items()}
    d["nutrition"] = nutri
    return d

def adapt_material_input(m_input: str): 
    material_ships = dict()

    m_input.replace('\n', ' ')
    ws = iter(m_input.split())
    _s = next(ws)
    for s in ws: 
        if s.isdigit() ^ _s.isdigit(): 
            raise ValueError("强化素材输入格式错误")
        elif s.isdigit(): 
            material_ships[_s] = int(s)
        else: 
            material_ships[s] = -1
    return material_ships

@dataclass
class EnhanceSolverConfig: 
    medal_weight: float = 1000      #勋章相对物资权重
    sc_weight: float = 0            #特装原型相对物资权重

    @classmethod
    def get_ships_data(cls, ships: Dict[str, int]): 
        data = []
        df = pd.read_excel(SHIP_DATA_PATH, sheet_name="Sheet1")
        for i in range(len(df)): 
            d = df.iloc[i].to_dict()
            if (n := d.pop("舰船名称")) not in ships: 
                continue
            d["name"] = n
            d["max_num"] = ships[n]
            d["retire_coins"] = SHIP_CLS_COIN_MAP[d.pop("舰船类型")]
            d.update(RARITY_MEDAL_SC_MAP[d.pop("稀有度")])
            nutri = {v: d.pop(k) for k, v in STAT_TRANS.items()}
            d["nutrition"] = nutri
            data.append(d)
        return data
