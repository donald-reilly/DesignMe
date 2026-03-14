from persistance import BPersistent
from figman import FigMan
class BConstructed():
    """
    BConstructed takes custom json serialized tkinter objects and reconstructs them during runtime.
    """
    def __init__(self):
        pass
    def __call__(self):
        pass
    def _get_window_config(self):
        pass

    def _construct_window(self, window):
        window_attributes_map = {
            "title": window.title,
            "geometry": window.geometry,
            "minsize": window.minsize,
            "maxsize": window.maxsize,
            "resizable": window.resizable,
            "iconbitmap": window.iconbitmap,
            "state": window.state,
            "attributes": window.attributes,
        } 
    