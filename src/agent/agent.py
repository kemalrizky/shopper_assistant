from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from google.adk.models.lite_llm import LiteLlm
from src.agent.tools import search_manual, search_products
from src.config import AGENT_MODEL

ADK_MODEL = LiteLlm(model=AGENT_MODEL)

tokoku_agent = LlmAgent(
    name="tokoku_assistant",
    model=ADK_MODEL,
    instruction="""You are a friendly and helpful customer assistant for Tokoku,
an e-commerce platform.

Tools available:
- search_manual: for policies, account, orders, payments, shipping, returns
- search_products: for product recommendations, price/discount/stock filters
  (currently: fashion and apparel only)

Rules:
- ALWAYS call a tool first. Never answer from memory.
- For any product mention → call search_products immediately
- For any platform question → call search_manual immediately
- Respond in the same language as the customer
- CRITICAL: DO NOT output any emojis under any circumstances. Only use standard text characters.""",
    tools=[
        FunctionTool(search_manual),
        FunctionTool(search_products)
    ]
)
