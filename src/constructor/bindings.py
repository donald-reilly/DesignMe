class BBound:
    def __init__(self, function_map: dict):
        """
        Initialize the BBound class.
        """
        self.function_map = function_map

    def __call__(self, widget, widget_config):
        self.bind_widget(widget, widget_config)

    def bind_widget(self, widget, widget_config):
        print(widget_config)
        if widget_config["command"].value is not None:
            widget.config(command =  lambda: self.function_map[widget_config["command"].value]())
            