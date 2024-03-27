import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.artist import Artist
import numpy as np

from tkinter import filedialog
from dataProcessing.budgetReader import budgetReader
from dataProcessing.dataAnalysis import dataAnalysis
from dataProcessing.marketData import MarketData
import assets

from tkinter import * 
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  NavigationToolbar2Tk) 

# popup
from interface.popupWindow import PopupWindow
import os


class CsvDataView(object):
    def __init__(self, canvas, data_logger, event_logger, file, readBudget, fig):
        self.canvas = canvas
        self.data_logger = data_logger
        self.event_logger = event_logger
        self.file = file
        self.readBudget = readBudget
        self.fig = fig

        button1 = Button(self.canvas.get_tk_widget(), text="Calculate")
        button3 = Button(self.canvas.get_tk_widget(), text="Predict")

        canvas_height = self.canvas.get_tk_widget().winfo_height()
        button1.place(x=50, y=canvas_height-50)
        button3.place(x=250, y=canvas_height-50)

        button3.bind("<Button-1>", self.predict)
        button1.bind("<Button-1>", self.calculate)

    def predict(self, event):
        self.event_logger.addtext("predictions incoming ...")
        self.open_popup_user_predict("Input your budget data", self.readBudget.getDependentVar())
    

    def calculate(self, event): 

        if not self.file:
            self.event_logger.addtext("no file to read from")
            return
        
        self.event_logger.addtext("Calculating for "+ self.file)

        
        self.readBudget.dataClean()
        
        # analyzeBudget.randomForest()
        self.plot()
        self.dataanalyze = self.readBudget
    

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
        


    
    def plot(self):
        n=1
        analyzeBudget = dataAnalysis(self.readBudget, self.data_logger)
        for col in self.readBudget.getCol():
            line  = analyzeBudget.linearRegression(col)
            self.showGraph([self.readBudget.data[self.readBudget.independent_var], self.readBudget.data[col]], 330+n, col, "scatter", line)
            self.textBox(line)
            n+=1
        

    def textBox(self, line):
        # show text
        textstr = ""
        for i in line:
            textstr += str(i) + ":" + str(line[i])
            textstr += "\n"

        self.currPlot.text(0, 0, textstr, fontsize = 8, bbox = dict(facecolor = 'white', alpha = 0.5))


    
    
    def open_popup_error(self, message):
        # Create and open the popup window
        popup = PopupWindow(self.canvas.get_tk_widget())
        popup.open_err_message(message)


    
    def open_popup_user_predict(self, text, variables):
        # Create and open the popup window
        def handle_done(selected_vars):
            # selected_vars = popup.get_selected_variables()
            self.data_logger.addtext("Inputed the following variables: "+ str(selected_vars))
            
            analyzeBudget = dataAnalysis(self.dataanalyze, self.data_logger)
            analyzeBudget.predict(selected_vars)
        popup = PopupWindow(self.canvas.get_tk_widget())
        popup.open_text_entry(text, variables, handle_done)