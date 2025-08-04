from typing import List, Any, Callable, Union, Tuple
import importlib
import dearpygui.dearpygui as dpg
import dearpygui._dearpygui as internal_dpg
from abc import ABC, abstractmethod
from datetime import date
import os
import importlib.resources
import threading
import queue
import time
from timeit import default_timer as timer

# ICONS
ICO_CALENDAR    = 'ico_calendar_14'
ICO_ABC         = 'ico_abc_14'
ICO_FILE        = {ICO_CALENDAR : 'calendar_month_14dp_FFFFFF_FILL0_wght200_GRAD0_opsz20.png',
                    ICO_ABC: 'abc_16dp_FFFFFF_FILL0_wght200_GRAD0_opsz20.png'}

# Create a thread-safe queue for communication with the Background Worker thread
TASK_QUEUE = queue.Queue()
START_TIME = timer() # https://github.com/hoffstadt/DearPyGui/issues/579


def worker_thread():
    """ Background Worker thread """
    while True:
        try:
            task = TASK_QUEUE.get(timeout=1)  # Get a task from the queue with a timeout
            if task is None:  # Sentinel value for stopping the thread
                print(f"[Background Worker] Got Signal to exit")
                break
            print(f"Processing task: {task}")
            time.sleep(1)  # Simulate work being done
            print(f"Finished task: {task}")
            TASK_QUEUE.task_done()  # Mark the task as done
        except queue.Empty:
            # No tasks in the queue, continue waiting
            pass
        except Exception:
            pass

def create_and_lunch_shell(title = None):
    ''' Creates and lunch the main app shell '''    

    def on_app_exit():
        ''' Signal the Background Worker thread to stop'''
        TASK_QUEUE.join()
        TASK_QUEUE.put(None) # Signal the worker thread to stop
        time.sleep(1)

    def on_render():
        '''Take care of animations on this render loop'''
        global START_TIME        
        frame_count = dpg.get_frame_count()
        delta_time = 1000 * dpg.get_delta_time()
        elapsed_time = 1000 * (timer() - START_TIME)
        START_TIME = timer()
        frame_rate =   int(1000 / delta_time) if delta_time > 0 else 0
        #dpg.set_value("TIMERID", f"Frame rate: {frame_rate:.2f} Delta time: {delta_time:.2f} ms / Time between worker calls: {elapsed_time:.2f} ms , frame count {frame_count}")

    dpg.create_context()
    
    with dpg.window(tag="_PW_"):
        dpg.add_spacer()
        dpg.add_component(ModuleSearchBarComp, tag=f'SEARCH_BAR')


    dpg.create_viewport(title=title, width=1280, height=720)
    
	# Enable docking ( doesn't work with primary window ?)
    # dpg.configure_app(docking=True, docking_space=True)
    
    # Register the exit callback
    dpg.set_exit_callback(on_app_exit)

	# setup_dearpygui must be called after creating the viewport and before showing it.
    dpg.setup_dearpygui()
	
    dpg.show_viewport()
    dpg.set_primary_window("_PW_", True)

     # Start the background worker thread
    worker = threading.Thread(name='daemon', target=worker_thread, daemon=True)
    worker.start()


	# Use the manual render loop as requested
    while dpg.is_dearpygui_running():
        try:
            on_render()
            dpg.render_dearpygui_frame()
        except Exception as ex:
            print(ex)

    dpg.destroy_context()

    worker.join(5)

def use_icon(icon_name : str):
     '''
        Register icons for future user
     '''
     if  not dpg.does_item_exist(icon_name):
        if __package__ is not None:
            with importlib.resources.path('DPGComponents.icons', ICO_FILE[icon_name]) as fd_img_path:
                width, height, _, data = dpg.load_image(str(fd_img_path))
                ico_ = [width, height, data]
                with dpg.texture_registry():
                    dpg.add_static_texture(width=ico_[0], height=ico_[1], default_value=ico_[2], tag=icon_name)

class DPGComponent(ABC):

    def __init__(self, tag: Union[int, str] = 0, parent: Union[int, str] = 0 , show : bool = True):
        
        #self._parent    = parent if parent else dpg.last_container()
        self._parent    = parent
        self._tag       = tag if tag else dpg.generate_uuid() 
        self._configuration = {'show':show}


    def get_item_configuration(self, **kwargs):
        '''
            Returns the item configuration
        '''
        return self._configuration
        

    @abstractmethod
    def configure_item(self, **kwargs):
        '''
            Configure item. Implement the keys that make sense for this component
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

###########################################################################
#  Module
###########################################################################
class DPGModule():

    ''' A Module . Name must be unique within the group'''
    
    def __init__(self, group_name : str, module_name : str, key_words : List ):

        self._group_name = group_name
        self._module_name = module_name
        self._key_words = key_words
        self.show()    
    
    @abstractmethod
    def delete(self, **kwargs):
        '''
            Delete all the widgets from the visual tree. 
            IMPORTANT: if sub components are created as part of this component, you need to delete them here. 
        '''

    @abstractmethod
    def show(self):
        '''
            Show (or render) the visual widgets that form this Module.
        '''

###########################################################################
#  Components
###########################################################################


class DatePickerComp(DPGComponent):
    '''
        The Date Picker will be created using two widgets: a text box to to show the current value and date 
        picker on a modal window
    '''

    def __init__(self, tag = 0, parent = 0):
        
        super().__init__(tag, parent)

        self._group_tag                 = dpg.generate_uuid()
        self._text_box_tag              = dpg.generate_uuid()
        self._date_picker_window_tag    = dpg.generate_uuid()
        self._date_picker               = dpg.generate_uuid()

        use_icon(ICO_CALENDAR)

        self.show()
    
   
    def delete(self, children_only: bool =False, **kwargs):
        if dpg.does_item_exist(self._group_tag):
            dpg.delete_item(self._group_tag, children_only=children_only, **kwargs)
        if dpg.does_item_exist(self._date_picker_window_tag):
            dpg.delete_item(self._date_picker_window_tag, children_only=children_only, **kwargs)

    def configure_item(self, **kwargs):
        if 'default_value' in kwargs:
            dpg.set_value(self._tag, kwargs['default_value'])
        if 'show' in  kwargs:
            dpg.configure_item(self._group_tag, show=kwargs['show'])

    def get_value(self):
        return dpg.get_value(self._tag)

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
            dpg.set_value(self._tag, value)

        dpg.configure_item(self._date_picker_window_tag, show=False)

    def show(self):
        '''
           This component is a text box and and date picker
        '''

        if not dpg.does_item_exist(self._group_tag) and self._configuration['show']:
        
            # Create a group at the root level
            with dpg.group(tag=self._group_tag, horizontal=True, show=self._configuration['show']):
                
                with dpg.window(label='Pick Date', modal=True, show=False, no_title_bar=False, tag=self._date_picker_window_tag):
                    dpg.add_date_picker(level=dpg.mvDatePickerLevel_Day, tag=self._date_picker,
                                        default_value={'month_day': 8, 'year':93, 'month':5}, callback=self.on_value_selected)
            
                dpg.add_input_text(tag = self._text_box_tag, enabled = False, width=80)
                dpg.add_image_button(ICO_CALENDAR, callback=self.show_date_picker)

            if self._parent:
                dpg.move_item(self._group_tag, parent=self._parent)
                
class TextBoxComp(DPGComponent):
    '''
        A wrapper for dpg TextBox 
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
        if 'show' in  kwargs:
            dpg.configure_item(self._group_tag, show=kwargs['show'])

    def get_value(self):
        return dpg.get_value(self._tag)

    def set_value(self, value:any):
        if dpg.does_item_exist(self._text_box_tag):
            dpg.set_value(self._text_box_tag,  value)

    def show(self):
        '''
           This component is a text box 
        '''

        if not dpg.does_item_exist(self._group_tag):
        
            # Create a group at the root level
            with dpg.group(tag=self._group_tag, show=self._configuration['show']):
                dpg.add_input_text(tag=self._text_box_tag, width=120)

            if self._parent:
                dpg.move_item(self._group_tag, parent=self._parent)

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
        if 'show' in  kwargs:
            dpg.configure_item(self._group_tag, show=kwargs['show'])

    def get_value(self):
        return dpg.get_value(self._tag)

    def set_value(self, value:any):
        self.delete()
        self.show()   

    def _export(self, sender, app_data, user_data):
        print(f"sender: {sender}, \t app_data: {app_data}, \t user_data: {user_data}")
        # TODO

    def show(self):
        '''
           Use the table API to render the Data Grid.
        '''

            
        def sort_callback(sender, sort_specs):

            # sort_specs scenarios:
            #   1. no sorting -> sort_specs == None
            #   2. single sorting -> sort_specs == [[column_id, direction]]
            #   3. multi sorting -> sort_specs == [[column_id, direction], [column_id, direction], ...]
            #
            # notes:
            #   1. direction is ascending if == 1
            #   2. direction is ascending if == -1

            # no sorting case
            if sort_specs is None: return

            rows = dpg.get_item_children(sender, 1)

            # create a list that can be sorted based on first cell
            # value, keeping track of row and value used to sort
            sortable_list = []
            for row in rows:
                first_cell = dpg.get_item_children(row, 1)[0]
                sortable_list.append([row, dpg.get_value(first_cell)])

            def _sorter(e):
                return e[1]

            sortable_list.sort(key=_sorter, reverse=sort_specs[0][1] < 0)

            # create list of just sorted row ids
            new_order = []
            for pair in sortable_list:
                new_order.append(pair[0])
                            
            dpg.reorder_items(sender, 1, new_order)

        def _delete_table():
            if dpg.does_item_exist(self._table_tag):
                dpg.delete_item(self._table_tag)

        if not dpg.does_item_exist(self._group_tag):

            _delete_table()
        
            # Create a group at the root level
            with dpg.group(tag=self._group_tag, show=self._configuration['show']):

                with dpg.table(tag=self._table_tag, header_row=True, borders_innerH=True, sortable=True, callback=sort_callback,
                               borders_outerH=True, borders_innerV=True, borders_outerV=True):
                    
                    _data = dpg.get_value(self._tag)
                    if _data is not None and not _data.empty:
                        for c in _data.columns:
                            dpg.add_table_column(label=c)
                        for index, row in _data.iterrows():
                            with dpg.table_row():
                                for c in _data.columns:
                                     dpg.add_text(default_value=row[c])

                #dpg.add_combo(("csv","excel"), label="export", width=100, callback= self._export)
                
            if self._parent:
                dpg.move_item(self._group_tag, parent=self._parent)

class ModuleSearchBarComp(DPGComponent):
    '''
        Search bar used in main window
    '''

    def __init__(self, tag = 0, parent = 0):
        
        super().__init__(tag, parent)
        self._group_tag                 = dpg.generate_uuid()
        self.show()
    
    def delete(self, children_only: bool =False, **kwargs):
        if dpg.does_item_exist(self._group_tag):
            dpg.delete_item(self._group_tag, children_only=children_only, **kwargs)

    def configure_item(self, **kwargs):
        if 'show' in  kwargs:
            dpg.configure_item(self._group_tag, show=kwargs['show'])

    def get_value(self):
        return dpg.get_value(self._tag)

    def set_value(self, value:any):
        pass

    
    def show(self):
        '''
           Render visual components
        '''

        if not dpg.does_item_exist(self._group_tag) and self._configuration['show']:
            dpg.add_input_text(hint="search", width=-1)
            with dpg.child_window(tag="_SR_", autosize_x=True, auto_resize_y=True):
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Header 1", width=75, height=75)
                    dpg.add_button(label="Header 2", width=75, height=75)
                    dpg.add_button(label="Header 3", width=75, height=75)

        
    