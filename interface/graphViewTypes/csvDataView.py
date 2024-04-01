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

        self.deg = 2

        # type of predict
        self.reg_type = None

        # placing the canvas on the Tkinter window 
        self.canvas.get_tk_widget().pack(fill="both", expand=True)  # Fill the entire window
        self.canvas.get_tk_widget().config(borderwidth=2, relief="solid")
        
        self.fig.suptitle("Graphs View", fontsize=12)


        # Create two Tkinter buttons
        self.button1 = Button(self.canvas.get_tk_widget(), text="Linear Reg", width=20)
        self.button2 = Button(self.canvas.get_tk_widget(), text="Polynomial Reg", width=20)
        self.button3 = Button(self.canvas.get_tk_widget(), text="Predict", width=20)

        # Position the buttons at the bottom of the canvas
        canvas_height = self.canvas.get_tk_widget().winfo_height()
        self.button1.place(x=50, y=canvas_height-50)
        self.button2.place(x=250, y=canvas_height-50)
        self.button3.place(x=450, y=canvas_height-50)

        # Bind the buttons to their respective functions
        self.button1.bind("<Button-1>", self.calculate)
        self.button2.bind("<Button-1>", self.polymomial_reg)
        self.button3.bind("<Button-1>", self.predict)

        # Change button color on hover
        def change_button_color(button, color):
            button.config(bg=color)

        self.button1.bind("<Enter>", lambda event: change_button_color(self.button1, "#4CAF50"))  # Green color on hover
        self.button1.bind("<Leave>", lambda event: change_button_color(self.button1, "SystemButtonFace"))  # Original color on leave
        self.button2.bind("<Enter>", lambda event: change_button_color(self.button2, "#4CAF50"))  # Green color on hover
        self.button2.bind("<Leave>", lambda event: change_button_color(self.button2, "SystemButtonFace"))  # Original color on leave
        self.button3.bind("<Enter>", lambda event: change_button_color(self.button3, "#4CAF50"))  # Green color on hover
        self.button3.bind("<Leave>", lambda event: change_button_color(self.button3, "SystemButtonFace"))  # Original color on leave


    def predict(self, event):
        self.event_logger.addtext("predictions incoming ...")
        self.open_popup_user_predict("Input your budget data", self.readBudget.getDependentVar())
    

    def calculate(self, event): 

        if not self.file:
            self.event_logger.addtext("no file to read from")
            return
        # Iterate over all subplots and remove them
        for ax in self.fig.axes:
            ax.remove()
        self.event_logger.addtext("Calculating for "+ self.file)
        self.data_logger.addtext("________________________________________________________")
        self.reg_type = "linear"
        self.plot()
    
    def polymomial_reg(self, event): 

        if not self.file:
            self.event_logger.addtext("no file to read from")
            return
        
        # Iterate over all subplots and remove them
        for ax in self.fig.axes:
            ax.remove()

        self.event_logger.addtext("Calculating for "+ self.file)
        self.data_logger.addtext("________________________________________________________")
        self.reg_type = "poly"
        self.plot()
    

    def showGraph(self, graph, subplot, title, type, line):
        # self.currPlot = self.fig.add_subplot(subplot)
        self.currPlot = self.fig.add_subplot(subplot[0], subplot[1], subplot[2])
        
        
        if type == "scatter":
            self.currPlot.scatter(x =graph[1], y=graph[0], s=1)
        else:
            self.currPlot.plot(graph)
        
        # plt.xlabel(title) 
        self.currPlot.set_title(title)
        self.currPlot.set_xlabel(title)
        self.currPlot.set_ylabel(str(self.readBudget.independent_var))

        # plot line
        if self.reg_type  == "linear":
            self.fig.suptitle("Linear Regression Model", fontsize=12)
            x_vals = np.array(self.currPlot.get_xlim())
            y_vals = line["intercept"] + line["slope"] * x_vals
            self.currPlot.plot(x_vals, y_vals, 'r--')
        if self.reg_type == "poly":
            self.fig.suptitle("Polynomial Regression Model", fontsize=12)
            self.currPlot.plot(line[0], line[1], color='red', linewidth=1, label='Polynomial Regression Line')


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
            # Initialize variables to store the best grid dimensions and the minimum difference
            best_diff = float('inf')
            best_rows = 1
            best_cols = numPlots
            
            # Iterate through all possible combinations of rows and columns
            for rows in range(1, numPlots + 1):
                cols = math.ceil(numPlots / rows)
                total_plots = rows * cols
                
                # Update the best grid dimensions if it fits all the plots and minimizes the difference
                if total_plots >= numPlots and abs(rows - cols) < best_diff:
                    best_diff = abs(rows - cols)
                    best_rows = rows
                    best_cols = cols
            
            return best_rows, best_cols

        num_rows, num_cols = calculate_grid_dimensions(len(self.readBudget.getDependentVar()))
        grid = [num_rows, num_cols, 0]

        for col in self.readBudget.getDependentVar():
            if self.reg_type == "linear":
                line  = analyzeBudget.linearRegression(col)
                if not line:
                    self.event_logger.addtext("Could not output graph for column : " + str(col) + "due to calculation error.")
                else:
                    # self.showGraph([self.readBudget.data[self.readBudget.independent_var], self.readBudget.data[col]], 330+n, col, "scatter", line)
                    grid[2] = n
                    self.showGraph([self.readBudget.data[self.readBudget.independent_var], self.readBudget.data[col]], grid, col, "scatter", line)
                    self.textBox(line, col)
                n+=1
            if self.reg_type == "poly":
                output = analyzeBudget.polynomial_regression(col, self.deg)
                if not output:
                    self.event_logger.addtext("Could not output graph for column : " + str(col) + " due to calculation error.")
                else:
                    # self.showGraph([self.readBudget.data[self.readBudget.independent_var], self.readBudget.data[col]], 330+n, col, "scatter", line)
                    grid[2] = n
                    line = [output["x_range"], output["y_pred"]]
                    self.showGraph([self.readBudget.data[self.readBudget.independent_var], self.readBudget.data[col]], grid, col, "scatter", line)
                    # Keys to exclude from the output
                    keys_to_exclude = ["x_range", "y_pred"]

                    # Create a new dictionary excluding the specified keys  
                    show = {key: value for key, value in output.items() if key not in keys_to_exclude}
                    self.textBox(show, col)
                n+=1

            
        

    # def textBox(self, line, col):
    #     self.data_logger.addtext("The following was calculated for " + str(col) + " against " + str(self.readBudget.independent_var))

    #     # show text
    #     textstr = ""
    #     for i in line:
    #         textstr += str(i) + ":" + str(line[i])
    #         textstr += "\n"
    #         self.data_logger.addtext(str(i) + ":" + str(line[i]))
    
    #     self.currPlot.text(0, 0, textstr, fontsize = 8, bbox = dict(facecolor = 'white', alpha = 0.5))
    #     self.canvas.draw() 
    def textBox(self, line, col):
        self.data_logger.addtext("The following was calculated for " + str(col) + " against " + str(self.readBudget.independent_var))

        # Create text string
        textstr = ""
        for i in line:
            textstr += str(i) + ":" + str(line[i])
            textstr += "\n"
            self.data_logger.addtext(str(i) + ":" + str(line[i]))

        # Position the text box on the top right corner
        x_pos = 0.95  # Adjust the x-coordinate to position the text box horizontally
        y_pos = 0.95  # Adjust the y-coordinate to position the text box vertically

        self.currPlot.text(x_pos, y_pos, textstr, fontsize=8, bbox=dict(facecolor='white', alpha=0.5),
                            horizontalalignment='right', verticalalignment='top', transform=self.currPlot.transAxes)
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
            
            if self.reg_type == "linear":
                analyzeBudget.predict(selected_vars)
            if self.reg_type == "poly":
                analyzeBudget.predict_polynomial_reg(selected_vars, self.deg)
                budget = sum(selected_vars.values())
                analyzeBudget.recommend_changes_polynomial_reg(selected_vars, self.deg, budget)
        popup = PopupWindow(self.canvas.get_tk_widget())
        popup.open_text_entry(text, variables, handle_done)

    