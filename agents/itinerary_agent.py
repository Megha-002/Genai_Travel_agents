from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from graph.state import TravelState

from dotenv import load_dotenv
import os

load_dotenv()


llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant"
)


def itinerary_builder_agent(state: TravelState):

    destination = state["destination"]

    check_in = state["check_in"]
    check_out = state["check_out"]

    destination_info = state["destination_info"]

    selected_hotel = state["selected_hotel"]

    prompt = f"""
    You are an expert travel planner.

    Create a detailed day-by-day travel itinerary.

    DESTINATION:
    {destination}

    TRAVEL DATES:
    Check-in: {check_in}
    Check-out: {check_out}

    HOTEL:
    {selected_hotel}

    DESTINATION INFORMATION:
    {destination_info}

    Instructions:
    - Create a day-by-day itinerary
    - Include morning, afternoon, and evening activities
    - Suggest famous attractions
    - Include food recommendations
    - Keep travel realistic and enjoyable
    - Make the itinerary clean and easy to read
    """

    response = llm.invoke(
        [HumanMessage(content=prompt)]
    )

    # Save itinerary into state
    state["final_itinerary"] = response.content

    return state