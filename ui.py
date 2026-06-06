import streamlit as st
import requests
import json


# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide"
)


# ---------------- CUSTOM CSS ---------------- #

st.markdown(
    """
    <style>

    .stApp {
        background-color: #F5EEFF;
    }

    .main-title {
        font-size: 42px;
        font-weight: bold;
        color: #6A0DAD;
        text-align: center;
        margin-bottom: 20px;
    }

    .section-title {
        font-size: 24px;
        font-weight: bold;
        color: #7B2CBF;
        margin-top: 20px;
    }

    .agent-box {
        padding: 15px;
        border-radius: 12px;
        background-color: #E9D8FD;
        margin-bottom: 10px;
        color: black;
        font-weight: bold;
    }

    .active-agent {
        background-color: #C77DFF;
        color: white;
        border: 3px solid #7B2CBF;
    }

    .hotel-card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        margin-top: 15px;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
    }

    .itinerary-box {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        margin-top: 20px;
        color: black;
        box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------- TITLE ---------------- #

st.markdown(
    "<div class='main-title'>✈️ AI Travel Planner</div>",
    unsafe_allow_html=True
)


# ---------------- SIDEBAR INPUTS ---------------- #

st.sidebar.header("Trip Details")


destination = st.sidebar.text_input(
    "Destination",
    "Bali"
)

check_in = st.sidebar.date_input(
    "Check-In Date"
)

check_out = st.sidebar.date_input(
    "Check-Out Date"
)

budget = st.sidebar.slider(
    "Budget Per Night ($)",
    50,
    1000,
    150
)

preferences = st.sidebar.text_area(
    "Preferences",
    "Luxury resorts near beach"
)


plan_button = st.sidebar.button(
    "Plan My Trip"
)


# ---------------- FLOW DIAGRAM ---------------- #

st.markdown(
    "<div class='section-title'>Agent Workflow</div>",
    unsafe_allow_html=True
)


flow_container = st.empty()


def render_flow(active_agent=None):

    agents = [

        "destination_researcher",

        "hotel_finder",

        "availability_checker",

        "itinerary_builder"
    ]

    html = ""

    for agent in agents:

        css_class = "agent-box"

        if agent == active_agent:
            css_class += " active-agent"

        html += (
            f"<div class='{css_class}'>"
            f"{agent}"
            f"</div>"
        )

    flow_container.markdown(
        html,
        unsafe_allow_html=True
    )


render_flow()


# ---------------- LIVE STATUS ---------------- #

status_box = st.empty()


# ---------------- FINAL OUTPUT ---------------- #

hotel_container = st.empty()

itinerary_container = st.empty()


# ---------------- API CALL ---------------- #

if plan_button:

    status_box.info(
        "Starting AI Agents..."
    )

    url = "http://localhost:8000/plan"

    payload = {

        "destination": destination,

        "check_in": str(check_in),

        "check_out": str(check_out),

        "budget": budget
    }

    try:

        response = requests.post(
            url,
            json=payload,
            stream=True
        )

        final_data = None

        for line in response.iter_lines():

            if line:

                decoded_line = line.decode(
                    "utf-8"
                )

                if decoded_line.startswith(
                    "data:"
                ):

                    json_data = decoded_line.replace(
                        "data: ",
                        ""
                    )

                    event = json.loads(
                        json_data
                    )

                    # Status Updates
                    if "status" in event:

                        status = event["status"]

                        status_box.success(
                            status
                        )

                        # Highlight active agent
                        if "destination_researcher" in status:
                            render_flow(
                                "destination_researcher"
                            )

                        elif "hotel_finder" in status:
                            render_flow(
                                "hotel_finder"
                            )

                        elif "availability_checker" in status:
                            render_flow(
                                "availability_checker"
                            )

                        elif "itinerary_builder" in status:
                            render_flow(
                                "itinerary_builder"
                            )

                    # Final Output
                    if event.get("status") == "completed":

                        final_data = event

        # ---------------- HOTEL DISPLAY ---------------- #

        if final_data:

            selected_hotel = final_data.get(
                "selected_hotel"
            )

            itinerary = final_data.get(
                "itinerary"
            )

            if selected_hotel:

                hotel_html = f"""
                <div class='hotel-card'>
                    <h2>🏨 Selected Hotel</h2>

                    <p><b>Name:</b> {selected_hotel.get('name')}</p>

                    <p><b>Price:</b> ${selected_hotel.get('price')}</p>

                    <p><b>Rating:</b> ⭐ {selected_hotel.get('rating')}</p>

                    <p>
                        <a href="{selected_hotel.get('link')}" target="_blank">
                        View Hotel
                        </a>
                    </p>
                </div>
                """

                hotel_container.markdown(
                    hotel_html,
                    unsafe_allow_html=True
                )

            # ---------------- ITINERARY DISPLAY ---------------- #

            itinerary_html = f"""
            <div class='itinerary-box'>

            <h2>🗺️ Final Itinerary</h2>

            <pre style="white-space: pre-wrap;">
            {itinerary}
            </pre>

            </div>
            """

            itinerary_container.markdown(
                itinerary_html,
                unsafe_allow_html=True
            )

            status_box.success(
                "Trip Planning Completed!"
            )

            render_flow()

    except Exception as e:

        st.error(
            f"Error: {str(e)}"
        )