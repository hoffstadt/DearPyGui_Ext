import logging
import queue
from logging.handlers import QueueHandler

import dearpygui.dearpygui as dpg

class mvLogger:
    """Class to show log mesages raised by the logging module."""

    def __init__(self, parent=None):

        self._auto_scroll = True
        self.filter_id = None
        if parent:
            self.window_id = parent
        else:
            self.window_id = dpg.add_window(label="mvLogger", pos=(200, 200), width=500, height=500)
        self.count = 0
        self.flush_count = 1000

        with dpg.group(horizontal=True, parent=self.window_id):
            dpg.add_checkbox(label="Auto-scroll", default_value=True, callback=lambda sender:self.auto_scroll(dpg.get_value(sender)))
            dpg.add_button(label="Clear", callback=lambda: dpg.delete_item(self.filter_id, children_only=True))

        dpg.add_input_text(label="Filter", callback=lambda sender: dpg.set_value(self.filter_id, dpg.get_value(sender)),
                    parent=self.window_id)
        self.child_id = dpg.add_child_window(parent=self.window_id, autosize_x=True, autosize_y=True)
        self.filter_id = dpg.add_filter_set(parent=self.child_id)

        with dpg.theme() as self.trace_theme:
            with dpg.theme_component(0):
                dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 255, 0, 255))

        with dpg.theme() as self.debug_theme:
            with dpg.theme_component(0):
                dpg.add_theme_color(dpg.mvThemeCol_Text, (64, 128, 255, 255))

        with dpg.theme() as self.info_theme:
            with dpg.theme_component(0):
                dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255, 255))

        with dpg.theme() as self.warning_theme:
            with dpg.theme_component(0):
                dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 0, 255))

        with dpg.theme() as self.error_theme:
            with dpg.theme_component(0):
                dpg.add_theme_color(dpg.mvThemeCol_Text, (220, 128, 64, 255))

        with dpg.theme() as self.critical_theme:
            with dpg.theme_component(0):
                dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 0, 0, 255))

    def auto_scroll(self, value):
        self._auto_scroll = value

    def _log(self, message, level):
        """Take in a log message to show in DPG."""

        self.count+=1

        if self.count > self.flush_count:
            self.clear_log()

        levelname = logging._levelToName[level].lower()
        logtheme = getattr(self, f'{levelname}_theme')

        new_log = dpg.add_text(message, parent=self.filter_id, filter_key=message)
        dpg.bind_item_theme(new_log, logtheme)
        if self._auto_scroll:
            scroll_max = dpg.get_y_scroll_max(self.child_id)
            dpg.set_y_scroll(self.child_id, -1.0)

    def clear_log(self):
        dpg.delete_item(self.filter_id, children_only=True)
        self.count = 0


if __name__ == "__main__":

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    log_queue = queue.Queue(1000)
    queue_handler = QueueHandler(log_queue)
    queue_formatter = logging.Formatter('%(levelname)8s: %(message)s')
    queue_handler.setFormatter(queue_formatter)
    queue_handler.setLevel(logging.NOTSET)

    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter('%(levelname)8s: %(message)s')
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.WARNING)

    logger.addHandler(queue_handler)
    logger.addHandler(console_handler)

    dpg.create_context()

    dpg.create_viewport()


    logger.debug("We can log to a debug level.")
    logger.info("We can log to an info level.")
    logger.warning("We can log to a warning level.")
    logger.error("We can log to a error level.")
    logger.critical("We can log to a critical level.")

    dpglogger = mvLogger()

    dpg.setup_dearpygui()

    dpg.show_viewport()
    def callback_log():
        """Pass messages from logging queue to dpg logger."""
        if not log_queue.empty():
            log_copy = log_queue.get()
            dpglogger._log(log_copy.message, log_copy.levelno)

    while dpg.is_dearpygui_running():
        callback_log()
        dpg.render_dearpygui_frame()

    dpg.destroy_context()
