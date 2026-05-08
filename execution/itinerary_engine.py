"""
Core AI itinerary generation engine for SmartTrip-AI.
Constructs prompts, calls Gemini, parses structured itineraries.
"""

from datetime import datetime, timedelta
from execution.gemini_client import generate_json
from execution.models import (
    TripInput, Itinerary, DayPlan, Activity,
)
from execution.budget_optimizer import allocate_budget
from execution.route_optimizer import build_route_summary


def _count_days(dates_start: str, dates_end: str) -> int:
    """Calculate trip duration in days (inclusive)."""
    start = datetime.strptime(dates_start, "%Y-%m-%d")
    end = datetime.strptime(dates_end, "%Y-%m-%d")
    return max(1, (end - start).days + 1)


def _get_date_list(dates_start: str, num_days: int) -> list[str]:
    """Generate list of date strings for the trip."""
    start = datetime.strptime(dates_start, "%Y-%m-%d")
    return [
        (start + timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range(num_days)
    ]


def _build_system_prompt() -> str:
    """System prompt that defines the AI's role and output format."""
    return """You are SmartTrip-AI, an expert travel planner.
You create personalized, day-wise itineraries that balance budget, time, and user preferences.

RULES:
- Every activity MUST have a realistic cost in ₹ (Indian Rupees)
- Total cost across all days MUST NOT exceed the given budget
- Each day should have 4-6 activities including meals
- Include a mix of the user's interests throughout the trip
- Suggest at least 2 food spots per day matching the travel style
- Each activity needs: name, description, cost, duration_minutes, category, location, is_indoor
- Provide route_summary as "Place A → Place B → Place C"
- Include 2-3 alternative suggestions the user can swap in
- Include 3-5 practical travel tips specific to the destination

Return valid JSON matching this exact schema:
{
  "destination": "string",
  "days": [
    {
      "day_number": 1,
      "date": "YYYY-MM-DD",
      "theme": "short theme for the day",
      "activities": [
        {
          "name": "string",
          "description": "1-2 sentence description",
          "cost": 0,
          "duration_minutes": 60,
          "category": "cafe|temple|park|museum|food|shopping|nature|landmark|entertainment",
          "location": "specific area name",
          "is_indoor": false
        }
      ],
      "total_cost": 0,
      "route_summary": "A → B → C",
      "meals": ["Breakfast at X", "Lunch at Y", "Dinner at Z"]
    }
  ],
  "total_cost": 0,
  "summary": "2-3 sentence trip summary",
  "budget_remaining": 0,
  "alternatives": ["Alt 1 description", "Alt 2"],
  "travel_tips": ["Tip 1", "Tip 2"]
}"""


def _build_user_prompt(
    trip: TripInput,
    num_days: int,
    date_list: list[str],
    budget_plan: dict,
    places_context: str,
) -> str:
    """Build the user-facing prompt with all context."""
    return f"""Plan a {num_days}-day trip to {trip.destination}.

TRAVELLER PROFILE:
- Budget: ₹{trip.budget} total (₹{budget_plan['per_day']}/day)
- Dates: {date_list[0]} to {date_list[-1]}
- Interests: {', '.join(trip.interests)}
- Travel Style: {trip.travel_style.value}
- Budget Status: {"⚠️ TIGHT budget, prioritize free/cheap activities" if budget_plan['is_tight'] else "Comfortable budget"}

BUDGET ALLOCATION PER DAY:
- Activities: ₹{budget_plan['categories']['activities']}
- Food: ₹{budget_plan['categories']['food']}
- Transport: ₹{budget_plan['categories']['transport']}
- Miscellaneous: ₹{budget_plan['categories']['misc']}

KNOWN PLACES & ATTRACTIONS:
{places_context}

Create the itinerary with dates: {', '.join(date_list)}
Ensure total_cost ≤ ₹{trip.budget}."""


async def generate_itinerary(
    trip: TripInput,
    places: list[dict],
) -> Itinerary:
    """
    Generate a complete itinerary using Gemini AI.

    Args:
        trip: Validated user input
        places: Pre-fetched places from places_service

    Returns:
        Structured Itinerary object
    """
    num_days = _count_days(trip.dates.start, trip.dates.end)
    date_list = _get_date_list(trip.dates.start, num_days)
    budget_plan = allocate_budget(trip, num_days)

    # Format places as context for the AI
    places_ctx = "\n".join(
        f"- {p['name']} ({p['category']}): "
        f"₹{p.get('cost', 0)}, {p.get('duration', 60)}min, "
        f"at {p['location']}, "
        f"{'indoor' if p.get('is_indoor') else 'outdoor'}, "
        f"rating: {p.get('rating', 'N/A')}"
        for p in places
    )

    system_prompt = _build_system_prompt()
    user_prompt = _build_user_prompt(
        trip, num_days, date_list, budget_plan, places_ctx,
    )

    # Call Gemini (Flash for standard generation)
    raw = generate_json(
        prompt=user_prompt,
        system_instruction=system_prompt,
        use_pro=False,
        temperature=0.7,
    )

    return _parse_itinerary(raw, trip.budget)


def _parse_itinerary(raw: dict, budget: int) -> Itinerary:
    """Parse raw Gemini JSON into a validated Itinerary model."""
    days = []
    running_cost = 0

    for day_data in raw.get("days", []):
        activities = [
            Activity(
                name=a.get("name", "Activity"),
                description=a.get("description", ""),
                cost=max(0, int(a.get("cost", 0))),
                duration_minutes=max(15, int(a.get("duration_minutes", 60))),
                category=a.get("category", "general"),
                location=a.get("location", ""),
                is_indoor=a.get("is_indoor", False),
            )
            for a in day_data.get("activities", [])
        ]

        day_cost = sum(a.cost for a in activities)
        running_cost += day_cost

        # Build route from activity locations
        locations = [a.location for a in activities if a.location]
        route = day_data.get(
            "route_summary",
            build_route_summary(locations),
        )

        days.append(DayPlan(
            day_number=day_data.get("day_number", len(days) + 1),
            date=day_data.get("date", ""),
            theme=day_data.get("theme", f"Day {len(days) + 1}"),
            activities=activities,
            total_cost=day_cost,
            route_summary=route,
            meals=day_data.get("meals", []),
        ))

    return Itinerary(
        destination=raw.get("destination", ""),
        days=days,
        total_cost=running_cost,
        summary=raw.get("summary", "Your personalized trip itinerary."),
        budget_remaining=max(0, budget - running_cost),
        alternatives=raw.get("alternatives", []),
        travel_tips=raw.get("travel_tips", []),
    )
