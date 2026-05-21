from langgraph.graph import StateGraph, END

from graph.state import TravelState

from agents.destination_agent import destination_research_agent
from agents.hotel_agent import hotel_finder_agent
from agents.availability_agent import availability_checker_agent
from agents.itinerary_agent import itinerary_builder_agent


# Create Graph
workflow = StateGraph(TravelState)


# Add Nodes
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


# Entry Point
workflow.set_entry_point(
    "destination_researcher"
)


# Normal Flow Edges
workflow.add_edge(
    "destination_researcher",
    "hotel_finder"
)

workflow.add_edge(
    "hotel_finder",
    "availability_checker"
)


# Conditional Logic
def availability_router(state: TravelState):

    available_hotels = state["available_hotels"]

    retry_count = state["retry_count"]

    # Hotels found → continue
    if available_hotels:

        # Select best hotel automatically
        state["selected_hotel"] = available_hotels[0]

        return "itinerary_builder"

    # Retry search up to 3 times
    if retry_count < 3:
        return "hotel_finder"

    # Stop workflow if retries exceeded
    return END


workflow.add_conditional_edges(
    "availability_checker",
    availability_router,
    {
        "hotel_finder": "hotel_finder",
        "itinerary_builder": "itinerary_builder",
        END: END
    }
)


# Final Edge
workflow.add_edge(
    "itinerary_builder",
    END
)


# Compile Graph
travel_graph = workflow.compile()