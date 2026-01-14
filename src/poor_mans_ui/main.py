"""UI."""

from fasthtml.common import (
    H1,
    H2,
    A,
    Button,
    Div,
    FastHTML,
    Form,
    Input,
    Label,
    Li,
    Link,
    P,
    Script,
    Ul,
    serve,
)

from poor_mans_ui.version import __version__

daisyui_headers = (
    Link(href="https://cdn.jsdelivr.net/npm/daisyui@5", rel="stylesheet", type="text/css"),
    Script(src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"),
)

app = FastHTML(
    hdrs=daisyui_headers,
)
route = app.route


# Dummy storage, replace with DB
chat_store = {
    "1": [("user", "Hello, world!"), ("assistant", "Howdy, how can I help you?")],
    "2": [("user", "What's the weather?"), ("assistant", "I don't have access to weather data.")],
    "3": [],
}
current_chat_id = None


def create_chat_bubble(role, text):
    """Create a DaisyUI chat bubble."""
    align_cls = "chat-start" if role == "user" else "chat-end"
    bubble_cls = (
        "chat-bubble chat-bubble-secondary"
        if role == "assistant"
        else "chat-bubble chat-bubble-primary"
    )
    return Div(
        Div(role.title(), cls="chat-header text-sm opacity-70"),
        Div(text, cls=bubble_cls),
        cls=f"chat {align_cls}",
    )


def chat_input(oob=False):
    """Create chat input field with optional OOB swap."""
    return Input(
        name="message",
        id="chat-input",
        placeholder="Ask me anything...",
        cls="input input-bordered input-primary flex-1 shadow-sm",
        hx_swap_oob="true" if oob else None,
    )


def get_chat_panel(messages: list[dict]):
    """Get chat area with messages and input."""
    if messages:
        bubbles = [create_chat_bubble(role, text) for role, text in messages]
    else:
        # TODO: Improve styling
        bubbles = Div(P("Let start a new conversation"))

    return Div(
        Div(
            # Chat messages area
            Div(
                *bubbles,
                id="messages",
                cls="flex flex-col gap-4 p-6 bg-base-200 rounded-box flex-1 overflow-y-auto",
            ),
            # Input form
            Form(
                Div(
                    chat_input(),
                    Button(
                        "Send",
                        type="submit",
                        cls="btn btn-primary shadow-md hover:shadow-lg transition-shadow",
                    ),
                    Button("Clear", type="submit", cls="btn btn-secondary"),
                    cls="flex gap-3 items-center",
                ),
                hx_post="/send-message",
                hx_target="#messages",
                hx_swap="beforeend",
                cls="p-4 bg-base-200 rounded-box shadow-md",
            ),
            cls="flex flex-col gap-4 h-full",
        ),
        cls="p-4 flex-1 bg-base-100",
    )


def get_sidebar(chat_history):
    """Get sidebar for chat history."""
    chat_links = [
        Li(
            A(
                f"Chat {chat_id}",
                hx_get=f"/chat/{chat_id}",
                hx_target="#chat-content",
                hx_swap="innerHTML",
            )
        )
        for chat_id in chat_history
    ]
    return Div(
        Label(fr="my-drawer", cls="drawer-overlay"),
        Ul(
            Li(H2("Chat history", cls="menu-title text-lg px-4 py-2")),
            *chat_links,
            cls="menu bg-base-200 text-base-content min-h-full w-80 p-4",
        ),
        cls="drawer-side",
    )


def get_header():
    """Get header."""
    return Div(
        Label(
            "☰",
            fr="my-drawer",
            cls="btn btn-ghost btn-circle drawer-button text-2xl",
        ),
        H1(
            "Poor Man's Agent",
            cls="text-2xl flex-1 text-center",
        ),
        cls="navbar bg-base-300 shadow-lg",
    )


def get_footer():
    """Get footer."""
    return Div(
        P(f"Powered by poor man's UI (version {__version__}).", cls="text-center text-sm"),
        cls="footer footer-center p-4 bg-base-300 text-base-content",
    )


def chat(message: str) -> str:
    """Dummy chat function."""
    return f"Mirror: {message}"


@route("/chat/{chat_id}")
def get_chat(chat_id: str):
    """Load a specific chat."""
    global current_chat_id
    current_chat_id = chat_id
    messages = chat_store.get(chat_id, [])
    return get_chat_panel(messages)


@route("/send-message")
def post(message: str):
    """Handle chat message submission."""
    global current_chat_id

    # Store message in current chat
    if current_chat_id:
        chat_store.setdefault(current_chat_id, []).append(("user", message))
        response = chat(message)
        chat_store[current_chat_id].append(("assistant", response))

    user_bubble = create_chat_bubble("user", message)
    response = chat(message)
    assistant_bubble = create_chat_bubble("assistant", response)
    # Return bubbles to append to chat + cleared input via OOB
    return user_bubble, assistant_bubble, chat_input(oob=True)


@route("/")
def get():
    """Main page layout with DaisyUI drawer sidebar."""
    return Div(
        Input(id="my-drawer", type="checkbox", cls="drawer-toggle"),
        Div(
            get_header(),
            Div(
                get_chat_panel(messages=[]),
                id="chat-content",
            ),
            get_footer(),
            cls="drawer-content flex flex-col h-screen",
        ),
        get_sidebar(chat_history=list(chat_store.keys())),
        cls="drawer",
    )


serve()
