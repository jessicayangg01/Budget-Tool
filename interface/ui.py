from dataProcessing.datasets import datasets
import logging
import tkinter as tk

class SimpleApp:
    def __init__(self):
        # Logger maybe should be passed in?
        
        logger = logging.getLogger(__name__)
        self.root  = tk.Tk()
        self.root.title("XYZ")
        self.datasets = datasets(logger)

        # Error handling?
        if not self.datasets.get_dataset_names():
            raise ValueError("No datasets found")

        # Create menu for swapping between files
        self.selected_option = tk.StringVar(str(self.datasets.get_dataset_names()[0]))
        self.option_menu = tk.OptionMenu(self.root, self.selected_option, *self.datasets.get_dataset_names(), command=self.selection_changed)
        self.option_menu.pack()

    def selection_changed(self, *args):
        self.datasets.dataset = self.selected_option.get()
