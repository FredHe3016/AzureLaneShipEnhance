#一些不太需要随着游戏更新而更新的内容
import datetime

RARITY_MEDAL_SC_MAP = {
    "n": {"medal": 0, "sc": 0}, 
    "r": {"medal": 1, "sc": 0}, 
    "sr": {"medal": 4, "sc": 0}, 
    "ssr": {"medal": 10, "sc": 0}, 
    "ur": {"medal": 30, "sc": 500}, 
}

SHIP_CLS_COIN_MAP = {
    "驱逐": 12,
    "轻巡": 14,
    "重巡": 18,
    "战巡": 22,
    "战列": 26,
    "轻航": 16,
    "正航": 24,
    "潜艇": 10,
    "航巡": 18,
    "航战": 25,
    "雷巡": 15,
    "维修": 13,
    "重炮": 13,
    "潜母": 10,
    "超巡": 19,
    "运输": 11,
    "导驱": 12,
    "风帆S": 12,
    "风帆V": 14,
    "风帆M": 22
}

SHIP_NAME = "舰船名称"
RARITY = "稀有度"
SHIP_CLS = "舰船类型"

DATA_ENHANCR_TRANS = {
    "durability": "最大强化属性", 
    "level_exp": "每级强化值", 
    "attr_exp": "素材强化值", 
}

STAT_TRANS = {
    "fp": "炮击", 
    "trp": "雷击",
    "avi": "航空", 
    "rld": "装填", 
}

INPUT_TRANS = {
    "cur_stats": "当前属性", 
    "max_stats": "最大属性",
    "nutri_per_lv": "每级强化值",
    "nutri_cur_lv": "当前强化值",
}

TITLE = "舰船强化省钱小助手"

ENHANCE_SHIP_NAME = "强化舰船名称"
CUSTOMIZED_TAB = "自定义输入"
PREDEFINED_TAB = "预定义输入"
ENHANCE_STAT = "强化属性"
MATERIAL_SHIPS = "强化素材"
RETIRE_RES_WEIGHT = "其他退役资源权重"
RETIRE_RW_TRANS ={
    "勋章": "medal", 
    "特装原型": "sc"
}
CAL_BUTTON = "计算"
RESET_BUTTON = "重置"

REQ_ENHANCE = "所需强化值"
REC_MATERIAL = "推荐强化材料" 
TOTAL_ENHANCE = "总计强化值"
EQ_RESOURCE = "等价消耗资源"
COIN = "物资"
MEDAL = "勋章"
SPECIAL_CORE = "特装原型"

DEFAULT_FONT = ("Microsoft YaHei", 12)
SECTION_FONT = ("Microsoft YaHei", 13, "bold")
TEXT_FONT = ("Microsoft YaHei", 10)
