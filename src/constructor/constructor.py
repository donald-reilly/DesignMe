from persistance import BPersistent
from figman import FigMan
from serializer import BSerialized
class BConstructed():
    """
    BConstructed takes custom json serialized tkinter objects and reconstructs them during runtime.
    """
    def __init__(self):
        self.persistance = BPersistent()
        self.manager  = FigMan()
    
    def __call__(self, file_path):
        return self._load_configuration(file_path)
    
    def _load_configuration(self, file_path):
        new_dict = self.persistance(file_path)
        return self._deserialize_all(new_dict)

    def _deserialize_all(self, config: dict, top_level= None, current_level= None):
        """
        Recursively deserialize a configuration dictionary into a MasterGroup structure.
        
        Params:
            config (dict): The configuration dictionary to deserialize.
        Args:
            top_level (MasterGroup, optional): The top-level group being built.
            current_level (MasterGroup, optional): The current group being populated.
            
        Returns:
            MasterGroup: The fully constructed configuration group hierarchy.
        """

        for member_id, member_config in config.items():
            if isinstance(member_config, dict):
                if not top_level:
                    top_level = self.manager(member_id)
                    current_level = top_level
                    self._deserialize_all(member_config, top_level, current_level)  
                else:
                    new_group = current_level[member_id] # type: ignore
                    self._deserialize_all(member_config, top_level, new_group)# type: ignore
            else:
                current_level[member_id]= member_config # type: ignore
        return top_level # type: ignore
