import json
import mlflow
from mlflow.store.entities import PagedList
from mlflow import MlflowClient
from mlflow.entities import Trace

# from mlflow.genai.datasets import create_dataset
from dotenv import load_dotenv
from rich import print as rprint

load_dotenv()
mlflow.set_tracking_uri("http://localhost:5000")

client = MlflowClient(tracking_uri="http://localhost:5000")


def main() -> None:
    # First, retrieve traces that will become the basis of the dataset
    # Handle pagination manually using the token

    all_traces: list[Trace] = []
    page_token: str | None = None

    while True:
        page: PagedList[Trace] = client.search_traces(
            locations=["1"],  # or in databricks: `<catalog_name>.<schema_name>`
            max_results=50,
            page_token=page_token,
            filter_string="tags.application_name = 'dspy_traveler' AND tags.agent_type = 'travel_agent'",
        )
        next = page.to_list()
        all_traces.extend(next)
        rprint(f"fetched {len(next)} traces")

        # Check if there are more pages
        if not page.token:
            break
        page_token = page.token

    rprint(f"got {len(all_traces)} traces total")

    for idx, trace in enumerate(all_traces):
        dict = trace.to_dict()
        path = f"traces/trace{idx}.json"
        with open(path, "w") as file:
            json.dump(dict, file, indent=2)
        rprint(f"wrote trace to {path}")


if __name__ == "__main__":
    main()
