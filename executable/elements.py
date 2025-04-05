import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from functools import cached_property

from typing import Literal, Dict

from data.static import STAT_TRANS

class AbsCreator: 
    root: tk.Tk

    def __init__(self, root: tk.Tk):
        self.root = root

    @cached_property
    def stat_vcmd(self): 
        def valid_stat(v: str): 
            return v.isdigit() and int(v) >= 0
        vcmd = self.root.register(valid_stat)
        return vcmd
    
    def stat_entry(
        self, 
        text: str|None = None, 
        row: int = 0, 
        column: int = 0, 
        column_span: int = 1
    ): 
        tk.Label(self.root, text=text).grid(row=row, column=column)
        e = tk.Entry(self.root, validate="key", validatecommand=(self.stat_vcmd, "%P"))
        e.insert(0, "0")
        e.grid(row=row, column=column+1, columnspan=column_span)
        return e
    
    def scrolled_inputs(
        self, 
        text: str|None = None, 
        row: int = 0, 
        column: int = 0,
        width: int = 50, 
        height: int = 12, 
        rowspan: int = 12,
        columnspan: int = 8,
        default_value: str = "", 
    ): 
        tk.Frame.pack()
        tk.Label(self.root, text=text).grid()
        si = ScrolledText(self.root, width=width, height=height)
        si.tag_config("error", foreground="red")
        si.grid(row=row+1, column=column, padx=10, pady=10, rowspan=rowspan, columnspan=columnspan)
        si.insert("1.0", default_value)
        return si
        ...
    
class StatElement: 
    text: str
    attr: str
    entries = Dict[str, tk.Entry]

    def __init__(
        self, 
        abs_creator: AbsCreator, 
        text: str, 
        attr: str, 
        row: int, 
        column: int, 
        layout: Literal["v", "h"] = "h", 
    ):
        self.layout = layout
        self.text = text
        self.attr = attr
        self.entries: Dict[str, tk.Entry] = dict()
        for k, v in STAT_TRANS.items(): 
            self.entries[v] = abs_creator.stat_entry(text=k, row=row, column=column)
            match layout: 
                case "h": 
                    column += 2
                case "v": 
                    row += 1
                case _: 
                    raise ValueError
            
    @property
    def get_inputs(self): 
        return {k: int(e.get()) for k, e in self.entries.items()}
    
    def toggle(self, var: tk.BooleanVar): 
        if var.get(): 
            for e in self.entries.values(): 
                e.config(state="normal")
        else: 
            for e in self.entries.values(): 
                e.delete(0, tk.END)
                e.insert(0, "0")
                e.config(state="disabled")
    
        