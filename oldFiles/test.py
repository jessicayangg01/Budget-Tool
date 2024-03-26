import sys
from PyQt5 import QtGui, QtCore
from pyqtgraph.dockarea import *

class DockArea(DockArea):
    ## This is to prevent the Dock from being resized to te point of disappear
    def makeContainer(self, typ):
        new = super(DockArea, self).makeContainer(typ)
        new.setChildrenCollapsible(False)
        return new

class MyApp(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        central_widget = QtGui.QWidget()
        layout = QtGui.QVBoxLayout()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
    
        label = QtGui.QLabel('This is a label, The widgets will be below')
        label.setMaximumHeight(15)
        ## The DockArea as its name says, is the are where we place the Docks
        dock_area = DockArea(self)
        ## Create the Docks and change some esthetic of them
        self.dock1 = Dock('Widget 1', size=(300, 500))
        self.dock2 = Dock('Widget 2', size=(400, 500))
        self.dock1.hideTitleBar()
        self.dock2.hideTitleBar()
        self.dock1.nStyle = """
        Dock > QWidget {
            border: 0px solid #000;
            border-radius: 0px;
        }"""
        self.dock2.nStyle = """
        Dock > QWidget {
            border: 0px solid #000;
            border-radius: 0px;
        }"""
        self.button = QtGui.QPushButton('Exit')
        self.widget_one = WidgetOne()
        self.widget_two = WidgetTwo()
        ## Place the Docks inside the DockArea
        dock_area.addDock(self.dock1)
        dock_area.addDock(self.dock2, 'right', self.dock1)
        ## The statment above means that dock2 will be placed at the right of dock 1
        layout.addWidget(label)
        layout.addWidget(dock_area)
        layout.addWidget(self.button)
        ## Add the Widgets inside each dock
        self.dock1.addWidget(self.widget_one)
        self.dock2.addWidget(self.widget_two)
        ## This is for set the initial size and posotion of the main window
        self.setGeometry(100, 100, 600, 400)
        ## Connect the actions to functions, there is a default function called close()
        self.widget_one.TitleClicked.connect(self.dob_click)
        self.button.clicked.connect(self.close)
        
    def dob_click(self, feed):
        self.widget_two.text_box.clear()
        ## May look messy but wat i am doing is somethin like this:
        ## 'Title : ' + feed[0]  + '\n\n' + 'Summary : ' + feed[1]
        self.widget_two.text_box.setText(
            'Title : ' + feed[0]\
            + '\n\n' +\
            'Summary : ' + feed[1]
        )
        
class WidgetOne(QtGui.QWidget):
    ## This signal is created to pass a "list" when it (the signal) is emited
    TitleClicked = QtCore.pyqtSignal([list])
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)
        self.titleList = QtGui.QListWidget()
        self.label = QtGui.QLabel('Here is my list:')
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.titleList)
        
        self.titleList.addItem(QtGui.QListWidgetItem('Title 1'))
        self.titleList.addItem(QtGui.QListWidgetItem('Title 2'))
        self.titleList.itemDoubleClicked.connect(self.onClicked)

    def onClicked(self, item):
        ## Just test values
        title = item.text()
        summary = "Here you will put the summary of {}. ".format(title)*50
        ## Pass the values as a list in the signal. You can pass as much values
        ## as you want, remember that all of them have to be inside one list
        self.TitleClicked.emit([title, summary]) 

class WidgetTwo(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)
        self.label2 = QtGui.QLabel('Here we show results?:')
        self.text_box = QtGui.QTextBrowser()
        
        self.layout.addWidget(self.label2)
        self.layout.addWidget(self.text_box)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())