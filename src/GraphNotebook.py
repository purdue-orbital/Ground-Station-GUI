from tkinter import ttk
import tkinter as tk


class GraphNotebook(ttk.Notebook):
    def __init__(self, row, col, height, span, master=None):
        # Create Style
        custom_style = ttk.Style()
        custom_style.configure('Custom.TNotebook.Tab', width=20, padding=[0, 40], font=('System', 8))
        custom_style.configure('Custom.TNotebook', tabposition='wn')

        # Initialize Notebook with Custom Style
        self.graphs = ttk.Notebook(master, style='Custom.TNotebook')
        # self.bind("<<NotebookTabChanged>>", self._on_tab_changed)

        # Based on input, configuring and place
        self.graphs.config(height=height)
        self.graphs.grid(row=row, column=col, rowspan=span)

    def add_tab(self, title, *widgets):
        f = tk.Frame(self.graphs, width=200, height=200)
        self.graphs.add(f, text=title)

    def _on_tab_changed(self, event):
        event.widget.update_idletasks()

        tab = event.widget.nametowidget(event.widget.select())
        event.widget.configure(height=tab.winfo_reqheight())
