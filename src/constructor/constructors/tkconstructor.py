import tkinter as tk
from tkinter import ttk


class TkConstructor:
    def __init__(self):

        self.widget_constructor = WidgetConstructor()

    def __call__(self, config, root):
        if config["type"].value in self.widget_constructor.widget_map:
            new_widget = self.widget_constructor(config, root)
            return new_widget
        else:
            print("widget type not yet implemented")

class WidgetConstructor:
    def __init__(self):
        self.widget_map = {
            "Window": tk.Tk,
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

    def __call__(self, config, root=None):
        if config["type"].value == "Window":
            new_widget = self._construct_window(config)
        else:
            new_widget = self._construct_widget(config, root)
        return new_widget
    def _construct_window(self, window_build):
        """
        Construct the root tkinter window using the provided configuration.

        Params:
            window_build: Configuration group describing the window.

        Returns:
            tk.Tk: The constructed root window.
        """

        root = tk.Tk()
        # Apply window configuration parameters
        self._set_window_attributes(window_build["config"], root)
        return root

    def _set_window_attributes(self, window_build, root):
        
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

    def _construct_widget(self, widget_build, root):
        """
        Create the widget described in the configuration
        
        Params:
            widget_build (SubGroup): A widget configuration group.
            root: The parent tkinter widget.
        """

        special_case_widget = {
            "Listbox": self._list_box,
            "TEntry": self._entry,
            "Menu": self._menu
        }

        # Resolve the tkinter class corresponding to the widget type
        widget_call = self._verify_supported_widget(widget_build)

        # Special handling for widgets requiring data insertion
        special_case_call = special_case_widget.get(widget_build["type"].value)
        if special_case_call:
            new_widget = special_case_call(widget_build, root)
        else:
            # Create widget instance
            new_widget = widget_call(root, **widget_build["config"].kwargs)

            # Apply geometry placement configuration
            self._place_widget(widget_build, new_widget)
            
            return new_widget
        
    def _verify_supported_widget(self, widget_build):
        """
        Verify that the widget type is supported and return the required tkinter call.
        
        Params:
            widget_build (SubGroup): A widget configuration group.
        Returns:
            widget_call: The call required to instantiate the widget.
        """

        try:
            widget_call = self.widget_map[widget_build["type"].value]
            return widget_call
        except:
            # Fallback for unsupported or unimplemented widget types
            print("widget type not yet implemented")

    def _place_widget(self, widget_build, new_widget):
        """
        Place the widget on screen
        
        Params:
            widget_build (SubGroup): A widget configuration group.
            new_widget: The widget object to be placed.
        """

        new_widget.place(**widget_build["place"].kwargs)
                
    def _list_box(self, widget_build, new_widget):
        """
        Place values in listbox

        Params:
            widget: The listbox build
            new_widget: The listbox
        """

        new_widget.insert("end", *widget_build["set"].value)

    def _entry(self, widget, new_widget):
        """
        Place values in entry

        Params:
            widget: The entry build
            new_widget: The entry
        """
        print(widget["set"].value)
        new_widget.insert(0, widget["set"].value)

    def _menu(self, widget_build, root):
        """
        Create menu items and submenus for a Menu widget.
        Params:
            widget_build: The menu widget configuration group.
            root: The parent tkinter widget (usually the root window).
        """
        
        menu_bar = self.widget_map[widget_build["type"].value](root, **widget_build["config"].kwargs)
        self._recurse_children(widget_build, parent_menu= menu_bar)
        root.config(menu=menu_bar)
        return menu_bar

    def _recurse_children(self, widget_build, parent_menu=None):
        for child in widget_build["children"]:
            if child["type"].value == "cascade":
                new_menu = tk.Menu(parent_menu, tearoff=0)
                parent_menu.add_cascade(label=child["config"]["label"].value, menu=new_menu)
                if child["children"]:
                    self._recurse_children(child, parent_menu=new_menu)
            elif child["type"].value == "command":
                parent_menu.add_command(label=child["config"]["label"].value)

