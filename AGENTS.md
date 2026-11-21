# AGENTS.md

## DSPy Airline Customer Service Agent

This project demonstrates building a customer service agent using DSPy's ReAct framework with MLflow tracking and model versioning.

### Requirements and Setup

The project uses Python 3.15, DSPy 3.5, MLflow 3.18, and FastAPI 0.165.
Gradio 6.32 is a development-only test client. Install the locked dependencies with:

```bash
uv sync --group dev
```

Copy `.env.example` to `.env` and set `OPENAI_API_KEY`. Start an MLflow server on
port 5000 before running the agent.

### Agent Architecture

The main agent is defined in [src/agent.py](src/agent.py) as a `dspy.ReAct` module created via the `new_agent()` function. It uses the `CustomerServiceRequest` signature and processes natural language requests using available tools to fulfill customer service tasks.

DSPy 3.5 uses structured ReAct history and a typed `submit` tool. Results contain
`history` and `termination_reason`; the old `trajectory` representation is not used.

### Agent Tools

The agent has access to the following tools (defined in [src/tools.py](src/tools.py)):

- **`fetch_flight_info(date, origin, destination)`**: Search for available flights
- **`fetch_itinerary(confirmation_number)`**: Retrieve existing bookings
- **`pick_flight(flights)`**: Select optimal flight from search results (shortest duration, cheapest on ties)
- **`book_flight(flight, user_profile)`**: Create new flight reservations
- **`cancel_itinerary(confirmation_number, user_profile)`**: Cancel existing bookings
- **`get_user_info(name)`**: Look up user profiles by name
- **`file_ticket(user_request, user_profile)`**: Create support tickets for unhandled requests

### Data Models

Defined in [src/models.py](src/models.py) using Pydantic:
- **Date**: Custom date representation (year, month, day, hour)
- **UserProfile**: User identification and contact info
- **Flight**: Flight details including timing, route, and pricing
- **Itinerary**: Booked flight with confirmation number
- **Ticket**: Customer support ticket

### Mock Database

[src/data.py](src/data.py) contains in-memory dictionaries simulating:
- User database with sample users (Adam, Bob, Chelsie, David)
- Flight database with sample flights (DA123, DA125, DA456, DA460)
- Itinerary and ticket databases (populated at runtime)

### MLflow Integration

- Tracking URI: `http://localhost:5000`
- Experiment: "DSPy Model State"
- Model name: "AirlineReActAgent"
- Auto-logging enabled for DSPy components
- Model versioning and loading capabilities
- New models use DSPy's built-in save format through `use_dspy_model_save=True`

Models created with DSPy 3.4 or earlier are not compatible with the DSPy 3.5
ReAct state. Run the optimizer again and set `MODEL_VERSION` to the new registered
model version.

### Running the Agent

#### Optimizer ([src/optimizer.py](src/optimizer.py))
Runs a request and logs the agent model:
```bash
uv run src/optimizer.py
```
Books a flight from SFO to JFK for user "Bob" and logs the model to MLflow with the signature.

#### HTTP server ([src/server.py](src/server.py))
Loads the model version set by `MODEL_VERSION` (default: 1) during startup:

```bash
MODEL_VERSION=1 uv run src/server.py
```

The FastAPI endpoint is `POST /v1/travel-requests`. Interactive API documentation
is available at `/docs`, and the health check is `/health`.

The service code is in [src/service.py](src/service.py). It accepts a validated
`TravelRequest` from [src/schemas.py](src/schemas.py). FastAPI does not import or
mount Gradio.

For development testing, run `uv run dev/agent_client.py` while FastAPI is
running. The standalone Gradio client sends requests to the FastAPI endpoint, so
Pydantic performs all request validation. Its browser UI listens on port 7860 by
default. Set `API_BASE_URL` to the FastAPI address.

### Development Checks

Run the linter, formatter check, and type checker before committing changes:

```bash
uv run ruff check .
uv run ruff format --check .
uv run ty check
uv run pytest
```

Format the code with `uv run ruff format .`. Use Conventional Commits for commit
messages.
