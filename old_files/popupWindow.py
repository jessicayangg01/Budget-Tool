#### NEW POP UP --------------------------------------------
from tkinter import Button, Toplevel, Label, Entry

class PopupWindow:
    def __init__(self, canvas, text):
        self.canvas = canvas
        self.text = text

    def open(self):
        # Define the behavior of the pop-up window
        def button1_clicked():
            print("Button 1 clicked")
            user_input = entry.get()  # Get the user input from the Entry widget
            print("User input:", user_input)
            popup_window.destroy()

        def button2_clicked():
            print("Button 2 clicked")
            popup_window.destroy()

        # Create the pop-up window
        popup_window = Toplevel()
        popup_window.title("Popup Window")

        # Add text to the pop-up window
        label = Label(popup_window, text=self.text)
        label.pack()

        # Add an Entry widget for user input
        entry = Entry(popup_window)
        entry.pack()

        # Add buttons to the pop-up window
        button1 = Button(popup_window, text="Button 1", command=button1_clicked)
        button1.pack(side="left")

        button2 = Button(popup_window, text="Button 2", command=button2_clicked)
        button2.pack(side="left")

        # Position the pop-up window on the canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        popup_window.geometry(f"+{canvas_width // 2}+{canvas_height // 2}")