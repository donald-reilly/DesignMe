from constructor import BConstructed
import tkinter as tk
from typing import List, Dict

class BDesigned:
    def __init__(self):
        """
        Initialize the BDesigned class.
        """
        #self.menu_command_map: Dict[str, callable] = self.create_menu_command_map()
        #self.gui_manager: GUIController = GUIController(self.menu_command_map)
        #
        #self.main_window = self.gui_manager.gui_dict['Window']
        #self.main_window_widget_list = self.gui_manager.gui_dict['Widgets']
        #self.config_dict = self.gui_manager.config_dict
        #self.config_dict_manager = self.gui_manager.config_dict_manager
        #
        #self.edit_popups = []
        loader = BConstructed()
        self.build = loader.create_widget("window")

        
    def create_menu_command_map(self) -> Dict[str, callable]:
        """
        Create a mapping of menu commands to functions.
        
        Returns:
        dict: A dictionary mapping menu commands to functions.
        """

        command_map = {
            'Delete_Widget': self._delete_widget,
            'Apply_Widget_Settings': self._apply_widget_settings,
            'Save_Widget_Settings': self._save_widget_settings,
            'View_Mode': self.mode_selection,
            'Edit_Mode': self.mode_selection,
            'Move_Mode': self.mode_selection,
        }
        return command_map
        
    def mode_selection(self, widget_list: List, mode: str = 'Move_Mode') -> None:
        """
        Handle mode selection for widgets.
        
        Parameters:
        widget_list (list): List of widgets to apply the mode to.
        mode (str): The mode to apply. Default is 'Move'.
        """
        print(f"Mode: {mode}")
        mode_methods = {
            'View_Mode': self._widget_bindings_unbind,
            'Move_Mode': self._widget_bindings_move,
            'Edit_Mode': self._widget_bindings_edit
        }
        if mode in mode_methods:
            mode_methods[mode](widget_list)
            
    def _widget_bindings_unbind(self, widget_list: List) -> None:
        """
        Unbind widget events.
        
        Parameters:
        widget_list (list): List of widgets to unbind events from.
        """
        for widget in widget_list:
            widget.unbind("<Button-1>")
            widget.unbind("<B1-Motion>")
            widget.unbind("<ButtonRelease-1>")
            
    def _widget_bindings_move(self, widget_list: List) -> None:
        """
        Bind widget events for moving.
        
        Parameters:
        widget_list (list): List of widgets to bind move events to.
        """
        for widget in widget_list:
            widget.bind("<Button-1>", self._start_drag)
            widget.bind("<B1-Motion>", self._drag)
            widget.bind("<ButtonRelease-1>", self._finish_drag)
            
    def _widget_bindings_edit(self, widget_list: List) -> None:
        """
        Bind widget events for editing.
        
        Parameters:
        widget_list (list): List of widgets to bind edit events to.
        """
        for widget in widget_list:
            widget.unbind("<Button-1>")
            widget.unbind("<B1-Motion>")
            widget.bind("<ButtonRelease-1>", self._widget_edit_popup)
            
    def _start_drag(self, event) -> None:
        """
        Start dragging a widget.
        
        Parameters:
        event (Event): The event object.
        """
        self.drag_data = {"x": event.x, "y": event.y, "widget": event.widget}
        self.widget = event.widget
        
    def _drag(self, event) -> None:
        """
        Handle dragging of a widget.
        
        Parameters:
        event (Event): The event object.
        """
        widget = self.drag_data["widget"]
        root = widget.winfo_toplevel()
        
        x, y = self.calculate_drag_position(event, widget)
        relx, rely = self.calculate_relative_position(root, x, y)
        wid_rel_x, wid_rel_y = self.calculate_widget_relative_size(widget)
        max_x, max_y = self.calculate_max_position(wid_rel_x, wid_rel_y)
        
        relx = max(0, min(relx, max_x))
        rely = max(0, min(rely, max_y))
        
        widget.place(relx=relx, rely=rely)

    def calculate_drag_position(self, event, widget) -> tuple:
        """
        Calculate the new position of the widget during drag.
        
        Parameters:
        event (Event): The event object.
        widget (Widget): The widget being dragged.
        
        Returns:
        tuple: The new x and y coordinates.
        """
        x = event.x - self.drag_data["x"] + widget.winfo_x()
        y = event.y - self.drag_data["y"] + widget.winfo_y()
        return x, y

    def calculate_max_position(self, wid_rel_x: float, wid_rel_y: float) -> tuple:
        """
        Calculate the maximum position for the widget.
        
        Parameters:
        wid_rel_x (float): The relative width of the widget.
        wid_rel_y (float): The relative height of the widget.
        
        Returns:
        tuple: The maximum x and y coordinates.
        """
        max_x = 1 - wid_rel_x
        max_y = 1 - wid_rel_y
        return max_x, max_y

    def calculate_relative_position(self, root, x: int, y: int) -> tuple:
        """
        Calculate the relative position of the widget.
        
        Parameters:
        root (Widget): The root widget.
        x (int): The x coordinate.
        y (int): The y coordinate.
        
        Returns:
        tuple: The relative x and y coordinates.
        """
        # todo: This method should handle all relative position calculations
        # todo: This method should be moved to a utility class
        # todo: This method should only take the widget as a parameter
        
        relx = x / root.winfo_width()
        rely = y / root.winfo_height()
        return relx, rely

    def calculate_widget_relative_size(self, widget) -> tuple:
        """
        Calculate the relative size of the widget.
        
        Parameters:
        widget (Widget): The widget to calculate the size for.
        
        Returns:
        tuple: The relative width and height of the widget.
        """
        wid_x = widget.winfo_width()
        wid_y = widget.winfo_height()
        window = widget.master
        wid_rel_x = wid_x / window.winfo_width()
        wid_rel_y = wid_y / window.winfo_height()
        return wid_rel_x, wid_rel_y
        
    def _finish_drag(self, event) -> None:
        """
        Finish dragging a widget and update its position.
        
        Parameters:
        event (Event): The event object.
        """
        
        #todo: clean this function up
        #TODO: This needs to change, it uses old logic and old updates
        widget_id = f'{self.widget}'
        self.widget.relx = self.widget.winfo_x() / self.widget.winfo_toplevel().winfo_width()
        self.widget.rely = self.widget.winfo_y() / self.widget.winfo_toplevel().winfo_height()
        new_position = [self.widget.relx, self.widget.rely]
        
        self.config_dict_manager.update_widget_position(new_position=new_position, widget_id=widget_id)
        
    def _widget_edit_popup(self, event) -> None:
        """
        Show a popup for editing the widget.
        
        Parameters:
        event (Event): The event object.
        """
        # todo: clean this up once calculation function is cleaned up
        self.current_widget = event.widget
        root = self.current_widget.winfo_toplevel()
        x = self.current_widget.winfo_x()
        y = self.current_widget.winfo_y()
        self.calculate_relative_position(root, x, y)
        self.edit_pop_up = self.gui_manager.create_window(window_name="popUp")
        
        
    def _delete_widget(self) -> None:
        """
        Delete a widget.
        
        Parameters:
        widget (Widget): The widget to delete.
        """
        print(f'Delete Widget')
        
        widget_id = f'{self.current_widget}'
        self.config_dict_manager.remove_widget(widget_id=widget_id)
        self.current_widget.destroy()
        self.main_window_widget_list.remove(self.current_widget)
        self.current_widget = None
        self.edit_popups[-1].destroy()
    
    def _apply_widget_settings(self) -> None:
        print("Applying Widget Settings!")
        
        for key, value in self.edit_pop_up['Variables'].items():
            if value.get() != '':
                if isinstance(value.get(), str) and isinstance(key, str):
                    self.current_widget.config({key: value.get()})
                elif key == 'relx':
                    self.current_widget.place(relx = value.get())
                elif key == 'rely':
                    self.current_widget.place(rely = value.get())
    def _save_widget_settings(self) -> None:
        print("Saving Widget Settings!")
        
if __name__ == '__main__':
    main = BDesigned()
    main.build.mainloop()