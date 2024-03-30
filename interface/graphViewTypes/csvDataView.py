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
import math



class CsvDataView(object):
    def __init__(self, canvas, data_logger, event_logger, file, readBudget, fig):
        self.canvas = canvas
        self.data_logger = data_logger
        self.event_logger = event_logger
        self.file = file
        self.readBudget = readBudget
        self.fig = fig

        # placing the canvas on the Tkinter window 
        self.canvas.get_tk_widget().pack(fill="both", expand=True)  # Fill the entire window
        self.canvas.get_tk_widget().config(borderwidth=2, relief="solid")
        
        self.fig.suptitle("Graphs View", fontsize=12)


        # Create two Tkinter buttons
        self.button1 = Button(self.canvas.get_tk_widget(), text="Calculate", width=35)
        self.button3 = Button(self.canvas.get_tk_widget(), text="Predict", width=35)

        # Position the buttons at the bottom of the canvas
        canvas_height = self.canvas.get_tk_widget().winfo_height()
        self.button1.place(x=50, y=canvas_height-50)
        self.button3.place(x=350, y=canvas_height-50)

        # Bind the buttons to their respective functions
        self.button1.bind("<Button-1>", self.calculate)
        self.button3.bind("<Button-1>", self.predict)

        # Change button color on hover
        def change_button_color(button, color):
            button.config(bg=color)

        self.button1.bind("<Enter>", lambda event: change_button_color(self.button1, "#4CAF50"))  # Green color on hover
        self.button1.bind("<Leave>", lambda event: change_button_color(self.button1, "SystemButtonFace"))  # Original color on leave
        self.button3.bind("<Enter>", lambda event: change_button_color(self.button3, "#4CAF50"))  # Green color on hover
        self.button3.bind("<Leave>", lambda event: change_button_color(self.button3, "SystemButtonFace"))  # Original color on leave


    def predict(self, event):
        self.event_logger.addtext("predictions incoming ...")
        self.open_popup_user_predict("Input your budget data", self.readBudget.getDependentVar())
    

    def calculate(self, event): 

        if not self.file:
            self.event_logger.addtext("no file to read from")
            return
        
        self.event_logger.addtext("Calculating for "+ self.file)
        self.data_logger.addtext("________________________________________________________")
        
        self.plot()
    

    def showGraph(self, graph, subplot, title, type, line):
        self.currPlot = self.fig.add_subplot(subplot)
        if type == "scatter":
            self.currPlot.scatter(x =graph[1], y=graph[0], s=1)
        else:
            self.currPlot.plot(graph)
        
        # plt.xlabel(title) 
        self.currPlot.set_title(title)
        self.currPlot.set_xlabel(title)
        self.currPlot.set_ylabel(str(self.readBudget.independent_var))
        

        # plot line
        x_vals = np.array(self.currPlot.get_xlim())
        y_vals = line["intercept"] + line["slope"] * x_vals
        self.currPlot.plot(x_vals, y_vals, 'r--')

        # adjust size to leave room for other graphs
        self.fig.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.2, 
                    hspace=0.6)
        

        # adjust size to leave room for buttons
        self.fig.subplots_adjust(bottom=0.2) 


        self.canvas.draw() 
        


    
    def plot(self):
        n=1
        analyzeBudget = dataAnalysis(self.readBudget, self.data_logger, self.event_logger)


        def calculate_grid_dimensions(numPlots):
            # Initialize variables to store the best grid dimensions
            best_rows = 1
            best_cols = numPlots
            
            # Find the factors of numPlots
            for i in range(2, int(math.sqrt(numPlots)) + 1):
                if numPlots % i == 0:
                    rows = i
                    cols = numPlots // i
                    
                    # Update the best grid dimensions if the new dimensions are closer to being square
                    if abs(cols - rows) < abs(best_cols - best_rows):
                        best_rows = rows
                        best_cols = cols
            
            return best_rows, best_cols

        num_rows, num_cols = calculate_grid_dimensions(len(self.readBudget.getDependentVar()))
        grid = str(num_rows) + str(num_cols)

        for col in self.readBudget.getDependentVar():
            line  = analyzeBudget.linearRegression(col)

            if not line:
                self.event_logger.addtext("Could not output graph for column : " + str(col) + "due to calculation error.")
            else:
                # self.showGraph([self.readBudget.data[self.readBudget.independent_var], self.readBudget.data[col]], 330+n, col, "scatter", line)
                pos = grid + str(n)
                self.showGraph([self.readBudget.data[self.readBudget.independent_var], self.readBudget.data[col]], int(pos), col, "scatter", line)
                self.textBox(line, col)
                n+=1
        

    def textBox(self, line, col):
        self.data_logger.addtext("The following was calculated for " + str(col) + " against " + str(self.readBudget.independent_var))

        # show text
        textstr = ""
        for i in line:
            textstr += str(i) + ":" + str(line[i])
            textstr += "\n"
            self.data_logger.addtext(str(i) + ":" + str(line[i]))

        self.currPlot.text(0, 0, textstr, fontsize = 8, bbox = dict(facecolor = 'white', alpha = 0.5))
        self.canvas.draw() 
        


    
    
    def open_popup_error(self, message):
        # Create and open the popup window
        popup = PopupWindow(self.canvas.get_tk_widget())
        popup.open_err_message(message)


    
    def open_popup_user_predict(self, text, variables):
        # Create and open the popup window
        def handle_done(selected_vars):
            # selected_vars = popup.get_selected_variables()
            self.data_logger.addtext("Inputed the following variables: "+ str(selected_vars))
            
            analyzeBudget = dataAnalysis(self.readBudget, self.data_logger, self.event_logger)
            analyzeBudget.predict(selected_vars)
        popup = PopupWindow(self.canvas.get_tk_widget())
        popup.open_text_entry(text, variables, handle_done)

    