import tkinter as tk
from tkinter import ttk
from executable.components.base import ThemedScrolledText

if __name__ == "__main__": 

    root = tk.Tk()
    _frame = ttk.Frame(root)

    label = ttk.Label(_frame, text="test")

    switch_var = tk.IntVar()
    style = ttk.Style()
    style.configure("Switch.TCheckbutton", 
                font=("Arial", 14), 
                indicatoron=False, 
                background="lightgray", 
                foreground="black", 
                padding=10)
    switch = ttk.Checkbutton(
        _frame, 
        text="Switch", 
        variable=switch_var, 
        # style="Switch.TCheckbutton"
    )

    texts = [tk.Text(root, width=10, height=20) for i in range(4)]

    text = ThemedScrolledText(_frame, width=10, height=20)

    _frame.pack(anchor=tk.NW, fill=tk.X, padx=10)

    text.pack(anchor=tk.NW, pady=10, side=tk.TOP, fill=tk.X)
    label.pack(anchor=tk.NW, pady=10, side=tk.LEFT)
    switch.pack(anchor=tk.SE, pady=10, side=tk.RIGHT)

    b = tk.Button(_frame, text="test")

    # for text in texts: 
    #     text.pack(anchor=tk.SW, pady=10, padx=10, side=tk.LEFT)

    # s = tk.StringVar(root, value="test1", name="test")
    # e1 = tk.Entry(root, textvariable=s, state="disabled")
    # e2 = tk.Entry(root, textvariable=s)
    # e1.pack()
    # e2.pack()
    # switch.pack(pady=20)

    root.mainloop()
    pass
