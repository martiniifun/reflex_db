import reflex as rx
from .state import State


class ListTodoState(State):
    item: tuple[int, str]
    item_list: list[str] = ["aa", "bb", "cc"]

    @rx.var
    def enum_list(self) -> list[tuple[int, str]]:
        return [(i, j) for i, j in enumerate(self.item_list)]

    def append_list(self, i):
        self.item_list.append(i["input_todo"])
        return rx.set_value("input_todo", "")

    def delete_item(self, item):
        self.item_list.pop(item[0])

    def update_item(self, item):
        self.item_list[item[0]] = item[1]


def render_fn(item: tuple[int, str]) -> rx.Component:
    return rx.hstack(
        render_editable(item),  # val
        rx.button("x", on_click=lambda: ListTodoState.delete_item(item))
    )

def render_editable(item: tuple[int, str]) -> rx.Component:
    return rx.tooltip(
        rx.editable(
            rx.editable_preview(py=2, px=4, _hover={"background": "green.100"}),
            rx.editable_input(),
            placeholder=ListTodoState.item_list[item[0]],
            on_submit=lambda val: ListTodoState.update_item(item)
        ),
        label="Click to edit", should_wrap_children=True)


@rx.page(route="list_todo", title="list로 구현한 투두리스트 CRUD")
def list_todo() -> rx.Component:
    return rx.container(
        rx.heading("Todo list"),
        rx.foreach(ListTodoState.enum_list, render_fn),
        rx.form(
            rx.input(placeholder=" + 할 일을 입력하세요.",
                     id="input_todo"),
            on_submit=ListTodoState.append_list
        )
    )
