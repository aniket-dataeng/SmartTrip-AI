"""
Pydantic models for SmartTrip-AI input/output contracts.
All data flowing through the system uses these schemas.
"""

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


# --- Enums ---

class TravelStyle(str, Enum):
    BUDGET = "budget"
    MODERATE = "moderate"
    LUXURY = "luxury"


class ReplanTrigger(str, Enum):
    WEATHER = "weather"
    CLOSURE = "closure"
    BUDGET_EXCEEDED = "budget_exceeded"
    USER_PREFERENCE = "user_preference"


# --- Input Models ---

class DateRange(BaseModel):
    start: str = Field(..., description="Start date YYYY-MM-DD")
    end: str = Field(..., description="End date YYYY-MM-DD")


class TripInput(BaseModel):
    destination: str = Field(..., min_length=2, max_length=100)
    budget: int = Field(..., gt=0, description="Total budget in ₹")
    dates: DateRange
    interests: list[str] = Field(..., min_length=1)
    travel_style: TravelStyle = TravelStyle.MODERATE


class ReplanEvent(BaseModel):
    trigger: ReplanTrigger
    details: str = Field(..., min_length=5)
    affected_day: Optional[int] = Field(
        None, ge=0, description="Day index affected, None = auto-detect"
    )


# --- Output Models ---

class Activity(BaseModel):
    name: str
    description: str
    cost: int = Field(ge=0, description="Cost in ₹")
    duration_minutes: int = Field(gt=0)
    category: str
    location: str
    is_indoor: bool = False


class DayPlan(BaseModel):
    day_number: int
    date: str
    theme: str
    activities: list[Activity]
    total_cost: int = Field(ge=0)
    route_summary: str
    meals: list[str] = Field(default_factory=list)


class Itinerary(BaseModel):
    destination: str
    days: list[DayPlan]
    total_cost: int = Field(ge=0)
    summary: str
    budget_remaining: int = Field(ge=0)
    alternatives: list[str] = Field(default_factory=list)
    travel_tips: list[str] = Field(default_factory=list)


class ReplanResult(BaseModel):
    updated_itinerary: Itinerary
    changes_summary: list[str]
    reasoning: str


# --- API Response Wrappers ---

class GenerateResponse(BaseModel):
    success: bool
    itinerary: Optional[Itinerary] = None
    error: Optional[str] = None


class ReplanResponse(BaseModel):
    success: bool
    result: Optional[ReplanResult] = None
    error: Optional[str] = None


class WeatherInfo(BaseModel):
    date: str
    condition: str
    temp_celsius: float
    is_rainy: bool
    description: str


class WeatherResponse(BaseModel):
    success: bool
    destination: str
    forecasts: list[WeatherInfo] = Field(default_factory=list)
    error: Optional[str] = None
