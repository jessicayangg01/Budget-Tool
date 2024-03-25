import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.artist import Artist
import numpy as np

# other classes
from dataProcessing.budgetReader import budgetReader
from dataProcessing.dataAnalysis import dataAnalysis
import assets

# file
from tkinter import filedialog

class GraphsView(object):
    def __init__(self):
        axcut = plt.axes([0.8, 0.0, 0.2, 0.075])
        self.button1 = Button(axcut, 'Linear Regression', color='white', hovercolor='green')
        self.button1.on_clicked(self.calculate)

        axcut = plt.axes([0.67, 0.0, 0.12, 0.075])
        self.button2 = Button(axcut, 'Open File', color='white', hovercolor='green')
        self.button2.on_clicked(self.openFile)

        axcut = plt.axes([0.55, 0.0, 0.12, 0.075])
        self.button2 = Button(axcut, 'Predict', color='white', hovercolor='green')
        self.button2.on_clicked(self.predict)
        
        # # adding text
        # text  = plt.text(-5, 0.5, "jessicas text", fontsize = 12)
        # text.set_visible(False)
        # Artist.set_visible(text, True)
        # # Artist.remove(text)
        self.addText("hi there")

        self.dataanalyze = None


        plt.show()

    def addText(self, text_message):
        # adding text
        text  = plt.text(-5, 0.5, text_message, fontsize = 12)
        text.set_visible(False)
        Artist.set_visible(text, True)
        # Artist.remove(text)
        plt.draw()



    def showGraph(self, graph, subplot, title, type, line):
        plt.subplot(subplot)
        if type == "scatter":
            plt.scatter(x =graph[1], y=graph[0], s=1)
        else:
            plt.plot(graph)
        
        # plt.xlabel(title) 
        plt.title(title)
        

        # plot line
        axes = plt.gca()
        x_vals = np.array(axes.get_xlim())
        y_vals = line["intercept"] + line["slope"] * x_vals
        plt.plot(x_vals, y_vals, 'r--')


        plt.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.2, 
                    hspace=0.6)
        

        plt.draw()
        


        
        
    
    def plot(self, readBudget):
        n=1
        analyzeBudget = dataAnalysis(readBudget)
        for col in readBudget.getCol():
            line  = analyzeBudget.linearRegression(col)
            # values = {}
            # values["slope"] = model.coef_[0]
            # values["intercept"] = model.intercept_
            # # values["r squared"] = model.score(X, Y)
            self.showGraph([readBudget.data["Sales"], readBudget.data[col]], 330+n, col, "scatter", line)

            # new line
            
            self.textBox(line)
            n+=1
        

    def textBox(self, line):
        ## show text
        textstr = ""
        for i in line:
            textstr += str(i) + ":" + str(line[i])
            textstr += "\n"

        # these are matplotlib.patch.Patch properties
        plt.text(0, 0, textstr, fontsize = 8, bbox = dict(facecolor = 'white', alpha = 0.5))

### BUTTONS -------------------------------------------
    def calculate(self, event):
        print("button clicked")
        assets.load_dataFiles()


        # maybe add a way you can add multiple files
        
        readBudget = budgetReader(assets.get_dataFile("DummyData"))
        readBudget.dataClean()


        
        # analyzeBudget.randomForest()
        self.plot(readBudget)
        self.dataanalyze = readBudget
       

        # window = GraphsView()
        # self.showGraph(graph, 221, "hi")
        # self.showGraph([2,2,2], 222, "bye")
    def openFile(self, event):
        filepath = filedialog.askopenfilename(initialdir="C:\\Users\\Cakow\\PycharmProjects\\Main",
                                            title="Open file okay?",
                                            filetypes= (("text files","*.txt"),
                                            ("all files","*.*")))
        file = open(filepath,'r')
        print(file.read())
        file.close()

        self.addText("added file "+ filepath)
    

    def predict(self, event):
        analyzeBudget = dataAnalysis(self.dataanalyze)
        analyzeBudget.predict([[1, 16,6.566230788,2.907982773,1]])