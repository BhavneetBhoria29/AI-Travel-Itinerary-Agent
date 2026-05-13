import logfire
from langchain_tavily import TavilySearch
from src.config.config import TAVILY_API_KEY

def get_tavily_context(query: str, max_results: int = 3):
    """
    A standardized helper to fetch travel research from Tavily.
    This is used to build the evaluation 'Gold Standard' with ground-truth evidence.
    """
    with logfire.span("Tavily Search: {query}", query=query):
        try:
            # Set max_results during instantiation as required by this version
            tavily = TavilySearch(
                tavily_api_key=TAVILY_API_KEY,
                max_results=max_results
            )
            # Invoke with just the query
            raw_results = tavily.invoke({"query": query})
            
            # 🚀 TOKENS OPTIMIZATION: Truncate large content blocks to stay under TPM limits
            if isinstance(raw_results, dict) and "results" in raw_results:
                for res in raw_results["results"]:
                    if "content" in res and res["content"]:
                        # 800 chars is usually enough for key travel facts without wasting tokens
                        res["content"] = res["content"][:800] + " [TRUNCATED]"
            
            return raw_results
        except Exception as e:
            logfire.error("Tavily helper failed", error=str(e))
            return f"Error fetching search results: {str(e)}"