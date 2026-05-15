import sys
import uuid
from pathlib import Path

# Force UTF-8 encoding for standard streams to prevent charmap errors on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# Ensure project root is in sys.path regardless of how Streamlit is invoked
_ROOT = Path(__file__).parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import streamlit as st
from google.genai import types

from src import config
from src.agent.runner import build_runner
from src.session import clear_session, create_session
from styles import get_css
from components import (
    render_sidebar,
    render_chat_history,
    render_user_bubble,
    _welcome_message,
)


def _init_state() -> None:
    if "runner" not in st.session_state:
        st.session_state.runner = build_runner()
    if "session_id" not in st.session_state:
        new_session_id = str(uuid.uuid4())
        st.session_state.session_id = new_session_id
        create_session(st.session_state.runner.session_service, new_session_id, user_id="streamlit_user")
    if "messages" not in st.session_state:
        st.session_state.messages = [_welcome_message()]


def _run_agent(question: str, session_id: str) -> str:
    """Run one agent turn. Returns final_answer."""
    final_answer = ""

    try:
        event_stream = st.session_state.runner.run(
            user_id="streamlit_user",
            session_id=session_id,
            new_message=types.Content(
                role="user",
                parts=[types.Part(text=question)],
            ),
        )

        for event in event_stream:
            # final answer from agent
            if hasattr(event, "is_final_response") and event.is_final_response():
                if hasattr(event, "content") and getattr(event.content, "parts", None):
                    final_answer = event.content.parts[0].text
                elif hasattr(event, "response") and hasattr(event.response, "text"):
                    final_answer = event.response.text
                elif hasattr(event, "text"):
                    final_answer = event.text
                
        if not final_answer:
            final_answer = "⚠️ **Oops! Server is busy (Rate Limit).**\n\nOur AI system is experiencing high traffic, or a connection error occurred. Please try again in a few moments."
                
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "RateLimit" in error_msg or "traffic" in error_msg.lower():
            final_answer = "⚠️ **Oops! Server is busy (Rate Limit).**\n\nOur AI system is experiencing high traffic. Please try again in a few moments."
        else:
            final_answer = f"⚠️ **An internal error occurred:**\n\n`{error_msg}`"

    return final_answer


def main() -> None:
    st.set_page_config(
        page_title=config.APP_TITLE,
        page_icon=config.APP_ICON,
        layout=config.APP_LAYOUT,
    )
    st.markdown(get_css(), unsafe_allow_html=True)

    _init_state()
    render_sidebar()
    render_chat_history()

    if question := st.chat_input("Ask me anything about Tokoku..."):
        # render and save user message immediately
        render_user_bubble(question)
        st.session_state.messages.append(
            {"role": "user", "content": question}
        )

        # run agent and render response
        with st.chat_message("assistant"):
            with st.spinner("Assistant is processing..."):
                final_answer = _run_agent(
                    question, st.session_state.session_id
                )

            # render final answer
            st.markdown(final_answer)

        # save to history for replay on rerender
        st.session_state.messages.append({
            "role": "assistant",
            "content": final_answer,
        })


if __name__ == "__main__":
    main()
