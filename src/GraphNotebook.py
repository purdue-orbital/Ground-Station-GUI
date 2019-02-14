from tkinter import ttk
import tkinter as tk

class GraphNotebook(ttk.Notebook):
  def __init__(self, master=None):
    # Create Style
    self.style = ttk.Style(master)
    self.style.configure('lefttab.TNotebook', tabposition='ws')

    self.graphs = ttk.Notebook(master, width=200, height=200, style='lefttab.TNotebook')
    # self.bind("<<NotebookTabChanged>>", self._on_tab_changed)

    f1 = tk.Frame(self.graphs, width=200, height=200)
    f2 = tk.Frame(self.graphs, width=200, height=200)
    self.graphs.add(f1, text='\n\n\nGyrometer\n\n\n\n\n\n\n\n\n\n')
    self.graphs.add(f2, text='\n\n\nAccelerometer\n\n\n\n\n\n\n\n\n\n')
    self.graphs.config(height=800)
    self.graphs.grid(row=1, column=12, rowspan=4)

  def _on_tab_changed(self, event):
    event.widget.update_idletasks()

    tab = event.widget.nametowidget(event.widget.select())
    event.widget.configure(height=tab.winfo_reqheight())
