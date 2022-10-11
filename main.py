from tkinter import *
from tkinter import messagebox
from tkinter import ttk

from bp_tracker.front import BpTableFrame

class MainApp(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Enrico's Blood Pressure Tracker")
        self.option_add("*tearOff", FALSE)
        self._create_menu()

    def _create_menu(self):
        menubar = Menu(self)
        sysmenu = Menu(menubar, name="system")
        menu_about = Menu(menubar)
        menu_about.add_command(label="About", command=self._about)
        menubar.add_cascade(menu=menu_about, label="Help")
        menubar.add_cascade(menu=sysmenu)

        self["menu"] = menubar

    def _about(self):
        messagebox.showinfo("About this program", "Created by Enrico Tuvera Jr on October 10, 2022")

if __name__ == "__main__":
    app = MainApp()
    notebook = ttk.Notebook(app)
    bp = BpTableFrame(notebook)

    app.columnconfigure(0, weight=1)
    app.rowconfigure(0, weight=1)

    notebook.add(bp, text="Entries")
    notebook.grid(column=0, row=0, sticky="NEWS")

    app.mainloop()
