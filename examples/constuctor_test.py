from constructor import BConstructed
from serializer import BSerialized

builder = BConstructed()
serializer = BSerialized()


def capture_state(root):
    new_config = serializer()
    serializer.save_configuration("examples/capture_state_test.json", new_config)

    
new_root = builder("examples/tkinter_window_test.json")
new_root["app"].mainloop()