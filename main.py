import dearpygui.dearpygui as dpg
import dearpygui.demo as demo
import warnings
import dearpygui_ext

warnings.simplefilter('always', DeprecationWarning)

dpg.enable_docking()

demo.show_demo()

with dpg.window(label="tutorial", width=500, height=500):
    dpg.add_button(label="Press me")

dpg.start_dearpygui()
