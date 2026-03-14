import tkinter as tk
from tkinter import ttk
class TkConstructor:
    """
    TkConstructor provides the logic for reconstruction of a tkinter app from a FigMan configuraiton
    """
    def __init__(self):
        """Initialize TkConstuctor"""

        self.tk_object_creation_dispatch = {
            "window": self._create_window,
            "widget": self._create_widget
        }
        self.widget_map = {
            "frame": ttk.Frame,
            "labelframe": ttk.LabelFrame,
            "label": ttk.Label,
            "button": ttk.Button,
            "entry": ttk.Entry,
            "checkbutton": ttk.Checkbutton,
            "radiobutton": ttk.Radiobutton,
            "combobox": ttk.Combobox,
            "progressbar": ttk.Progressbar,
            "scale": ttk.Scale,
            "scrollbar": ttk.Scrollbar,
            "separator": ttk.Separator,
            "sizegrip": ttk.Sizegrip,
            "treeview": ttk.Treeview,
            "notebook": ttk.Notebook,
            "panedwindow": ttk.PanedWindow,
            "canvas":tk.Canvas,
            "text": tk.Text,
            "listbox":tk.Listbox,
            "menu":tk.Menu,
            "menubutton":tk.Menubutton,
            "toplevel":tk.Toplevel,
            "spinbox":tk.Spinbox
        }
    def __call__(self, configuration):
        return self._build_app(configuration)
    def _build_app(self, configuration):
        window_build, widget_build = self._extract_dictionaries(configuration)
        self._create_window(window_build)
    def _extract_dictionaries(self, configruation):
        window_build = configruation["window"]["config"]
        widget_build = configruation["window"]["children"]
        return window_build, widget_build
    def _create_window(self, window_build):
        root = tk.Tk()
        root.title(window_build["title"])

        root.geometry(window_build["geometry"])

        root.minsize(*window_build["minsize"])
        root.maxsize(*window_build["maxsize"])

        root.resizable(*window_build["resizable"])

        root.configure(**window_build["config"]["configure"])

        root.iconbitmap(window_build["iconbitmap"])

        root.attributes(*window_build["attributes"])
        

        root.state(window_build["state"])   # maximize
    def _create_widget(self):
        pass