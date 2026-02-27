"""UI."""

from fasthtml.common import *
from fhdaisy import *
from fhdaisy.xtras import ChatTurn

app, rt = fast_app(pico=False, hdrs=daisy_hdrs, htmlkw={"data-theme": "light"})


def navbar() -> Navbar:
    return Navbar(
        NavbarStart(Btn("Poor Man's UI", cls="btn-ghost text-xl font-bold")),
        NavbarEnd(Label("☰", fr="drawer", cls="btn btn-ghost")),
        cls="bg-base-200 shadow-sm",
    )


def sidebar() -> DrawerSide:
    return DrawerSide(
        DrawerOverlay(fr="drawer"),
        Ul(Li(A("Chat 1")), Li(A("Chat 2")), cls="menu bg-base-200 min-h-full w-80 p-4"),
    )


def chat_area() -> Div:
    return Div(
        ChatTurn("Hello", cls="-start", bubblecls="-primary"),
        ChatTurn("World!", cls="-end", bubblecls="-secondary"),
        ChatTurn("What's", cls="-start", bubblecls="-primary"),
        ChatTurn("up?", cls="-end", bubblecls="-secondary"),
        id="chatturns",
        cls="flex flex-1 flex-col gap-4 p-4 overflow-y-auto",
    )


def input_bar() -> Form:
    return Form(
        Join(
            Input(
                name="message",
                placeholder="Any poor thoughts on your mind?",
                cls="w-full",
            ),
            Btn("Send", cls="-primary"),
            Btn(
                "Clear",
                cls="-accent",
                hx_target="#chatturns",
                hx_swap="innerHTML",
                hx_post="/clear",
            ),
            cls="w-full p-8",
        ),
        hx_post="/send",
        hx_target="#chatturns",
        hx_swap="beforeend show:bottom",
        hx_on__after_request="this.reset()",
    )


def footer() -> Footer:
    return Footer("An UI to chat with Poor Man's agent", cls="bg-base-300 p-2 footer-center")


@rt("/send")
def chat(message: str):
    if message:
        return ChatTurn(message, cls="-start", bubblecls="-primary"), ChatTurn(
            f"Mirror: {message}", cls="-end", bubblecls="-secondary"
        )


@rt("/clear")
def clear():
    return ""


@rt("/")
def get():
    return (
        (
            Title("Poor Man's UI"),
            Drawer(
                DrawerToggle(id="drawer"),
                DrawerContent(
                    navbar(), chat_area(), input_bar(), footer(), cls="flex flex-col flex-1"
                ),
                sidebar(),
                cls="flex flex-col min-h-screen",
            ),
        ),
    )


serve()
