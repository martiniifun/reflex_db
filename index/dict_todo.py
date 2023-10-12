import reflex as rx
from .state import State


class DictTodoState(State):
    item_dict: dict[int, str] = {0: "aa", 1: "bb", 2: "cc"}

    @rx.var
    def max_key(self):
        if len(self.item_dict):
            return max(self.item_dict.keys())
        else:
            return 0

    @rx.var
    def items(self) -> list[tuple[int, str]]:
        return list(self.item_dict.items())

    def append_dict(self, i):
        self.item_dict[self.max_key+1] = i["input_todo"]
        return rx.set_value("input_todo", "")

    def delete_item(self, item):
        self.item_dict.pop(item[0])

    def update_item(self, item):
        self.item_dict[item[0]] = item[1]


def render_fn(item: tuple[int, str]) -> rx.Component:
    return rx.hstack(
        render_editable(item),  # val
        rx.button("x", on_click=lambda: DictTodoState.delete_item(item))
    )

def render_editable(item: tuple[int, str]) -> rx.Component:
    return rx.tooltip(
        rx.editable(
            rx.editable_preview(py=2, px=4, _hover={"background": "green.100"}),
            rx.editable_input(),
            placeholder=DictTodoState.item_dict[item[0]],
            on_submit=lambda val: DictTodoState.update_item(item)
        ),
        label="Click to edit", should_wrap_children=True)


@rx.page(route="dict_todo", title="dict로 구현한 투두리스트 CRUD")
def dict_todo() -> rx.Component:
    return rx.container(
        rx.heading("Todo list"),
        rx.foreach(DictTodoState.items, render_fn),
        rx.form(
            rx.input(placeholder=" + 할 일을 입력하세요.",
                     id="input_todo"),
            on_submit=DictTodoState.append_dict
        )
    )
