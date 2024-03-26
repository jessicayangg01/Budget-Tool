
from interface.graphsView import GraphsView
from dataProcessing.budgetReader import budgetReader


# graphView = GraphsView()
# file = budgetReader("./assets/DummyData.csv")
# graphView.plot()


import tkinter as tk
from interface.textView import textView
## tinker stuff
win=tk.Tk()
newText = textView(win)
newText.addText("what")
win.mainloop()

