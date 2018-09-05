from tkinter import *

TITLE = "WallThick"


class App:

    def __init__(self):
        self.title = TITLE
        self.root = Tk()

        self.root_view = RootView(self.root)

    def run(self):
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            # self.log.info("Keyboard interrupt called. Shutting down.")
            sys.exit()


class RootView:
    """
    Root view for wallthick root controller
    """

    def __init__(self, root):
        # Configure root
        self.root = root
        self.root.minsize(200, 200)
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
        self.frame = Frame(self.root)
        self.frame.grid()

    def config_menubar(self):
        """
        Configure the menu bar
        """
        self.root_menu = Menu(self.root)
        self.root.config(menu=self.root_menu)

        self.app_menu = Menu(self.root_menu)
        self.root_menu.add_cascade(label='App', menu=self.app_menu)

        self.file_menu = Menu(self.root_menu)
        self.root_menu.add_cascade(label='File', menu=self.file_menu)

    def config_main_view(self):
        """
        Confugure the main view
        """
        self.label_1 = Label(self.frame, text="Diameter")
        self.label_2 = Label(self.frame, text="Pressure")
        self.diameter = Entry(self.frame)
        self.pressure = Entry(self.frame)

        self.label_1.grid(row=0, sticky=E)
        self.label_2.grid(row=1, sticky=E)
        self.diameter.grid(row=0, column=1)
        self.pressure.grid(row=1, column=1)

        self.runButton = Button(self.frame, text="Run",
                                command=self.runCalculation)
        self.runButton.grid(row=2, column=1, sticky=E)

    def runCalculation(self):
        print("Wall thickness calculation running")


def main():
    app = App()
    app.run()


if __name__ == '__main__':
    main()
