from persistance import BPersistent
from figman import FigMan
from constructor.constuctors import TkConstructor


class BConstructed():
    """
    BConstructed loads a serialized tkinter configuration and reconstructs
    the application during runtime.

    The configuration is loaded from disk, deserialized into a FigMan
    configuration structure, and then passed to the TkConstructor
    to build the tkinter interface.
    """

    def __init__(self):
        """
        Initialize BConstructed and its core components.

        Components:
            BPersistent  -> Handles loading serialized configuration files.
            FigMan       -> Manages configuration group structures.
            TkConstructor-> Builds tkinter widgets from the configuration.
        """

        # Handles loading JSON/YAML configuration files
        self.persistance = BPersistent()

        # TODO:
        # Extensions might be useful in the future (custom widget builders,
        # plugins, or alternative constructors). Something worth exploring later.
        self.constructor = TkConstructor()

        # Manages the configuration hierarchy
        self.manager = FigMan()

    def __call__(self, file_path):
        """
        Build the application described by a configuration file.

        Params:
            file_path: Path to the .json or .yaml file holding the
                       serialized window configuration.

        Returns:
            dict: A dictionary containing the configuration object
            and the constructed tkinter application.

            {
                "config": config,  # FigMan configuration object
                "app": app         # Root tkinter window
            }
        """

        build = self._build_configuration(file_path)
        return build

    def _build_configuration(self, file_path):
        """
        Load the configuration file and construct the tkinter application.

        Params:
            file_path: Path to the serialized configuration file.

        Returns:
            dict: A dictionary containing the configuration and
                  constructed tkinter root window.
        """

        # Load and deserialize configuration structure
        config = self._load_configuration(file_path)

        # Build tkinter application using the configuration
        app = self.constructor(config)

        # Return both the configuration and the constructed app
        build = {
            "config": config,
            "app": app
        }

        return build

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