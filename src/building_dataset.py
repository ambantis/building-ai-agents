from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

import mlflow
from dotenv import load_dotenv
from mlflow import MlflowClient
from rich import print as rprint

if TYPE_CHECKING:
    from mlflow.entities import Trace
    from mlflow.store.entities import PagedList

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
        page_traces = page.to_list()
        all_traces.extend(page_traces)
        rprint(f"fetched {len(page_traces)} traces")

        # Check if there are more pages
        if not page.token:
            break
        page_token = page.token

    rprint(f"got {len(all_traces)} traces total")

    for idx, trace in enumerate(all_traces):
        trace_dict = trace.to_dict()
        trace_path = Path(f"traces/trace{idx}.json")
        with trace_path.open("w", encoding="utf-8") as file:
            json.dump(trace_dict, file, indent=2)
        rprint(f"wrote trace to {trace_path}")


if __name__ == "__main__":
    main()
