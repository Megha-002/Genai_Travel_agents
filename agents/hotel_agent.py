from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from graph.state import TravelState
from tools.tavily_search import tavily_search

from dotenv import load_dotenv
import os
import json

load_dotenv()


llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant"
)


def hotel_finder_agent(state: TravelState):

    destination = state["destination"]
    budget = state["budget"]
    check_in = state["check_in"]
    check_out = state["check_out"]

    # Search hotels using Tavily
    hotel_results = tavily_search(
        f"""
        Best hotels in {destination}
        under ${budget} per night
        between {check_in} and {check_out}

        Include hotel prices, ratings, and booking links.
        """
    )

    # LLM prompt to structure hotel data
    prompt = f"""
    You are a hotel data extraction assistant.

    Extract hotels from the search results.

    Return ONLY valid JSON list format.

    Each hotel must contain:
    - name
    - price
    - rating
    - link

    Example:

    [
        {{
            "name": "Hotel Paradise",
            "price": 120,
            "rating": 4.5,
            "link": "https://example.com"
        }}
    ]

    SEARCH RESULTS:
    {hotel_results}
    """

    response = llm.invoke(
        [HumanMessage(content=prompt)]
    )

    # Convert JSON string to Python list
    try:
        hotels = json.loads(response.content)
    except Exception:
        hotels = []

    # Save hotels into state
    state["hotels_found"] = hotels

    return state