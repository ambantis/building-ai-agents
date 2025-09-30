# AGENTS.md

## DSPy Airline Customer Service Agent

This project demonstrates building a customer service agent using DSPy's ReAct framework with MLflow tracking and model versioning.

### Agent Architecture

The main agent is defined in [src/agent.py](src/agent.py) as a `dspy.ReAct` module created via the `new_agent()` function. It uses the `CustomerServiceRequest` signature and processes natural language requests using available tools to fulfill customer service tasks.

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

### Running the Agent

#### Optimizer ([src/optimizer.py](src/optimizer.py))
Trains and logs the agent model:
```bash
python src/optimizer.py
```
Books a flight from SFO to JFK for user "Adam" and logs the model to MLflow with the signature.

#### Runner ([src/runner.py](src/runner.py))
Loads a specific model version and runs inference:
```bash
python src/runner.py --name Bob --version 1
```
- `--name`: Traveler name (default: "Bob")
- `--version`: Model version to load (default: 1)

Loads the specified model version from MLflow and books a flight from SFO to JFK for the specified user.