

# Import the required library
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from interface.graphsView import GraphsView
from dataProcessing.budgetReader import budgetReader


# loggers
from interface.eventLogger import EventLogger
from interface.dataLogger import DataLogger


class mainWindow(object):
    def __init__(self, win):
        self.win = win
        self.win.state('zoomed')          
        self.win.title("Jessica Plot")
        
        # Create a frame to contain the loggers
        loggers_frame = Frame(win)
        loggers_frame.pack(fill="x")  # Pack horizontally

        # Create and pack the EventLogger frame
        self.event_logger = EventLogger(loggers_frame)
        self.event_logger.pack(side="left", fill="both", expand=True)

        # Create and pack the DataLogger frame
        self.data_logger = DataLogger(loggers_frame)
        self.data_logger.pack(side="left", fill="both", expand=True)


    

        # Create a plot button
        self.plot_button = Button(master=self.win, 
                                  command=self.plot,
                                  height=2, 
                                  width=10, 
                                  text="Add New Plot") 
        self.plot_button.pack(side=BOTTOM, pady=10)

        # Initialize a list to hold GraphsView instances
        self.graph_views = []

    def plot(self):
        if len(self.graph_views) >=3:
            self.event_logger.addtext("Error. Too many graphs. Please delete a graph view before adding another.")
            return
        # Create a new GraphsView instance
        new_graph_view = GraphsView(self.win, self.data_logger, self.event_logger)
        self.graph_views.append(new_graph_view)

        # Create a button to remove the canvas
        def remove_canvas():
            self.graph_views.remove(new_graph_view)
            new_graph_view.remove()
            button_remove.destroy()

        button_remove = Button(self.win, text="Remove Canvas", command=remove_canvas)
        button_remove.place(in_=new_graph_view.canvas.get_tk_widget(), relx=1.0, rely=0.0, anchor=NE)

        # Pack the new GraphsView instance within the content frame
        new_graph_view.canvas.get_tk_widget().pack(side=LEFT, fill=BOTH, expand=True)
