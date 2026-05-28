from graph.state import TravelState
from tools.availability_check import check_availability


def availability_checker_agent(state: TravelState):

    # Current retry count
    current_retry = state.get("retry_count", 0)

    # Inputs from state
    hotels_found = state.get("hotels_found", [])

    check_in = state.get("check_in")
    check_out = state.get("check_out")

    budget = state.get("budget", 0)

    # Filter hotels
    available_hotels = check_availability(
        hotels=hotels_found,
        check_in=check_in,
        check_out=check_out,
        max_budget=budget
    )

    # Retry logic
    new_retry_count = current_retry

    if not available_hotels:
        new_retry_count += 1

    # Auto-select best hotel
    selected_hotel = None

    if available_hotels:
        selected_hotel = available_hotels[0]

    # Return updates
    return {
        "available_hotels": available_hotels,
        "selected_hotel": selected_hotel,
        "retry_count": new_retry_count
    }