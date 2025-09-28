import dspy
from mlflow.models import ModelSignature
from mlflow.types.schema import ColSpec, Schema

from tools import (
    book_flight,
    cancel_itinerary,
    fetch_flight_info,
    fetch_itinerary,
    file_ticket,
    get_user_info,
    pick_flight,
)

EXPERIMENT_NAME = "DSPy Model State"
FLOW_NAME = "model_state_evaluation"
MODEL_NAME = "AirlineReActAgent"
ML_FLOW_URI = "http://localhost:5000"


class CustomerServiceRequest(dspy.Signature):
    """You are an airline customer service agent that helps user book and manage flights.

    You are given a list of tools to handle user request, and you should decide on
    the right tool to user to fulfil users' request."""

    user_request: str = dspy.InputField()
    process_result: str = dspy.OutputField(
        desc=(
            "Message that summarizes the process result, and the information users need",
            "e.g., the confirmation_number if a new flight is booked.",
        )
    )


def agent_signature() -> ModelSignature:
    input_schema = Schema([ColSpec("string", "user_request")])
    output_schema = Schema([ColSpec("string", "process_result")])
    return ModelSignature(inputs=input_schema, outputs=output_schema)


def new_agent() -> dspy.ReAct:
    return dspy.ReAct(
        signature=CustomerServiceRequest,
        tools=[
            fetch_flight_info,
            fetch_itinerary,
            pick_flight,
            book_flight,
            cancel_itinerary,
            get_user_info,
            file_ticket,
        ],
    )
