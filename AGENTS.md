# AGENTS.md

## DSPy Airline Customer Service Agent

This project demonstrates building a customer service agent using DSPy's ReAct framework with MLflow tracking and model versioning.

### Requirements and Setup

The project uses Python 3.15, DSPy 3.5, and MLflow 3.18. Install the locked
dependencies with:

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
ReAct state. Run the optimizer again and use the new registered model version.

### Running the Agent

#### Optimizer ([src/optimizer.py](src/optimizer.py))
Runs a request and logs the agent model:
```bash
uv run src/optimizer.py
```
Books a flight from SFO to JFK for user "Bob" and logs the model to MLflow with the signature.

#### Runner ([src/runner.py](src/runner.py))
Loads a specific model version and runs inference:
```bash
uv run src/runner.py --name Bob --version 1
```
- `--name`: Traveler name (default: "Bob")
- `--version`: Model version to load (default: 1)

Loads the specified model version from MLflow and books a flight from SFO to JFK for the specified user.

### Development Checks

Run the linter, formatter check, and type checker before committing changes:

```bash
uv run ruff check .
uv run ruff format --check .
uv run ty check
```

Format the code with `uv run ruff format .`. Use Conventional Commits for commit
messages.
