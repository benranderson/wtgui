import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

from wtgui.wallthick import calc_wallthick

TITLE = "WallThick"


class App:

    def __init__(self):
        self.title = TITLE
        self.root = tk.Tk()

        self.root_view = RootView(self.root)

    def run(self):
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            tk.sys.exit()


class RootView:
    """
    Root view for wallthick root controller
    """

    def __init__(self, root):
        # Configure root
        self.root = root
        # self.root.minsize(200, 200)
        self.root.title(TITLE)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # Run setup
        self.setup()

        # Set focus
        self.root.focus()

    def setup(self):
        """
        Call all relevant config methods
        """
        self.config_main_frame()
        self.config_menubar()
        self.config_main_view()

    def config_main_frame(self):
        """
        Configure the main outer frame for the main view
        """
        self.frame = tk.Frame(self.root)
        self.frame.grid()

    def config_menubar(self):
        """
        Configure the menu bar
        """
        self.root_menu = tk.Menu(self.root)
        self.root.config(menu=self.root_menu)

        self.app_menu = tk.Menu(self.root_menu)
        self.root_menu.add_cascade(label='WTGUI', menu=self.app_menu)
        self.app_menu.add_command(label='Quit WTGUI', command=self.frame.quit)

        # self.file_menu = Menu(self.root_menu)
        # self.root_menu.add_cascade(label='File', menu=self.file_menu)

    def config_main_view(self):
        """
        Confugure the main view
        """
        self.heading1 = tk.Label(self.frame, text="Parameter",
                                 font="Helvetica 9 bold")
        self.heading2 = tk.Label(self.frame, text="Units",
                                 font="Helvetica 9 bold")
        self.heading3 = tk.Label(self.frame, text="Value",
                                 font="Helvetica 9 bold")
        self.diameter_label = tk.Label(self.frame, text="Diameter")
        self.pressure_label = tk.Label(self.frame, text="Pressure")
        self.smys_label = tk.Label(self.frame, text="SMYS")
        self.diameter_units_label = tk.Label(self.frame, text="[mm]")
        self.pressure_units_label = tk.Label(self.frame, text="[bar]")
        self.smys_units_label = tk.Label(self.frame, text="[MPa]")
        self.diameter = tk.Entry(self.frame)
        self.pressure = tk.Entry(self.frame)
        self.smys = tk.Entry(self.frame)

        self.heading1.grid(row=0, sticky='w')
        self.heading2.grid(row=0, column=1)
        self.heading3.grid(row=0, column=2, sticky='w')

        self.diameter_label.grid(row=1, sticky='w')
        self.pressure_label.grid(row=2, sticky='w')
        self.smys_label.grid(row=3, sticky='w')

        self.diameter_units_label.grid(row=1, column=1)
        self.pressure_units_label.grid(row=2, column=1)
        self.smys_units_label.grid(row=3, column=1)

        self.diameter.grid(row=1, column=2)
        self.pressure.grid(row=2, column=2)
        self.smys.grid(row=3, column=2)

        self.runButton = ttk.Button(self.frame, text="Run",
                                    command=self.runCalculation)
        self.runButton.grid(row=4, column=2, sticky='e')

    def runCalculation(self):
        d = 0.001 * float(self.diameter.get())
        p = 100_000 * float(self.pressure.get())
        smys = 1_000_000 * float(self.smys.get())
        t = calc_wallthick(d, p, smys)
        showinfo("Result", f'Minimim Wall Thickness:\n{1000 * t:.2f} mm')


def main():
    app = App()
    app.run()


if __name__ == '__main__':
    main()
