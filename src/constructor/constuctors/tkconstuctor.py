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
            "TFrame": ttk.Frame,
            "TLabelframe": ttk.LabelFrame,
            "TLabel": ttk.Label,
            "TButton": ttk.Button,
            "TEntry": ttk.Entry,
            "TCheckbutton": ttk.Checkbutton,
            "TRadiobutton": ttk.Radiobutton,
            "TCombobox": ttk.Combobox,
            "TProgressbar": ttk.Progressbar,
            "TScale": ttk.Scale,
            "TScrollbar": ttk.Scrollbar,
            "TSeparator": ttk.Separator,
            "TSizegrip": ttk.Sizegrip,
            "TTreeview": ttk.Treeview,
            "TNotebook": ttk.Notebook,
            "TPanedwindow": ttk.PanedWindow,
            "Canvas":tk.Canvas,
            "Text": tk.Text,
            "Listbox":tk.Listbox,
            "Menu":tk.Menu,
            "Menubutton":tk.Menubutton,
            "Toplevel":tk.Toplevel,
            "Spinbox":tk.Spinbox
        }
    def __call__(self, configuration):
        return self._build_app(configuration)
    def _build_app(self, configuration):
        window_build, widget_build = self._extract_dictionaries(configuration)
        root = self._create_window(window_build)
        self._create_widget(widget_build, root)
        return root
    def _extract_dictionaries(self, configruation):
        window_build = configruation["config"]
        widget_build = configruation["children"]
        return window_build, widget_build
    def _create_window(self, window_build):
        root = tk.Tk()
        root.title(window_build["title"].value)
        root.geometry(window_build["geometry"].value)
        root.minsize(*window_build["minsize"].value)
        root.maxsize(*window_build["maxsize"].value)
        root.resizable(*window_build["resizable"].value)
        root.configure(**window_build["configure"].kwargs)
        root.iconbitmap(window_build["iconbitmap"].value)
        root.attributes(*window_build["attributes"].value)
        root.state(window_build["state"].value)   # maximize
        return root
    def _create_widget(self, widget_build, root):
        for widget in widget_build:
            try:
                widget_call = self.widget_map[widget["type"].value]
            except:
                print("widget type not yet implemented")
            new_widget = widget_call(root, **widget["config"].kwargs)
            new_widget.place(**widget["place"].kwargs)