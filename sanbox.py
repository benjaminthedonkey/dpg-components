import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()

uuid = dpg.generate_uuid()

e = dpg.does_item_exist(uuid)

out = dpg.delete_item(e)

dpg.mvMouseButton_Right

def get_id():
    print(dpg.get_alias_id("button"))

with dpg.window(label="tutorial"):
    dpg.add_button(tag="button", label="Press me", callback=get_id)


dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()