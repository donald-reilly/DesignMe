from figman import FigMan, MasterGroup
from persistance import BPersistent
from serializer.serializers import TkSerializer
import  tkinter as tk

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
        self.persistance = BPersistent()
        self.serializer_registry = {
            tk.Tk: TkSerializer
        }

    def __call__(self, object_to_serialize):
        """
        Serializes the given Tkinter window.

        Params:
            window (tkinter.Tk | tkinter.Toplevel): The window to serialize.

        Returns:
            MasterGroup: An instance of MasterGroup populated with the attributes to rebuild a tkinter window and it's children.
        """
        
        serializer = self.serializer_registry[type(object_to_serialize)]()
        return serializer(self.manager, object_to_serialize)

    def save_configuration(self, file_path, configuration):
        """
        Saves the FigMan object to file
        
        Params:
            configuration (MasterGroup): The MasterGroup to save to file.
            file_path (str): The file path to be used.
        """

        self.persistance(file_path, configuration)
