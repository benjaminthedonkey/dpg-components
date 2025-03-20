import dpgx
from components import DateTimePickerComp
from datetime import date , datetime


def save_callback():
    print("Save Clicked")

dpgx.create_context()
dpgx.create_viewport()
dpgx.setup_dearpygui()


def _on_demo_close(sender, app_data, user_data):
    for i in range(1,10):
        dpgx.delete_item(f'date_picker_{i}')

    dpgx.delete_item(sender)

    
with dpgx.window(label="Example Window", on_close=_on_demo_close, width=800, 
                 height=800, pos=(100,100) ) as w:
    
    with dpgx.tree_node(label="Date time picker"):
        for i in range(1,5):
            dpgx.add_component('components','DateTimePickerComp',tag=f'date_picker_{i}')
            dpgx.configure_item(f'date_picker_{i}', default_value = datetime.now().date() )
    
        for i in range(1,5):
            dpgx.add_component('components','TextBoxComp',tag=f'text_box{i}', source=f'date_picker_{i}')


dpgx.show_viewport()
dpgx.start_dearpygui()
dpgx.destroy_context()