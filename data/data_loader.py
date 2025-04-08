import json
import pandas as pd
from functools import cache
from typing import Dict, Any, Literal

from data.static import SHIP_NAME, RARITY, DATA_ENHANCR_TRANS, STAT_TRANS, SHIP_CLS, SHIP_CLS_COIN_MAP, REQUISITE_RATES, RARITY_MEDAL_SC_MAP
from config import SHIP_DATA_PATH, EQUIP_DATA_PATH, REQUISITION_PATH

_SHEET_NAME = "Sheet1"

@cache
def load_ships_data() -> Dict[str, Dict[str, Any]]: 
    ship_data = dict()
    df = pd.read_excel(SHIP_DATA_PATH, sheet_name=_SHEET_NAME)
    for _ in df.iloc: 
        d = _.to_dict()
        for k, v in DATA_ENHANCR_TRANS.items(): 
            d[k] = {_k: d.pop(f"{v}_{_v}") for _k, _v in STAT_TRANS.items()}
        ship_data[d.pop(SHIP_NAME).strip()] = d
    return ship_data

def generate_material_ships(key: Literal["all", "drop_all", "drop_main"] | None = None): 
    match key: 
        case None: #XXX
            names = [k for k, v in load_ships_data().items() if v.get(RARITY) == "n"]
        case "all": 
            names = load_ships_data().keys()
        case _: 
            raise NotImplementedError
    return ", ".join(names)

@cache
def load_equip_data(): 
    
    equip_data = dict()
    df = pd.read_excel(EQUIP_DATA_PATH, sheet_name=_SHEET_NAME)
    for _ in df.iloc: 
        d = _.to_dict()
        equip_data[d.pop("id")] = d
    return equip_data
    
def requisition_expect(ndigits: int = 6): 
    with open(REQUISITION_PATH, 'r', encoding='utf-8') as f: 
        ships = json.load(f)
    ship_data = load_ships_data()
    equip_data = load_equip_data()

    ship_equip_keys = ["equip_id_1", "equip_id_2", "equip_id_3"]
    def _ship_retire_coin(d: dict): 
        coin = SHIP_CLS_COIN_MAP[d[SHIP_CLS]]
        for k in ship_equip_keys: 
            coin += equip_data[d[k]]["destory_gold"] if d[k] else 0
        return coin

    grouped_ships = {k: [] for k in REQUISITE_RATES}
    for s in ships: 
        grouped_ships[ship_data[s][RARITY]].append(s)
    
    medal_per_req = 6
    res_0 = sum(
        sum(
            map(_ship_retire_coin, [ship_data[n] for n in grouped_ships[rarity]])
        ) * rate / len(grouped_ships[rarity]) for rarity, rate in REQUISITE_RATES.items()
    ) / 100
    extra_medal = sum(RARITY_MEDAL_SC_MAP[rarity]["medal"] * rate for rarity, rate in REQUISITE_RATES.items()) / 100
    res = res_0 / (medal_per_req - extra_medal)

    return round(res, ndigits=ndigits)
