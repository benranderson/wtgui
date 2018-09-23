import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from . import widgets as w


class InputDataForm(tk.Frame):
    """The input data form"""

    def __init__(self, parent, fields, settings, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.settings = settings
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

        if self.settings['autofill date'].get():
            current_date = datetime.today().strftime('%Y-%m-%d')
            self.inputs['Date'].set(current_date)

    def get_errors(self):
        """Get a list of field errors in the form"""

        errors = {}
        for key, widget in self.inputs.items():
            if hasattr(widget.input, 'trigger_focusout_validation'):
                widget.input.trigger_focusout_validation()
            if widget.error.get():
                errors[key] = widget.error.get()

        return errors


class MainMenu(tk.Menu):
    """The Application's main menu"""

    def __init__(self, parent, settings, callbacks, **kwargs):
        super().__init__(parent, **kwargs)

        # The file menu
        file_menu = tk.Menu(self, tearoff=False)
        file_menu.add_command(label="Select file…",
                              command=callbacks['file->select'])
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=callbacks['file->quit'])
        self.add_cascade(label='File', menu=file_menu)

        # The options menu
        options_menu = tk.Menu(self, tearoff=False)
        options_menu.add_checkbutton(
            label='Autofill Date',
            variable=settings['autofill date']
        )
        options_menu.add_checkbutton(
            label='Autofill Sheet data',
            variable=settings['autofill sheet data']
        )
        self.add_cascade(label='Options', menu=options_menu)

        # The help menu
        help_menu = tk.Menu(self, tearoff=False)
        help_menu.add_command(label='About…', command=self.show_about)
        self.add_cascade(label='Help', menu=help_menu)

    def show_about(self):
        """Show the about dialog"""
        about_message = 'Wall Thickness'
        about_detail = ('by Ben Randerson\n'
                        'For assistance please contact the author.')
        messagebox.showinfo(title='About', message=about_message,
                            detail=about_detail)
