"""
Tests for Pydantic models — validates input/output contracts.
"""

import pytest
from pydantic import ValidationError
from execution.models import (
    TripInput, DateRange, TravelStyle,
    ReplanEvent, ReplanTrigger,
    Activity, DayPlan, Itinerary,
)


class TestTripInput:
    """Validate trip input constraints."""

    def test_valid_input(self):
        trip = TripInput(
            destination="Bangalore",
            budget=10000,
            dates=DateRange(start="2026-05-10", end="2026-05-12"),
            interests=["cafes", "photography"],
        )
        assert trip.destination == "Bangalore"
        assert trip.budget == 10000
        assert trip.travel_style == TravelStyle.MODERATE

    def test_budget_must_be_positive(self):
        with pytest.raises(ValidationError):
            TripInput(
                destination="Goa",
                budget=0,
                dates=DateRange(start="2026-06-01", end="2026-06-03"),
                interests=["beaches"],
            )

    def test_destination_too_short(self):
        with pytest.raises(ValidationError):
            TripInput(
                destination="X",
                budget=5000,
                dates=DateRange(start="2026-06-01", end="2026-06-03"),
                interests=["food"],
            )

    def test_interests_must_not_be_empty(self):
        with pytest.raises(ValidationError):
            TripInput(
                destination="Mumbai",
                budget=15000,
                dates=DateRange(start="2026-07-01", end="2026-07-05"),
                interests=[],
            )

    def test_luxury_style(self):
        trip = TripInput(
            destination="Jaipur",
            budget=50000,
            dates=DateRange(start="2026-08-01", end="2026-08-04"),
            interests=["history", "food"],
            travel_style=TravelStyle.LUXURY,
        )
        assert trip.travel_style == TravelStyle.LUXURY


class TestReplanEvent:
    """Validate replan event constraints."""

    def test_valid_weather_event(self):
        event = ReplanEvent(
            trigger=ReplanTrigger.WEATHER,
            details="Heavy rain expected tomorrow afternoon",
        )
        assert event.trigger == ReplanTrigger.WEATHER
        assert event.affected_day is None

    def test_details_too_short(self):
        with pytest.raises(ValidationError):
            ReplanEvent(
                trigger=ReplanTrigger.CLOSURE,
                details="oops",
            )

    def test_affected_day_negative(self):
        with pytest.raises(ValidationError):
            ReplanEvent(
                trigger=ReplanTrigger.BUDGET_EXCEEDED,
                details="Over budget by ₹2000 on day 2",
                affected_day=-1,
            )


class TestActivity:
    """Validate activity model."""

    def test_valid_activity(self):
        a = Activity(
            name="Cubbon Park",
            description="Beautiful green park in the city center",
            cost=0,
            duration_minutes=90,
            category="park",
            location="MG Road",
            is_indoor=False,
        )
        assert a.cost == 0
        assert not a.is_indoor
