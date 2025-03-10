from abc import ABC, abstractmethod
from typing import List, Any, Callable, Union, Tuple
import dearpygui.dearpygui as dpg
from datetime import date , datetime

class DPGComponent(ABC):

    def __init__(self, tag: Union[int, str] = 0, parent: Union[int, str] = 0):
        
        #self._parent    = parent if parent else dpg.last_item()
        self._parent    = parent
        self._tag       = tag if tag else dpg.generate_uuid()


    @abstractmethod
    def configure(self, **kwargs):
        '''
            Configure item
        '''

    @abstractmethod
    def delete(self, children_only: bool =False, **kwargs):
        '''
            Delete all the widgets from the visual tree
        '''

    @abstractmethod
    def show(self):
        '''
            Show (or render) the visual widgets
        '''

    @abstractmethod 
    def get_value(self):
        '''
            Returns the component value
        '''
    @abstractmethod
    def set_value(self, value:any):
        '''
            Set the component's value
        '''
    
class DateTimePickerComp(DPGComponent):
    '''
        The Date time Picker will be created using two widgets: a text box to to show the current value and date picker on a modal window
    '''

    def __init__(self, tag = 0, parent = 0):
        
        super().__init__(tag, parent)

        self._group_tag                 = dpg.generate_uuid()
        self._text_box_tag              = dpg.generate_uuid()
        self._date_picker_window_tag    = dpg.generate_uuid()
        self._date_picker               = dpg.generate_uuid()

        self.show()
        self.set_value(datetime.now().date())

    
    def delete(self, children_only: bool =False, **kwargs):
        if dpg.does_item_exist(self._group_tag):
            dpg.delete_item(self._group_tag, children_only=children_only, **kwargs)

    def configure(self, **kwargs):
        pass

    def get_value(self):
        return self.value

    def set_value(self, value:any):
        self.value = value
        if dpg.does_item_exist(self._text_box_tag):
            dpg.set_value(self._text_box_tag,  self.value.strftime("%Y-%m-%d"))
        if dpg.does_item_exist(self._date_picker):
            dpg.set_value(self._date_picker, {'month_day': self.value.day, 'year':self.value.year-1900, 'month':self.value.month-1})

    def show_date_picker(self, sender, app_data, user_data):
        dpg.configure_item(self._date_picker_window_tag, show=True)
    
    def on_value_selected(self, sender, app_data, user_data):
        
        if app_data:
            self.value  = date(int(app_data['year']+1900), int(app_data['month']+1), int(app_data['month_day']))
            dpg.set_value(self._text_box_tag,  self.value.strftime("%Y-%m-%d"))

        dpg.configure_item(self._date_picker_window_tag, show=False)

    def show(self):
        '''
           This component is a text box and and date picker
        '''

        if not dpg.does_item_exist(self._group_tag):
        
            # Create a group at the root level
            with dpg.group(tag=self._group_tag, horizontal=True):
                
                with dpg.window(label='Pick Date', modal=True, show=False, no_title_bar=False, tag=self._date_picker_window_tag):
                    dpg.add_date_picker(level=dpg.mvDatePickerLevel_Day, tag=self._date_picker,
                                        default_value={'month_day': 8, 'year':93, 'month':5}, callback=self.on_value_selected)
            
                dpg.add_input_text(tag = self._text_box_tag, enabled = False, width=80)
                dpg.add_button(label='+', callback=self.show_date_picker)

            if self._parent:
                pass
                # TODO move item to parent node
                

                    

