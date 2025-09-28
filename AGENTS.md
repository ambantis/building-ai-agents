# AGENTS.md

## DSPy Airline Customer Service Agent

This project demonstrates building a customer service agent using DSPy's ReAct framework with MLflow tracking.

### Agent Architecture

The main agent is defined in `src/agent.py` as `DSPyAirlineCustomerService` using the `dspy.ReAct` pattern. It processes natural language requests and uses available tools to fulfill customer service tasks.

### Agent Tools

The agent has access to the following tools (defined in `src/tools.py`):

- **`fetch_flight_info(date, origin, destination)`**: Search for available flights
- **`fetch_itinerary(confirmation_number)`**: Retrieve existing bookings
- **`pick_flight(flights)`**: Select optimal flight from search results (shortest duration, cheapest on ties)
- **`book_flight(flight, user_profile)`**: Create new flight reservations
- **`cancel_itinerary(confirmation_number, user_profile)`**: Cancel existing bookings
- **`get_user_info(name)`**: Look up user profiles by name
- **`file_ticket(user_request, user_profile)`**: Create support tickets for unhandled requests

### Data Models

Defined in `src/models.py` using Pydantic:
- **Date**: Custom date representation (year, month, day, hour)
- **UserProfile**: User identification and contact info
- **Flight**: Flight details including timing, route, and pricing
- **Itinerary**: Booked flight with confirmation number
- **Ticket**: Customer support ticket

### Mock Database

`src/data.py` contains in-memory dictionaries simulating:
- User database with sample users (Adam, Bob, Chelsie, David)
- Flight database with sample flights (DA123, DA125, DA456, DA460)
- Itinerary and ticket databases (populated at runtime)

### MLflow Integration

- Tracking URI: `http://localhost:5000`
- Experiment: "DSPy Building AI Agents"
- Auto-logging enabled for DSPy components
- Model logging and loading capabilities included

### Running the Agent

```bash
python src/agent.py
```

The demo books a flight from SFO to JFK for user "Adam" and displays the result along with the updated database state.