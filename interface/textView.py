

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
        self.win.title("Marketing Budget Tool")
        # self.win.configure(bg="black")
        
        # Create a frame to contain the loggers
        loggers_frame = Frame(win)
        loggers_frame.pack(fill="x")  # Pack horizontally

        # Create and pack the EventLogger frame
        self.event_logger = EventLogger(loggers_frame)
        self.event_logger.pack(side="left", fill="both", expand=True)

        # Create and pack the DataLogger frame
        self.data_logger = DataLogger(loggers_frame)
        self.data_logger.pack(side="left", fill="both", expand=True)


    

        # # Create a plot button
        # self.plot_button = Button(master=self.win, 
        #                           command=self.plot,
        #                           height=2, 
        #                           width=10, 
        #                           text="Add New Plot") 
        # self.plot_button.pack(side=BOTTOM, pady=10)

        # Create a plot button
        self.plot_button = Button(master=self.win, 
                                  command=self.plot,
                                  height=2, 
                                  width=10, 
                                  text="Add New Plot",
                                  bg="dark grey")
        self.plot_button.pack(side=BOTTOM, fill=X, pady=10)  # Fill the entire bottom space

        # Bind events to change button color on hover
        self.plot_button.bind("<Enter>", lambda event: self.change_button_color("#4CAF50"))  # Green color on hover
        self.plot_button.bind("<Leave>", lambda event: self.change_button_color("dark grey"))  # Original color on leave


        # Initialize a list to hold GraphsView instances
        self.graph_views = []

    def plot(self):
        if len(self.graph_views) >=3:
            self.event_logger.addtext("Error. Too many graphs. Please delete a graph view before adding another.")
            return
        # Create a new GraphsView instance
        self.event_logger.addtext("Adding new window to frame...")
        new_graph_view = GraphsView(self.win, self.data_logger, self.event_logger)
        self.graph_views.append(new_graph_view)

        # Create a button to remove the canvas
        def remove_canvas():
            self.event_logger.addtext("Removing window from frame...")
            self.graph_views.remove(new_graph_view)
            new_graph_view.remove()
            button_remove.destroy()

        # button_remove = Button(self.win, text="Remove Canvas", command=remove_canvas)
        # button_remove.place(in_=new_graph_view.canvas.get_tk_widget(), relx=1.0, rely=0.0, anchor=NE)
        button_remove = Button(self.win, text="Remove", command=remove_canvas)
        button_remove.place(in_=new_graph_view.canvas.get_tk_widget(), relx=0.99, rely=0.005, anchor=NE)

        # Bind events to change button color on hover
        button_remove.bind("<Enter>", lambda event: button_remove.config(bg='red'))
        button_remove.bind("<Leave>", lambda event: button_remove.config(bg='SystemButtonFace'))

        # Pack the new GraphsView instance within the content frame
        new_graph_view.canvas.get_tk_widget().pack(side=LEFT, fill=BOTH, expand=True)
    
    def change_button_color(self, color):
            self.plot_button.config(bg=color)