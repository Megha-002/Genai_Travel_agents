from typing import List, Optional
from datetime import datetime, timedelta

from pydantic import BaseModel, Field

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from graph.state import TravelState
from tools.tavily_search import tavily_search

from dotenv import load_dotenv
import os


load_dotenv()


# -------------------------------
# Structured Output Models
# -------------------------------

class Hotel(BaseModel):

    name: str = Field(
        description="The name of the hotel"
    )

    price: Optional[float] = Field(
        default=None,
        description="Hotel price per night"
    )

    rating: Optional[float] = Field(
        default=None,
        description="Hotel rating out of 5"
    )

    link: str = Field(
        description="Booking URL"
    )


class HotelList(BaseModel):

    hotels: List[Hotel] = Field(
        description="List of extracted hotels"
    )


# -------------------------------
# LLM Setup
# -------------------------------

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.1-8b-instant",
    temperature=0
)

structured_llm = llm.with_structured_output(
    HotelList
)


# -------------------------------
# Agent
# -------------------------------

def hotel_finder_agent(state: TravelState):

    destination = state["destination"]
    budget = state["budget"]

    check_in = state["check_in"]
    check_out = state["check_out"]

    print("\n========== HOTEL FINDER ==========")

    try:

        # ----------------------------------
        # Tavily Search
        # ----------------------------------

        hotel_results = tavily_search(
            f"""
            Best hotels in {destination}
            under ${budget} per night
            between {check_in} and {check_out}

            Include:
            - hotel names
            - prices
            - ratings
            - booking links
            """
        )

        # ----------------------------------
        # LLM Extraction
        # ----------------------------------

        prompt = f"""
        You are a hotel extraction assistant.

        Extract hotel information from the search results.

        IMPORTANT RULES:

        - Never return null values.
        - If price is unavailable use 99999.
        - If rating is unavailable use 0.
        - Price must always be numeric.
        - Rating must always be numeric.
        - Include booking link whenever available.

        SEARCH RESULTS:

        {hotel_results}
        """

        response = structured_llm.invoke(
            [HumanMessage(content=prompt)]
        )

        hotels_found = []

        for hotel in response.hotels:

            hotel_dict = hotel.model_dump()

            # -----------------------------
            # Defensive Cleanup
            # -----------------------------

            hotel_dict["price"] = (
                hotel_dict["price"]
                if hotel_dict["price"] is not None
                else 99999
            )

            hotel_dict["rating"] = (
                hotel_dict["rating"]
                if hotel_dict["rating"] is not None
                else 0
            )

            hotels_found.append(
                hotel_dict
            )

        # ----------------------------------
        # Simulate Availability
        # ----------------------------------

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
                current_date.strftime(
                    "%Y-%m-%d"
                )
            )

            current_date += timedelta(days=1)

        for hotel in hotels_found:

            hotel["available_dates"] = trip_dates

        state["hotels_found"] = hotels_found

        print(
            f"Hotels Extracted: {len(hotels_found)}"
        )

        for hotel in hotels_found:

            print(
                f"{hotel['name']} | "
                f"${hotel['price']} | "
                f"⭐ {hotel['rating']}"
            )

    except Exception as e:

        print(
            f"\nHotel Extraction Failed: {e}"
        )

        state["hotels_found"] = []

    return state