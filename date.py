from __future__ import print_function

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


class DateEntry(tk.Frame):
    def __init__(self, master, frame_look={}, **look):
        args = dict(relief=tk.SUNKEN, border=1)
        args.update(frame_look)
        tk.Frame.__init__(self, master, **args)

        args = {'relief': tk.FLAT}
        args.update(look)

        self.entry_1 = tk.Entry(self, width=4, **args,highlightcolor='ivory3',highlightbackground='ivory3')
        self.label_1 = tk.Label(self, text='/', **args,background='ivory3')
        self.entry_2 = tk.Entry(self, width=4, **args,highlightcolor='ivory3',highlightbackground='ivory3')

        self.entry_1.pack(side=tk.LEFT)
        self.label_1.pack(side=tk.LEFT)
        self.entry_2.pack(side=tk.LEFT)

        self.entries = [ self.entry_1, self.entry_2]

        self.entry_1.bind('<KeyRelease>', lambda e: self._check(0, 4))
        self.entry_2.bind('<KeyRelease>', lambda e: self._check(1, 4))

    def _backspace(self, entry):
        cont = entry.get()
        entry.delete(0, tk.END)
        entry.insert(0, cont[:-1])

    def _check(self, index, size):
        entry = self.entries[index]
        next_index = index + 1
        next_entry = self.entries[next_index] if next_index < len(self.entries) else None
        data = entry.get()

        if len(data) > size or not data.isdigit():
            self._backspace(entry)
        if len(data) >= size and next_entry:
            next_entry.focus()

    def get(self):
        return [e.get() for e in self.entries]




