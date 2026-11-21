from pydantic import BaseModel, ConfigDict, Field

DEFAULT_REQUEST = "Please help me book a flight from SFO to JFK on 09/01/2025."


class TravelRequest(BaseModel):
    """Input for one airline customer service request."""

    model_config = ConfigDict(str_strip_whitespace=True)

    traveler_name: str = Field(min_length=1, max_length=100, examples=["Bob"])
    user_request: str = Field(
        min_length=1,
        max_length=4_000,
        examples=[DEFAULT_REQUEST],
    )


class TravelResponse(BaseModel):
    """The completed agent response."""

    process_result: str
    termination_reason: str
    model_version: int


class HealthResponse(BaseModel):
    """The current server and model status."""

    status: str
    model_loaded: bool
    model_version: int | None
