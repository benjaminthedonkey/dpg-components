from datetime import datetime
import pandas as pd
import dpgx as dpgx

dpgx.create_context()
dpgx.create_viewport()
dpgx.setup_dearpygui()


def _on_demo_close(sender, app_data, user_data):
    
    dpgx.delete_item('date_picker_1')
    dpgx.delete_item('text_box_1')
    dpgx.delete_item(sender)

    
with dpgx.window(label="Example Window", on_close=_on_demo_close, width=800, 
                 height=800, pos=(100,100) ) as w:
    
    with dpgx.tree_node(label="Date picker"):

        dpgx.add_component('components','DatePickerComp',tag=f'date_picker_1')

        # Set default date to today
        dpgx.configure_item(f'date_picker_1', default_value = datetime.now().date() )
    
        # Add another component with the same source as Date picker
        dpgx.add_component('components','TextBoxComp',tag='text_box_1', source='date_picker_1')
    

    with dpgx.tree_node(label="Data Grid"):

        # Add Data Grid component
        dpgx.add_component('components','DataGridComp',tag=f'data_grid_1')
        
        data = {
            'Name': ['Alice', 'Bob', 'Charlie'],
            'Age': [25, 30, 28],
            'City': ['New York', 'London', 'Paris']
        }
        df = pd.DataFrame(data)
        
        # Set data grid value
        dpgx.set_value(f'data_grid_1', value = df)


dpgx.show_viewport()
dpgx.start_dearpygui()
dpgx.destroy_context()