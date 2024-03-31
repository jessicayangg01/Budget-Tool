import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
from dataProcessing.marketDataAnalysis import MarketDataAnalysis
from dataProcessing.marketData import MarketData
import numpy as np



class GraphTabs:
    def __init__(self, canvas, stockData: MarketData, data_logger):
        self.canvas = canvas
        self.stockData = stockData
        self.notebook = ttk.Notebook(self.canvas.get_tk_widget())
        # self.notebook.pack(fill=tk.BOTH, expand=True)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=55)
        self.data_logger = data_logger

        # Configure the style for the notebook
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Use the 'clam' theme
        self.style.configure('TNotebook', background='lightgrey')  # Set background color for the notebook
        self.style.map('TNotebook.Tab', background=[('selected', 'lightgreen')])  # Set background color for selected tab


        self.TimeSeries = self.create_graph("Time Series Analysis")
        # self.Correlation = self.create_graph("Correlation Analysis")
        self.Reg = self.create_graph("Linear Regression")
        # self.ROI = self.create_graph("Return on Investment Analysis")
        self.Predict = self.create_graph("Random Forest Regression")


        self.allPlotLines1 = {}
        self.allPlotLines2 = {}
        # self.marketDataAnalysis = MarketDataAnalysis()
        self.marketDataAnalysis = MarketDataAnalysis()
        # self.lin_reg_line = None

        # Bind the function to the <<NotebookTabChanged>> event
        # self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
    
    def create_graph(self, title):
        # Create a new subplot for each tab
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text=title)
        return tab

    def update(self, data, ticker):
        self.time_series_add(data, ticker)
        self.correlation_add()
        self.linear_reg_add(data, ticker)
        self.random_forest_reg_add()
    
    def delete(self, ticker):
        self.time_series_remove(ticker)
        self.linear_reg_remove(ticker)
        return True
    
    
    def time_series_add(self, data, ticker):
        # Ensure the figure and axes are already created
        if not hasattr(self, 'fig1') or not hasattr(self, 'ax1'):
            self.fig1, self.ax1 = plt.subplots()
            self.ax1.set_title("Sales over Marketing Budget Trend Over Time")
            self.canvas1 = FigureCanvasTkAgg(self.fig1, master=self.TimeSeries)
            self.canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Plot some example data
        x = data["years"]
        y = data["ratio"]
        plot = self.ax1.plot(x, y, label=ticker)

        # Append the line data to self.allPlotLines
        self.allPlotLines1[ticker] = plot

        # self.lin_reg_line = None

        self.ax1.legend()

        # Embed the plot in the canvas
        self.canvas1.draw()
    
    def time_series_remove(self, ticker):
        if ticker in self.allPlotLines1:
            self.allPlotLines1[ticker][0].remove()
            del self.allPlotLines1[ticker]  # Remove the plot from the dictionary
            self.canvas1.draw()
            if not self.allPlotLines1:
                self.ax1.clear()
                self.canvas1.draw()
                return
            self.ax1.legend()
            self.canvas1.draw()  # Redraw the canvas
            return True
        else:
            print("Plot with ticker '{}' does not exist.".format(ticker))
            return False
    

    def correlation_add(self):
        data = self.stockData.getPlotList("X", "Y")
        if not data["X"]:
            return

        corr = self.marketDataAnalysis.correlation_analysis(data["X"], data["Y"])
        # Create a new tab
        self.data_logger.addtext("Correlation between all X and Y: " + str(corr))
        
        
        # Display correlation coefficient on the tab
        # label = tk.Label(self.Correlation, text=f"Correlation between Sales and Marketing Budget: {corr:.2f}")
        # label.pack(padx=10, pady=10)
    

    def linear_reg_add(self, data, ticker):
        # Ensure the figure and axes are already created
        if not hasattr(self, 'fig2') or not hasattr(self, 'ax2'): 
            self.fig2, self.ax2 = plt.subplots()
            self.ax2.set_title("Sales over Marketing")
            self.canvas2 = FigureCanvasTkAgg(self.fig2, master=self.Reg)
            self.canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Plot some example data
        x = data["X"]
        y = data["Y"]
        plot = self.ax2.scatter(x, y, label=ticker)

        # Append the line data to self.allPlotLines
        self.allPlotLines2[ticker] = plot
        self.ax2.legend()

        self.caculate_linear_reg()

        # Embed the plot in the canvas
        self.canvas2.draw()
    
    def linear_reg_remove(self, ticker):
        if ticker in self.allPlotLines2:
            self.allPlotLines2[ticker].remove()
            del self.allPlotLines2[ticker]  # Remove the plot from the dictionary
            self.canvas2.draw()
            if not self.allPlotLines2:
                self.ax2.clear()
                return 
            self.ax2.legend()
            self.caculate_linear_reg()
            self.canvas2.draw()  # Redraw the canvas
            return True
        else:
            print("Plot with ticker '{}' does not exist.".format(ticker))
            return False
    
    def caculate_linear_reg(self):
        if hasattr(self, 'lin_reg_line'):
            self.lin_reg_line[0].remove()
            del self.lin_reg_line
        ## add linear regression
        plotList = self.stockData.getPlotList("X", "Y")
        x = plotList["X"]
        y = plotList["Y"]
        if not x:
            return
        data = self.marketDataAnalysis.linearRegression(x, y)
        self.lin_reg_line = self.ax2.plot(x, data.predict(np.array(x).reshape(-1, 1)), color='red', label='Linear regression')
        # Display linear regression results in a text box
        self.lin_reg_text_box = tk.Text(self.Reg)
        self.lin_reg_text_box.insert(tk.END, f"Slope (Coefficient): {data.coef_[0]:.2f}\n")
        self.lin_reg_text_box.insert(tk.END, f"Intercept: {data.intercept_:.2f}")
        self.lin_reg_text_box.pack(padx=10, pady=10)
        self.canvas2.draw()
    
    def random_forest_reg_add(self):
        # Ensure the figure and axes are already created
        if not hasattr(self, 'fig3') or not hasattr(self, 'ax3'): 
            self.fig3, self.ax3 = plt.subplots()
            self.ax3.set_title("Sales over Marketing")
            self.canvas3 = FigureCanvasTkAgg(self.fig3, master=self.Predict)
            # self.canvas3.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            self.canvas3.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        else:
            self.ax3.clear()

        # Plot some example data
        data = self.stockData.getPlotList("X", "Y")
        x = data["X"]
        y = data["Y"]
        data = self.stockData.getPlotList("X", "years")
        z = data["years"]

        if not x:
            return False
        
        output = self.marketDataAnalysis.randomForestRegression(y,x,z)

        # Plot the actual values against the predicted values
        
        y_test = output["y_test"].ravel()
        y_pred = output["y_pred"]

        self.ax3.scatter(y_test, y_pred, color='blue', label='Actual vs Predicted')
        if len(y_test) >1:
            self.ax3.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', linestyle='--', label='Perfect Prediction')

        # Add labels and title
        self.ax3.set_xlabel('Actual Sales')
        self.ax3.set_ylabel('Predicted Sales')
        self.ax3.set_title('Actual vs Predicted Sales')

        self.ax3.legend()

        if hasattr(self, 'text_box'):
            self.text_box.destroy()

        

        # # Display Mean Squared Error (MSE) and model data in a text box
        self.text_box = tk.Text(self.Predict, width=20)
        model = output["model"]
        mse = output["mse"]
        importance = model.feature_importances_
        prediction_variance = output['prediction_variance']
        model_parameters = model.get_params()
        residuals = y_test - y_pred
        
        self.data_logger.addtext("__________________________________________")
        self.data_logger.addtext("Data Prediction Model Information: ")
        self.data_logger.addtext("Mean Squared Error (MSE): " + str(mse))
        self.data_logger.addtext("Importance score for each input feature: " + str(importance))
        self.data_logger.addtext("Prediction Variance: " + str(prediction_variance))
        self.data_logger.addtext("Model Params: " + str(model_parameters))
        self.data_logger.addtext("Residuals: " + str(residuals))
        self.data_logger.addtext("__________________________________________")
        
        # Embed the plot in the canvas
        self.canvas3.draw()
    
    # def on_tab_change(self, event):
    #     # Get the index of the currently selected tab
    #     current_tab_index = self.notebook.index("current")

    #     # Get the text label of the currently selected tab
    #     current_tab_label = event.widget.tab(current_tab_index, "text")

    #     if current_tab_label == "Predictive Modelling":
    #         self.data_logger.addtext("__________________________________________")
    #         self.data_logger.addtext("Data Prediction Model Information: ")
    #         self.random_forest_reg_add()
            
