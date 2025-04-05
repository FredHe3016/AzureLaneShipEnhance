import tkinter as tk
from tkinter import ttk
from functools import cached_property, wraps
from typing import Dict, Any, Self, Tuple

from ..utils import pack_decorator

class Component: 
    frame: ttk.Frame
    _sub_comp_names: Tuple[str, ...]
    # sub_components: Dict[str, Self | tk.Widget]

    # def __getattr__(self, attr: str): 
    #     if attr in self.sub_components: 
    #         return self.sub_components[attr]
    #     raise AttributeError
    
    @cached_property
    def sub_components(self) -> Dict[str, Self|tk.Widget]: 
        return {k: getattr(self, k) for k in self._sub_comp_names}

    def get_input(self) -> Dict[str, Any]: 
        return {k: _ for k, c in self.sub_components.items() if (_ := _get_input(c)) is not _NOT_REQUIRED}
    
    def clear(self): 
        """清除输入内容，输入默认值"""
        for v in self.sub_components.values(): 
            if isinstance(v, Component): 
                v.clear()
            elif isinstance(v, (ttk.Label, ttk.Button, ttk.Notebook)): 
                continue
            elif isinstance(v, ttk.Widget): 
                raise NotImplementedError(f"Component {self} with Widget instance as subcomponent needs independent definition of clear function. ")
            else: 
                raise ValueError

    def write(self, content: Any, clear: bool = True): 
        if not isinstance(content, dict): 
            raise NotImplementedError
        for k, v in content.items(): 
            sub_comp = self.sub_components[k]
            if isinstance(sub_comp, tk.Widget): 
                raise NotImplementedError
            sub_comp.insert(v, clear=clear)

    def _pack_sub_comps(self): 
        #内部组件打包
        raise NotImplementedError

    @pack_decorator
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)
        self._pack_sub_comps()

    # def grid(self, **kwargs): 
    #     raise NotImplementedError
 
    def disabled(self): 
        for c in self.sub_components.values():
            if isinstance(c, (tk.Entry, tk.Text, tk.Button)): 
                c.config(state=tk.DISABLED)
            elif isinstance(c, Component): 
                c.disabled()

    def enabled(self): 
        for c in self.sub_components.values():
            if isinstance(c, (tk.Entry, tk.Text, tk.Button)): 
                c.config(state=tk.NORMAL)
            elif isinstance(c, Component): 
                c.enabled()

_NOT_REQUIRED = object()
def _get_input(comp: Component | tk.Widget): 
    match comp: 
        case Component(): 
            return comp.get_input()
        case ttk.Entry(): 
            return comp.get()
        case tk.Text(): 
            return comp.get("1.0", tk.END)
        case ttk.Label() | ttk.Button(): 
            return _NOT_REQUIRED
        case _: 
            raise NotImplementedError(f"Requesting inputs from unexpected component type {type(comp)}")

#XXX: 生搬的scrolledtext代码，不知道会不会有问题
class ThemedScrolledText(tk.Text):
    def __init__(self, master=None, **kw):
        self.frame = ttk.Frame(master)
        self.vbar = ttk.Scrollbar(self.frame)
        self.vbar.pack(side=tk.RIGHT, fill=tk.Y)

        kw.update({'yscrollcommand': self.vbar.set})
        tk.Text.__init__(self, self.frame, **kw)
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.vbar['command'] = self.yview

        # Copy geometry methods of self.frame without overriding Text
        # methods -- hack!
        text_meths = vars(tk.Text).keys()
        methods = vars(tk.Pack).keys() | vars(tk.Grid).keys() | vars(tk.Place).keys()
        methods = methods.difference(text_meths)

        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))

    def __str__(self):
        return str(self.frame)