from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
from src.tools.tavily_tool import tavily_search_tool
from src.tools.serper_tool import google_serper_search_tool
from src.utils.logger import get_logger

logger = get_logger(__name__)

llm = ChatAnthropic(
    model_name="claude-sonnet-4-6",
    temperature=0.3,
    timeout=None,
    stop=None
)


SYSTEM_PROMPT = """
You are an expert AI travel planner.

Rules:
- Always use web search tools for real-world accuracy
- Create a detailed day-wise itinerary
- Include food suggestions, local tips, and travel advice

User Inputs:
City, Number of days, Interests, Travel style, Pace
"""

agent = create_react_agent(
    model=llm,
    tools=[tavily_search_tool, google_serper_search_tool],
    prompt=SYSTEM_PROMPT.strip()
)

logger.info("AGENT CREATED")
