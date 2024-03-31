# Import the required library
from tkinter import *
from tkinter import ttk
from tkinter import messagebox



class EventLogger(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        v = Scrollbar(self, orient='vertical')
        v.grid(row=0, column=2, rowspan=2, sticky="ns")

        # Title for the left text box
        label_left = Label(self, text="Event Logger", font=("Georgia", 12))
        label_left.grid(row=0, column=0, sticky="w", padx=(5, 0))

        # Add a text widget on the top-left side
        self.text_left = Text(self, font=("Georgia", 10), yscrollcommand=v.set, fg="blue")
        self.text_left.grid(row=1, column=0, padx=(5, 0), pady=(0, 0), sticky="nsew")  # Set padx and pady to 0

        # Attach the scrollbar with the left text widget
        v.config(command=self.text_left.yview)

        # Configure row and column weights to make the text boxes resizable
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
    def addtext(self, message):
        self.text_left.insert(END, ""+message)
        self.text_left.insert(END, "\n")
        self.text_left.see(END) 