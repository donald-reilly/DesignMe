import json
import yaml

class BPersistent():
    def __init__(self):
        file_paths = {
            "tkinter_window_1": "somefilepath"
        }
        self.supported_formats = {
            "json": json,
            "yaml": yaml
        }
    def __call__(self, file_path, master_group = None):
        #TODO: I'm not sure if I like this or not yet, this allows for a call to BPersistent to save or load. Depending upon the existence of a master group.
        if master_group:
            self._to_file(master_group.serialized_state, file_path)
        else:
            self._from_file(file_path)
        
    def _to_file(self, configuration_dict, file_path):
        """
        Serialize a configuration dictionary to a file.

        Params:
            configuration_dict (dict): The configuration data to serialize.
            file_path (str): Path to the file where the data should be saved. Must end in .json or .yaml.
        """

        with open(file_path, 'w') as config_dict:
            self.supported_formats[self._get_file_format(file_path)].dump(
                configuration_dict, config_dict, indent=4, default = str)

    def _from_file(self, file_path: str) -> dict:
        """
        Load a configuration from a file.

        Params:
            file_path (str): Path to the configuration file to load. Must end in .json or .yaml.
        Returns:
            dict: The loaded configuration data.
        Raises:
            ValueError: If the file format is not supported.
        """

        with open(file_path, 'r') as config_dict:
            loaders = {
                "json": json.load(config_dict),
                "yaml": yaml.load(config_dict, Loader=yaml.FullLoader)
            }
            return loaders[self.file_format(file_path)]

    def _get_file_format(self, file_path: str) -> str:
        """
        Extract the file format from a file path.

        Params:
            file_path (str): The path to the file.

        Returns:
            str: The file format (json or yaml).
        """

        return file_path[-4:len(file_path)]

