from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from graph.state import TravelState
from tools.tavily_search import tavily_search

from dotenv import load_dotenv
import os

load_dotenv()


llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant"
)


def destination_research_agent(state: TravelState):

    destination = state["destination"]
    check_in = state["check_in"]
    check_out = state["check_out"]

    # Search 1 - General destination info
    general_info = tavily_search(
        f"""
        Best travel information about {destination}
        for travelers visiting between
        {check_in} and {check_out}
        """
    )

    # Search 2 - Top attractions
    attractions_info = tavily_search(
        f"""
        Top tourist attractions and things to do in
        {destination}
        """
    )

    # Combine search results
    combined_info = f"""
    GENERAL INFORMATION:
    {general_info}

    TOP ATTRACTIONS:
    {attractions_info}
    """

    # LLM Summary
    prompt = f"""
    You are a travel expert.

    Create a clean travel summary for {destination}.

    Include:
    - Overview
    - Weather
    - Best attractions
    - Food
    - Travel tips

    Keep it concise and helpful.

    DATA:
    {combined_info}
    """

    response = llm.invoke(
        [HumanMessage(content=prompt)]
    )

    # Save into state
    state["destination_info"] = response.content

    return state