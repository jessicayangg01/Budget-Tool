import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.artist import Artist
import numpy as np


from tkinter import filedialog
from dataProcessing.budgetReader import budgetReader
from dataProcessing.dataAnalysis import dataAnalysis
import assets


## new

from tkinter import * 
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  NavigationToolbar2Tk) 



class GraphsView(object):
    def __init__(self, window, data_logger, event_logger):
        self.data_logger = data_logger
        self.event_logger = event_logger
        self.fig = Figure(figsize = (5, 5), dpi = 100) 
        
        # creating the Tkinter canvas 
        # containing the Matplotlib figure 
        self.canvas = FigureCanvasTkAgg(self.fig, master = window)   
        self.canvas.draw() 
        
        # placing the canvas on the Tkinter window 
        self.canvas.get_tk_widget().pack() 
        
        # # creating the Matplotlib toolbar 
        # toolbar = NavigationToolbar2Tk(self.canvas, window) 
        # toolbar.update() 
        # # placing the toolbar on the Tkinter window 
        # self.canvas.get_tk_widget().pack() 


        self.canvas.get_tk_widget().config(borderwidth=2, relief="solid")
        self.fig.suptitle("Graphs View", fontsize=12)

        # Create three Tkinter buttons
        button1 = Button(self.canvas.get_tk_widget(), text="Calculate")
        button2 = Button(self.canvas.get_tk_widget(), text="Open File")
        button3 = Button(self.canvas.get_tk_widget(), text="Predict")

        # Position the buttons at the bottom of the canvas
        window.update_idletasks()
        canvas_height = self.canvas.get_tk_widget().winfo_height()
        button1.place(x=50, y=canvas_height-50)
        button2.place(x=150, y=canvas_height-50)
        button3.place(x=250, y=canvas_height-50)

        # Bind the buttons to their respective functions
        button1.bind("<Button-1>", self.calculate)
        button2.bind("<Button-1>", self.openFile)
        button3.bind("<Button-1>", self.predict)


        ### this is for the file 
        self.file = None



    def remove(self):
        self.canvas.get_tk_widget().destroy()


    def showGraph(self, graph, subplot, title, type, line):
        self.currPlot = self.fig.add_subplot(subplot)
        if type == "scatter":
            self.currPlot.scatter(x =graph[1], y=graph[0], s=1)
        else:
            self.currPlot.plot(graph)
        
        # plt.xlabel(title) 
        self.currPlot.set_title(title)
        self.currPlot.set_xlabel('X Label')
        self.currPlot.set_ylabel('Y Label')
        

        # plot line
        x_vals = np.array(self.currPlot.get_xlim())
        y_vals = line["intercept"] + line["slope"] * x_vals
        self.currPlot.plot(x_vals, y_vals, 'r--')


        self.fig.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.2, 
                    hspace=0.6)
        

        # self.currPlot.draw()
        self.canvas.draw() 
        


    
    def plot(self, readBudget):
        n=1
        analyzeBudget = dataAnalysis(readBudget, self.data_logger)
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
        # show text
        textstr = ""
        for i in line:
            textstr += str(i) + ":" + str(line[i])
            textstr += "\n"

        # these are matplotlib.patch.Patch properties
        self.currPlot.text(0, 0, textstr, fontsize = 8, bbox = dict(facecolor = 'white', alpha = 0.5))
        print("YES ADD TEXT 3")


### BUTTONS -------------------------------------------
    # def calculate(self, event):
        
        
    #     print("button clicked")
    #     assets.load_dataFiles()

    #     # maybe add a way you can add multiple files
    #     readBudget = budgetReader(assets.get_dataFile("DummyData"))
    #     readBudget.dataClean()
        
    #     # analyzeBudget.randomForest()
    #     self.plot(readBudget)
    #     self.dataanalyze = readBudget
        

    def calculate(self, event): 

        if not self.file:
            self.event_logger.addtext("no file to read from")
            return
        
        self.event_logger.addtext("Calculating for "+ self.file)

        # maybe add a way you can add multiple files
        readBudget = budgetReader(self.file, self.data_logger)
        readBudget.dataClean()
        
        # analyzeBudget.randomForest()
        self.plot(readBudget)
        self.dataanalyze = readBudget
       

    def openFile(self, event):
        filepath = filedialog.askopenfilename(initialdir="C:\\Users\\Cakow\\PycharmProjects\\Main",
                                            title="Open file okay?",
                                            filetypes= (("text files","*.txt"),
                                            ("all files","*.*")))
        file = open(filepath,'r')
        self.file = filepath
        # print(file.read())
        file.close()
        self.event_logger.addtext("added file "+ filepath)
        
    

    def predict(self, event):
        self.event_logger.addtext("predictions incoming ...")
        analyzeBudget = dataAnalysis(self.dataanalyze, self.data_logger)
        analyzeBudget.predict([[1, 16,6.566230788,2.907982773,1]])