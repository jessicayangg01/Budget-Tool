

# Import the required library
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from interface.graphsView import GraphsView
from dataProcessing.budgetReader import budgetReader


class textView(object):
    def __init__(self, win):
        self.win = win
        self.win.state('zoomed')          
        self.win.title("Jessica Plot")

        
        # Create a frame to contain the text boxes and graphs
        content_frame = Frame(self.win)
        
        # Add a Scrollbar(horizontal)
        v = Scrollbar(content_frame, orient='vertical')
        v.grid(row=0, column=2, rowspan=2, sticky="ns")

        # Title for the left text box
        label_left = Label(content_frame, text="Event Logger", font=("Georgia", 12))
        label_left.grid(row=0, column=0)

        # Add a text widget on the top-left side
        self.text_left = Text(content_frame, font=("Georgia", 10), yscrollcommand=v.set)
        self.text_left.grid(row=1, column=0, padx=(0, 5), pady=(0, 5), sticky="nsew")

        # Attach the scrollbar with the left text widget
        v.config(command=self.text_left.yview)

        # Title for the right text box
        label_right = Label(content_frame, text="Data Tool", font=("Georgia", 12))
        label_right.grid(row=0, column=1)

        # Add another text widget on the top-right side
        self.text_right = Text(content_frame, font=("Georgia", 10), yscrollcommand=v.set)
        self.text_right.grid(row=1, column=1, padx=(0, 5), pady=(0, 5), sticky="nsew")

        # Attach the scrollbar with the right text widget
        v.config(command=self.text_right.yview)
        
        # Configure row and column weights to make the text boxes resizable
        content_frame.grid_rowconfigure(1, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        
        # Pack the content frame to take up 1/3 of the window height
        content_frame.pack(fill=BOTH, expand=True)








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
            self.addText_left("Error. Too many graphs. Please delete a graph view before adding another.")
            return
        # Create a new GraphsView instance
        new_graph_view = GraphsView(self.win)
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

        # new_graph_view.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)

    def addText_right(self, message):
        self.text_right.insert(END, ""+message)
        self.text_right.insert(END, "\n")
        self.text_right.see(END) 
    
    def addText_left(self, message):
        self.text_left.insert(END, ""+message)
        self.text_left.insert(END, "\n")
        self.text_left.see(END) 