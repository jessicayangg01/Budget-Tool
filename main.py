
from interface.graphsView import GraphsView
from dataProcessing.budgetReader import budgetReader


# graphView = GraphsView()
# file = budgetReader("./assets/DummyData.csv")
# graphView.plot()


import tkinter as tk
from interface.textView import mainWindow
win=tk.Tk()
newText = mainWindow(win)
newText.event_logger.addtext("Successfully started program.")
win.mainloop()

