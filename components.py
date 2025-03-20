from abc import ABC, abstractmethod
from typing import List, Any, Callable, Union, Tuple
import dearpygui.dearpygui as dpg
import dpgx
from datetime import date , datetime

class DPGComponent(ABC):

    def __init__(self, tag: Union[int, str] = 0, parent: Union[int, str] = 0):
        
        self._parent    = parent
        self._tag       = tag if tag else dpg.generate_uuid()


    @abstractmethod
    def configure_item(self, **kwargs):
        '''
            Configure item. Implement the keys that make sence for this component
        '''

    @abstractmethod
    def delete(self, children_only: bool =False, **kwargs):
        '''
            Delete all the widgets from the visual tree. 
            IMPORTANT: if sub components are created as part of this component, you need to delete them here. 
        '''

    @abstractmethod
    def show(self):
        '''
            Show (or render) the visual widgets that form this component.
        '''

    @abstractmethod 
    def get_value(self):
        '''
            Returns the component value of the component
        '''
    @abstractmethod
    def set_value(self, value:any):
        '''
            Set the value of the component
        '''


################################################################
#  Components
################################################################

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
   
    def delete(self, children_only: bool =False, **kwargs):
        if dpg.does_item_exist(self._group_tag):
            dpg.delete_item(self._group_tag, children_only=children_only, **kwargs)

    def configure_item(self, **kwargs):
        if 'default_value' in kwargs:
            dpgx.set_value(self._tag, kwargs['default_value'])

    def get_value(self):
        return dpgx.get_value(self._tag)

    def set_value(self, value:any):
        if dpg.does_item_exist(self._text_box_tag):
            dpg.set_value(self._text_box_tag,  value.strftime("%Y-%m-%d"))
        if dpg.does_item_exist(self._date_picker):
            dpg.set_value(self._date_picker, {'month_day': value.day, 'year':value.year-1900, 'month':value.month-1})

    def show_date_picker(self, sender, app_data, user_data):
        dpg.configure_item(self._date_picker_window_tag, show=True)
    
    def on_value_selected(self, sender, app_data, user_data):
        
        if app_data:
            value  = date(int(app_data['year']+1900), int(app_data['month']+1), int(app_data['month_day']))
            dpgx.set_value(self._tag, value)

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
                
class TextBoxComp(DPGComponent):
    '''
        A wrapper for DPG TextBox 
    '''                    
    def __init__(self, tag = 0, parent = 0):
        
        super().__init__(tag, parent)

        self._group_tag                 = dpg.generate_uuid()
        self._text_box_tag              = dpg.generate_uuid()
      
        self.show()
      

    def delete(self, children_only: bool =False, **kwargs):
        if dpg.does_item_exist(self._group_tag):
            dpg.delete_item(self._group_tag, children_only=children_only, **kwargs)

    def configure_item(self, **kwargs):
        pass

    def get_value(self):
        return dpgx.get_value(self._tag)

    def set_value(self, value:any):
        if dpg.does_item_exist(self._text_box_tag):
            dpg.set_value(self._text_box_tag,  value)

    def show(self):
        '''
           This component is a text box 
        '''

        if not dpg.does_item_exist(self._group_tag):
        
            # Create a group at the root level
            with dpg.group(tag=self._group_tag):
                dpg.add_input_text(tag=self._text_box_tag, width=120)

            if self._parent:
                pass
                # TODO move item to parent node


class DataGridComp(DPGComponent):
    '''
        A Data Grid Component. The value is a Pandas Data Frame.
    '''                    
    def __init__(self, tag = 0, parent = 0):
        
        super().__init__(tag, parent)
        self._group_tag                 = dpg.generate_uuid()
        self._table_tag                 = dpg.generate_uuid()
        self.show()
      

    def delete(self, children_only: bool =False, **kwargs):
        if dpg.does_item_exist(self._group_tag):
            dpg.delete_item(self._group_tag, children_only=children_only, **kwargs)

    def configure_item(self, **kwargs):
        pass

    def get_value(self):
        return dpgx.get_value(self._tag)

    def set_value(self, value:any):
        if dpg.does_item_exist(self._group_tag):
            #  TODO
            #  1) Delete current rows fom table 
            #  2) Add new rows to table
            pass


    def show(self):
        '''
           Use the table API to render the Data Grid.
        '''

        if not dpg.does_item_exist(self._group_tag):
        
            # Create a group at the root level
            with dpg.group(tag=self._group_tag):
                dpg.add_table(tag=self._table_tag)
                

            if self._parent:
                pass
                # TODO move item to parent node