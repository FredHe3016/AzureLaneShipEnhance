import tkinter as tk
from tkinter import ttk
from functools import partial

from executable.components.base import Component, ThemedScrolledText
from executable.components.stat_components import InputStatsComp
from executable.utils import check_float_input
from algorithm.utils import adapt_material_input
from data.static import *
from data.data_loader import generate_material_ships, requisition_expect, load_ships_data

class OutputComp(Component): 
    default_text: str
    _sub_comp_names = ("text",)

    def __init__(self, root: ttk.Frame, default_text: str):
        self.frame = ttk.Frame(root)
        self.text = ThemedScrolledText(
            self.frame, 
            font=TEXT_FONT, 
            background="#fafafa", 
            foreground="#333333",
            insertbackground="#1e90ff", 
            borderwidth=0, 
            relief="solid", 
            highlightthickness=1,
            highlightbackground="#cccccc", 
            highlightcolor="#1e90ff",
            width=60
        )

        self.text.insert(tk.END, default_text)
        self.default_text = default_text
        self.disabled()
    
    def _pack_sub_comps(self):
        self.text.pack(anchor=tk.SE, fill=tk.Y, expand=True)

    def clear(self):
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, self.default_text)

    def write(self, content: str, clear: bool = True):
        if clear:
            self.text.delete("1.0", tk.END) 
        self.text.insert(tk.END, content)

class ShipNameComp(Component): 
    var: tk.StringVar
    default_value: str
    _sub_comp_names = ("label", "entry", "hint")

    def __init__(self, root: ttk.Frame, text: str = SHIP_NAME, default_value: str = ""):
        self.frame = ttk.Frame(root)

        self.var = tk.StringVar(root.winfo_toplevel(), value=default_value)
        self.label = ttk.Label(self.frame, text=text, font=SECTION_FONT)
        self.entry = ttk.Entry(self.frame, textvariable=self.var)
        self.hint = ttk.Label(self.frame, font=HINT_FONT)

        self.default_value = default_value
        self.hint.config(**SHIP_NAME_HINT["default"])
    
    def clear(self):
        self.var.set(self.default_value)

    def get_input(self):
        return self.var.get()
    
    def write(self, content: str, clear: bool = True):
        if clear: 
            self.var.set(content)
        else: 
            self.var = self.var.get() + content

    def _pack_sub_comps(self):
        self.label.pack(anchor=tk.NW, side=tk.TOP, fill=tk.X)
        self.entry.pack(anchor=tk.NW, side=tk.LEFT, padx=5, pady=5)
        self.hint.pack(anchor=tk.W, side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)

class TargetShipComp(Component): 
    _sub_comp_names = ("name", "input_stats")

    def __init__(self, root: ttk.Frame):
        self.frame = ttk.Frame(root)
        
        self.name = ShipNameComp(self.frame, text=SHIP_NAME)
        self.input_stats = InputStatsComp(self.frame, text=ENHANCE_STAT)
    
    def _pack_sub_comps(self):
        self.name.pack(anchor=tk.NW, fill=tk.X)
        self.input_stats.pack(anchor=tk.NW, fill=tk.X, pady=10)

class MaterialComp(Component): 
    _sub_comp_names = ("label", "material_ships")

    def __init__(self, root: ttk.Frame, text: str = MATERIAL_SHIPS, default_value: str = ""):
        self.frame = ttk.Frame(root)

        self.label = ttk.Label(self.frame, text=text, font=SECTION_FONT)
        self.material_ships = ThemedScrolledText(
            self.frame, 
            font=TEXT_FONT, 
            background="#fafafa", 
            foreground="#333333",
            insertbackground="#1e90ff", 
            borderwidth=0, 
            relief="solid", 
            highlightthickness=1,
            highlightbackground="#cccccc", 
            highlightcolor="#1e90ff",
            width=40, 
            height=8
        )

        self.material_ships.insert(tk.END, default_value)
        self.default_value = default_value

    def get_input(self):
        return adapt_material_input(self.material_ships.get("1.0", tk.END))
    
    def write(self, content: bool, clear: bool = True):
        if clear: 
            self.material_ships.delete("1.0", tk.END)
        self.material_ships.insert(tk.END, content)

    def _pack_sub_comps(self):
        self.label.pack(anchor=tk.NW, padx=10, pady=5)
        self.material_ships.pack(anchor=tk.NW, padx=10, fill=tk.X, expand=True)
        
    def clear(self):
        self.material_ships.delete("1.0", tk.END)
        self.material_ships.insert(tk.END, self.default_value)

class _WeightComp(Component): 
    var: tk.StringVar
    default_value: float
    _sub_comp_names = ("label", "entry")
    
    def __init__(self, root: ttk.Frame, text: str, default_value: float = 0.0):
        self.frame = ttk.Frame(root)

        self.var = tk.StringVar(root.winfo_toplevel(), value=default_value)
        self.label = ttk.Label(self.frame, text=text, width=8)
        self.entry = ttk.Entry(self.frame, textvariable=self.var, width=7)
        #TODO: 考虑使用变量设置默认值
        self.default_value = default_value

        self.entry.bind("<KeyRelease>", check_float_input, add="+")
        self.entry.bind("<FocusOut>", self._validate_input, add="+")

    def _validate_input(self, event: tk.Event): 
        try: 
            f = float(self.var.get())
            if f > 1000: 
                self.var.set("1000.0")
            elif f >= 0: 
                self.var.set(str(float(f)))
                return
        except: 
            pass
        self.clear()
        check_float_input(event)

    def clear(self):
        self.var.set(str(self.default_value))
    
    def write(self, content: str, clear: bool = True):
        if clear: 
            self.var.set(content)
        else: 
            self.var.set(self.var.get() + content)

    def get_input(self):
        return float(self.entry.get())
    
    def _pack_sub_comps(self):
        self.label.pack(anchor=tk.W, side=tk.LEFT, padx=10)
        self.entry.pack(anchor=tk.W, side=tk.LEFT, padx=10)

class WeightsComp(Component): 
    _sub_comp_names = ("label", *RETIRE_RW_TRANS.values())

    def __init__(self, root: ttk.Frame, text: str = RETIRE_RES_WEIGHT):
        self.frame = ttk.Frame(root)
        self.label = ttk.Label(self.frame, text=text, font=SECTION_FONT)
        for k, v in RETIRE_RW_TRANS.items(): 
            setattr(self, v, _WeightComp(self.frame, text=k))
        self.medal.default_value = requisition_expect(ndigits=6)
        self.medal.clear()

    def _pack_sub_comps(self):
        self.label.pack(anchor=tk.NW, side=tk.TOP, fill=tk.X, pady=5)
        self.medal.pack(anchor=tk.NW, side=tk.TOP, fill=tk.X)
        self.sc.pack(anchor=tk.NW, side=tk.TOP, fill=tk.X)

class InputsComp(Component): 
    _sub_comp_names = ("target_ship", "material_ships", "weights", "reset_button", "cal_button")

    def __init__(self, root: ttk.Frame):
        self.frame = ttk.Frame(root)

        self.target_ship = TargetShipComp(self.frame)
        self.material_ships = MaterialComp(self.frame, text=MATERIAL_SHIPS, default_value=generate_material_ships("all"))
        self.weights = WeightsComp(self.frame, text=RETIRE_RES_WEIGHT)

        self.target_ship.name.entry.bind("<KeyRelease>", partial(self.check_ship_name, focus_out=False), add="+")
        self.target_ship.name.entry.bind("<FocusOut>", partial(self.check_ship_name, focus_out=True), add="+")
        self.reset_button = ttk.Button(self.frame, text=RESET_BUTTON)
        self.cal_button = ttk.Button(self.frame, text=CAL_BUTTON)

    def _pack_sub_comps(self):
        self.target_ship.pack(anchor=tk.NW, side=tk.TOP, fill=tk.X, pady=10)
        self.material_ships.pack(anchor=tk.NW, side=tk.TOP, fill=tk.X, expand=True, pady=10)
        self.weights.pack(anchor=tk.NW, side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        self.cal_button.pack(anchor=tk.SE, side=tk.RIGHT, pady=10, padx=10)
        self.reset_button.pack(anchor=tk.SE, side=tk.RIGHT, pady=10, padx=10)

    def get_input(self):
        res = super().get_input()
        weights = res.pop("weights")
        res["medal_weight"] = weights["medal"]
        res["sc_weight"] = weights["sc"]
        return res
    
    def clear(self): 
        super().clear()
        self.check_ship_name()

    def check_ship_name(self, event: tk.Event = None, focus_out: bool = False):
        name_comp = self.target_ship.name
        name = name_comp.get_input()

        if name == name_comp.default_value: 
            name_comp.hint.config(**SHIP_NAME_HINT["default"])
        elif ship_data := load_ships_data().get(name): 
            stats = {
                "max_stats": ship_data["durability"], 
                "nutri_per_lv": ship_data["level_exp"]
            }
            input_stats_comp = self.target_ship.input_stats
            input_stats_comp.clear()
            input_stats_comp.write(stats)
            name_comp.hint.config(**SHIP_NAME_HINT["match"])
        elif focus_out: 
            name_comp.hint.config(**SHIP_NAME_HINT["no_match"])