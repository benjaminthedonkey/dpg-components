## dpg-components

 From React JS documentation:  "A component is a piece of the UI (user interface) that has its own logic and appearance. A component can be as small as a button, or as large as an entire page." Components are a powerful abstraction.   

The goal of this project is to bring Components to [DearPyGui](https://github.com/hoffstadt/DearPyGui)   

 - Components should be first class citizens, i.e. use the same API as regular Items.
 - Components can contain other Components or regular Items.
 - Reusability is achieved through composition.

### How it works ?
Import module dpg_components, then you can call method add_component as follows:

```python 
import dpg_components
import dearpygui.dearpygui as dpg
```

### How to create and use a new Component ?

First, create a new class and implement abstract class "DPGComponent". Then you can use your new component as follows:   
```python 
  dpg.add_component(dpg_components.DatePickerComp ,tag=f'com_1')
```
