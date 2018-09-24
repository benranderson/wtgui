import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from datetime import datetime
from . import views as v
from . import models as m


class Application(tk.Tk):
    """Application root window"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title('Wall Thickness')
        # self.geometry("800x600")
        # self.resizable(width=False, height=False)

        ttk.Label(
            self,
            text="Wall Thickness Design",
            font=('TkDefaultFont', 16)
        ).grid(row=0)

        datestring = datetime.today().strftime('%Y-%m-%d')
        default_filename = f'wt_data_{datestring}.csv'
        self.filename = tk.StringVar(value=default_filename)

        self.settings_model = m.SettingsModel()
        self.load_settings()

        self.callbacks = {
            'file->select': self.on_file_select,
            'file->quit': self.quit
        }

        menu = v.MainMenu(self, self.settings, self.callbacks)
        self.config(menu=menu)

        self.inputdataform = v.InputDataForm(
            self, m.CSVModel.fields, self.settings)
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
            message = "Cannot run calculation"
            detail = "The following fields have errors: \n * {}".format(
                '\n * '.join(errors.keys())
            )
            self.status.set(
                f"Cannot calculate, error in fields: {', '.join(errors.keys())}"
            )
            messagebox.showerror(title='Error', message=message, detail=detail)

            return False

        filename = self.filename.get()
        model = m.CSVModel(filename)
        data = self.inputdataform.get()
        model.save_record(data)
        self.cals_ran += 1

        if self.cals_ran > 1:
            plural = 's'
        else:
            plural = ''

        self.status.set(
            f'{self.cals_ran} calculation{plural} run this session')
        self.inputdataform.reset()

    def on_file_select(self):
        """Handle the file->select action from the menu"""

        filename = filedialog.asksaveasfilename(
            title='Select the target file for saving records',
            defaultextension='.csv',
            filetypes=[('Comma-Separated Values', '*.csv *.CSV')]
        )
        if filename:
            self.filename.set(filename)

    def save_settings(self, *args):
        """Save the current settings to the preferences file"""

        for key, variable in self.settings.items():
            self.settings_model.set(key, variable.get())
        self.settings_model.save()

    def load_settings(self):
        """Load settings into the self.settings dict"""

        vartypes = {
            'bool': tk.BooleanVar,
            'str': tk.StringVar,
            'int': tk.IntVar,
            'float': tk.DoubleVar
        }

        # create dict of settings variables from the model's settings
        self.settings = {}
        for key, data in self.settings_model.variables.items():
            vartype = vartypes.get(data['type'], tk.StringVar)
            self.settings[key] = vartype(value=data['value'])

        # put a trace on the variables so they get stored when changed
        for var in self.settings.values():
            var.trace('w', self.save_settings)
