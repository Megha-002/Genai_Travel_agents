from langgraph.graph import StateGraph, END

from graph.state import TravelState

from agents.destination_agent import (
    destination_research_agent
)

from agents.hotel_agent import (
    hotel_finder_agent
)

from agents.availability_agent import (
    availability_checker_agent
)

from agents.itinerary_agent import (
    itinerary_builder_agent
)


# Create workflow graph
workflow = StateGraph(TravelState)


# ---------------- ADD NODES ---------------- #

workflow.add_node(
    "destination_researcher",
    destination_research_agent
)

workflow.add_node(
    "hotel_finder",
    hotel_finder_agent
)

workflow.add_node(
    "availability_checker",
    availability_checker_agent
)

workflow.add_node(
    "itinerary_builder",
    itinerary_builder_agent
)


# ---------------- ENTRY POINT ---------------- #

workflow.set_entry_point(
    "destination_researcher"
)


# ---------------- NORMAL FLOW ---------------- #

workflow.add_edge(
    "destination_researcher",
    "hotel_finder"
)

workflow.add_edge(
    "hotel_finder",
    "availability_checker"
)


# ---------------- ROUTER ---------------- #

def availability_router(state: TravelState):

    available_hotels = state.get(
        "available_hotels",
        []
    )

    retry_count = state.get(
        "retry_count",
        0
    )

    # Hotels found
    if available_hotels:
        return "itinerary_builder"

    # Retry hotel search
    if retry_count < 3:
        return "hotel_finder"

    # Stop workflow
    return END


# ---------------- CONDITIONAL EDGES ---------------- #

workflow.add_conditional_edges(
    "availability_checker",
    availability_router,
    {
        "hotel_finder": "hotel_finder",
        "itinerary_builder": "itinerary_builder",
        END: END
    }
)


# ---------------- FINAL EDGE ---------------- #

workflow.add_edge(
    "itinerary_builder",
    END
)


# ---------------- COMPILE GRAPH ---------------- #

travel_graph = workflow.compile()