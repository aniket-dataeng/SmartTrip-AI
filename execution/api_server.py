"""
FastAPI REST server for SmartTrip-AI.
Orchestrates between directives and execution scripts.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
import traceback

from execution.models import (
    TripInput, ReplanEvent, Itinerary,
    GenerateResponse, ReplanResponse, WeatherResponse,
)
from execution.itinerary_engine import generate_itinerary
from execution.replan_engine import replan_itinerary
from execution.places_service import search_places
from execution.weather_service import get_forecast
from execution.budget_optimizer import check_budget_health


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown lifecycle."""
    print("🚀 SmartTrip-AI server starting...")
    yield
    print("👋 SmartTrip-AI server shutting down.")


app = FastAPI(
    title="SmartTrip-AI",
    description="AI travel copilot that rebuilds your trip when reality changes.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS — allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Health Check ---

@app.get("/api/health")
async def health():
    """Server health check."""
    return {"status": "ok", "service": "SmartTrip-AI"}


# --- Generate Itinerary ---

@app.post("/api/generate", response_model=GenerateResponse)
async def generate(trip: TripInput):
    """
    Generate a personalized itinerary from user inputs.
    Follows directive: directives/generate_itinerary.md
    """
    try:
        # Step 1: Fetch places for the destination
        places = await search_places(
            destination=trip.destination,
            interests=trip.interests,
        )

        # Step 2: Generate itinerary via AI engine
        itinerary = await generate_itinerary(trip, places)

        return GenerateResponse(success=True, itinerary=itinerary)

    except ValueError as e:
        return GenerateResponse(success=False, error=str(e))
    except Exception as e:
        traceback.print_exc()
        return GenerateResponse(
            success=False,
            error=f"Failed to generate itinerary: {str(e)}",
        )


# --- Replan Trip ---

@app.post("/api/replan", response_model=ReplanResponse)
async def replan(
    event: ReplanEvent,
    itinerary: Itinerary,
):
    """
    Replan an existing itinerary based on a disruption event.
    Follows directive: directives/replan_trip.md
    """
    try:
        result = await replan_itinerary(itinerary, event)
        return ReplanResponse(success=True, result=result)

    except ValueError as e:
        return ReplanResponse(success=False, error=str(e))
    except Exception as e:
        traceback.print_exc()
        return ReplanResponse(
            success=False,
            error=f"Failed to replan: {str(e)}",
        )


# --- Weather ---

@app.get("/api/weather", response_model=WeatherResponse)
async def weather(destination: str, dates: str):
    """
    Get weather forecast for a destination.
    dates: comma-separated YYYY-MM-DD strings.
    """
    try:
        date_list = [d.strip() for d in dates.split(",")]
        forecasts = await get_forecast(destination, date_list)
        return WeatherResponse(
            success=True,
            destination=destination,
            forecasts=forecasts,
        )
    except Exception as e:
        return WeatherResponse(
            success=False,
            destination=destination,
            error=str(e),
        )


# --- Budget Health ---

@app.get("/api/budget-health")
async def budget_health(spent: int, total: int):
    """Check budget health indicators."""
    return check_budget_health(spent, total)


# --- Serve frontend in production ---

_FRONTEND_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "frontend", "dist",
)
if os.path.isdir(_FRONTEND_DIR):
    app.mount(
        "/", StaticFiles(directory=_FRONTEND_DIR, html=True),
        name="frontend",
    )
