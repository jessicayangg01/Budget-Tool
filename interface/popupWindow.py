#### NEW POP UP --------------------------------------------
from tkinter import Button, Toplevel, Label, Entry, Checkbutton, IntVar, Text

class PopupWindow:
    def __init__(self, canvas):
        self.canvas = canvas
        self.selected_variables = []
        

    def open_text_entry(self, text, variables, on_enter):
        popup_window = Toplevel()
        popup_window.title("Text Entry")

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

        
        print(text_entries)
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
    
    def open_variable_list(self, text, variables, on_done):
        popup_window = Toplevel()
        popup_window.title("Select Menu")

        label = Label(popup_window, text=text)
        label.pack()

        checkbox_vars = []
        for var in variables:
            var_checkbox = IntVar(value=0)
            checkbox_vars.append(var_checkbox)
            checkbox = Checkbutton(popup_window, text=var, variable=var_checkbox)
            checkbox.pack()

        button_done = Button(popup_window, text="Done", command=lambda: self._get_selected_variables(checkbox_vars, variables, popup_window, on_done))
        button_done.pack()

        self._center_window(popup_window)

    def _get_selected_variables(self, checkbox_vars, variables, window, on_done):
        self.selected_variables.clear()
        for var, var_checkbox in zip(variables, checkbox_vars):
            if var_checkbox.get() == 1:
                self.selected_variables.append(var)
        window.destroy()
        on_done(self.selected_variables)

    
    def open_text_yes_no(self, text, on_yes, on_no):
        popup_window = Toplevel()
        popup_window.title("Select Menu")

        label = Label(popup_window, text=text)
        label.pack()

        button_yes = Button(popup_window, text="Yes", command=on_yes)
        button_yes.pack(side="left")

        button_no = Button(popup_window, text="No", command=on_no)
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
            on_enter(ticker)
            window.destroy()
        else:
            # showerror("Error", "Please enter a valid ticker")
            None

    def _center_window(self, window):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        window.geometry(f"+{canvas_width // 2}+{canvas_height // 2}")
