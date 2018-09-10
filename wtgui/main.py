import tkinter as tk
from tkinter import ttk


class WallthickView(tk.Frame):
    """Wall thickness module"""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.wallthick = tk.StringVar()
        self.answer_string = tk.StringVar()
        self.answer_string.set("The wall thickness is unknown")

        wallthick_label = ttk.Label(self, text="Wall Thickness [mm]:")
        wallthick_entry = ttk.Entry(self, textvariable=self.wallthick)
        calc_button = ttk.Button(
            self, text="Calculate", command=self.on_calculate)
        answer_label = ttk.Label(self, textvariable=self.answer_string, font=(
            "TkDefaultFont", 50), wraplength=600)

        # Layout form
        wallthick_label.grid(row=0, column=0, sticky=tk.W)
        wallthick_entry.grid(row=0, column=1, sticky=(tk.W + tk.E))
        calc_button.grid(row=0, column=2, sticky=tk.E)
        answer_label.grid(row=1, column=0, columnspan=3)
        self.columnconfigure(1, weight=1)

    def on_calculate(self):
        """Handle calculate button clicks"""
        if self.wallthick.get().strip():
            self.answer_string.set(
                f"The wall thickness is {self.wallthick.get()} mm")
        else:
            self.answer_string.set("The wall thickness is unknown")


class App(tk.Tk):
    """Wallthick Main Application"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # set the window properties
        self.title("Wall Thickness")
        self.geometry("800x600")
        self.resizable(width=False, height=False)

        # Define the UI
        WallthickView(self).grid(sticky=(tk.E + tk.W + tk.N + tk.S))
        self.columnconfigure(0, weight=1)


def main():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
