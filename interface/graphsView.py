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
        # self.fig = Figure(figsize = (5, 5), dpi = 100) 
        self.fig = Figure() 
        
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

        # placing the canvas on the Tkinter window 
        self.canvas.get_tk_widget().pack(fill="both", expand=True)  # Fill the entire window
        
        self.canvas.get_tk_widget().config(borderwidth=2, relief="solid")
        self.fig.suptitle("Graphs View", fontsize=12)

        # Create three Tkinter buttons
        self.button1 = Button(self.canvas.get_tk_widget(), command=self.openFile, text="Open File", height=2)
        self.button2 = Button(self.canvas.get_tk_widget(), command=self.marketData, text="Add Market Data",  height=2)


        # Position the buttons at the bottom of the canvas
        self.button1.pack(side="bottom", fill="x")  # Stretch horizontally
        self.button2.pack(side="bottom", fill="x")  # Stretch horizontally

        # Change button color on hover
        self.button1.bind("<Enter>", lambda event: self.button1.config(bg="#4CAF50"))  # Green color on hover
        self.button1.bind("<Leave>", lambda event: self.button1.config(bg="SystemButtonFace"))  # Original color on leave
        self.button2.bind("<Enter>", lambda event: self.button2.config(bg="#4CAF50"))  # Green color on hover
        self.button2.bind("<Leave>", lambda event: self.button2.config(bg="SystemButtonFace"))  # Original color on leave


        ### this is for the file 
        self.file = None
        # this is for the budget reader
        self.readBudget = None
        # for stock market
        self.stockData = None


    def remove(self):
        self.canvas.get_tk_widget().destroy()


    def openFile(self):
        filepath = filedialog.askopenfilename(initialdir="C:\\Users\\Cakow\\PycharmProjects\\Main",
                                        title="Open file okay?",
                                        filetypes=(("CSV files", "*.csv"),
                                        ("all files","*.*")))

        if filepath:
            if os.path.splitext(filepath)[1] == ".csv":
                # File is a CSV file, proceed with your code
                self.event_logger.addtext("added file "+ filepath)
                self.file = filepath
                # maybe add a way you can add multiple files
                self.readBudget = budgetReader(self.file, self.data_logger)
                self.clean_data_popup()
            else:
                # File is not a CSV file, handle accordingly
                self.event_logger.addtext("This file type is not supported. Please input a csv file")
                self.open_popup_error("This file type is not supported. Please input a csv file")
        else:
            # User canceled the file dialog
            self.event_logger.addtext("File selection canceled by the user.")
        
        
    
        
    
    def marketData(self):
        self.stockData = MarketData(self.data_logger)
        self.destroyButtons()
        newMarketDataView = MarketDataView(self.canvas, self.data_logger, self.event_logger, self.stockData, self.fig)
        # self.event_logger.addtext("getting market information ...")
        # self.open_popup_ticker_entry("Input a ticker: ")
        
        


#### POPUP STUFF
    
    def open_popup_selectIndependent(self):
        def handle_done(selected_vars):
            # selected_vars = popup.get_selected_variables()
            self.data_logger.addtext("Selected the following variable(s) as dependent variables: "+ str(selected_vars))
            if not selected_vars:
                self.event_logger.addtext("It is required that you select a dependent variable.")
                return
            # if len(selected_vars) > 1:
            #     self.event_logger.addtext("this application does not yet support more than one dependent variable")

            self.readBudget.setIndependentVar(selected_vars)
            self.destroyButtons()
            # newCsvDataView = CsvDataView(self.canvas, self.data_logger, self.event_logger, self.file, self.readBudget)
            newCsvDataView = CsvDataView(self.canvas, self.data_logger, self.event_logger, self.file, self.readBudget, self.fig)
        popup = PopupWindow(self.canvas.get_tk_widget())
        popup.open_variable_list("Select the dependent variable", self.readBudget.getCol(), handle_done)
    
    def clean_data_popup(self):
        def handle_yes():
            self.readBudget.dataClean()
            self.open_popup_selectIndependent()
        def handle_no():
            self.event_logger.addtext("WARNING: The data is not clean and you may run into some issues.")
            self.open_popup_selectIndependent()

        popup = PopupWindow(self.canvas.get_tk_widget())
        popup.open_text_yes_no("Would you like to clean the data? It is highly recommended so that you dont run into errors.", handle_yes, handle_no)
    
    def destroyButtons(self):
        # Remove the buttons
        self.button1.destroy()
        self.button2.destroy()