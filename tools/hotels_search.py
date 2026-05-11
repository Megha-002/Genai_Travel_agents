from dotenv import load_dotenv
import os
import json

from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch

# Load environment variables
load_dotenv()

# Initialize Groq LLM
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant"
)

# Initialize Tavily Search
search_tool = TavilySearch(
    api_key=os.getenv("TAVILY_API_KEY"),
    max_results=5
)

def search_hotels(destination: str, budget: int):

    # Search query
    query = f"best hotels in {destination} under ${budget}"

    # Get raw search results
    search_results = search_tool.invoke(query)

    # Prompt for LLM
    prompt = f"""
    You are a hotel data extraction assistant.

    Extract hotel information from the search results below.

    Return ONLY valid JSON.

    Format:
    [
        {{
            "name": "",
            "price": "",
            "rating": "",
            "location": ""
        }}
    ]

    Search Results:
    {search_results}
    """

    # Get LLM response
    response = llm.invoke(prompt)

    # Print raw response
    print("\nLLM RAW RESPONSE:\n")
    print(response.content)

    # Convert JSON string to Python list
    try:
        hotels = json.loads(response.content)

        print("\nPARSED HOTELS:\n")

        for hotel in hotels:
            print(hotel)

        return hotels

    except Exception as e:
        print("\nJSON Parsing Error:\n", e)
        return []


# Test
if __name__ == "__main__":

    search_hotels(
        destination="India",
        budget=150
    )