from datetime import datetime
import pandas as pd
import dearpygui.dearpygui as dpg
import dpg_components

dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()

def _on_demo_close(sender, app_data, user_data):
    dpg.delete_item('date_picker_1')
    dpg.delete_item('text_box_1')
    dpg.delete_item(sender)


with dpg.window(label="Example Window", on_close=_on_demo_close, width=800, 
                 height=800, pos=(100,100) ) as w:
    
    with dpg.tree_node(label="Date picker"):

        dpg.add_component('dpg_components','DatePickerComp',tag=f'date_picker_1')

        # Set default date to today
        dpg.configure_item(f'date_picker_1', default_value = datetime.now().date())
    
        # Add another component with the same source as Date picker
        dpg.add_component('dpg_components','TextBoxComp',tag='text_box_1', source='date_picker_1')
    
    with dpg.tree_node(label="Data Grid"):

        # Add Data Grid component
        dpg.add_component('dpg_components','DataGridComp',tag=f'data_grid_1')
        
        data = {
            'Name': ['Alice', 'Bob', 'Charlie'],
            'Age': [25, 30, 28],
            'City': ['New York', 'London', 'Paris']
        }
        df = pd.DataFrame(data)
        
        # Set data grid value
        dpg.set_value('data_grid_1', value = df)
        
        # get component config
        config = dpg.get_item_configuration('data_grid_1')

dpg.show_item_registry()

dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()