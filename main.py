from dataProcessing.budgetReader import budgetReader
from dataProcessing.dataAnalysis import dataAnalysis
import assets


assets.load_dataFiles()


# maybe add a way you can add multiple files
readBudget = budgetReader(assets.get_dataFile("DummyData"))
readBudget.dataClean()



# analyzeBudget = dataAnalysis(readBudget)
# analyzeBudget.plot()
import sys
from PyQt5.QtWidgets import QApplication 
from interface.applicationWindow import ApplicationWindow


app = QApplication(sys.argv)
win = ApplicationWindow()
win.setWindowTitle("Jessica's Thesis")
win.show()
sys.exit(app.exec_())