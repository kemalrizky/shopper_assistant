from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from src.agent.agent import tokoku_agent

# Shared session service singleton
session_service = InMemorySessionService()

def build_runner() -> Runner:
    """Build and return the Runner for the Tokoku agent."""
    return Runner(
        agent=tokoku_agent,
        session_service=session_service,
        app_name="tokoku_assistant",
        auto_create_session=True
    )
