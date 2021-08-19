import dearpygui.dearpygui as dpg
import warnings
from dearpygui_ext.logger import mvLogger

warnings.simplefilter('always', DeprecationWarning)

logger = mvLogger()
logger.log_info(dpg.get_dearpygui_version())

dpg.start_dearpygui()
