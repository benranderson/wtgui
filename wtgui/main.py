import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

from wtgui.wallthick import calc_wallthick

TITLE = "WallThick"
LARGE_FONT = ("Open Sans", 12, "bold")
NORMAL_FONT = ("Open Sans", 12)


class App(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        # tk.Tk.iconbitmap(self, "icon.ico")
        tk.Tk.wm_title(self, TITLE)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage,):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(
            self, text="Calculate Wall Thickness", font=LARGE_FONT, pady=10)
        label.grid(row=0)

        self.setup()

    def setup(self):
        """
        Call all relevant config methods
        """
        # self.config_menubar()
        self.config_main_view()

    # def config_menubar(self):
    #     """
    #     Configure the menu bar
    #     """
    #     self.root_menu = tk.Menu(self.root)
    #     self.root.config(menu=self.root_menu)

    #     self.app_menu = tk.Menu(self.root_menu)
    #     self.root_menu.add_cascade(label='WTGUI', menu=self.app_menu)
    #     self.app_menu.add_command(label='Quit WTGUI', command=self.frame.quit)

    def config_main_view(self):
        """
        Confugure the main view
        """
        heading1 = tk.Label(self, text="Parameter", font=LARGE_FONT)
        heading2 = tk.Label(self, text="Units", font=LARGE_FONT)
        heading3 = tk.Label(self, text="Value", font=LARGE_FONT)
        diameter_label = tk.Label(self, text="Diameter", font=NORMAL_FONT)
        pressure_label = tk.Label(self, text="Pressure", font=NORMAL_FONT)
        smys_label = tk.Label(self, text="SMYS", font=NORMAL_FONT)
        diameter_units_label = tk.Label(self, text="[mm]", font=NORMAL_FONT)
        pressure_units_label = tk.Label(self, text="[bar]", font=NORMAL_FONT)
        smys_units_label = tk.Label(self, text="[MPa]", font=NORMAL_FONT)
        self.diameter = tk.Entry(self)
        self.pressure = tk.Entry(self)
        self.smys = tk.Entry(self)

        heading1.grid(row=1, sticky='w')
        heading2.grid(row=1, column=1)
        heading3.grid(row=1, column=2, sticky='w')

        diameter_label.grid(row=2, sticky='w')
        pressure_label.grid(row=3, sticky='w')
        smys_label.grid(row=4, sticky='w')

        diameter_units_label.grid(row=2, column=1)
        pressure_units_label.grid(row=3, column=1)
        smys_units_label.grid(row=4, column=1)

        self.diameter.grid(row=2, column=2)
        self.pressure.grid(row=3, column=2)
        self.smys.grid(row=4, column=2)

        runButton = ttk.Button(self, text="Run",
                               command=self.runCalculation)
        runButton.grid(row=5, column=2, sticky='e')

    def runCalculation(self):
        d = 0.001 * float(self.diameter.get())
        p = 100_000 * float(self.pressure.get())
        smys = 1_000_000 * float(self.smys.get())
        t = calc_wallthick(d, p, smys)
        showinfo("Result", f'Minimim Wall Thickness:\n{1000 * t:.2f} mm')


def main():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
