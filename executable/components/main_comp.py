import json
import tkinter as tk
import traceback
from tkinter import ttk
from ttkthemes import ThemedTk

from executable.components.base import Component
from executable.components.components import InputsComp, OutputComp
from executable.utils import get_info
from algorithm.wrapped import minimize_cost

class MainComp(Component): 
    _sub_comp_names = ("input_comp", "output_comp")

    def __init__(self, root: ThemedTk):
        self.frame = ttk.Frame(root)

        self.input_comp = InputsComp(self.frame)
        self.output_comp = OutputComp(self.frame, default_text=get_info())

        self.input_comp.cal_button.config(command=self.cal_command)
        self.input_comp.reset_button.config(command=self.reset_command)
    
    def _pack_sub_comps(self):
        self.input_comp.pack(anchor=tk.NW, side=tk.LEFT, padx=10, pady=10)
        self.output_comp.pack(anchor=tk.NW, padx=10, pady=10, fill=tk.Y, expand=True)
    
    def cal_command(self): 
        self.input_comp.disabled()
        try: 
            algo_input = self.input_comp.get_input()
            res = json.dumps(minimize_cost(**algo_input), indent=4, ensure_ascii=False)
        except Exception as e: 
            res = traceback.format_exc()
        self.output_comp.enabled()
        self.output_comp.write(res)
        self.output_comp.disabled()
        self.input_comp.enabled()

    def reset_command(self): 
        self.input_comp.clear()
        self.output_comp.enabled()
        self.output_comp.clear()
        self.output_comp.disabled()