from tkinter import *
from tkinter.simpledialog import Dialog
from tkinter import messagebox
from tkinter import ttk


class EntryDialog(Dialog):

    # NOTE: How this works
    # - Subclass the builtin Dialog class, and then override one or more of the
    #   following:
    # - body() defines the shape of the dialog, including any widgets
    #   first argument to body() is the parent widget, so it can be
    #   passed into the child widgets e.g Label(), Entry()
    # - buttonbox() defines the buttons you need. You need to do Frame(self)
    #   at the beginning of the function to have something to grid/pack into.
    #   By default it comes with an OK and CANCEL button that are bound to
    #   `self.ok` and `self.cancel`
    #   Override this if you need something else.
    # - By default `self.ok()` will call `self.validate()` to check any values
    #   in the widget. `self.validate()` should return boolean (or truthy/falsy value).
    # - `self.ok()` then calls `self.apply()`, and does `finally` on `self.cancel()`

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def body(self, master):
        sys: Label = Label(master, text="Sys")
        sys.grid(column=0, row=0)

        dia: Label = Label(master, text="Dia", anchor="e")
        dia.grid(column=0, row=1)

        pulse: Label = Label(master, text="Pulse")
        pulse.grid(column=0, row=2)

        notes: Label = Label(master, text="Notes")
        notes.grid(column=0, row=3)

        self.sys_entry = Entry(master, name="sys")
        self.sys_entry.grid(column=1, row=0, padx=1)

        self.dia_entry = Entry(master, name="dia")
        self.dia_entry.grid(column=1, row=1, padx=2)

        self.pulse_entry = Entry(master, name="pulse")
        self.pulse_entry.grid(column=1, row=2, padx=2)

        self.notes_entry = Entry(master, name="notes")
        self.notes_entry.grid(column=1, row=3, padx=2)
        return self.sys_entry

    def validate(self):
        try:
            sys: int = int(self.sys_entry.get())
        except ValueError:
            messagebox.showwarning(
                "Only numbers allowed!",
                "Only numbers are allowed in the 'sys' field!",
                parent=self
            )
            return 0

        try:
            dia: int = int(self.dia_entry.get())
        except ValueError:
            messagebox.showwarning(
                "Only numbers allowed!",
                "Only numbers are allowed in the 'dia' field!",
                parent=self
            )
            return 0

        try:
            pulse: int = int(self.pulse_entry.get())
        except ValueError:
            messagebox.showwarning(
                "Only numbers allowed!",
                "Only numbers are allowed in the pulse field!",
                parent=self
            )
            return 0

        notes: str = self.notes_entry.get()
        self._result: dict = {
            "sys": sys,
            "dia": dia,
            "pulse": pulse,
            "notes": notes
        }
        return 1

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

        self.add_button.grid(column=0, row=0, sticky="NEWS", padx=5, pady=5)
        self.tree.grid(column=0, row=1, sticky="NEWS", padx=5, pady=5)

    def _spawn_dialog(self):
        modal: EntryDialog = EntryDialog(self)
        return modal

