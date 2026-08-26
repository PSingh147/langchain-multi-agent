
import os

from langchain.tools import Tool, tool
from langchain_tavily import TavilySearch

from dotenv import load_dotenv
from tavily import TavilyClient

from bs4 import BeautifulSoup
import requests
from readability import Document


load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def tavily_search(query: str) -> str:
    """
    A tool that uses Tavily to search for information.
    """
    search_results = tavily_client.search(query, max_results=5)

    out =[]

    if search_results:
        for result in search_results:
            out.append(
                f"Title: {result['title']}\nURL: {result['url']}\nSnippet: {result['content'][:300]}\n")
        return "------\n".join(out)
    else:
        return "No results found."



@tool
def readable_text(url: str) -> str:
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    doc = Document(response.content)
    soup = BeautifulSoup(doc.summary(), "html.parser")
    return soup.get_text(separator="\n")

