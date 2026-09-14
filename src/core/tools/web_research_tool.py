from dotenv import load_dotenv
load_dotenv()
from langchain_tavily import TavilyResearch
from langchain.tools import tool
import os

tavily_research = TavilyResearch(api_key=os.getenv("TAVILY_API_KEY"))

@tool("web_research", args_schema={"query": str})
def web_research(query: str) -> str:
    """Perform web research about a given query for medical purposes."""
    if not query:
        raise ValueError("Query cannot be empty.")
    
    result = tavily_research.invoke({"input": query})
    return str(result)