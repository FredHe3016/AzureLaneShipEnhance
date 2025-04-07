import itertools as it
import numpy as np
from functools import partial, cached_property
from dataclasses import dataclass, replace

from typing import Self, Any, List, Iterable

from algorithm.utils import cls_annots

@dataclass
class EnhanceStats:
    """强化所对应的强化/属性值等（用于写代码偷懒）"""
    fp: int = 0         #炮击
    trp: int = 0        #雷击
    avi: int = 0        #航空
    rld: int = 0        #装填
    
    @cached_property
    def array(self): 
        return np.array([self.fp, self.trp, self.avi, self.rld]).astype(object)

class _Ship:
    # 作为强化素材的相关属性
    nutrition: EnhanceStats     # 强化加成（营养成分？）
    retire_coins: int           # 退役物资
    medal: int = 0              # 退役勋章
    sc: int = 0                 # 特装原型
    max_num: int = -1           # 最大数量，-1代表不限量

class Ship(_Ship):
    name: str           #舰船名称

    cur_stats: EnhanceStats         #当前属性值
    max_stats: EnhanceStats         #满强化属性值
    nutri_per_lv: EnhanceStats      #属性升级所需强化值
    nutri_cur_lv: EnhanceStats      #当前等级已有强化值

    def __init__(self, name: str):
        self.name = name

    def value(self, tar_ship: Self | None = None):
        #同名船强化加成翻倍
        if tar_ship.name == self.name:
            return (*(self.nutrition.array * 2), self.retire_coins, self.medal, self.sc)
        return (*self.nutrition.array, self.retire_coins, self.medal, self.sc)

    @cached_property
    def nutri_requirements(self) -> EnhanceStats:
        """满强化所需最低强化值"""
        return EnhanceStats(
            *(self.nutri_per_lv.array * (self.max_stats.array - self.cur_stats.array) - self.nutri_cur_lv.array)
        )
    
    @classmethod
    def from_dict(cls, d: dict):
        name = d.pop("name")
        ship = cls(name)
        for k, v in d.items(): 
            if (tp := cls_annots(cls).get(k)) is None: 
                raise ValueError(f"{cls} should not have attribute {k}")
            if tp is EnhanceStats: 
                v = EnhanceStats(**{k: int(_) for k, _ in v.items()})
            setattr(ship, k, v)
        return ship

    @classmethod
    def target_ship(cls, d: dict): 
        d = d.copy()
        _ = d.pop("input_stats")
        d.update(_)
        return cls.from_dict(d)

class EnhanceMaterial(_Ship):
    ships: List[Ship]

    var_num: Any
    res_num: int

    # @property
    # def value(self):
    #     return (*self.nutrition, self.medal, self.sc)

    @cached_property
    def name(self): 
        return "/".join(s.name for s in self.ships)

    @property
    def max_num(self):
        if any(s.max_num < 0 for s in self.ships):
            return -1
        return sum(s.max_num for s in self.ships)

    @classmethod
    def from_ships(cls, tar_ship: Ship, ships: Iterable[Ship]) -> List[Self]:
        """合并作为强化素材没有区别的舰船"""
        materials = []

        eval = partial(Ship.value, tar_ship=tar_ship)
        grouped_ships = it.groupby(sorted(ships, key=eval), key=eval)
        for v, _ in grouped_ships:
            material = EnhanceMaterial()
            material.ships = list(_)
            material.nutrition = EnhanceStats(*v[:4])
            material.retire_coins, material.medal, material.sc = v[-3:]
            materials.append(material)

        return materials
