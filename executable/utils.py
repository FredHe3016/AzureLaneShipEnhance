import os
import tkinter as tk
from tkinter import ttk
from functools import cache, wraps

from typing import ParamSpec, TypeVar, Callable, Any

from config import BASE_DIR

_P = ParamSpec("P")
_T = TypeVar("_T")

def get_info(): 
    with open(os.path.join(BASE_DIR, "README.md"), encoding="utf-8") as f: 
        text = f.read()
    info = ""
    key_words = ["简介", "项目仓库", "输入注意事项：", "待完成事项：", "其他计划："]
    for _ in text.split("## "): 
        if any(map(_.startswith, key_words)): 
            info += _
    return info

@cache
def ensure_digit_vcmd(root: tk.Tk): 
    def ensure_digit(s: str): 
        return s.isdigit() or s == ""
    return (root.register(ensure_digit), "%P")

def check_float_input(event: tk.Event): 
    #entry.bind("<KeyRelease>", check_float_input)
    def is_valid(s: str): 
        try: 
            f = s == "" or float(s)
        except: 
            return False
        return True
    entry: ttk.Entry = event.widget
    entry.config(foreground="#333333" if is_valid(entry.get()) else "red")

def decorator(func: Callable[_P, _T]) -> Callable[[Any], Callable[_P, _T]]:
    def decorated(f): 
        def wrapper(*args, **kwargs): 
            return f(*args, **kwargs)
        return wrapper
    return decorated

_widget = object.__new__(tk.Widget)
pack_decorator = decorator(_widget.pack_configure)
grid_decorator = decorator(_widget.grid_configure)
