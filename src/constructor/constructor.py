
from constructor.constructors import TkConstructor
from constructor.defined import BDefined
from constructor.bindings import BBound

class BConstructed():
    """
    BConstructed loads a serialized tkinter configuration and reconstructs
    the application during runtime.

    The configuration is loaded from disk, deserialized into a FigMan
    configuration structure, and then passed to the TkConstructor
    to build the tkinter interface.
    """

    def __init__(self, command_map: dict = None):
        """
        Initialize BConstructed and its core components.

        Components:
            BPersistent  -> Handles loading serialized configuration files.
            ESM-1       -> Manages configuration group structures.
            TkConstructor-> Builds tkinter widgets from the configuration.
        """

        # Extensions might be useful in the future (custom widget builders,
        # plugins, or alternative constructors). Something worth exploring later.
        self.constructor = TkConstructor()
        self.defined = BDefined()
        self.bound = BBound(command_map)
    def __call__(self, widget_type, root = None):
        """
        Build the application described by a configuration file.

        Params:
            widget_type: The type of widget to construct.

        Returns:
            dict: A dictionary containing the configuration object
            and the constructed tkinter application.

            {
                "config": config,  # FigMan configuration object
                "app": app         # Root tkinter window
            }
        """

        config = self.defined(widget_type)
        build = self.constructor(config, root)
        if config["type"].value != "Window" and config["type"].value != "Menu":
            self.bound(build, config)
        return build
