"""UI."""

from datetime import datetime

from fasthtml.common import A, Div, Form, Li, Title, Ul, fast_app, serve
from fhdaisy import (
    Btn,
    Chat,
    ChatBubble,
    ChatFooter,
    ChatHeader,
    Drawer,
    DrawerContent,
    DrawerOverlay,
    DrawerSide,
    DrawerToggle,
    Footer,
    Input,
    Label,
    Loading,
    Navbar,
    NavbarEnd,
    NavbarStart,
    daisy_hdrs,
)
from poor_mans_agent import Agent

from poor_mans_ui.config import get_config
from poor_mans_ui.constants import (
    APP_FOOTER_LINK,
    APP_FOOTER_TITLE,
    APP_INPUT_BOX_PLACEHOLDER,
    APP_TITLE,
)
from poor_mans_ui.database import ChatSchema
from poor_mans_ui.logger import get_logger

config = get_config()
logger = get_logger(__name__, level=config.log_level)
agent = Agent()

app, rt = fast_app(
    pico=False,
    hdrs=daisy_hdrs,
    htmlkw={"data-theme": config.theme},
)


def _make_chat(msg: str, role: str) -> Chat:
    now = datetime.now().isoformat(timespec="seconds")  # noqa: DTZ005
    # messages.insert(Message(chat_id=1, role=role, content=msg, timestamp=now))

    return Chat(
        ChatHeader(role.upper()),
        ChatBubble(msg, cls="-primary" if role == "user" else "-secondary"),
        ChatFooter(now),
        cls="-start" if role == "user" else "-end",
    )


def navbar() -> Navbar:  # noqa: D103
    return Navbar(
        NavbarStart(Btn(APP_TITLE, cls="btn-ghost text-xl font-bold")),
        NavbarEnd(Label("☰", fr="drawer", cls="btn btn-ghost")),
        cls="bg-base-200 shadow-sm",
    )


def sidebar() -> DrawerSide:  # noqa: D103
    return DrawerSide(
        DrawerOverlay(fr="drawer"),
        Ul(
            [Li(A(c.title, href=f"/chat/{c.id}")) for c in [ChatSchema(title="Hello, world")]],
            cls="menu bg-base-200 min-h-full w-80 p-4",
        ),
    )


def chat_area() -> Div:  # noqa: D103 # ty: ignore[invalid-type-form]
    return Div(
        id="chatturns",
        cls="flex flex-1 flex-col gap-4 p-4 overflow-y-auto",
    )


def input_bar() -> Form:  # noqa: D103 # ty: ignore[invalid-type-form]
    return Form(
        Div(
            Input(
                name="msg",
                placeholder=APP_INPUT_BOX_PLACEHOLDER,
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
            cls="flex gap-2 p-4 w-full p-8",
        ),
        hx_post="/send",
        hx_target="#chatturns",
        hx_swap="beforeend show:bottom",
        hx_on__after_request="this.reset()",
    )


def footer() -> Footer:  # noqa: D103 # ty: ignore[invalid-type-form]
    return Footer(
        A(
            APP_FOOTER_TITLE,
            href=APP_FOOTER_LINK,
        ),
        cls="bg-base-300 p-2 footer-center",
    )


@rt("/send")
def send_message(msg: str):
    """Send chat message."""
    if msg:
        return (
            _make_chat(msg, role="user"),
            Chat(
                ChatHeader("AI"),
                ChatBubble(Loading(cls="-dots"), cls="-secondary"),
                cls="-end",
                hx_get=f"/agent?msg={msg}",
                hx_trigger="load",
                hx_swap="outerHTML",
                hx_request={"timeout": config.timeout},
            ),
        )


@rt("/agent")
def call_agent(msg: str):
    """Call Poor Man's Agent."""
    logger.debug("Calling agent")
    try:
        response = agent.run(msg)
    except Exception as err:  # noqa: BLE001
        logger.error("Could not run agent: %s", err)
        response = "The agent hit a wall, please try again."

    return _make_chat(msg=response, role="ai")  # ty: ignore[invalid-argument-type]


@rt("/clear")
def clear_messages():
    """Clear chat message area."""
    return ""


@rt("/")
def get():
    """Load UI."""
    return (
        (
            Title(APP_TITLE),
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
