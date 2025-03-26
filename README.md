## dpg-components

[DearPyGui](https://github.com/hoffstadt/DearPyGui) is an amazing library and yet, I often find myself wishing there were an easy way to define reusable pieces of UI. From React JS documentation:  "A component is a piece of the UI (user interface) that has its own logic and appearance. A component can be as small as a button, or as large as an entire page." Components are a powerful abstraction.   

The goal of this project is to test a few ideas on how to bring Components to DearPyGui.  

 - Components should be first class citizens, i.e. use the same API as regular Widgets.
 - Components can contain other Components or regular Widgets.
 - Although Components are required to implements a contract (DPGComponent), reusability is achieved through composition.

### How it works ?
Simply import module dpg_components. It will be add function "add_component" to the DearPyGui module.

```python 
import dpg_components
import dearpygui.dearpygui as dpg
```

