"""
Route sequencing for SmartTrip-AI.
Orders activities per day to minimize travel time using nearest-neighbor.
"""

import math


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two lat/lon points in km."""
    R = 6371  # Earth radius in km
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(d_lon / 2) ** 2
    )
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def optimize_route(locations: list[dict]) -> list[dict]:
    """
    Nearest-neighbor ordering for a list of locations.

    Args:
        locations: List of dicts with 'name', 'lat', 'lon' keys.

    Returns:
        Same list reordered for minimal total travel distance.
    """
    if len(locations) <= 2:
        return locations

    remaining = list(locations)
    ordered = [remaining.pop(0)]  # Start from the first location

    while remaining:
        last = ordered[-1]
        nearest_idx = 0
        nearest_dist = float("inf")

        for i, loc in enumerate(remaining):
            dist = _haversine_km(
                last.get("lat", 0), last.get("lon", 0),
                loc.get("lat", 0), loc.get("lon", 0),
            )
            if dist < nearest_dist:
                nearest_dist = dist
                nearest_idx = i

        ordered.append(remaining.pop(nearest_idx))

    return ordered


def build_route_summary(activities: list[str]) -> str:
    """Create a human-readable route string like 'A → B → C'."""
    if not activities:
        return "No route"
    return " → ".join(activities)
