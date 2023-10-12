import random

import reflex as rx
from .state import State


class PowerTwoState(State):
    result: list[str] = [f"2 ** {i} = {2 ** i:,} ({len(str(2 ** i))} digits)" for i in range(1, 65)]


@rx.page(route="/pow2", title="2의 64제곱까지 출력해주는 페이지")
def power_two() -> rx.Component:
    return rx.container(
        rx.foreach(PowerTwoState.result, rx.text),
        rx.link(
            rx.button("홈"),
            href="/",
            color=f"rgb({random.randint(1, 255)}, {random.randint(1, 255)}, {random.randint(1, 255)})",
            button=True,
        )
    )
