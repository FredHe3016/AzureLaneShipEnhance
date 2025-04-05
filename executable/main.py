from ttkthemes import ThemedTk

from executable.components.main_comp import MainComp
from data.static import TITLE

root = ThemedTk(screenName=TITLE, theme="arc")

main_comp = MainComp(root)
main_comp.pack()

root.mainloop()

...