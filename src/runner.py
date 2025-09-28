import mlflow
import agent
import argparse

from rich import print as rprint

from data import itinery_database


def load_model(version: int):
    model_uri = f"models:/{agent.MODEL_NAME}/{version}"
    return mlflow.dspy.load_model(model_uri=model_uri)  # type: ignore


def main():
    parser = argparse.ArgumentParser(description="agent runner")
    parser.add_argument("--name", type=str, default="Bob", help="Traveler name")
    parser.add_argument("--version", type=int, default=1, help="Model version")
    args = parser.parse_args()

    mlflow.set_tracking_uri(agent.ML_FLOW_URI)
    mlflow.set_experiment(agent.EXPERIMENT_NAME)
    mlflow.dspy.autolog()  # type: ignore

    user_request = (
        "Please help me book a flight from SFO to JFK on 09/01/2025.",
        f"My name is {args.name}",
    )

    with mlflow.start_run(run_name="travel_agent_evaluation"):
        model = load_model(args.version)  # type: ignore

        result = model(user_request=user_request)
        rprint(f"agent response: {result.process_result}")
        rprint(f"database={itinery_database}")

        model_info = mlflow.dspy.log_model(  # type: ignore
            dspy_model=agent.new_agent(),
            registered_model_name=agent.MODEL_NAME,
            signature=agent.agent_signature(),
        )
        rprint(f"model_info={repr(model_info)}")


if __name__ == "__main__":
    main()
