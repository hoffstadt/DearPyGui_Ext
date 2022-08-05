import dearpygui.dearpygui as dpg
from typing import List, Any


class SimpleTable:
    def __init__(self, rows: int, columns: int):
        self.rows = rows
        self.columns = columns

        with dpg.table() as table:
            for _ in range(self.columns):
                dpg.add_table_column()

            for i in range(self.rows):
                with dpg.table_row():
                    for j in range(self.columns):
                        dpg.add_text("")

        self.id = table

    def get_data(self) -> List[List[str]]:
        return [[dpg.get_value(cell) for cell in dpg.get_item_children(row, 1)] for row in dpg.get_item_children(self.id, 1)]

    def get_item_cell(self, x: int, y: int) -> str:
        row = dpg.get_item_children(self.id, 1)[y]
        cell = dpg.get_item_children(row, 1)[x]
        return dpg.get_value(cell)

    def get_item_row(self, row: int) -> List[str]:
        row = dpg.get_item_children(self.id, 1)[row]
        return [dpg.get_value(i) for i in dpg.get_item_children(row, 1)]

    def get_item_column(self, column: int) -> List[str]:
        return [dpg.get_value(dpg.get_item_children(row, 1)[column]) for row in dpg.get_item_children(self.id, 1)]

    def set_data(self, data: List[List[Any]]) -> None:
        with dpg.mutex():
            # set new data
            for row, items in zip(dpg.get_item_children(self.id, 1), data):
                for cell, value in zip(dpg.get_item_children(row, 1), items):
                    dpg.set_value(cell, value)

    def set_item_cell(self, data: Any, x: int, y: int) -> None:
        with dpg.mutex():
            row = dpg.get_item_children(self.id, 1)[y]
            cell = dpg.get_item_children(row, 1)[x]
            dpg.set_value(cell, data)

    def set_item_row(self, data: List[Any], index: int) -> None:
        with dpg.mutex():
            row = dpg.get_item_children(self.id, 1)[index]
            for cell, value in zip(dpg.get_item_children(row, 1), data):
                dpg.set_value(cell, value)

    def set_item_column(self, data: List[Any], index: int) -> None:
        with dpg.mutex():
            cells = [dpg.get_item_children(row, 1)[index] for row in dpg.get_item_children(self.id, 1)]
            for cell, value in zip(cells, data):
                dpg.set_value(cell, value)

    def add_row(self, index: int) -> None:
        with dpg.table_row(parent=self.id, before=dpg.get_item_children(self.id, 1)[index]):
            for _ in range(self.columns):
                dpg.add_text("")
        self.rows += 1

    # TODO
    #  def add_column(self, index: int) -> None:

    def remove_row(self, index: int) -> None:
        dpg.delete_item(dpg.get_item_children(self.id, 1)[index])

    # TODO
    #  def remove_column(self, index: int) -> None:
