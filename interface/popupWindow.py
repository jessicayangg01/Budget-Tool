#### NEW POP UP --------------------------------------------
from tkinter import Button, Toplevel, Label, Entry, Checkbutton, IntVar, Text

class PopupWindow:
    def __init__(self, canvas):
        self.canvas = canvas
        self.selected_variables = []
        

    def open_text_entry(self, text, on_enter):
        popup_window = Toplevel()
        popup_window.title("Popup Window")

        label = Label(popup_window, text=text)
        label.pack()

        label = Label(popup_window, text="Enter text:")
        label.pack()

        text_box = Text(popup_window, height=4, width=30)
        text_box.pack()

        button_enter = Button(popup_window, text="Enter", command=lambda: on_enter(text_box.get("1.0", "end-1c")))
        button_enter.pack()

        self._center_window(popup_window)
    
    def open_variable_list(self, text, variables, on_done):
        popup_window = Toplevel()
        popup_window.title("Popup Window")

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
        popup_window.title("Popup Window")

        label = Label(popup_window, text=text)
        label.pack()

        button_yes = Button(popup_window, text="Yes", command=on_yes)
        button_yes.pack(side="left")

        button_no = Button(popup_window, text="No", command=on_no)
        button_no.pack(side="left")

        self._center_window(popup_window)

    def _center_window(self, window):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        window.geometry(f"+{canvas_width // 2}+{canvas_height // 2}")
