from dotenv import load_dotenv
import os

from langchain_tavily import TavilySearch

# Load environment variables
load_dotenv()

# Initialize Tavily tool
search_tool = TavilySearch(
    api_key=os.getenv("TAVILY_API_KEY"),
    max_results=5
)

# Search function
def tavily_search(query: str):
    results = search_tool.invoke(query)
    return results

# Test
if __name__ == "__main__":
    response = tavily_search("Best places to visit in India")

    print("\nSearch Results:\n")
    print(response)