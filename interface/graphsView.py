import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.artist import Artist
import numpy as np


from tkinter import filedialog
from dataProcessing.budgetReader import budgetReader
from dataProcessing.dataAnalysis import dataAnalysis
import assets


## new

from tkinter import * 
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  NavigationToolbar2Tk) 

# popup
from interface.popupWindow import PopupWindow



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
        button1 = Button(self.canvas.get_tk_widget(), text="Calculate")
        button2 = Button(self.canvas.get_tk_widget(), text="Open File")
        button3 = Button(self.canvas.get_tk_widget(), text="Predict")

        # Position the buttons at the bottom of the canvas
        window.update_idletasks()
        canvas_height = self.canvas.get_tk_widget().winfo_height()
        button1.place(x=50, y=canvas_height-50)
        button2.place(x=150, y=canvas_height-50)
        button3.place(x=250, y=canvas_height-50)

        # Bind the buttons to their respective functions
        button1.bind("<Button-1>", self.calculate)
        button2.bind("<Button-1>", self.openFile)
        button3.bind("<Button-1>", self.predict)


        ### this is for the file 
        self.file = None
        # this is for the budget reader
        self.readBudget = None

        # popup
        # self.popup_button = Button(self.canvas.get_tk_widget(), text="Open Popup", command=self.open_popup)
        # self.popup_button.place(x=350, y=canvas_height-50)
                


    def remove(self):
        self.canvas.get_tk_widget().destroy()


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

        # these are matplotlib.patch.Patch properties
        self.currPlot.text(0, 0, textstr, fontsize = 8, bbox = dict(facecolor = 'white', alpha = 0.5))
        print("YES ADD TEXT 3")


### BUTTONS -------------------------------------------
    # def calculate(self, event):
        
        
    #     print("button clicked")
    #     assets.load_dataFiles()

    #     # maybe add a way you can add multiple files
    #     readBudget = budgetReader(assets.get_dataFile("DummyData"))
    #     readBudget.dataClean()
        
    #     # analyzeBudget.randomForest()
    #     self.plot(readBudget)
    #     self.dataanalyze = readBudget
        

    def calculate(self, event): 

        if not self.file:
            self.event_logger.addtext("no file to read from")
            return
        
        self.event_logger.addtext("Calculating for "+ self.file)

        
        self.readBudget.dataClean()
        
        # analyzeBudget.randomForest()
        self.plot()
        self.dataanalyze = self.readBudget
       

    def openFile(self, event):
        filepath = filedialog.askopenfilename(initialdir="C:\\Users\\Cakow\\PycharmProjects\\Main",
                                            title="Open file okay?",
                                            filetypes= (("text files","*.txt"),
                                            ("all files","*.*")))
        file = open(filepath,'r')
        self.file = filepath
        # print(file.read())
        file.close()
        self.event_logger.addtext("added file "+ filepath)
        
        # maybe add a way you can add multiple files
        self.readBudget = budgetReader(self.file, self.data_logger)
        self.open_popup_selectIndependent()


        
    

    def predict(self, event):
        self.event_logger.addtext("predictions incoming ...")
        analyzeBudget = dataAnalysis(self.dataanalyze, self.data_logger)
        analyzeBudget.predict([[1, 16,6.566230788,2.907982773,1]])


#### POPUP STUFF
    def open_popup_selectIndependent(self):
        # Create and open the popup window
        # popup = PopupWindow(self.canvas.get_tk_widget())
        # # popup.open_text_entry("this is the text",print("HI"))
        # popup.open_variable_list("this is the text",["one", "two", 3, 4])
        # print("why doesnt this work", popup.get_selected_variables())
        # # popup.open_text_yes_no("this is the text", print("yes"), print("NO"))
        

        def handle_done(selected_vars):
            # selected_vars = popup.get_selected_variables()
            self.data_logger.addtext("Selected the following variable(s) as dependent variables: "+ str(selected_vars))
            if len(selected_vars) > 1:
                self.event_logger.addtext("this application does not yet support more than one dependent variable")

            self.readBudget.setIndependentVar(selected_vars[0])

        popup = PopupWindow(self.canvas.get_tk_widget())
        popup.open_variable_list("Select the dependent variable", self.readBudget.getCol(), handle_done)