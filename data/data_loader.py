import pandas as pd
from functools import cache
from typing import Dict, Any, Literal

from .static import SHIP_NAME, RARITY
from config import SHIP_DATA_PATH

_SHEET_NAME = "Sheet1"

@cache
def load_ships_data() -> Dict[str, Dict[str, Any]]: 
    ship_data = dict()
    df = pd.read_excel(SHIP_DATA_PATH, sheet_name=_SHEET_NAME)
    for _ in df.iloc: 
        d = _.to_dict()
        ship_data[d.pop(SHIP_NAME)] = d
    return ship_data

def generate_material_ships(key: Literal["all", "drop_all", "drop_main"] | None = None): 
    match key: 
        case None: #XXX
            names = [k for k, v in load_ships_data().items() if v.get(RARITY) == "n"]
        case "all": 
            names = load_ships_data().keys()
        case _: 
            raise NotImplementedError
    return " ".join(n for n in names)