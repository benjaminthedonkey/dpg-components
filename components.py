from abc import ABC, abstractmethod
from typing import List, Any, Callable, Union, Tuple
import dearpygui.dearpygui as dpg
import dpgx
from datetime import date , datetime

class dpgxComponent(ABC):

    def __init__(self, tag: Union[int, str] = 0, parent: Union[int, str] = 0):
        
        self._parent    = parent
        self._tag       = tag if tag else dpgx.generate_uuid()


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

class DatePickerComp(dpgxComponent):
    '''
        The Date Picker will be created using two widgets: a text box to to show the current value and date picker on a modal window
    '''

    def __init__(self, tag = 0, parent = 0):
        
        super().__init__(tag, parent)

        self._group_tag                 = dpgx.generate_uuid()
        self._text_box_tag              = dpgx.generate_uuid()
        self._date_picker_window_tag    = dpgx.generate_uuid()
        self._date_picker               = dpgx.generate_uuid()

        self.show()
   
    def delete(self, children_only: bool =False, **kwargs):
        if dpgx.does_item_exist(self._group_tag):
            dpgx.delete_item(self._group_tag, children_only=children_only, **kwargs)

    def configure_item(self, **kwargs):
        if 'default_value' in kwargs:
            dpgx.set_value(self._tag, kwargs['default_value'])

    def get_value(self):
        return dpgx.get_value(self._tag)

    def set_value(self, value:any):
        if dpgx.does_item_exist(self._text_box_tag):
            dpgx.set_value(self._text_box_tag,  value.strftime("%Y-%m-%d"))
        if dpgx.does_item_exist(self._date_picker):
            dpgx.set_value(self._date_picker, {'month_day': value.day, 'year':value.year-1900, 'month':value.month-1})

    def show_date_picker(self, sender, app_data, user_data):
        dpgx.configure_item(self._date_picker_window_tag, show=True)
    
    def on_value_selected(self, sender, app_data, user_data):
        
        if app_data:
            value  = date(int(app_data['year']+1900), int(app_data['month']+1), int(app_data['month_day']))
            dpgx.set_value(self._tag, value)

        dpgx.configure_item(self._date_picker_window_tag, show=False)

    def show(self):
        '''
           This component is a text box and and date picker
        '''

        if not dpgx.does_item_exist(self._group_tag):
        
            # Create a group at the root level
            with dpgx.group(tag=self._group_tag, horizontal=True):
                
                with dpgx.window(label='Pick Date', modal=True, show=False, no_title_bar=False, tag=self._date_picker_window_tag):
                    dpgx.add_date_picker(level=dpg.mvDatePickerLevel_Day, tag=self._date_picker,
                                        default_value={'month_day': 8, 'year':93, 'month':5}, callback=self.on_value_selected)
            
                dpgx.add_input_text(tag = self._text_box_tag, enabled = False, width=80)
                dpgx.add_button(label='+', callback=self.show_date_picker)

            if self._parent:
                pass
                # TODO move item to parent node
                
class TextBoxComp(dpgxComponent):
    '''
        A wrapper for dpgx TextBox 
    '''                    
    def __init__(self, tag = 0, parent = 0):
        
        super().__init__(tag, parent)

        self._group_tag                 = dpgx.generate_uuid()
        self._text_box_tag              = dpgx.generate_uuid()
      
        self.show()
      

    def delete(self, children_only: bool =False, **kwargs):
        if dpgx.does_item_exist(self._group_tag):
            dpgx.delete_item(self._group_tag, children_only=children_only, **kwargs)

    def configure_item(self, **kwargs):
        pass

    def get_value(self):
        return dpgx.get_value(self._tag)

    def set_value(self, value:any):
        if dpgx.does_item_exist(self._text_box_tag):
            dpgx.set_value(self._text_box_tag,  value)

    def show(self):
        '''
           This component is a text box 
        '''

        if not dpgx.does_item_exist(self._group_tag):
        
            # Create a group at the root level
            with dpgx.group(tag=self._group_tag):
                dpgx.add_input_text(tag=self._text_box_tag, width=120)

            if self._parent:
                pass
                # TODO move item to parent node


class DataGridComp(dpgxComponent):
    '''
        A Data Grid Component. The value is a Pandas Data Frame.
    '''                    
    def __init__(self, tag = 0, parent = 0):
        
        super().__init__(tag, parent)
        self._group_tag                 = dpgx.generate_uuid()
        self._table_tag                 = dpgx.generate_uuid()
        self.show()
      

    def delete(self, children_only: bool =False, **kwargs):
        if dpgx.does_item_exist(self._group_tag):
            dpgx.delete_item(self._group_tag, children_only=children_only, **kwargs)

    def configure_item(self, **kwargs):
        pass

    def get_value(self):
        return dpgx.get_value(self._tag)

    def set_value(self, value:any):
        self.delete()
        self.show()   

    def show(self):
        '''
           Use the table API to render the Data Grid.
        '''

        def _delete_table():
            if dpgx.does_item_exist(self._table_tag):
                dpg.delete_item(self._table_tag)

        if not dpgx.does_item_exist(self._group_tag):

            _delete_table()
        
            # Create a group at the root level
            with dpgx.group(tag=self._group_tag):

                with dpgx.table(tag=self._table_tag, header_row=True, borders_innerH=True, 
                               borders_outerH=True, borders_innerV=True, borders_outerV=True):
                    
                    _data = dpgx.get_value(self._tag)
                    if _data is not None and not _data.empty:
                        for c in _data.columns:
                            dpgx.add_table_column(label=c)
                        for index, row in _data.iterrows():
                            with dpgx.table_row():
                                for c in _data.columns:                                      
                                    with dpgx.table_cell():
                                        dpgx.add_text(default_value=row[c])

            if self._parent:
                pass
                # TODO move item to parent node