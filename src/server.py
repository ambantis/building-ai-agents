from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from starlette.concurrency import run_in_threadpool

from schemas import HealthResponse, TravelRequest, TravelResponse
from service import AgentService, configure_mlflow

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

load_dotenv()

logger = logging.getLogger(__name__)


def configured_model_version() -> int:
    """Read the registered model version from the environment."""
    raw_version = os.getenv("MODEL_VERSION", "1")
    try:
        version = int(raw_version)
    except ValueError as exc:
        raise ValueError("MODEL_VERSION must be an integer.") from exc
    if version < 1:
        raise ValueError("MODEL_VERSION must be at least 1.")
    return version


def create_app(service: AgentService | None = None) -> FastAPI:
    """Create the FastAPI and mounted Gradio applications."""
    agent_service = service or AgentService()

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
        if agent_service.model is None:
            configure_mlflow()
            await run_in_threadpool(
                agent_service.load_model,
                configured_model_version(),
            )
        yield

    app = FastAPI(
        title="Airline Customer Service Agent",
        version="1.0.0",
        lifespan=lifespan,
    )
    app.state.agent_service = agent_service

    @app.get("/", include_in_schema=False)
    def index() -> RedirectResponse:
        return RedirectResponse(url="/docs")

    @app.get("/health", response_model=HealthResponse)
    def health() -> HealthResponse:
        return HealthResponse(
            status="ok" if agent_service.model is not None else "unavailable",
            model_loaded=agent_service.model is not None,
            model_version=agent_service.model_version,
        )

    @app.post("/v1/travel-requests", response_model=TravelResponse)
    def create_travel_request(payload: TravelRequest) -> TravelResponse:
        if agent_service.model_version is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="The agent model is not loaded.",
            )

        try:
            result = agent_service.handle_request(payload)
        except Exception as exc:
            logger.exception("Agent request failed")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="The agent could not complete the request.",
            ) from exc

        return TravelResponse(
            process_result=result.process_result,
            termination_reason=result.termination_reason,
            model_version=agent_service.model_version,
        )

    return app


app = create_app()


def main() -> None:
    """Run the HTTP server."""
    uvicorn.run(
        app,
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "8000")),
        log_level=os.getenv("LOG_LEVEL", "info"),
    )


if __name__ == "__main__":
    main()
