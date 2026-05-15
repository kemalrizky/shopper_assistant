import sys
import uuid
import asyncio
from pathlib import Path

# Ensure project root is in sys.path
_ROOT = Path(__file__).parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

# Fix Windows console encoding
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from google.genai import types
from src.agent.runner import build_runner, session_service

async def init_session(session_id, user_id):
    print("Creating session...")
    await session_service.create_session(
        app_name="tokoku_assistant",
        user_id=user_id,
        session_id=session_id
    )

def run_test():
    runner = build_runner()
    session_id = str(uuid.uuid4())
    user_id = "test_user"

    print("Creating session...")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(session_service.create_session(
        app_name="tokoku_assistant",
        user_id=user_id,
        session_id=session_id
    ))

    test_queries = [
        "Rekomendasikan jaket hangat untuk saya di bawah Rp 200.000",
        "Which one is the cheapest?",
        "Can I return it if it doesn't fit?"
    ]

    import time

    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"User : {query}")
        
        response = runner.run(
            user_id=user_id,
            session_id=session_id,
            new_message=types.Content(
                role="user",
                parts=[types.Part(text=query)]
            )
        )

        final_response = "No response received."
        for event in response:
            if hasattr(event, "is_tool_call") and event.is_tool_call():
                print(f"🔧 Tool Called: {event.tool_name}")
            elif hasattr(event, "is_final_response") and event.is_final_response():
                if event.content and event.content.parts:
                    final_response = event.content.parts[0].text
                    break
        
        print(f"\nAgent: {final_response}")
        print("\nWaiting 15 seconds to avoid rate limits...")
        time.sleep(15)

if __name__ == "__main__":
    run_test()
