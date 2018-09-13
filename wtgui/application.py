import tkinter as tk
from tkinter import ttk
from datetime import datetime
from . import views as v
from . import models as m


class Application(tk.Tk):
    """Application root window"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title('Wall Thickness')
        # self.geometry("800x600")
        self.resizable(width=False, height=False)

        ttk.Label(
            self,
            text="Wall Thickness Design",
            font=('TkDefaultFont', 16)
        ).grid(row=0)

        self.inputdataform = v.InputDataForm(self, m.CSVModel.fields)
        self.inputdataform.grid(row=1, padx=10)

        # calculate button
        self.calcbutton = ttk.Button(self, text='Calculate',
                                     command=self.on_calculate)
        self.calcbutton.grid(row=2, sticky=tk.E, padx=10)

        # status bar
        self.status = tk.StringVar()
        self.statusbar = ttk.Label(self, textvariable=self.status)
        self.statusbar.grid(row=3, sticky=(tk.W + tk.E), padx=10)

        self.cals_ran = 0

    def on_calculate(self):
        """Handles calculation button clicks"""

        # Check for errors first
        errors = self.inputdataform.get_errors()
        if errors:
            self.status.set(
                f"Cannot calculate, error in fields: {', '.join(errors.keys())}"
            )
            return False

        # Hardcode filename with a datestring.
        # If it doesn't exist, create it, otherwise append existing file
        datestring = datetime.today().strftime('%Y-%m-%d')
        filename = f'wt_data_{datestring}.csv'
        model = m.CSVModel(filename)
        data = self.inputdataform.get()
        model.save_record(data)
        self.cals_ran += 1
        self.status.set(f'{self.cals_ran} calculations ran this session')
        self.inputdataform.reset()
