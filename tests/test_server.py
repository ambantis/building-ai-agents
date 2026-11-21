from __future__ import annotations

from typing import TYPE_CHECKING

import dspy
import mlflow
import pytest
from fastapi.testclient import TestClient

from schemas import TravelRequest
from server import create_app
from service import AgentService

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pathlib import Path


class FakeModel(dspy.Module):
    def __init__(self) -> None:
        super().__init__()
        self.requests: list[str] = []

    def forward(self, user_request: str) -> dspy.Prediction:
        self.requests.append(user_request)
        return dspy.Prediction(
            process_result=f"Completed: {user_request}",
            history=dspy.History(messages=[]),
            termination_reason="submit",
        )


@pytest.fixture
def client(tmp_path: Path) -> Iterator[TestClient]:
    mlflow.set_tracking_uri(f"sqlite:///{tmp_path}/mlflow.db")
    service = AgentService(model=FakeModel(), model_version=7)
    app = create_app(service)
    with TestClient(app) as test_client:
        yield test_client


def test_health(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "model_loaded": True,
        "model_version": 7,
    }


def test_create_travel_request(client: TestClient) -> None:
    user_request = "Book a flight for Bob."
    response = client.post(
        "/v1/travel-requests",
        json={"traveler_name": "Bob", "user_request": user_request},
    )

    assert response.status_code == 200
    assert response.json() == {
        "process_result": f"Completed: {user_request}\nTraveler name: Bob.",
        "termination_reason": "submit",
        "model_version": 7,
    }


def test_create_travel_request_rejects_blank_input(client: TestClient) -> None:
    response = client.post(
        "/v1/travel-requests",
        json={"traveler_name": " ", "user_request": "Book a flight."},
    )

    assert response.status_code == 422


def test_api_documentation_is_available(client: TestClient) -> None:
    response = client.get("/docs")

    assert response.status_code == 200
    assert "Airline Customer Service Agent" in response.text


def test_request_schema_strips_whitespace() -> None:
    request = TravelRequest(
        traveler_name="  Bob  ",
        user_request="  Book a flight.  ",
    )

    assert request.traveler_name == "Bob"
    assert request.user_request == "Book a flight."
