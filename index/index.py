"""
페이지함수는 (여기서 쓰지 않더라도) 꼭 임포트를 해야만 한다. 그래야 인식한다.
실제로 인덱스 코드 내에서는 쓰지 않더라도 말이다.
대신 서브페이지의 State인 GuguState, TodoState 등은 임포트하지 않아도 된다.
"""

import random

import reflex as rx

from .state import State
from .gugu import gugu
from .pow2 import power_two
from .todo import todo
from .dict_todo import dict_todo
from .list_todo import list_todo


def index() -> rx.Component:
    return rx.vstack(
        rx.heading("앱 목록"),
        rx.link(
            rx.button("구구단"),
            href="/gugu",
            color=f"rgb({random.randint(1, 255)}, {random.randint(1, 255)}, {random.randint(1, 255)})",
            button=True,
        ),
        rx.link(
            rx.button("2의 n승"),
            href="/pow2",
            color=f"rgb({random.randint(1, 255)}, {random.randint(1, 255)}, {random.randint(1, 255)})",
            button=True,
        ),
        rx.link(
            rx.button("todo with Azure SQL"),
            href="/todo",
            color=f"rgb({random.randint(1, 255)}, {random.randint(1, 255)}, {random.randint(1, 255)})",
            button=True,
        ),
    )


app = rx.App(state=State)
app.add_page(index)
app.compile()
