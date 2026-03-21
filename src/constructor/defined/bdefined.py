from persistance import BPersistent
from figman import FigMan

class BDefined:
    def __init__(self):
        """
        Initialize the BDefined class.

        This class serves as the manager of FigMan configurations, to be utilized by BDesigned.
        It is responsible for managing the configuration hierarchy and providing access to the configuration data for BDesigned.
        It holds default tkinter object configuration data, which can be accessed and modified by BConstructed, and ultimately used by BDesigned to construct the tkinter UI.

        Components:
            FigMan       -> Manages configuration group structures.
        """
        self.manager = FigMan()
        self.persistance = BPersistent()
        self.default_configurations = {
            "window": "src/constructor/defined/definitions/window.json",
            "button": "src/constructor/defined/definitions/button.json",
            "label": "src/constructor/defined/definitions/label.json",
            "entry": "src/constructor/defined/definitions/entry.json",
            "frame": "src/constructor/defined/definitions/frame.json",
            "canvas": "src/constructor/defined/definitions/canvas.json",
            "checkbutton": "src/constructor/defined/definitions/checkbutton.json",
            "radiobutton": "src/constructor/defined/definitions/radiobutton.json",
            "listbox": "src/constructor/defined/definitions/listbox.json",

        }
    def __call__(self, object_type):

        return self._get_widget_configuration(object_type)
    def _get_widget_configuration(self, widget_type):
        """
        Retrieve the configuration for a specific widget type.

        Params:
            widget_type (str): The type of widget to retrieve the configuration for.
        Returns:
        """

        config_path = self.default_configurations.get(widget_type)
        if not config_path:
            raise ValueError(f"No configuration found for widget type: {widget_type}")
        
        # Load the configuration file and return the FigMan structure
        return self._load_configuration(config_path)
    
    def _load_configuration(self, file_path):
        """
        Load the serialized configuration file and deserialize it
        into a FigMan configuration structure.

        Params:
            file_path: Path to the serialized configuration file.

        Returns:
            MasterGroup: The deserialized configuration hierarchy.
        """

        # Load raw dictionary from file
        new_dict = self.persistance(file_path)

        # Convert dictionary into FigMan structure
        return self._deserialize_all(new_dict)

    def _deserialize_all(self, config: dict, top_level=None, current_level=None):
        """
        Recursively deserialize a configuration dictionary into a
        FigMan MasterGroup hierarchy.

        The input dictionary structure is traversed and converted
        into nested configuration groups managed by FigMan.

        Params:
            config (dict):
                The configuration dictionary to deserialize.

            top_level (MasterGroup, optional):
                The root configuration group being constructed.

            current_level (MasterGroup, optional):
                The current group being populated during recursion.

        Returns:
            MasterGroup:
                The fully constructed configuration group hierarchy.
        """

        # Iterate through the configuration dictionary
        for member_id, member_config in config.items():

            # If the value is another dictionary, it represents
            # a nested configuration group
            if isinstance(member_config, dict):

                # If the top level group has not been created yet,
                # initialize it using the first key encountered
                if not top_level:
                    top_level = self.manager(member_id)
                    current_level = top_level

                    # Continue recursion into the nested structure
                    self._deserialize_all(member_config, top_level, current_level)

                else:
                    # Create or retrieve the nested configuration group
                    new_group = current_level[member_id]

                    # Continue recursion within this new group
                    self._deserialize_all(member_config, top_level, new_group)

            # If the value is not a dictionary, it represents
            # a configuration attribute for the current group
            else:
                current_level[member_id] = member_config

        # Return the completed configuration hierarchy
        return top_level
