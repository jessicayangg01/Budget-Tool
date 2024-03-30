#### NEW POP UP --------------------------------------------
from tkinter import (
    Tk, Frame, Toplevel, Label, Button, Entry, Checkbutton, Canvas, 
    Scrollbar, IntVar, StringVar, Text, Radiobutton, LEFT, RIGHT, BOTTOM, BOTH, VERTICAL, Y
)

class PopupWindow:
    def __init__(self, canvas):
        self.canvas = canvas
        self.selected_variables = []
        

    def open_text_entry(self, text, variables, on_enter):
        popup_window = Toplevel()
        popup_window.title("Data Entry")

        label = Label(popup_window, text=text)
        label.pack()

        text_boxes = []
        for prompt in variables:
            label = Label(popup_window, text=prompt)
            label.pack()

            text_box = Text(popup_window, height=4, width=30)
            text_box.pack()
            text_boxes.append(text_box)

        button_enter = Button(popup_window, text="Enter", command=lambda: self._get_text_entries(text_boxes, variables, on_enter, popup_window))
        button_enter.pack()

        self._center_window(popup_window)

    def _get_text_entries(self, text_boxes, variables, on_enter, window):
        text_entries = {}
        for i, text_box in enumerate(text_boxes):
            prompt = variables[i]  # Get the prompt text from the label
            val = text_box.get("1.0", "end-1c").strip()
            if val:
                if val.isdigit():  # Check if input is a valid integer
                    text_entries[prompt] = int(val)
                elif val.replace('.', '', 1).isdigit():  # Check if input is a valid float
                    text_entries[prompt] = float(val)
                else:
                    text_entries[prompt] = 0  # If input is neither integer nor float, set it to 0
            else:
                text_entries[prompt] = 0

        
        on_enter(text_entries)
        window.destroy()
    
    def open_err_message(self, text):
        popup_window = Toplevel()
        popup_window.title("Error Message")

        label = Label(popup_window, text=text)
        label.pack()

        def ok(window):
            window.destroy()  # Close the popup window after clicking "Yes"

        button = Button(popup_window, text="Okay", command=lambda: ok(popup_window))
        button.pack()

        self._center_window(popup_window)
    
    # def open_variable_list(self, text, variables, on_done):
    #     popup_window = Toplevel()
    #     popup_window.title("Selection Menu")

    #     label = Label(popup_window, text=text)
    #     label.pack()

    #     # Create a canvas to contain the checkbuttons
    #     canvas = Canvas(popup_window)
    #     canvas.pack(side=LEFT, fill=BOTH, expand=True)

    #     # Add a scrollbar to the canvas
    #     scrollbar = Scrollbar(popup_window, orient=VERTICAL, command=canvas.yview)
    #     scrollbar.pack(side=RIGHT, fill=Y)
    #     canvas.config(yscrollcommand=scrollbar.set)

    #     # Create a frame to hold the checkbuttons
    #     frame = Frame(canvas)
    #     canvas.create_window((0, 0), window=frame, anchor='nw')

    #     checkbox_vars = []
    #     for var in variables:
    #         var_checkbox = IntVar(value=0)
    #         checkbox_vars.append(var_checkbox)
    #         checkbox = Checkbutton(frame, text=var, variable=var_checkbox)
    #         checkbox.pack()

    #     # Update scroll region after widgets are packed
    #     frame.update_idletasks()
    #     canvas.config(scrollregion=canvas.bbox("all"))

    #     # Move the "Done" button to the bottom of the popup window
    #     button_done = Button(popup_window, text="Done", command=lambda: self._get_selected_variables(checkbox_vars, variables, popup_window, on_done))
    #     button_done.pack(side='bottom')

    #     # Bind mouse wheel scrolling to the canvas
    #     # canvas.bind_all("<MouseWheel>", lambda event: self._on_mousewheel(event, canvas))

    #     self._center_window(popup_window)
        
    # def _get_selected_variables(self, checkbox_vars, variables, window, on_done):
    #     self.selected_variables.clear()
    #     for var, var_checkbox in zip(variables, checkbox_vars):
    #         if var_checkbox.get() == 1:
    #             self.selected_variables.append(var)
        
    #     on_done(self.selected_variables)
    #     window.destroy()
        
    def open_variable_list(self, text, variables, on_done):
        popup_window = Toplevel()
        popup_window.title("Selection Menu")

        label = Label(popup_window, text=text)
        label.pack()

        # Create a canvas to contain the radio buttons
        canvas = Canvas(popup_window)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        # Add a scrollbar to the canvas
        scrollbar = Scrollbar(popup_window, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        canvas.config(yscrollcommand=scrollbar.set)

        # Create a frame to hold the radio buttons
        frame = Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor='nw')

        # Variable to track the selected option
        selected_option = StringVar()

        # List to store the Radiobutton objects
        radio_buttons = []

        for var in variables:
            radio_button = Radiobutton(frame, text=var, variable=selected_option, value=var)
            radio_button.pack()
            radio_buttons.append(radio_button)

        # Function to get the selected variable
        def get_selected_variable():
            selected_var = selected_option.get()
            popup_window.destroy()  # Close the popup window
            on_done(selected_var)  # Pass the selected variable to the callback function

        # Create a "Done" button to get the selected variable
        button_done = Button(popup_window, text="Done", command=get_selected_variable)
        button_done.pack(side='bottom')

        # Update scroll region after widgets are packed
        self._center_window(popup_window)


    
    def open_text_yes_no(self, text, on_yes, on_no):
        def close_window():
            popup_window.destroy()

        popup_window = Toplevel()
        popup_window.title("Select Menu")

        label = Label(popup_window, text=text)
        label.pack()

        button_yes = Button(popup_window, text="Yes", command=lambda: [on_yes(), close_window()])
        button_yes.pack(side="left")

        button_no = Button(popup_window, text="No", command=lambda: [on_no(), close_window()])
        button_no.pack(side="left")

        self._center_window(popup_window)
    

    def open_ticker_entry(self, text, on_enter):
        popup_window = Toplevel()
        popup_window.title("Ticker Entry")

        label = Label(popup_window, text=text)
        label.pack()

        entry = Entry(popup_window, width=30)
        entry.pack()

        button_enter = Button(popup_window, text="Okay", command=lambda: self._get_ticker_entry(entry, on_enter, popup_window))
        button_enter.pack()

        self._center_window(popup_window)

    def _get_ticker_entry(self, entry, on_enter, window):
        ticker = entry.get().strip()
        if ticker:
            window.destroy()
            on_enter(ticker)
        else:
            window.destroy()
            on_enter("")
        window.destroy()

    def _center_window(self, window):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        window.geometry(f"+{canvas_width // 2}+{canvas_height // 2}")
        window.attributes("-topmost", True)
