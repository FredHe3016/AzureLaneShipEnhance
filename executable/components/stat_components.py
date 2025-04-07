#因为属性相关组件较多，因此单独抽出来

import tkinter as tk
from tkinter import ttk
from functools import cached_property

from executable.components.base import Component
from executable.utils import ensure_digit_vcmd
from data.static import STAT_TRANS, INPUT_TRANS, CUSTOMIZED_TAB, PREDEFINED_TAB, ENHANCE_STAT, SECTION_FONT

class _StatComp(Component): 
    var: tk.StringVar
    default_value: int

    _sub_comp_names = ("label", "entry")

    def __init__(self, root: ttk.Frame, text: str, default_value: int = 0):
        top_root = root.winfo_toplevel()
        self.frame = ttk.Frame(root)

        self.var = tk.StringVar(top_root, value=default_value)
        self.label = ttk.Label(self.frame, text=text)
        self.entry = ttk.Entry(
            self.frame, 
            textvariable=self.var, 
            validate="key", 
            validatecommand=ensure_digit_vcmd(top_root), 
            width=5
        )

        #TODO: 考虑使用变量设置默认值
        self.default_value = default_value
        self.entry.bind("<FocusOut>", self._validate_input)

    def _pack_sub_comps(self):
        self.label.pack(side=tk.LEFT)
        self.entry.pack(side=tk.LEFT)
    
    def get_input(self) -> int:
        return int(self.entry.get())
    
    def clear(self):
        self.var.set(str(self.default_value))

    def _validate_input(self, event: tk.Event): 
        s = self.var.get()
        if s == "" or not s.isdigit(): 
            self.var.set("0")
        elif int(s) > 1000: 
            self.var.set(1000)

class _StatsColComp(Component): 
    _sub_comp_names = ("label", *STAT_TRANS.keys())
    # label: ttk.Label
    # fp: _StatComp
    # trp: _StatComp
    # avi: _StatComp
    # rld: _StatComp

    def __init__(self, root: ttk.Frame, text: str):
        self.frame = ttk.Frame(root)

        self.label = ttk.Label(self.frame, text=text)
        for k, v in STAT_TRANS.items(): 
            setattr(self, k, _StatComp(self.frame, v))
    
    def _pack_sub_comps(self):
        for comp in self.sub_components.values(): 
            comp.pack()

    @cached_property
    def vars(self): 
        return {k: v for k, v in self.sub_components.items() if isinstance(v, _StatComp)}

class CustomizedTabComp(Component): 
    _sub_comp_names = tuple(INPUT_TRANS.keys())

    def __init__(self, root: ttk.Frame):
        self.frame = ttk.Frame(root)

        for k, v in INPUT_TRANS.items(): 
            setattr(self, k, _StatsColComp(self.frame, v))

    def _pack_sub_comps(self):
        for comp in self.sub_components.values(): 
            comp.pack(padx=10, fill=tk.Y, side=tk.LEFT)

    @cached_property
    def vars(self): 
        return {k: v for k, v in self.sub_components.items() if isinstance(v, _StatsColComp)}

class PredefinedTabComp(Component): #TODO
    _sub_comp_names = ("label",)

    def __init__(self, root: ttk.Notebook):
        self.frame = ttk.Frame(root)
        self.label = ttk.Label(self.frame, text="Cuming s∞n (≥/////ω/////≤) ♡")

    def _pack_sub_comps(self):
        self.label.pack(anchor=tk.NW)
        ...
    ...

class InputStatsComp(Component): 
    _sub_comp_names = ("label", "notebook", "customized", "predefined")

    def __init__(self, root: ttk.Frame, text: str = ENHANCE_STAT):
        self.frame = ttk.Frame(root)

        self.label = ttk.Label(self.frame, text=text, font=SECTION_FONT)
        self.notebook = ttk.Notebook(self.frame, width=40)
        self.customized = CustomizedTabComp(self.notebook)
        self.predefined = PredefinedTabComp(self.notebook)

    def _pack_sub_comps(self):
        self.label.pack(anchor=tk.NW, padx=10, pady=5)
        self.notebook.pack(anchor=tk.NW, fill=tk.X, padx=10)
        self.customized.pack()
        self.predefined.pack()
        self.notebook.add(self.customized.frame, text=CUSTOMIZED_TAB)
        self.notebook.add(self.predefined.frame, text=PREDEFINED_TAB)

    def get_input(self):
        return self.customized.get_input()