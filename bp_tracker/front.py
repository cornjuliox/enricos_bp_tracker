from tkinter import *
from tkinter.simpledialog import Dialog
from tkinter import ttk

# from .database import BpDataProvider
from .models import Event

class EntryDialog(Dialog):
    def body(self, master):
        w = Label(master, text="Test Text 1", justify=LEFT)
        w.grid(column=0, row=0)

        e = Entry(master, name="entry")
        e.grid(column=1, row=0)
        return 


class BpTable(ttk.Treeview):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, columns=("sys", "dia", "pulse", "date_time", "notes"), show="headings")
        self.heading("sys", text="SYS")
        self.heading("dia", text="DIA")
        self.heading("pulse", text="PULSE")
        self.heading("date_time", text="DATE/TIME")
        self.heading("notes", text="Notes")

        self.column("sys", anchor=CENTER)
        self.column("dia", anchor=CENTER)
        self.column("pulse", anchor=CENTER)
        self.column("date_time", anchor=CENTER)

        # self.dataprovider: BpDataProvider = BpDataProvider()

        self._refresh()

    def _refresh(self):
        # grab data
        # data: list[Event] = self.dataprovider.provide()

        # clear all existing data on the tree
        self.delete(*self.get_children())

        # insert data (replace later)
        self.insert('', 0, values=(120, 80, 90, "October 10, 2022"))
        self.insert('', 0, values=(120, 80, 90, "October 10, 2022"))
        self.insert('', 0, values=(120, 80, 90, "October 10, 2022"))
        self.insert('', 0, values=(120, 80, 90, "October 10, 2022"))
        self.insert('', 0, values=(120, 80, 90, "October 10, 2022"))
        self.insert('', 0, values=(120, 80, 90, "October 10, 2022"))
        self.insert('', 0, values=(120, 80, 90, "October 10, 2022"))
        self.insert('', 0, values=(120, 80, 90, "October 10, 2022"))
        self.insert('', 0, values=(120, 80, 90, "October 10, 2022"))
        self.insert('', 0, values=(120, 80, 90, "October 10, 2022"))

class BpTableFrame(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=2)
        
        self.add_button: ttk.Button = ttk.Button(self, text="Add a new entry", command=self._spawn_dialog)
        self.tree: BpTable = BpTable(self)

        self.add_button.grid(column=0, row=0, sticky="NEWS")
        self.tree.grid(column=0, row=1, sticky="NEWS")

    def _spawn_dialog(self):
        modal: EntryDialog = EntryDialog(self)
