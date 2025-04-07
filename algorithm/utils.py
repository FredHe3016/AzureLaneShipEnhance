import pandas as pd
from dataclasses import dataclass
from functools import cache
from typing import Type, List, Dict, Any

from config import SHIP_DATA_PATH
from data.static import SHIP_CLS_COIN_MAP, RARITY_MEDAL_SC_MAP, STAT_TRANS, INPUT_TRANS, SHIP_CLS, RARITY

@cache
def cls_annots(cls: Type): 
    annots_list = [_.__annotations__.copy() for _ in cls.mro()[-2::-1]]
    annots = annots_list[0]
    for _ in annots_list[1:]: 
        annots.update(_)
    return annots

def adapt_ship_data(n: str, d: Dict[str, Any], num: int = -1): 
    return {
        "name": n, 
        "max_num": num, 
        "retire_coins": SHIP_CLS_COIN_MAP[d[SHIP_CLS]], 
        **RARITY_MEDAL_SC_MAP[d[RARITY]], 
        "nutrition": d["attr_exp"]
    }

def adapt_material_input(m_input: str): 
    material_ships = dict()

    m_input.replace('\n', ',')
    m_input.replace('，', ',')
    for s in filter(bool, map(str.strip, m_input.split(","))): 
        l = [_s.strip() for _s in s.split("<=")]
        if len(l) == 1: 
            material_ships[s] = -1
        elif len(l) == 2 and l[1].isdigit(): 
            material_ships[l[0]] = int(l[1])
        else: 
            raise ValueError(f"强化素材输入格式错误{s}")
    return material_ships
