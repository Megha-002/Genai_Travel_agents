from graph.travel_graph import travel_graph


initial_state = {

    "destination": "India",

    "check_in": "2026-05-23",
    "check_out": "2026-06-24",

    "budget": 10000,

    "search_results": "",

    "destination_info": "",

    "hotels_found": [],

    "available_hotels": [],

    "selected_hotel": None,

    "final_itinerary": "",

    "error": None,

    "retry_count": 0
}


print("\nStarting Travel Planner Graph...\n")


final_state = travel_graph.invoke(initial_state)


print("\nGraph Execution Completed!\n")


print("=" * 50)
print("DESTINATION INFO")
print("=" * 50)

print(final_state["destination_info"])


print("\n" + "=" * 50)
print("HOTELS FOUND")
print("=" * 50)

for hotel in final_state["hotels_found"]:
    print(hotel)


print("\n" + "=" * 50)
print("AVAILABLE HOTELS")
print("=" * 50)

for hotel in final_state["available_hotels"]:
    print(hotel)


print("\n" + "=" * 50)
print("SELECTED HOTEL")
print("=" * 50)

print(final_state["selected_hotel"])


print("\n" + "=" * 50)
print("FINAL ITINERARY")
print("=" * 50)

print(final_state["final_itinerary"])


print("\n" + "=" * 50)
print("RETRY COUNT")
print("=" * 50)

print(final_state["retry_count"])