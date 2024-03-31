import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.artist import Artist
import numpy as np

from tkinter import filedialog
from dataProcessing.budgetReader import budgetReader

from tkinter import * 
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  NavigationToolbar2Tk)

from interface.graphViewTypes.graphTabs import GraphTabs
from dataProcessing.marketData import MarketData

# popup
from interface.popupWindow import PopupWindow


class MarketDataView(object):
    def __init__(self, canvas, data_logger, event_logger, stockData: MarketData, fig):
        self.canvas = canvas
        self.stockData = stockData
        self.data_logger = data_logger
        self.event_logger = event_logger
        self.fig = fig


        # placing the canvas on the Tkinter window 
        self.canvas.get_tk_widget().pack(fill="both", expand=True)  # Fill the entire window
        
        self.canvas.get_tk_widget().config(borderwidth=2, relief="solid")
        self.fig.suptitle("Graphs View", fontsize=12)

        # Create three Tkinter buttons
        button1 = Button(self.canvas.get_tk_widget(), text="Add Ticker", width=25)
        button2 = Button(self.canvas.get_tk_widget(), text="Remove Ticker", width=25)
        # button3 = Button(self.canvas.get_tk_widget(), text="Predict", width=25)

        # Position the buttons at the bottom of the canvas
        canvas_height = self.canvas.get_tk_widget().winfo_height()
        button1.place(x=50, y=canvas_height-50)
        button2.place(x=250, y=canvas_height-50)
        # button3.place(x=450, y=canvas_height-50)

        # Bind the buttons to their respective functions
        button1.bind("<Button-1>", self.add)
        button2.bind("<Button-1>", self.remove)
        # button3.bind("<Button-1>", self.predict)

        # Change button color on hover
        def change_button_color(button, color):
            button.config(bg=color)

        button1.bind("<Enter>", lambda event: change_button_color(button1, "#4CAF50"))  # Green color on hover
        button1.bind("<Leave>", lambda event: change_button_color(button1, "SystemButtonFace"))  # Original color on leave
        button2.bind("<Enter>", lambda event: change_button_color(button2, "#4CAF50"))  # Green color on hover
        button2.bind("<Leave>", lambda event: change_button_color(button2, "SystemButtonFace"))  # Original color on leave
        # button3.bind("<Enter>", lambda event: change_button_color(button3, "#4CAF50"))  # Green color on hover
        # button3.bind("<Leave>", lambda event: change_button_color(button3, "SystemButtonFace"))  # Original color on leave
        
        # self.showGraph("Market Data")
        self.graphsTabs = GraphTabs(self.canvas, self.stockData, self.data_logger)

    
####################### ADD  
    def add(self, event):
        self.event_logger.addtext("getting market information ...")
        self.open_popup_ticker_entry("Input a ticker: ")

    
    def open_popup_ticker_entry(self, text):
        # Create and open the popup window
        def handle_X_selection(ticker):
            self.event_logger.addtext("Searching in the Yahoo Finance database for the following ticker: " + str(ticker))

            if ticker in self.stockData.tickerList:
                self.event_logger.addtext("ERROR: This ticker already exists in the ticker list. ")
                return
            
            if not self.stockData.addTicker(ticker):
                self.event_logger.addtext(f"ERROR: The ticker {ticker} does not exist in the database.")
                return

            # Define a callback function to handle X and Y selections
            def handle_Y_selection(Y):
                X = self.open_popup_XY_selection("What is the independent var? (Suggest: Marketing Expense Data)", self.stockData.getIncomeStatement(ticker), lambda X: self.handle_XY_selection(X, Y, ticker), ticker)
            
            # Open the popup for selecting the dependent variable (Y)
            if not self.stockData.getIncomeStatement(ticker):
                self.event_logger.addtext("ERROR: This ticker does not have sufficient financial data to perform analysis. ")
                self.stockData.removeTicker(ticker)
                return
            self.open_popup_XY_selection("What is the dependent var? (Suggest: Sales or Revenue Data)", self.stockData.getIncomeStatement(ticker), handle_Y_selection, ticker)

        popup = PopupWindow(self.canvas.get_tk_widget())
        popup.open_ticker_entry(text, handle_X_selection)

    def handle_XY_selection(self, X, Y, ticker):
        data = self.stockData.getVars(ticker, Y, X)
        self.graphsTabs.update(data, ticker)
    
    def open_popup_XY_selection(self, text, vars, callback, ticker):
        # Create and open the popup window
        def handle_done2(data):
            if not data:
                self.event_logger.addtext("ERROR: Failed to select a variable.")
                self.stockData.removeTicker(ticker)
                return
            self.data_logger.addtext("Using Var: " + str(data))
            callback(data)  # Pass the selected data to the callback function
        popup = PopupWindow(self.canvas.get_tk_widget())
        popup.open_selection_list(text, vars, handle_done2)
    

        
############################ REMOVE 
    def remove(self, event):
        tickers = list(self.stockData.tickerList.keys())
        self.open_popup_remove("Which tickers would you like to remove?", tickers)

    
    def open_popup_remove(self, text, tickers):
        # Create and open the popup window
        def handle_done(data):
            self.data_logger.addtext("Removing Tickers: " + str(data))
            for i in data:
                self.stockData.removeTicker(i)
                self.graphsTabs.delete(i)
            self.graphsTabs.random_forest_reg_add()

        popup = PopupWindow(self.canvas.get_tk_widget())
        popup.open_variable_list(text, tickers, handle_done)



    ############## GRAPH STUFF
        

    def textBox(self, line):
        # show text
        if hasattr(self, 'textbox'):
            self.textbox.remove()
        textbox_text = ""
        for i in line:
            textbox_text += str(i) + ":" + str(line[i])
            textbox_text += "\n"
        textbox_x = 0.5  # X-coordinate of the text box (0.5 is the center)
        textbox_y = 0.5  # Y-coordinate of the text box (0.5 is the center)
        self.textbox = self.currPlot.text(textbox_x, textbox_y, textbox_text, ha='center', va='center', fontsize=8, bbox=dict(facecolor='white', alpha=0.5), transform=self.currPlot.transAxes)
        self.canvas.draw()
