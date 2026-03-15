import tkinter as tk
from tkinter import ttk


class TkConstructor:
    """
    TkConstructor provides the logic for reconstructing a tkinter
    application from a FigMan configuration structure.

    The class reads configuration groups describing the window and
    widgets, then dynamically builds the tkinter UI from that data.
    """

    def __init__(self):
        """Initialize TkConstructor and register supported widget types."""

        # Dispatch table for creating top-level tkinter objects
        # based on configuration group type.
        self.tk_object_creation_dispatch = {
            "window": self._create_window,
            "widget": self._create_widget
        }

        # Mapping between serialized widget identifiers and the
        # actual tkinter/ttk classes used to construct them.
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
            "Canvas": tk.Canvas,
            "Text": tk.Text,
            "Listbox": tk.Listbox,
            "Menu": tk.Menu,
            "Menubutton": tk.Menubutton,
            "Toplevel": tk.Toplevel,
            "Spinbox": tk.Spinbox
        }

    def __call__(self, configuration):
        """
        Build a tkinter application from a FigMan configuration.

        Params:
            configuration: The FigMan configuration object describing
                           the window and widget hierarchy.

        Returns:
            tk.Tk: The root tkinter application window.
        """
        return self._build_app(configuration)

    def _build_app(self, configuration):
        """
        Construct the root window and all widgets from the configuration.

        Params:
            configuration: FigMan configuration object.

        Returns:
            tk.Tk: The constructed root window.
        """

        # Extract window configuration and widget configuration
        window_build, widget_build = self._extract_dictionaries(configuration)

        # Create root window
        root = self._create_window(window_build)

        # Create widgets attached to the root window
        self._create_widget(widget_build, root)

        return root

    def _extract_dictionaries(self, configruation):
        """
        Extract the window configuration and widget configuration
        sections from the FigMan configuration object.

        Params:
            configruation: FigMan configuration structure.

        Returns:
            tuple:
                window_build -> configuration for the root window
                widget_build -> list of widget configuration groups
        """

        window_build = configruation["config"]
        widget_build = configruation["children"]

        return window_build, widget_build

    def _create_window(self, window_build):
        """
        Construct the root tkinter window using the provided configuration.

        Params:
            window_build: Configuration group describing the window.

        Returns:
            tk.Tk: The constructed root window.
        """

        root = tk.Tk()

        # Apply window configuration parameters
        root.title(window_build["title"].value)
        root.geometry(window_build["geometry"].value)

        root.minsize(*window_build["minsize"].value)
        root.maxsize(*window_build["maxsize"].value)

        root.resizable(*window_build["resizable"].value)

        # Apply root window configuration dictionary
        root.configure(**window_build["configure"].kwargs)

        # Set application icon
        root.iconbitmap(window_build["iconbitmap"].value)

        # Apply window attributes (fullscreen, transparency, etc.)
        root.attributes(*window_build["attributes"].value)

        # Set window state (normal, iconic, zoomed, etc.)
        root.state(window_build["state"].value)

        return root

    def _create_widget(self, widget_build, root):
        """
        Create all widgets described in the configuration and attach
        them to the provided root window.

        Params:
            widget_build: Iterable containing widget configuration groups.
            root: The parent tkinter widget (usually the root window).
        """

        for widget in widget_build:

            # Resolve the tkinter class corresponding to the widget type
            try:
                widget_call = self.widget_map[widget["type"].value]
            except:
                # Fallback for unsupported or unimplemented widget types
                print("widget type not yet implemented")

            # Create widget instance
            new_widget = widget_call(root, **widget["config"].kwargs)

            # Apply geometry placement configuration
            new_widget.place(**widget["place"].kwargs)

            # Special handling for widgets requiring data insertion
            if widget["type"].value == "Listbox":
                print("yes")
                new_widget.insert("end", *widget["set"].value)