import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from . import widgets as w


class InputDataForm(tk.Frame):
    """The input data form"""

    def __init__(self, parent, fields, settings, callbacks, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.settings = settings
        self.callbacks = callbacks

        self.current_pipeline = None

        # a dict to keep track of input widgets
        self.inputs = {}

        # build the form
        self.pipeline_label = ttk.Label()
        self.pipeline_label.grid(row=0, column=0)

        # General Information
        generalinfo = tk.LabelFrame(self, text='General Information')
        self.inputs['Project'] = w.LabelInput(
            generalinfo, 'Project',
            field_spec=fields['Project']
        )
        self.inputs['Project'].grid(row=0, column=0, columnspan=2)
        self.inputs['Pipeline'] = w.LabelInput(
            generalinfo, 'Pipeline',
            field_spec=fields['Pipeline']
        )
        self.inputs['Pipeline'].grid(row=1, column=0, columnspan=2)
        self.inputs['Originator'] = w.LabelInput(
            generalinfo, 'Originator',
            field_spec=fields['Originator']
        )
        self.inputs['Originator'].grid(row=2, column=0)
        self.inputs['Date'] = w.LabelInput(
            generalinfo, 'Date',
            field_spec=fields['Date']
        )
        self.inputs['Date'].grid(row=2, column=1)
        self.inputs['Checker'] = w.LabelInput(
            generalinfo, 'Checker',
            field_spec=fields['Checker']
        )
        self.inputs['Checker'].grid(row=3, column=0)
        self.inputs['CheckDate'] = w.LabelInput(
            generalinfo, 'Check Date',
            field_spec=fields['CheckDate']
        )
        self.inputs['CheckDate'].grid(row=3, column=1)
        generalinfo.grid(row=1, column=0, sticky=(tk.W + tk.E))

        # Pipe Dimensional Data
        dimensiondata = tk.LabelFrame(self, text='Pipe Dimensional Data')
        self.inputs['D_o'] = w.LabelInput(
            dimensiondata, 'Outside Diameter [mm]',
            field_spec=fields['D_o']
        )
        self.inputs['D_o'].grid(row=0, column=0)
        self.inputs['t_sel'] = w.LabelInput(
            dimensiondata, 'Sel. Wall Thickness [mm]',
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
        dimensiondata.grid(row=2, column=0, sticky=(tk.W + tk.E))

        # Pipe Material Data
        materialdata = tk.LabelFrame(self, text='Pipe Material Data')
        self.inputs['SMYS'] = w.LabelInput(
            materialdata, 'SMYS [MPa]',
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
        materialdata.grid(row=3, column=0, sticky=(tk.W + tk.E))

        # the calculate button
        self.calcbutton = ttk.Button(
            self,
            text="Calculate",
            command=self.callbacks["on_calculate"])
        self.calcbutton.grid(sticky="e", row=5, padx=10)

        # default the form
        self.reset()

    def get(self):
        """Retrieve data from form as a dict"""

        # retrieve the data from Tkinter variables and place it in regular
        # Python objects

        data = {}
        for key, widget in self.inputs.items():
            data[key] = widget.get()
        return data

    def reset(self):
        """Resets the form entries"""

        # apply current date
        if self.settings['autofill date'].get():
            current_date = datetime.today().strftime('%Y-%m-%d')
            self.inputs['Date'].set(current_date)
            check_date = datetime.today().strftime('%Y-%m-%d')
            self.inputs['CheckDate'].set(check_date)

        # apply default values
        if self.settings['autofill sheet data'].get():
            self.inputs['tol'].set(12.5)
            self.inputs['SMYS'].set(450)
            self.inputs['E'].set(207)
            self.inputs['v'].set(0.3)

    def get_errors(self):
        """Get a list of field errors in the form"""

        errors = {}
        for key, widget in self.inputs.items():
            if hasattr(widget.input, 'trigger_focusout_validation'):
                widget.input.trigger_focusout_validation()
            if widget.error.get():
                errors[key] = widget.error.get()

        return errors

    def load_pipeline(self, rownum, data=None):
        self.current_pipeline = rownum
        if rownum is None:
            self.reset()
            self.pipeline_label.config(text='New Pipeline')
        else:
            self.pipeline_label.config(text=f'Pipeline #{rownum}')
            for key, widget in self.inputs.items():
                self.inputs[key].set(data.get(key, ''))
                try:
                    widget.input.trigger_focusout_validation()
                except AttributeError:
                    pass


class MainMenu(tk.Menu):
    """The Application's main menu"""

    def __init__(self, parent, settings, callbacks, **kwargs):
        """Constructor for MainMenu

        Args:
          parent - The parent widget
          settings - a dict containing Tkinter variables
          callbacks - a dict containing Python callables
        """
        super().__init__(parent, **kwargs)

        # the file menu
        file_menu = tk.Menu(self, tearoff=False)
        file_menu.add_command(label="Select file…",
                              command=callbacks['file->select'])
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=callbacks['file->quit'])
        self.add_cascade(label='File', menu=file_menu)

        # the options menu
        options_menu = tk.Menu(self, tearoff=False)
        options_menu.add_checkbutton(
            label='Autofill Date',
            variable=settings['autofill date']
        )
        options_menu.add_checkbutton(
            label='Autofill Sheet Data',
            variable=settings['autofill sheet data']
        )
        self.add_cascade(label='Options', menu=options_menu)

        # the go menu to switch from pipelinelist to pipelineform
        go_menu = tk.Menu(self, tearoff=False)
        go_menu.add_command(label='Pipeline List',
                            command=callbacks['show_pipelinelist'])
        go_menu.add_command(label='New Pipeline',
                            command=callbacks['new_pipeline'])
        self.add_cascade(label='Go', menu=go_menu)

        # the help menu
        help_menu = tk.Menu(self, tearoff=False)
        help_menu.add_command(label='About…', command=self.show_about)
        self.add_cascade(label='Help', menu=help_menu)

    def show_about(self):
        """Show the about dialog"""
        about_message = 'Wall Thickness'
        about_detail = ('by Ben Randerson © 2018\n\n'
                        'An application to calculate the wall thickness of a '
                        'subsea pipeline.')
        messagebox.showinfo(title='About', message=about_message,
                            detail=about_detail)


class PipelineList(tk.Frame):
    """Display for CSV file contents"""

    column_defs = {
        '#0': {'label': 'Row'},
        'Date': {'label': 'Date'},
        'Pipeline': {'label': 'Pipeline', 'anchor': tk.W},
        'Originator': {'label': 'Originator'},
        'D_o': {'label': 'Diameter [mm]'},
        't_sel': {'label': 'Wall Thickness [mm]'}
    }
    default_width = 100
    default_minwidth = 10
    default_anchor = tk.CENTER

    def __init__(self, parent, callbacks, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.callbacks = callbacks
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # create treeview
        # note, #0 column is excluded as automatically created
        # browse mode selected so users can select individual rows
        self.treeview = ttk.Treeview(
            self,
            columns=list(self.column_defs.keys())[1:],
            selectmode='browse'
        )

        # configure scrollbar for treeview
        self.scrollbar = ttk.Scrollbar(
            self,
            orient=tk.VERTICAL,
            command=self.treeview.yview
        )
        # connect treeview back to scrollbar
        self.treeview.configure(yscrollcommand=self.scrollbar.set)
        self.treeview.grid(row=0, column=0, sticky='NSEW')
        # place scrollbar to right of treeview
        self.scrollbar.grid(row=0, column=1, sticky='NSW')

        # configure treeview columns
        for name, definition in self.column_defs.items():
            label = definition.get('label', '')
            anchor = definition.get('anchor', self.default_anchor)
            minwidth = definition.get('minwidth', self.default_minwidth)
            width = definition.get('width', self.default_width)
            stretch = definition.get('stretch', False)
            self.treeview.heading(name, text=label, anchor=anchor)
            self.treeview.column(name, anchor=anchor, minwidth=minwidth,
                                 width=width, stretch=stretch)

        # bind double click / enter event to open selected pipeline
        self.treeview.bind('<<TreeViewOpen>>', self.on_open_pipeline)

    def populate(self, rows):
        """Clear the treeview and write the supplied data rows to it"""

        # empty data from treeview
        for row in self.treeview.get_children():
            self.treeview.delete(row)

        # populate the table
        valuekeys = list(self.column_defs.keys())[1:]
        for rownum, rowdata in enumerate(rows):
            values = [rowdata[key] for key in valuekeys]
            self.treeview.insert('', 'end', iid=str(rownum),
                                 text=str(rownum), values=values)

        # set focus to first item in treeview
        if len(rows) > 0:
            self.treeview.focus_set()
            self.treeview.selection_set(0)
            self.treeview.focus('0')

    def on_open_pipeline(self, *args):
        selected_id = self.treeview.selection()[0]
        self.callbacks['on_open_pipeline'](selected_id)
