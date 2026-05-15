import asyncio

def create_session(session_service, session_id: str, user_id: str = "streamlit_user") -> None:
    """Create a new session in the given session service (async API)."""
    async def _create():
        await session_service.create_session(
            app_name="tokoku_assistant",
            user_id=user_id,
            session_id=session_id,
        )

    try:
        asyncio.run(_create())
    except Exception as e:
        print(f"Warning: Failed to create session {session_id}: {e}")


def clear_session(session_service, session_id: str, user_id: str = "streamlit_user") -> None:
    """Clear a specific session from the given session service (async API)."""
    async def _delete():
        await session_service.delete_session(
            app_name="tokoku_assistant",
            user_id=user_id,
            session_id=session_id,
        )

    try:
        asyncio.run(_delete())
    except Exception as e:
        print(f"Warning: Failed to clear session {session_id}: {e}")

