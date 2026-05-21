from graph.state import TravelState
from tools.availability_check import check_availability


def availability_checker_agent(state: TravelState):

    hotels_found = state["hotels_found"]

    check_in = state["check_in"]
    check_out = state["check_out"]

    budget = state["budget"]

    # Filter available hotels
    available_hotels = check_availability(
        hotels=hotels_found,
        check_in=check_in,
        check_out=check_out,
        max_budget=budget
    )

    # Save filtered hotels
    state["available_hotels"] = available_hotels

    # Retry handling
    if not available_hotels:
        state["retry_count"] += 1

    return state