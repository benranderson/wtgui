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

        datestring = datetime.today().strftime('%Y-%m-%d')
        default_filename = f'wt_data_{datestring}.csv'
        self.filename = tk.StringVar(value=default_filename)
        self.data_model = m.CSVModel(filename=self.filename.get())
        self.settings_model = m.SettingsModel()
        self.load_settings()

        self.callbacks = {
            'file->select': self.on_file_select,
            'file->quit': self.quit,
            'show_pipelinelist': self.show_pipelinelist,
            'new_pipeline': self.open_pipeline,
            'on_open_pipeline': self.open_pipeline,
            'on_calculate': self.on_calculate
        }

        menu = v.MainMenu(self, self.settings, self.callbacks)
        self.config(menu=menu)

        # the input data form
        self.inputdataform = v.InputDataForm(
            self, m.CSVModel.fields, self.settings, self.callbacks)
        self.inputdataform.grid(row=1, padx=10)

        # the pipeline list
        self.pipelinelist = v.PipelineList(self, self.callbacks)
        self.pipelinelist.grid(row=1, padx=10, sticky='NSEW')
        self.populate_pipelinelist()

        # status bar
        self.status = tk.StringVar()
        self.statusbar = ttk.Label(self, textvariable=self.status)
        self.statusbar.grid(sticky="we", row=2, padx=10)

        self.calcs_ran = 0

    def show_pipelinelist(self):
        """Show the pipeline list"""

        self.pipelinelist.tkraise()

    def populate_pipelinelist(self):
        try:
            rows = self.data_model.get_all_pipelines()
        except Exception as e:
            messagebox.showerror(
                title='Error',
                message='Problem reading file',
                detail=str(e)
            )
        else:
            self.pipelinelist.populate(rows)

    def open_pipeline(self, rownum=None):
        if rownum is None:
            pipeline = None
        else:
            rownum = int(rownum)
            try:
                pipeline = self.data_model.get_pipeline(rownum)
            except Exception as e:
                messagebox.showerror(
                    title='Error',
                    message='Problem reading file',
                    detail=str(e)
                )
                return
        self.inputdataform.load_pipeline(rownum, pipeline)
        self.inputdataform.tkraise()

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

        data = self.inputdataform.get()
        rownum = self.inputdataform.current_pipeline
        try:
            self.data_model.save_pipeline(data, rownum)
        except IndexError as e:
            messagebox.showerror(
                title='Error',
                message='Invalid row specified',
                detail=str(e)
            )
            self.status.set('Tried to update invalid row')
        except Exception as e:
            messagebox.showerror(
                title='Error',
                message='Problem saving pipeline',
                detail=str(e)
            )
            self.status.set('Problem saving pipeline')

        else:

            self.calcs_ran += 1

            if self.calcs_ran > 1:
                plural = 's'
            else:
                plural = ''

            self.status.set(
                f'{self.calcs_ran} calculation{plural} run this session')
            self.populate_pipelinelist()
            # only reset the form when we're appending pipelines
            if self.inputdataform.current_pipeline is None:
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
            self.data_model = m.CSVModel(filename=self.filename.get())
            self.populuate_pipelinelist()

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
