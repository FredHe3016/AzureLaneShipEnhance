import tkinter as tk
from tkinter import ttk
from functools import cache, wraps

from typing import ParamSpec, TypeVar, Callable, Any

_P = ParamSpec("P")
_T = TypeVar("_T")

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
    entry.config(foreground="black" if is_valid(entry.get()) else "red")

def decorator(func: Callable[_P, _T]) -> Callable[[Any], Callable[_P, _T]]:
    def decorated(f): 
        def wrapper(*args, **kwargs): 
            return f(*args, **kwargs)
        return wrapper
    return decorated

pack_decorator = decorator(object.__new__(tk.Widget).pack_configure)
