from figman import FigMan

class BSerialized:
    """
    Serializes a Tkinter window and its widgets into a FigMan-compatible
    configuration dictionary.

    This class is callable; invoking an instance with a Tkinter window
    returns a populated configuration describing the window's attributes,
    its child widgets, and each widget's configuration and geometry data.
    """

    def __init__(self):
        """Initializes the serializer and creates a FigMan manager instance."""

        self.manager = FigMan() #Initialize the FigMan
        self.convert_map ={
        "x": float,
        "relx": float,
        "y": float,
        "rely": float,
        "width": float,
        "relwidth": float,
        "height": float,
        "relheight": float
    }# A mapping to all current tkinter variables that need to be converted and their needed types.

    def __call__(self, window):
        """
        Serializes the given Tkinter window.

        Params:
            window (tkinter.Tk | tkinter.Toplevel): The window to serialize.

        Returns:
            MasterGroup: An instance of MasterGroup populated with the attributes to rebuild a tkinter window and it's children.
        """

        configuration = self.manager(window.title())# Create a new FigMan configuration
        self._get_configuration(window, configuration)# Populate the configuration with the provided window and all it's children.
        return configuration

    def save_configuration(self, configuration, file_path):
        """Leverage FigMan to save the configuraiton to file."""

        self.manager.save(configuration, file_path)# Saves the configuration in a json or yaml format.

    def _get_configuration(self, window, configuration):
        """
        Populates the configuration dictionary with window-level and widget-level data.

        Params:
            window (tkinter.Tk | tkinter.Toplevel): The window being serialized.
            configuration (dict): The configuration dictionary to populate.
        """

        self._get_window_entry(window, configuration)# populates the window attributes
        self._get_widget_entry(window, configuration)# populates the widget attributes

    def _get_window_config(self, window):
        """
        Yields key/value pairs representing the window's attributes.

        Params:
            window (tkinter.Tk | tkinter.Toplevel): The window whose attributes are read.

        Yields:
            tuple[str, Any]: A (key, value) pair for each window attribute.
        """

        window_attr = {
            "title": window.title,
            "geometry": window.geometry,
            "minsize": window.minsize,
            "maxsize": window.maxsize,
            "resizable": window.resizable,
            "iconbitmap": window.iconbitmap,
            "state": window.state,
            "attributes": window.attributes,
        }# A mapping to the window attributes.
        for key, attr in window_attr.items():# Creates a generator function that yeilds the attributes of the window.
            yield key, attr()

    def _get_window_entry(self, window, configuration):
        """
        Writes the window's attributes into the configuration dictionary.

        Params:
            window (tkinter.Tk | tkinter.Toplevel): The window being serialized.
            configuration (dict): The configuration dictionary to update.
        """

        for key, value in self._get_window_config(window):# Calls the generator function and creates a figman.Setting instance for each attribute.
            configuration["config"][key] = value

    def _get_window_children(self, parent):
        """
        Yields the direct child widgets of a window or widget.

        Params:
            parent (tkinter.Misc): A Tkinter widget whose children are iterated.

        Yields:
            tuple[str, tkinter.Widget]: The widget name and widget instance.
        """

        for name, child in parent.children.items():# Creates a generator function that yeilds the children of the provided window.
            yield name, child

    def _get_widget_config(self, widget):
        """
        Populates the configuration entry for a widget's configuration options.

        Params:
            name (str): The widget's Tkinter name.
            widget (tkinter.Widget): The widget being serialized.
            configuration (dict): The configuration dictionary to update.
        """

        for key in widget.keys():
            value = widget.cget(key)
            yield key, value

    def _get_widget_place(self, widget):
        """
        Populates the configuration entry for a widget's place geometry options.

        Params:
            widget (tkinter.Widget): The widget whose geometry is being serialized.
            configuration (dict): The configuration dictionary to update.
        """

        for key, value in self._place_values(widget):
            yield key, value

    def _place_values(self, widget):
        """
        Converts the strings provided by tkinter into floats.
        """

        for name, value in widget.place_info().items():
            if name in self.convert_map and value != '':
                value= self.convert_map[name](value)
            yield name, value

    def _get_widget_entry(self, window, configuration):
        """
        Populates configuration entries for all child widgets of the window.

        Params:
            window (tkinter.Tk | tkinter.Toplevel): The window whose widgets are serialized.
            configuration (dict): The configuration dictionary to update.
        """
        children_config = configuration["children"]
        for name, widget in self._get_window_children(window):
            children_config[name]["type"] = widget.winfo_class()
            children_config[name]["parent"] = widget.winfo_parent()
            for key, value in self._get_widget_config(widget):
                children_config[name]["config"][key] = value
            for key, value in self._get_widget_place(widget):
                children_config[name]["place"][key] = value
