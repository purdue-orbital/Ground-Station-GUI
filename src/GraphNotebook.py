from tkinter import ttk
import tkinter as tk

class GraphNotebook(ttk.Notebook):
  def __init__(self, master=None):
    # Create Style
    customed_style = ttk.Style()
    customed_style.configure('Custom.TNotebook.Tab', width=20, padding=[0, 40], font=('Helvetica', 8))
    customed_style.configure('Custom.TNotebook', tabposition='wn')

    self.graphs = ttk.Notebook(master, style='Custom.TNotebook')
    # self.bind("<<NotebookTabChanged>>", self._on_tab_changed)

    f1 = tk.Frame(self.graphs, width=200, height=200)
    f2 = tk.Frame(self.graphs, width=200, height=200)
    self.graphs.add(f1, text='Gyrometer')
    self.graphs.add(f2, text='Accelerometer')
    self.graphs.config(height=800)
    self.graphs.grid(row=1, column=12, rowspan=4)

  def _on_tab_changed(self, event):
    event.widget.update_idletasks()

    tab = event.widget.nametowidget(event.widget.select())
    event.widget.configure(height=tab.winfo_reqheight())
