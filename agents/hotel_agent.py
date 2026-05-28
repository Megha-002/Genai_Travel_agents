from typing import List
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from graph.state import TravelState
from tools.tavily_search import tavily_search

from dotenv import load_dotenv
import os

load_dotenv()

# 1. Define the desired output structure using Pydantic
class Hotel(BaseModel):
    name: str = Field(description="The name of the hotel")
    price: float = Field(description="The price per night, numeric value only")
    rating: float = Field(description="The hotel rating out of 5 stars, numeric value only")
    link: str = Field(description="The booking URL or link for the hotel")

class HotelList(BaseModel):
    hotels: List[Hotel] = Field(description="A list of extracted hotels matching the criteria")


# 2. Initialize the LLM and bind the structure
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant",
    temperature=0  # Lower temperature guarantees higher adherence to structure
)

# This forces the model to strictly follow your Pydantic model structure
structured_llm = llm.with_structured_output(HotelList)


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

    # Simplified LLM prompt (No need to give markdown examples anymore!)
    prompt = f"""
    You are a hotel data extraction assistant.
    Extract all relevant hotels from the search results based on the schema requested.

    SEARCH RESULTS:
    {hotel_results}
    """

    # 3. Invoke the structured LLM
    try:
        response = structured_llm.invoke([HumanMessage(content=prompt)])
        
        # Convert the Pydantic object to a standard Python list of dictionaries
        state["hotels_found"] = [
            hotel.model_dump()
            for hotel in response.hotels
        ]

        # --- SIMULATE AVAILABILITY INJECTOR ---
        trip_dates = []

        current_date = datetime.strptime(
            check_in,
            "%Y-%m-%d"
        )

        end_date = datetime.strptime(
            check_out,
            "%Y-%m-%d"
        )

        while current_date < end_date:
            trip_dates.append(
                current_date.strftime("%Y-%m-%d")
            )
            current_date += timedelta(days=1)

        for hotel in state["hotels_found"]:
            hotel["available_dates"] = trip_dates
        # --------------------------------------
        
    except Exception as e:
        print(f"Extraction failed: {e}")
        state["hotels_found"] = []

    return state