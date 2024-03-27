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
        button2.bind("<Button-1>", self.remove)
        button3.bind("<Button-1>", self.predict)
    

    def add(self, event):
        self.event_logger.addtext("getting market information ...")
        self.open_popup_ticker_entry("Input a ticker: ")
    
    def open_popup_ticker_entry(self, text):
        # Create and open the popup window
        def handle_done(ticker):
            # selected_vars = popup.get_selected_variables()
            self.data_logger.addtext("Inputed the following ticker: "+ str(ticker))
            self.stockData.addTicker(ticker)
        popup = PopupWindow(self.canvas.get_tk_widget())
        popup.open_ticker_entry(text, handle_done)