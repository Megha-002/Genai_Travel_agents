import json
import time
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import mlflow
from prometheus_fastapi_instrumentator import Instrumentator

from graph.travel_graph import travel_graph

# MLflow Configuration
mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("Travel_Planner")

app = FastAPI(title="AI Travel Planner", version="1.0.0")
Instrumentator().instrument(app).expose(app)


class TripRequest(BaseModel):
    destination: str
    check_in: str
    check_out: str
    budget: int


@app.get("/")
def home():
    return {"message": "AI Travel Planner API Running"}


@app.post("/plan")
def plan_trip(request: TripRequest):
    initial_state = {
        "destination": request.destination,
        "check_in": request.check_in,
        "check_out": request.check_out,
        "budget": request.budget,
        "search_results": "",
        "destination_info": "",
        "hotels_found": [],
        "available_hotels": [],
        "selected_hotel": None,
        "final_itinerary": "",
        "error": None,
        "retry_count": 0,
    }

    def event_generator():
        try:
            yield f"data: {json.dumps({'status': 'Starting workflow'})}\n\n"

            agent_timings = {}
            workflow_start = time.time()
            last_node_time = workflow_start

            # Stream the graph execution
            for event in travel_graph.stream(initial_state):
                node_name = list(event.keys())[0]
                
                # Calculate duration for this specific node execution
                current_time = time.time()
                agent_timings[node_name] = current_time - last_node_time
                last_node_time = current_time

                yield f"data: {json.dumps({'status': f'{node_name} completed'})}\n\n"

            # Execute the final state logic safely
            final_state = travel_graph.invoke(initial_state)
            workflow_end = time.time()
            total_latency = workflow_end - workflow_start

            # MLflow Logging Block (Correctly Indented)
            with mlflow.start_run():
                # Parameters
                mlflow.log_param("destination", request.destination)
                mlflow.log_param("budget", request.budget)
                mlflow.log_param("check_in", request.check_in)
                mlflow.log_param("check_out", request.check_out)

                # Metrics
                mlflow.log_metric("total_latency", total_latency)
                mlflow.log_metric(
                    "hotels_found_count", 
                    len(final_state.get("hotels_found", []))
                )
                mlflow.log_metric(
                    "available_hotels_count", 
                    len(final_state.get("available_hotels", []))
                )
                mlflow.log_metric(
                    "retry_count", 
                    final_state.get("retry_count", 0)
                )

                # Agent execution durations
                for agent_name, duration in agent_timings.items():
                    mlflow.log_metric(f"{agent_name}_duration_sec", duration)

            # Yield final payload response
            completion_payload = {
                "status": "completed",
                "selected_hotel": final_state.get("selected_hotel"),
                "itinerary": final_state.get("final_itinerary"),
            }
            yield f"data: {json.dumps(completion_payload)}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(
        event_generator(), media_type="text/event-stream"
    )