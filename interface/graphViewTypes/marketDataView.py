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

        # # Create three Tkinter buttons
        # button1 = Button(self.canvas.get_tk_widget(), text="Add Ticker")
        # button2 = Button(self.canvas.get_tk_widget(), text="Remove Ticker")
        # button3 = Button(self.canvas.get_tk_widget(), text="Predict")

        # # Position the buttons at the bottom of the canvas
        # canvas_height = self.canvas.get_tk_widget().winfo_height()
        # button1.place(x=50, y=canvas_height-50)
        # button2.place(x=150, y=canvas_height-50)
        # button3.place(x=250, y=canvas_height-50)

        # # Bind the buttons to their respective functions
        # button1.bind("<Button-1>", self.add)
        # button2.bind("<Button-1>", self.remove)
        # button3.bind("<Button-1>", self.predict)


        # placing the canvas on the Tkinter window 
        self.canvas.get_tk_widget().pack(fill="both", expand=True)  # Fill the entire window
        
        self.canvas.get_tk_widget().config(borderwidth=2, relief="solid")
        self.fig.suptitle("Graphs View", fontsize=12)

        # Create three Tkinter buttons
        button1 = Button(self.canvas.get_tk_widget(), text="Add Ticker", width=25)
        button2 = Button(self.canvas.get_tk_widget(), text="Remove Ticker", width=25)
        button3 = Button(self.canvas.get_tk_widget(), text="Predict", width=25)

        # Position the buttons at the bottom of the canvas
        canvas_height = self.canvas.get_tk_widget().winfo_height()
        button1.place(x=50, y=canvas_height-50)
        button2.place(x=250, y=canvas_height-50)
        button3.place(x=450, y=canvas_height-50)

        # Bind the buttons to their respective functions
        button1.bind("<Button-1>", self.add)
        button2.bind("<Button-1>", self.remove)
        button3.bind("<Button-1>", self.predict)

        # Change button color on hover
        def change_button_color(button, color):
            button.config(bg=color)

        button1.bind("<Enter>", lambda event: change_button_color(button1, "#4CAF50"))  # Green color on hover
        button1.bind("<Leave>", lambda event: change_button_color(button1, "SystemButtonFace"))  # Original color on leave
        button2.bind("<Enter>", lambda event: change_button_color(button2, "#4CAF50"))  # Green color on hover
        button2.bind("<Leave>", lambda event: change_button_color(button2, "SystemButtonFace"))  # Original color on leave
        button3.bind("<Enter>", lambda event: change_button_color(button3, "#4CAF50"))  # Green color on hover
        button3.bind("<Leave>", lambda event: change_button_color(button3, "SystemButtonFace"))  # Original color on leave
        
        self.showGraph("Market Data")

    
####################### ADD  
    def add(self, event):
        self.event_logger.addtext("getting market information ...")
        self.open_popup_ticker_entry("Input a ticker: ")

    
    def open_popup_ticker_entry(self, text):
        # Create and open the popup window
        def handle_X_selection(ticker):
            self.data_logger.addtext("Inputed the following ticker: " + str(ticker))
            self.stockData.addTicker(ticker)

            # Define a callback function to handle X and Y selections
            def handle_Y_selection(Y):
                X = self.open_popup_XY_selection("What is the independent var?", self.stockData.getIncomeStatement(ticker), lambda X: self.handle_XY_selection(X, Y, ticker))
            
            # Open the popup for selecting the dependent variable (Y)
            if not self.stockData.getIncomeStatement(ticker):
                self.data_logger.addtext("ERROR: This ticker does not have sufficient financial data to perform analysis. ")
                self.stockData.removeTicker(ticker)
                return
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
        
############################ REMOVE 
    def remove(self, event):
        tickers = list(self.stockData.tickerList.keys())
        self.open_popup_remove("Which tickers would you like to remove?", tickers)

    
    def open_popup_remove(self, text, tickers):
        # Create and open the popup window
        def handle_done(data):
            self.data_logger.addtext("Removing Tickers: " + str(data))
            for i in data:
                self.removeLine(i)

        popup = PopupWindow(self.canvas.get_tk_widget())
        popup.open_variable_list(text, tickers, handle_done)

    
    def predict(self, event):
        print("not done, remove")


    

    ############## GRAPH STUFF
        
    def showGraph(self, title):
        # self.currPlot = self.fig.add_subplot(111)

        bottom_margin = 0.15  # Adjust this value as needed to leave enough space for the buttons
        self.currPlot = self.fig.add_subplot(111, position=[0.1, bottom_margin, 0.8, 0.8 - bottom_margin])

    
        
        # plt.xlabel(title) 
        self.currPlot.set_title(title)
        # self.currPlot.set_xlabel('X Label')
        # self.currPlot.set_ylabel('Y Label')
        
        self.canvas.draw() 
    
    def plotLine(self, X, Y, ticker):
        plot = self.currPlot.plot(X, Y, label=ticker)
        # Append the line data to self.line_plts
        self.allPlotLines[ticker] = plot
        self.currPlot.legend()
        self.canvas.draw() 

    def removeLine(self, ticker):
        if ticker in self.allPlotLines:
            self.allPlotLines[ticker][0].remove()
            del self.allPlotLines[ticker]
            self.currPlot.legend()
            self.canvas.draw() 
            self.stockData.removeTicker(ticker)
        else:
            self.data_logger.addtext("Ticker does not exist.")
    
    # not in use 
    def textBox(self, line):
        # show text
        textstr = ""
        for i in line:
            textstr += str(i) + ":" + str(line[i])
            textstr += "\n"

        self.currPlot.text(0, 0, textstr, fontsize = 8, bbox = dict(facecolor = 'white', alpha = 0.5))
    