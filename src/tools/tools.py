import requests
from dotenv import load_dotenv
import os
from tavily import TavilyClient
from rich import print
from langchain.tools import tool

load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def web_search(query: str) -> str:
    """
    Perform a web search using the Tavily API and return the results.
    """
    results = tavily_client.search(query)
    out=[]

    for r in results['results']:
        out.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
        )
    
    return "\n----\n".join(out)

    
