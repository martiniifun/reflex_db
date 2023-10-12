import reflex as rx
from sqlmodel import Field, select
from datetime import datetime as dt

from .state import State


class Todo(rx.Model, table=True):
    id: int = Field(primary_key=True)
    item: str = Field(max_length=200, nullable=False)
    created_datetime: str = Field(max_length=30, nullable=False)
    updated_datetime: str = Field(max_length=30, nullable=False)
    ongoing: bool = Field(default=True, nullable=False)


class TodoState(State):
    item: str
    form_data: dict = {}
    items: list[Todo]

    def refresh_items(self):
        with rx.session() as sess:
            self.items = sess.query(Todo).filter_by(ongoing=True).all()

    def add_item(self, val: dict):
        self.item = val["item"]
        with rx.session() as sess:
            sess.add(Todo(item=self.item, created_datetime=dt.now().strftime("%Y-%m-%d-%H:%M:%S"),
                          updated_datetime=dt.now().strftime("%Y-%m-%d-%H:%M:%S"), ongoing=1))
            sess.commit()
        self.refresh_items()
        self.item = ""
        return rx.set_value("item", "")

    def complete_item(self, id: int):
        with rx.session() as sess:
            stmt = select(Todo).where(Todo.id == id)
            item = sess.exec(stmt).first()
            item.ongoing = False
            sess.add(item)
            sess.commit()
        self.refresh_items()

    def update_item(self, id: int, val: str):
        with rx.session() as sess:
            statement = select(Todo).where(Todo.id == id)
            target = sess.exec(statement).first()
            target.item = val
            target.updated_datetime = dt.now().strftime("%Y-%m-%d %H:%M:%S")
            sess.add(target)
            sess.commit()
        self.refresh_items()

    @rx.var
    def get_today(self) -> str:
        weekdays = "월화수목금토일"
        weekday = weekdays[dt.today().weekday()]
        curdate = dt.today().strftime(f"%#m월 %#d일 {weekday}요일")
        return curdate


def render_item(id, item):
    return rx.tooltip(
        rx.editable(
            rx.editable_preview(py=2, px=4, _hover={"background": "green.100"}),
            rx.editable_input(),
            placeholder=item,
            on_submit=lambda val: TodoState.update_item(id, val)
        ),
        label="Click to edit", should_wrap_children=True)


def render_fn(todo: Todo):
    return rx.tr(
        rx.td(render_item(todo.id, todo.item)),
        rx.td(todo.updated_datetime),
        rx.td(rx.button("X", on_click=lambda: TodoState.complete_item(todo.id), bg="white", color="red"))
    )


@rx.page(title="Azure SQL로 구현한 투두리스트 CRUD")
def todo():
    return rx.container(
        rx.heading("오늘 할 일"),
        rx.text(TodoState.get_today),
        rx.table_container(
            rx.table(
                rx.thead(
                    rx.tr(
                        rx.th("할 일"),
                        rx.th("생성일"),
                        rx.th("완료시 클릭")
                    )
                ),
                rx.tbody(
                    rx.foreach(TodoState.items, render_fn)
                )
            )
        ),
        rx.form(
            rx.input(placeholder="+ 작업 추가", id="item",
                     focus_border_color="green.500"),
            on_submit=TodoState.add_item,
            margin_top="0.5em",
        ),
        maxW="70%",
        on_mount=TodoState.refresh_items()
    )
