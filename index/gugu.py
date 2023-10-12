import reflex as rx
import random
from .state import State


class GuguState(State):
    num: str = "1"

    @rx.var
    def gugu(self) -> list[str]:
        if self.num.isdecimal():
            return [f"{int(self.num)} X {i} = {int(self.num) * i}" for i in range(1, 10)]
        else:
            return [f"{0} X {i} = {0}" for i in range(1, 10)]


@rx.page(route="gugu", title="구구단", description="구구단을 자동으로 계산해주는 웹앱")
def gugu() -> rx.Component:
    return rx.vstack(
        rx.foreach(GuguState.gugu, rx.text),
        rx.input(value=GuguState.num, on_change=GuguState.set_num),
        rx.link(
            rx.button("홈"),
            href="/",
            color=f"rgb({random.randint(1, 255)}, {random.randint(1, 255)}, {random.randint(1, 255)})",
            button=True,
        ),
    )
