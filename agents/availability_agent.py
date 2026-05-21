from graph.state import TravelState
from tools.availability_check import check_availability


def availability_checker_agent(state: TravelState):
    # Safely get the current retry count, defaulting to 0 if missing
    current_retry = state.get("retry_count", 0)
    
    # Extract required inputs from state
    hotels_found = state.get("hotels_found", [])
    check_in = state.get("check_in")
    check_out = state.get("check_out")
    budget = state.get("budget", 0)

    # Filter available hotels
    available_hotels = check_availability(
        hotels=hotels_found,
        check_in=check_in,
        check_out=check_out,
        max_budget=budget
    )

    # Determine the new retry count
    new_retry_count = current_retry
    if not available_hotels:
        new_retry_count += 1

    # Return the updates cleanly to LangGraph
    return {
        "available_hotels": available_hotels,
        "retry_count": new_retry_count
    }