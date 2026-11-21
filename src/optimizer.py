import dspy
import mlflow
from dotenv import load_dotenv
from rich import print as rprint

import agent

load_dotenv()

dspy.configure(lm=dspy.LM(model="openai/gpt-4o-mini"))
mlflow.set_tracking_uri(agent.ML_FLOW_URI)
mlflow.set_experiment(agent.EXPERIMENT_NAME)
mlflow.dspy.autolog(log_traces_from_compile=True, log_compiles=True)


def main() -> None:
    user_request = (
        "Please help me book a flight from SFO to JFK on 09/01/2025. My name is Bob."
    )

    with mlflow.start_run(run_name=agent.FLOW_NAME):
        result = agent.new_agent()(user_request=user_request)
        print(f"agent response: {result.process_result}\n")

        model_info = mlflow.dspy.log_model(
            dspy_model=agent.new_agent(),
            registered_model_name=agent.MODEL_NAME,
            signature=agent.agent_signature(),
            use_dspy_model_save=True,
        )
        rprint(f"model_info={model_info!r}")


if __name__ == "__main__":
    main()
