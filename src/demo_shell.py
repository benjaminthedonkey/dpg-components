import DPGComponents.DPGComponents as comps
import dearpygui.dearpygui as dpg

class Stock(comps.DPGModule):
    
    def __init__(self, group_name, module_name, key_words):
        super().__init__(group_name, module_name, key_words)

        #window_id = dpg.get_ne
    
    def delete(self, **kwargs):
        pass
    
    def show(self):
        ''' render Module'''
        with dpg.window():
            dpg.add_input_text(hint="search", width=-1)


# --- Main Application Logic ---
def main():

    comps.create_and_lunch_shell("Demo App")

if __name__ == "__main__":
    main() 