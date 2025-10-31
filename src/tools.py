import random
import string

import mlflow
from mlflow.entities import SpanType

from data import flight_database, itinery_database, ticket_database, user_database
from models import Date, Flight, Itinerary, Ticket, UserProfile


@mlflow.trace(span_type=SpanType.TOOL)
def fetch_flight_info(date: Date, origin: str, destination: str) -> list[Flight]:
    """Fetch flight information from origin to destination on the given date"""
    flights: list[Flight] = []

    for flight_id, flight in flight_database.items():
        if (
            flight.date_time.year == date.year
            and flight.date_time.month == date.month
            and flight.date_time.day == date.day
            and flight.origin == origin
            and flight.destination == destination
        ):
            flights.append(flight)
    if len(flights) == 0:
        raise ValueError("No matching flight found!")
    return flights


@mlflow.trace(span_type=SpanType.TOOL)
def fetch_itinerary(confirmation_number: str) -> Itinerary | None:
    """Fetch the booked itnerary information from database"""
    return itinery_database.get(confirmation_number)


@mlflow.trace(span_type=SpanType.TOOL)
def pick_flight(flights: list[Flight]):
    """Pick up the best flight that matches users' request. We pick the shortest, and cheaper one on ties."""
    sorted_flights = sorted(
        flights,
        key=lambda x: (
            x.get("duration") if isinstance(x, dict) else x.duration,
            x.get("price") if isinstance(x, dict) else x.price,
        ),
    )
    return sorted_flights[0]


def _generate_id(length=8) -> str:
    chars = string.ascii_lowercase + string.digits
    return "".join(random.choices(chars, k=length))


@mlflow.trace(span_type=SpanType.TOOL)
def book_flight(flight: Flight, user_profile: UserProfile):
    """Book a flight on behalf of the user."""
    print(f"itinerary database size={len(itinery_database)}")
    confirmation_number: str = _generate_id()
    while confirmation_number in itinery_database:
        confirmation_number = _generate_id()
    itinerary = Itinerary(
        confirmation_number=confirmation_number,
        user_profile=user_profile,
        flight=flight,
    )
    itinery_database[confirmation_number] = itinerary
    return confirmation_number, itinerary


@mlflow.trace(span_type=SpanType.TOOL)
def cancel_itinerary(confirmation_number: str, user_profile: UserProfile):
    """Cancel an itinerary on behalf of the user."""
    if confirmation_number in itinery_database:
        del itinery_database[confirmation_number]
    else:
        raise ValueError(
            "Cannot find the itinerary, please check your confirmation number."
        )


@mlflow.trace(span_type=SpanType.TOOL)
def get_user_info(name: str) -> UserProfile | None:
    """Fetch the user profile from database with given name."""
    return user_database.get(name)


@mlflow.trace(span_type=SpanType.TOOL)
def file_ticket(user_request: str, user_profile: UserProfile) -> str:
    """File a customer support ticket if this is something the agent cannot handle."""

    ticket_id = _generate_id(length=6)
    ticket_database[ticket_id] = Ticket(
        user_request=user_request, user_profile=user_profile
    )
    return ticket_id
