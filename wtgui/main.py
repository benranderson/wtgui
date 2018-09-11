from datetime import datetime
import os
import csv
import tkinter as tk
from tkinter import ttk


class LabelInput(tk.Frame):
    """A widget containing a label and input together."""

    def __init__(self, parent, label='', input_class=ttk.Entry,
                 input_var=None, input_args=None, label_args=None,
                 **kwargs):
        super().__init__(parent, **kwargs)
        input_args = input_args or {}
        label_args = label_args or {}
        self.variable = input_var

        if input_class in (ttk.Checkbutton, ttk.Button,
                           ttk.Radiobutton):
            input_args['text'] = label
            input_args['variable'] = input_var
        else:
            self.label = ttk.Label(self, text=label, **label_args)
            self.label.grid(row=0, column=0, sticky=(tk.W, tk.E))
            input_args['textvariable'] = input_var

        self.input = input_class(self, **input_args)
        self.input.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.columnconfigure(0, weight=1)

    def grid(self, sticky=(tk.E + tk.W), **kwargs):
        super().grid(sticky=sticky, **kwargs)

    def get(self):
        try:
            if self.variable:
                return self.variable.get()
            elif type(self.input) == tk.Text:
                return self.input.get('1.0', tk.END)
            else:
                return self.input.get()
        except (TypeError, tk.TclError):
            # happens when numeric fields are empty
            return ''

    def set(self, value, *args, **kwargs):
        if type(self.variable) == tk.BooleanVar:
            self.variable.set(bool(value))
        elif self.variable:
            self.variable.set(value, *args, **kwargs)
        elif type(self.input).__name__.endswith('button'):
            if value:
                self.input.select()
            else:
                self.input.deselect()
        elif type(self.input) == tk.Text:
            self.input.delete('1.0', tk.END)
            self.input.insert('1.0', value)
        else:
            self.input.delete(0, tk.END)
            self.input.insert(0, value)


class InputDataForm(tk.Frame):
    """The input data form"""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        # A dict to keep track of input widgets
        self.inputs = {}

        # Build the form
        # General Information
        generalinfo = tk.LabelFrame(self, text='General Information')
        self.inputs['Date'] = LabelInput(generalinfo, 'Date',
                                         input_var=tk.StringVar())
        self.inputs['Date'].grid(row=0, column=0)
        self.inputs['Originator'] = LabelInput(generalinfo, 'Originator',
                                               input_var=tk.StringVar())
        self.inputs['Originator'].grid(row=0, column=1)
        self.inputs['Project'] = LabelInput(generalinfo, 'Project',
                                            input_var=tk.StringVar())
        self.inputs['Project'].grid(row=0, column=2)
        generalinfo.grid(row=0, column=0, sticky=(tk.W + tk.E))

        # Pipe Dimensional Information
        dimensioninfo = tk.LabelFrame(
            self, text='Pipe Dimensional Information')
        self.inputs['D_o'] = LabelInput(
            dimensioninfo, 'Outside Diameter [mm]',
            input_class=tk.Spinbox,
            input_var=tk.DoubleVar(),
            input_args={'from_': 0, 'to': 1000, 'increment': 0.01}
        )
        self.inputs['D_o'].grid(row=0, column=0)
        self.inputs['t_sel'] = LabelInput(
            dimensioninfo, 'Selected Wall Thickness [mm]',
            input_class=tk.Spinbox,
            input_var=tk.DoubleVar(),
            input_args={'from_': 0, 'to': 1000, 'increment': 0.01}
        )
        self.inputs['t_sel'].grid(row=0, column=1)
        self.inputs['t_cor'] = LabelInput(
            dimensioninfo, 'Corrosion Allowance [mm]',
            input_class=tk.Spinbox,
            input_var=tk.DoubleVar(),
            input_args={'from_': 0, 'to': 1000, 'increment': 0.01}
        )
        self.inputs['t_cor'].grid(row=1, column=0)
        self.inputs['tol'] = LabelInput(
            dimensioninfo, 'Mill tolerance [%]',
            input_class=tk.Spinbox,
            input_var=tk.DoubleVar(),
            input_args={'from_': 0, 'to': 100, 'increment': 0.01}
        )
        self.inputs['tol'].grid(row=1, column=1)
        self.inputs['B'] = LabelInput(
            dimensioninfo, 'Bend Thinning [%]',
            input_class=tk.Spinbox,
            input_var=tk.DoubleVar(),
            input_args={'from_': 0, 'to': 100, 'increment': 0.01}
        )
        self.inputs['B'].grid(row=1, column=2)
        dimensioninfo.grid(row=1, column=0, sticky=(tk.W + tk.E))

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

        for widget in self.inputs.values():
            widget.set('')


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

        self.inputdataform = InputDataForm(self)
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

        # Hardcode filename with a datestring.
        # If it doesn't exist, create it, otherwise append existing file
        datestring = datetime.today().strftime('%Y-%m-%d')
        filename = f'wt_data_{datestring}.csv'
        newfile = not os.path.exists(filename)

        data = self.inputdataform.get()

        with open(filename, 'a') as f:
            csvwriter = csv.DictWriter(f, fieldnames=data.keys())
            if newfile:
                csvwriter.writeheader()
            csvwriter.writerow(data)

        self.cals_ran += 1
        self.status.set(f'{self.cals_ran} calculations ran this session')
        self.inputdataform.reset()


def main():
    app = Application()
    app.mainloop()


if __name__ == '__main__':
    main()
