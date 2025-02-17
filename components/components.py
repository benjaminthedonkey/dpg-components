from abc import ABC, abstractmethod
from typing import Union
import dearpygui.dearpygui as dpg

class DPGComponent(ABC):

    def __init__(self, tag: Union[int, str] = 0, parent: Union[int, str] = 0):
        self._parent_   = parent if parent else dpg.last_item()
        self._tag_      = tag if tag else dpg.generate_uuid()

    @abstractmethod
    def _delete_(self):
        '''
            Delete all the widgets from the visual tree
        '''

    @abstractmethod
    def _draw_(self):
        '''
            Draw (or render) the visual widgets
        '''

    @abstractmethod    
    def value(self):
        '''
            Returns the component value
        '''
    def value(self, value:any):
        '''
            Set the component's value
        '''
    

class DateTimePickerComponent(DPGComponent):
    '''
        The Date time Picker will be created using two widgets: a text box to to show the current value and date picker on a modal window
    '''

    def __init__(self, tag = 0, parent = 0):
        super().__init__(tag, parent)
        self._group_tag_ = dpg.generate_uuid()
    
    def _draw_(self):
        '''
           Add texbox and date picker to visual tree 
        '''

        # Create a group at the root 
        with dpg.add_group(parent=self._parent_, tag=self._group_tag_, horizontal=True):
            dpg.add_text(with=50)
                    
