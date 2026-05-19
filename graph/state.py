from typing import TypedDict, List, Dict, Optional


class TravelState(TypedDict):

    # User inputs
    destination: str
    check_in: str
    check_out: str
    budget: int

    # Search results
    search_results: str

    # Destination Research Summary
    destination_info: str

    # Hotels
    hotels_found: List[Dict]

    # Available hotels after filtering
    available_hotels: List[Dict]

    # Final selected hotel
    selected_hotel: Optional[Dict]

    # Final itinerary/response
    final_itinerary: str

    # Errors or status
    error: Optional[str]