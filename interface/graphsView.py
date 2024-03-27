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

from interface.graphViewTypes.marketDataView import MarketDataView
from interface.graphViewTypes.csvDataView import CsvDataView


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
        self.button1 = Button(self.canvas.get_tk_widget(), text="Open File")
        self.button2 = Button(self.canvas.get_tk_widget(), text="Add Market Data")

        # Position the buttons at the bottom of the canvas
        window.update_idletasks()
        canvas_height = self.canvas.get_tk_widget().winfo_height()
        self.button1.place(x=150, y=canvas_height-50)
        self.button2.place(x=350, y=canvas_height-50)

        # Bind the buttons to their respective functions
        self.button1.bind("<Button-1>", self.openFile)
        self.button2.bind("<Button-1>", self.marketData)


        ### this is for the file 
        self.file = None
        # this is for the budget reader
        self.readBudget = None
        # for stock market
        self.stockData = None

        # popup
        # self.popup_button = Button(self.canvas.get_tk_widget(), text="Open Popup", command=self.open_popup)
        # self.popup_button.place(x=350, y=canvas_height-50)
                


    def remove(self):
        self.canvas.get_tk_widget().destroy()


    def openFile(self, event):
        filepath = filedialog.askopenfilename(initialdir="C:\\Users\\Cakow\\PycharmProjects\\Main",
                                            title="Open file okay?",
                                            filetypes=(("CSV files", "*.csv"),
                                            ("all files","*.*")))
        
        if filepath and os.path.splitext(filepath)[1] == ".csv":
            # File is a CSV file, proceed with your code
            self.event_logger.addtext("added file "+ filepath)
            self.file = filepath
            # maybe add a way you can add multiple files
            self.readBudget = budgetReader(self.file, self.data_logger)
            self.open_popup_selectIndependent()

        else:
            # File is not a CSV file, handle accordingly
            self.event_logger.addtext("This file type is not supported. Please input a csv file")
            self.open_popup_error("This file type is not supported. Please input a csv file")
        
    
        
    
    def marketData(self, event):
        self.stockData = MarketData(self.data_logger)
        self.event_logger.addtext("getting market information ...")
        self.open_popup_ticker_entry("Input a ticker: ")
        
        


#### POPUP STUFF
        
    
    def open_popup_ticker_entry(self, text):
        # Create and open the popup window
        def handle_done(ticker):
            # selected_vars = popup.get_selected_variables()
            self.data_logger.addtext("Inputed the following ticker: "+ str(ticker))
            if ticker:
                self.stockData.addTicker(ticker)
                self.destroyButtons()
                newMarketDataView = MarketDataView(self.canvas, self.data_logger, self.event_logger, self.stockData, self.fig)
            else:
                self.data_logger.addtext("Invalid ticker inputed.")
        popup = PopupWindow(self.canvas.get_tk_widget())
        popup.open_ticker_entry(text, handle_done)
    
    def open_popup_selectIndependent(self):
        def handle_done(selected_vars):
            # selected_vars = popup.get_selected_variables()
            self.data_logger.addtext("Selected the following variable(s) as dependent variables: "+ str(selected_vars))
            if len(selected_vars) > 1:
                self.event_logger.addtext("this application does not yet support more than one dependent variable")

            self.readBudget.setIndependentVar(selected_vars[0])
            self.destroyButtons()
            # newCsvDataView = CsvDataView(self.canvas, self.data_logger, self.event_logger, self.file, self.readBudget)
            newCsvDataView = CsvDataView(self.canvas, self.data_logger, self.event_logger, self.file, self.readBudget, self.fig)
        popup = PopupWindow(self.canvas.get_tk_widget())
        popup.open_variable_list("Select the dependent variable", self.readBudget.getCol(), handle_done)
    
    def destroyButtons(self):
        # Remove the buttons
        self.button1.destroy()
        self.button2.destroy()