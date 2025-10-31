import argparse

import dspy
import mlflow
from mlflow.entities import SpanType
from rich import print as rprint

import agent
from data import itinery_database

model_version: int | None = None
model: dspy.Module | None = None


def load_model(version: int) -> None:
    global model_version, model
    model_version = version
    model_uri = f"models:/{agent.MODEL_NAME}/{model_version}"
    model = mlflow.dspy.load_model(model_uri=model_uri)  # type: ignore


@mlflow.trace(name="Travel Agent Request", span_type=SpanType.AGENT)
def handle_request(traveler_name: str, user_request: str):
    if model:
        mlflow.update_current_trace(
            tags={
                "traveler_name": traveler_name,
                "application_name": "dspy_traveler",
                "model_version": str(model_version),
                "agent_type": "travel_agent",
            },
            metadata={"request_name": f"Travel request for {traveler_name}"},
        )
        return model(user_request=user_request)


def main():
    parser = argparse.ArgumentParser(description="agent runner")
    parser.add_argument("--name", type=str, default="Bob", help="Traveler name")
    parser.add_argument("--version", type=int, default=1, help="Model version")
    args = parser.parse_args()

    mlflow.set_tracking_uri(agent.ML_FLOW_URI)
    mlflow.set_experiment(agent.EXPERIMENT_NAME)
    mlflow.set_active_model(name=agent.MODEL_NAME)
    # Enable autologging for traces during inference
    mlflow.dspy.autolog(log_traces=True)  # type: ignore

    user_request = (
        "Please help me book a flight from SFO to JFK on 09/01/2025.",
        f"My name is {args.name}",
    )

    with mlflow.start_run(run_name="travel_agent_evaluation"):
        load_model(args.version)
        mlflow.set_tags({"where_am_i": "idk"})
        result = handle_request(
            traveler_name=args.name,
            user_request=user_request,
        )
        rprint(f"agent response: {result.process_result}")
        rprint(f"database={itinery_database}")


if __name__ == "__main__":
    main()
