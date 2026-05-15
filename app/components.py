import html
import uuid
import streamlit as st

from src import config
from src.session import clear_session, create_session


def render_sidebar() -> None:
    with st.sidebar:
        st.markdown(f"## {config.APP_TITLE}")
        st.caption("Powered by Tokoku Knowledge Base & Product Catalog")
        st.divider()

        if st.button("+ New Chat", type="primary", use_container_width=True):
            if "session_id" in st.session_state and "runner" in st.session_state:
                clear_session(st.session_state.runner.session_service, st.session_state.session_id)
            new_session_id = str(uuid.uuid4())
            st.session_state.session_id = new_session_id
            if "runner" in st.session_state:
                create_session(st.session_state.runner.session_service, new_session_id, user_id="streamlit_user")
            st.session_state.messages = [_welcome_message()]
            st.rerun()

        st.divider()

        st.markdown(
            "**I can help you with:**\n"
            "- Product recommendations\n"
            "- Price & discount filters\n"
            "- Stock availability\n"
            "- Orders & payments\n"
            "- Returns & refunds\n"
            "- Account & security"
        )


def render_chat_history() -> None:
    """Replay full chat history on each Streamlit rerender."""
    for msg in st.session_state.get("messages", []):
        if msg["role"] == "user":
            render_user_bubble(msg["content"])
        else:
            with st.chat_message("assistant"):
                st.markdown(msg["content"])


def render_user_bubble(content: str) -> None:
    safe = html.escape(content)
    st.markdown(
        f'<div class="user-row">'
        f'  <div class="user-bubble">{safe}</div>'
        f'  <div class="user-avatar">U</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def _welcome_message() -> dict:
    return {
        "role": "assistant",
        "content": config.APP_WELCOME,
    }


def _score_color(score: float) -> str:
    if score >= 0.6:
        return "#2D6A4F"
    elif score >= 0.4:
        return "#74C69D"
    return "#7A7A6E"
