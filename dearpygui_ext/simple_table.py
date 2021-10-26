import dearpygui._dearpygui as internal_dpg
import dearpygui.dearpygui as dpg

# 0.6 functions
#   * add_column
#   * delete_column
#   * set_table_data
#   * get_table_data
#   * get_table_item
#   * set_table_item
#   * get_table_selections
#   * set_table_selections
#   * insert_column
#   * insert_row
#   * set_headers


class mvSimpleTable:

    def __init__(self, columns, data=None):

        self._table_id = dpg.generate_uuid()
        self._stage_id = dpg.generate_uuid()
        self._columns = columns
        self._rows = 0

        with dpg.theme() as self._theme_id:
            with dpg.theme_component(dpg.mvSelectable):
                dpg.add_theme_color(dpg.mvThemeCol_Header, (0, 119, 200, 153))
                dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (29, 151, 236, 103))

        self._selections = {}

        if data:
            self._rows = len(data)
            with dpg.mutex():



                with dpg.stage(tag=self._stage_id):

                    dpg.configure_app(skip_positional_args=True, skip_required_args=True)
                    for row_index in range(len(data)):
                        row = data[row_index]
                        internal_dpg.push_container_stack(internal_dpg.add_table_row())

                        for column in range(self._columns):
                            internal_dpg.add_selectable(label=str(row[column]),
                                                        user_data=[row_index, column, self],
                                                        callback=lambda s, a, u: u[2]._selection_toggle(s, a, u[0], u[1]))

                        internal_dpg.pop_container_stack()

                    dpg.configure_app(skip_positional_args=False, skip_required_args=False)

    def _selection_toggle(self, sender, value, row, column):
        self._selections[sender] = value

    def clear(self):
        dpg.delete_item(self._table_id, children_only=True, slot=1)
        self._rows = 0
        self._selections = {}

    def add_row(self, data):

        dpg.push_container_stack(self._table_id)
        internal_dpg.push_container_stack(internal_dpg.add_table_row())
        for i in range(len(data)):
            internal_dpg.add_selectable(label=str(data[i]),
                                        user_data=[self._rows, i, self],
                                        callback=lambda s, a, u: u[2]._selection_toggle(s, a, u[0], u[1]))

        dpg.pop_container_stack()
        dpg.pop_container_stack()
        self._rows += 1

    def delete_row(self, row):

        rows = dpg.get_item_children(self._table_id, slot=1)
        dpg.delete_item(rows[row])

    def submit(self):

        with dpg.group() as temporary_id:
            with dpg.table(header_row=True, no_host_extendX=True, delay_search=True,
                           borders_innerH=True, borders_outerH=True, borders_innerV=True,
                           borders_outerV=True, context_menu_in_body=True, row_background=True,
                           policy=dpg.mvTable_SizingFixedFit, height=-1,
                           scrollY=True, tag=self._table_id, clipper=True):

                for i in range(self._columns):
                    internal_dpg.add_table_column(label="Header " + str(i))

                dpg.unstage(self._stage_id)
                dpg.delete_item(self._stage_id)

        dpg.bind_item_theme(temporary_id, self._theme_id)
