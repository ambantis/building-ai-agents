from __future__ import annotations

from threading import Lock
from typing import TYPE_CHECKING

import mlflow
from mlflow.entities import SpanType

import agent

if TYPE_CHECKING:
    import dspy

    from schemas import TravelRequest


class AgentService:
    """Load and run the registered airline customer service agent."""

    def __init__(
        self,
        model: dspy.Module | None = None,
        model_version: int | None = None,
    ) -> None:
        self.model = model
        self.model_version = model_version
        self._request_lock = Lock()

    def load_model(self, version: int) -> None:
        """Load a registered model version from MLflow."""
        if version < 1:
            raise ValueError("Model version must be at least 1.")

        model_uri = f"models:/{agent.MODEL_NAME}/{version}"
        loaded_model = mlflow.dspy.load_model(model_uri=model_uri)
        self.model = loaded_model
        self.model_version = version

    @mlflow.trace(name="Travel Agent Request", span_type=SpanType.AGENT)
    def handle_request(self, request: TravelRequest) -> dspy.Prediction:
        """Run one validated traveler request with trace metadata."""
        if self.model is None:
            raise RuntimeError("The agent model is not loaded.")

        model_request = (
            f"{request.user_request}\nTraveler name: {request.traveler_name}."
        )

        mlflow.update_current_trace(
            tags={
                "traveler_name": request.traveler_name,
                "application_name": "dspy_traveler",
                "model_version": str(self.model_version),
                "agent_type": "travel_agent",
            },
            metadata={"request_name": f"Travel request for {request.traveler_name}"},
        )
        # The mock databases and loaded agent are shared by HTTP and Gradio calls.
        with self._request_lock:
            return self.model(user_request=model_request)


def configure_mlflow() -> None:
    """Configure MLflow tracking for model loading and inference."""
    mlflow.set_tracking_uri(agent.ML_FLOW_URI)
    mlflow.set_experiment(agent.EXPERIMENT_NAME)
    mlflow.set_active_model(name=agent.MODEL_NAME)
    mlflow.dspy.autolog(log_traces=True)
