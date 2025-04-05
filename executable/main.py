from ttkthemes import ThemedTk

from executable.components.main_comp import MainComp
from data.static import TITLE

def main_execute(): 
    root = ThemedTk(screenName=TITLE, theme="arc")

    main_comp = MainComp(root)
    main_comp.pack()

    return root

if __name__ == "__main__": 
    main_execute().mainloop()
    ...