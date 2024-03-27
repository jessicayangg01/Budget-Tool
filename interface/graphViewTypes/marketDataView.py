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


class MarketDataView(object):
    def __init__(self, canvas, data_logger, event_logger, stockData, fig):
        self.canvas = canvas
        self.stockData = stockData
        self.data_logger = data_logger
        self.event_logger = event_logger
        self.fig = fig

        self.allPlotLines = {}

        # Create three Tkinter buttons
        button1 = Button(self.canvas.get_tk_widget(), text="Add Ticker")
        button2 = Button(self.canvas.get_tk_widget(), text="Remove Ticker")
        button3 = Button(self.canvas.get_tk_widget(), text="Predict")

        # Position the buttons at the bottom of the canvas
        canvas_height = self.canvas.get_tk_widget().winfo_height()
        button1.place(x=50, y=canvas_height-50)
        button2.place(x=150, y=canvas_height-50)
        button3.place(x=250, y=canvas_height-50)

        # Bind the buttons to their respective functions
        button1.bind("<Button-1>", self.add)
        button2.bind("<Button-2>", self.remove)
        button3.bind("<Button-3>", self.predict)

        self.showGraph("Market Data")
    

    def add(self, event):
        self.event_logger.addtext("getting market information ...")
        self.open_popup_ticker_entry("Input a ticker: ")

        # make it so you start adding here
        
    
    def open_popup_ticker_entry(self, text):
        # Create and open the popup window
        def handle_X_selection(ticker):
            self.data_logger.addtext("Inputed the following ticker: " + str(ticker))
            self.stockData.addTicker(ticker)

            # Define a callback function to handle X and Y selections
            def handle_Y_selection(Y):
                X = self.open_popup_XY_selection("What is the independent var?", self.stockData.getIncomeStatement(ticker), lambda X: self.handle_XY_selection(X, Y, ticker))
            
            # Open the popup for selecting the dependent variable (Y)
            self.open_popup_XY_selection("What is the dependent var?", self.stockData.getIncomeStatement(ticker), handle_Y_selection)

        popup = PopupWindow(self.canvas.get_tk_widget())
        popup.open_ticker_entry(text, handle_X_selection)

    def handle_XY_selection(self, X, Y, ticker):
        data = self.stockData.getVars(ticker, Y, X)
        self.plotLine(data["years"], data["ratio"], ticker)
    
    def open_popup_XY_selection(self, text, vars, callback):
        # Create and open the popup window
        def handle_done2(data):
            one_data = data[0]  # Assuming data is a tuple or list containing X and Y
            self.data_logger.addtext("Using Var: " + str(one_data))
            callback(one_data)  # Pass the selected data to the callback function

        popup = PopupWindow(self.canvas.get_tk_widget())
        popup.open_variable_list(text, vars, handle_done2)
        

    

    def remove(self, event):
        print("not done, remove")
    def predict(self, event):
        print("not done, remove")


    

    ############## GRAPH STUFF
        
    def showGraph(self, title):
        self.currPlot = self.fig.add_subplot(111)
        
        # plt.xlabel(title) 
        self.currPlot.set_title(title)
        self.currPlot.set_xlabel('X Label')
        self.currPlot.set_ylabel('Y Label')
        
        self.canvas.draw() 
    
    def plotLine(self, X, Y, ticker):
        self.currPlot.plot(X, Y, label=ticker)
        # Append the line data to self.line_plts
        self.allPlotLines[ticker] = (X, Y)
        self.canvas.draw() 

    def removeLine(self, ticker):
        if ticker in self.allPlotLines:
            del self.allPlotLines[ticker]
            self.showGraph("Updated Graph")  # Redraw the graph without the removed plot line
        else:
            self.data_logger.addtext("ticker does not exist.")
    
    # not in use 
    def textBox(self, line):
        # show text
        textstr = ""
        for i in line:
            textstr += str(i) + ":" + str(line[i])
            textstr += "\n"

        self.currPlot.text(0, 0, textstr, fontsize = 8, bbox = dict(facecolor = 'white', alpha = 0.5))
    