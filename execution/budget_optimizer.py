"""
Budget allocation engine for SmartTrip-AI.
Distributes total budget across days and categories.
"""

from execution.models import TripInput, TravelStyle


# Category split ratios by travel style
_CATEGORY_RATIOS = {
    TravelStyle.BUDGET: {
        "activities": 0.25,
        "food": 0.35,
        "transport": 0.30,
        "misc": 0.10,
    },
    TravelStyle.MODERATE: {
        "activities": 0.35,
        "food": 0.30,
        "transport": 0.25,
        "misc": 0.10,
    },
    TravelStyle.LUXURY: {
        "activities": 0.40,
        "food": 0.30,
        "transport": 0.15,
        "misc": 0.15,
    },
}


def allocate_budget(trip: TripInput, num_days: int) -> dict:
    """
    Split total budget across days and categories.

    Returns:
        {
            "per_day": 3333,
            "categories": { "activities": 1166, "food": 1000, ... },
            "total": 10000,
            "is_tight": False
        }
    """
    if num_days <= 0:
        raise ValueError("Trip must be at least 1 day")

    per_day = trip.budget // num_days
    ratios = _CATEGORY_RATIOS[trip.travel_style]

    categories = {
        cat: int(per_day * ratio)
        for cat, ratio in ratios.items()
    }

    # "Tight" if per-day budget < ₹1500 (hard to do much)
    is_tight = per_day < 1500

    return {
        "per_day": per_day,
        "categories": categories,
        "total": trip.budget,
        "is_tight": is_tight,
    }


def check_budget_health(spent: int, total: int) -> dict:
    """
    Return budget health indicators.

    Returns:
        { "spent": 6000, "remaining": 4000, "percent_used": 60, "status": "ok" }
    """
    remaining = max(0, total - spent)
    percent = round((spent / total) * 100) if total > 0 else 0

    if percent > 100:
        status = "exceeded"
    elif percent > 85:
        status = "warning"
    else:
        status = "ok"

    return {
        "spent": spent,
        "remaining": remaining,
        "percent_used": percent,
        "status": status,
    }
