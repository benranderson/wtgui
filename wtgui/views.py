import tkinter as tk
from tkinter import ttk
from datetime import datetime
from . import widgets as w


class InputDataForm(tk.Frame):
    """The input data form"""

    def __init__(self, parent, fields, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        # A dict to keep track of input widgets
        self.inputs = {}

        # Build the form
        # General Information
        generalinfo = tk.LabelFrame(
            self, text='General Information',
            font=('TkDefaultFont 14 bold'),
            padx=5,
            pady=5
        )
        self.inputs['Project'] = w.LabelInput(
            generalinfo, 'Project',
            field_spec=fields['Project']
        )
        self.inputs['Project'].grid(row=0, column=0, columnspan=2)
        self.inputs['Originator'] = w.LabelInput(
            generalinfo, 'Originator',
            field_spec=fields['Originator']
        )
        self.inputs['Originator'].grid(row=1, column=0)
        self.inputs['Date'] = w.LabelInput(
            generalinfo, 'Date',
            field_spec=fields['Date']
        )
        self.inputs['Date'].grid(row=1, column=1)
        self.inputs['Checker'] = w.LabelInput(
            generalinfo, 'Checker',
            field_spec=fields['Checker']
        )
        self.inputs['Checker'].grid(row=2, column=0)
        self.inputs['CheckDate'] = w.LabelInput(
            generalinfo, 'Check Date',
            field_spec=fields['CheckDate']
        )
        self.inputs['CheckDate'].grid(row=2, column=1)
        generalinfo.grid(row=0, column=0, sticky=(tk.W + tk.E))

        # Pipe Dimensional Data
        dimensiondata = tk.LabelFrame(
            self, text='Pipe Dimensional Data',
            font=('TkDefaultFont 14 bold'),
            padx=5,
            pady=5)
        self.inputs['D_o'] = w.LabelInput(
            dimensiondata, 'Outside Diameter [mm]',
            field_spec=fields['D_o']
        )
        self.inputs['D_o'].grid(row=0, column=0)
        self.inputs['t_sel'] = w.LabelInput(
            dimensiondata, 'Selected Wall Thickness [mm]',
            field_spec=fields['t_sel']
        )
        self.inputs['t_sel'].grid(row=0, column=1)
        self.inputs['t_cor'] = w.LabelInput(
            dimensiondata, 'Corrosion Allowance [mm]',
            field_spec=fields['t_cor']
        )
        self.inputs['t_cor'].grid(row=1, column=0)
        self.inputs['tol'] = w.LabelInput(
            dimensiondata, 'Mill tolerance [%]',
            field_spec=fields['tol']
        )
        self.inputs['tol'].grid(row=1, column=1)
        self.inputs['B'] = w.LabelInput(
            dimensiondata, 'Bend Thinning [%]',
            field_spec=fields['B']
        )
        self.inputs['B'].grid(row=2, column=0)
        dimensiondata.grid(row=1, column=0, sticky=(tk.W + tk.E))

        # Pipe Material Data
        materialdata = tk.LabelFrame(
            self, text='Pipe Material Data',
            font=('TkDefaultFont 14 bold'),
            padx=5,
            pady=5)
        self.inputs['SMYS'] = w.LabelInput(
            materialdata, 'Specified Minimum Yield Strength [MPa]',
            field_spec=fields['SMYS']
        )
        self.inputs['SMYS'].grid(row=0, column=0)
        self.inputs['E'] = w.LabelInput(
            materialdata, "Young's Modulus [GPa]",
            field_spec=fields['E']
        )
        self.inputs['E'].grid(row=0, column=1)
        self.inputs['v'] = w.LabelInput(
            materialdata, "Poisson's Ratio [-]",
            field_spec=fields['v']
        )
        self.inputs['v'].grid(row=1, column=0)
        materialdata.grid(row=2, column=0, sticky=(tk.W + tk.E))

        # default the form
        self.reset()

    def get(self):
        """Retrieve data from form as a dict"""

        data = {}
        for key, widget in self.inputs.items():
            data[key] = widget.get()
        return data

    def reset(self):
        """Resets the form entries"""

        # # gather the values to keep for next calculation
        # project = self.inputs['project'].get()
        # originator = self.inputs['orig'].get()

        # # clear all values
        # for widget in self.inputs.values():
        #     widget.set('')

        current_date = datetime.today().strftime('%Y-%m-%d')
        self.inputs['Date'].set(current_date)

        # self.inputs['project'].set(project)
        # self.inputs['orig'].set(originator)
        # self.inputs['D_o'].input.focus()

    def get_errors(self):
        """Get a list of field errors in the form"""

        errors = {}
        for key, widget in self.inputs.items():
            if hasattr(widget.input, 'trigger_focusout_validation'):
                widget.input.trigger_focusout_validation()
            if widget.error.get():
                errors[key] = widget.error.get()

        return errors
