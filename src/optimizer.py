import dspy
import mlflow
import agent
from dotenv import load_dotenv
from rich import print as rprint

from data import itinery_database

load_dotenv()

dspy.configure(lm=dspy.LM(model="openai/gpt-4o-mini"))
mlflow.set_tracking_uri(agent.ML_FLOW_URI)
mlflow.set_experiment(agent.EXPERIMENT_NAME)
mlflow.dspy.autolog()  # type: ignore


def main():
    user_request = (
        "Please help me book a flight from SFO to JFK on 09/01/2025.",
        "My name is Adam",
    )

    with mlflow.start_run(run_name=agent.FLOW_NAME):
        result = agent.new_agent()(user_request=user_request)
        print(f"agent response: {result.process_result}\n")
        print(f"database={itinery_database}")

        model_info = mlflow.dspy.log_model(  # type: ignore
            dspy_model=agent.new_agent(),
            registered_model_name=agent.MODEL_NAME,
            signature=agent.agent_signature(),
        )
        rprint(f"model_info={repr(model_info)}")


if __name__ == "__main__":
    main()
