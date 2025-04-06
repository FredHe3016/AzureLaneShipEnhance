from tkinter import font
from tkinter import ttk
from ttkthemes import ThemedTk

from executable.components.main_comp import MainComp
from data.static import TITLE, DEFAULT_FONT
from config import ICO_PATH

def main_execute(): 
    root = ThemedTk(screenName=TITLE, theme="arc")
    root.title(TITLE)

    root.iconbitmap(ICO_PATH)

    main_comp = MainComp(root)
    main_comp.pack()

    style = ttk.Style()
    style.configure(".", font=DEFAULT_FONT)

    return root

if __name__ == "__main__": 
    main_execute().mainloop()
    ...