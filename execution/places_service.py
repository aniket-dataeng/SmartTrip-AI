"""
Google Places integration for SmartTrip-AI.
Fetches real attractions, cafes, restaurants for a destination.
Falls back to curated local data if no API key is configured.
"""

import os
import httpx
from dotenv import load_dotenv

load_dotenv()

_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY", "")
_BASE_URL = "https://places.googleapis.com/v1/places:searchText"


async def search_places(
    destination: str,
    interests: list[str],
    max_results: int = 20,
) -> list[dict]:
    """
    Search for places matching user interests in a destination.

    Returns list of dicts with: name, category, rating,
    price_level, location, lat, lon, is_indoor
    """
    if _API_KEY:
        return await _fetch_live(destination, interests, max_results)
    return _get_curated_places(destination, interests)


async def _fetch_live(
    destination: str,
    interests: list[str],
    max_results: int,
) -> list[dict]:
    """Call Google Places API (New) for real data."""
    query = f"top {', '.join(interests)} places in {destination}"
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post(
                _BASE_URL,
                headers={
                    "Content-Type": "application/json",
                    "X-Goog-Api-Key": _API_KEY,
                    "X-Goog-FieldMask": (
                        "places.displayName,places.rating,"
                        "places.priceLevel,places.location,"
                        "places.types,places.formattedAddress"
                    ),
                },
                json={
                    "textQuery": query,
                    "maxResultCount": max_results,
                },
            )
            resp.raise_for_status()
            data = resp.json()

        places = []
        for p in data.get("places", []):
            loc = p.get("location", {})
            types = p.get("types", [])
            is_indoor = any(
                t in types
                for t in [
                    "museum", "shopping_mall", "cafe",
                    "restaurant", "library", "art_gallery",
                ]
            )
            places.append({
                "name": p.get("displayName", {}).get("text", ""),
                "category": types[0] if types else "attraction",
                "rating": p.get("rating", 0),
                "price_level": p.get("priceLevel", "MODERATE"),
                "location": p.get("formattedAddress", destination),
                "lat": loc.get("latitude", 0),
                "lon": loc.get("longitude", 0),
                "is_indoor": is_indoor,
            })
        return places

    except Exception as e:
        print(f"Places API error: {e}, using curated data")
        return _get_curated_places(destination, interests)


# --- Curated Fallback Data ---

_CURATED_DATA = {
    "bangalore": [
        {"name": "Cubbon Park", "category": "park", "rating": 4.5, "cost": 0, "duration": 90, "location": "Cubbon Park, MG Road", "lat": 12.9763, "lon": 77.5929, "is_indoor": False},
        {"name": "Lalbagh Botanical Garden", "category": "garden", "rating": 4.6, "cost": 30, "duration": 120, "location": "Lalbagh, Mavalli", "lat": 12.9507, "lon": 77.5848, "is_indoor": False},
        {"name": "Third Wave Coffee", "category": "cafe", "rating": 4.4, "cost": 350, "duration": 60, "location": "Indiranagar", "lat": 12.9784, "lon": 77.6408, "is_indoor": True},
        {"name": "Matteo Coffea", "category": "cafe", "rating": 4.3, "cost": 400, "duration": 60, "location": "Church Street", "lat": 12.9732, "lon": 77.6067, "is_indoor": True},
        {"name": "Bangalore Palace", "category": "palace", "rating": 4.2, "cost": 230, "duration": 90, "location": "Palace Road", "lat": 12.9988, "lon": 77.5921, "is_indoor": True},
        {"name": "ISKCON Temple", "category": "temple", "rating": 4.7, "cost": 0, "duration": 90, "location": "Rajajinagar", "lat": 13.0104, "lon": 77.5510, "is_indoor": True},
        {"name": "Commercial Street", "category": "shopping", "rating": 4.3, "cost": 500, "duration": 120, "location": "Commercial Street", "lat": 12.9837, "lon": 77.6087, "is_indoor": False},
        {"name": "VV Puram Food Street", "category": "food", "rating": 4.5, "cost": 300, "duration": 90, "location": "VV Puram", "lat": 12.9500, "lon": 77.5720, "is_indoor": False},
        {"name": "National Gallery of Modern Art", "category": "museum", "rating": 4.1, "cost": 20, "duration": 90, "location": "Palace Road", "lat": 12.9960, "lon": 77.5883, "is_indoor": True},
        {"name": "Nandi Hills", "category": "nature", "rating": 4.5, "cost": 100, "duration": 240, "location": "Nandi Hills", "lat": 13.3702, "lon": 77.6835, "is_indoor": False},
        {"name": "UB City Mall", "category": "shopping", "rating": 4.2, "cost": 0, "duration": 90, "location": "Vittal Mallya Road", "lat": 12.9716, "lon": 77.5946, "is_indoor": True},
        {"name": "Vidhana Soudha", "category": "landmark", "rating": 4.4, "cost": 0, "duration": 30, "location": "Dr. Ambedkar Rd", "lat": 12.9793, "lon": 77.5913, "is_indoor": False},
        {"name": "Byg Brewski", "category": "brewery", "rating": 4.3, "cost": 800, "duration": 120, "location": "Sarjapur Road", "lat": 12.9089, "lon": 77.6753, "is_indoor": True},
        {"name": "Tipu Sultan's Summer Palace", "category": "palace", "rating": 4.0, "cost": 15, "duration": 60, "location": "Albert Victor Rd", "lat": 12.9593, "lon": 77.5737, "is_indoor": True},
        {"name": "Wonderla Amusement Park", "category": "amusement", "rating": 4.4, "cost": 1200, "duration": 360, "location": "Mysore Road", "lat": 12.8340, "lon": 77.4010, "is_indoor": False},
    ],
    "hyderabad": [
        {"name": "Charminar", "category": "landmark", "rating": 4.5, "cost": 25, "duration": 60, "location": "Charminar, Old City", "lat": 17.3616, "lon": 78.4747, "is_indoor": False},
        {"name": "Golconda Fort", "category": "fort", "rating": 4.6, "cost": 25, "duration": 180, "location": "Ibrahim Bagh", "lat": 17.3833, "lon": 78.4011, "is_indoor": False},
        {"name": "Ramoji Film City", "category": "entertainment", "rating": 4.3, "cost": 1500, "duration": 480, "location": "Hayathnagar", "lat": 17.2543, "lon": 78.6808, "is_indoor": False},
        {"name": "Salar Jung Museum", "category": "museum", "rating": 4.4, "cost": 50, "duration": 150, "location": "Musi River", "lat": 17.3713, "lon": 78.4804, "is_indoor": True},
        {"name": "Hussain Sagar Lake", "category": "lake", "rating": 4.2, "cost": 0, "duration": 90, "location": "Tank Bund", "lat": 17.4239, "lon": 78.4738, "is_indoor": False},
        {"name": "Paradise Biryani", "category": "food", "rating": 4.5, "cost": 400, "duration": 60, "location": "Secunderabad", "lat": 17.4400, "lon": 78.4982, "is_indoor": True},
        {"name": "Birla Mandir", "category": "temple", "rating": 4.6, "cost": 0, "duration": 60, "location": "Naubath Pahad", "lat": 17.4062, "lon": 78.4691, "is_indoor": True},
        {"name": "Laad Bazaar", "category": "shopping", "rating": 4.3, "cost": 500, "duration": 90, "location": "Near Charminar", "lat": 17.3607, "lon": 78.4735, "is_indoor": False},
    ],
}


def _get_curated_places(
    destination: str,
    interests: list[str],
) -> list[dict]:
    """Return curated places filtered by interests."""
    key = destination.lower().strip()

    # Check for partial matches
    matched_key = None
    for k in _CURATED_DATA:
        if k in key or key in k:
            matched_key = k
            break

    if not matched_key:
        # Return generic template places
        return _generate_generic_places(destination, interests)

    places = _CURATED_DATA[matched_key]

    # Filter by interests if possible
    interest_set = {i.lower() for i in interests}
    category_map = {
        "cafes": ["cafe", "brewery"],
        "coffee": ["cafe"],
        "photography": ["park", "garden", "landmark", "palace", "fort", "lake", "nature"],
        "temples": ["temple"],
        "food": ["food", "cafe", "brewery"],
        "history": ["palace", "fort", "museum", "landmark"],
        "shopping": ["shopping"],
        "nature": ["park", "garden", "nature", "lake"],
        "culture": ["museum", "temple", "landmark", "palace"],
        "adventure": ["amusement", "nature"],
        "nightlife": ["brewery"],
    }

    matched_categories = set()
    for interest in interest_set:
        if interest in category_map:
            matched_categories.update(category_map[interest])

    if matched_categories:
        # Prioritize matched, but include others too
        matched = [p for p in places if p["category"] in matched_categories]
        others = [p for p in places if p["category"] not in matched_categories]
        return matched + others[:5]

    return places


def _generate_generic_places(
    destination: str,
    interests: list[str],
) -> list[dict]:
    """Generate placeholder places for unknown destinations."""
    base_places = [
        {"name": f"Central Park of {destination}", "category": "park", "rating": 4.3, "cost": 0, "duration": 90, "location": f"Central {destination}", "lat": 0, "lon": 0, "is_indoor": False},
        {"name": f"{destination} Heritage Museum", "category": "museum", "rating": 4.1, "cost": 100, "duration": 120, "location": destination, "lat": 0, "lon": 0, "is_indoor": True},
        {"name": f"Old Town Market", "category": "shopping", "rating": 4.2, "cost": 300, "duration": 90, "location": destination, "lat": 0, "lon": 0, "is_indoor": False},
        {"name": f"Local Café District", "category": "cafe", "rating": 4.4, "cost": 250, "duration": 60, "location": destination, "lat": 0, "lon": 0, "is_indoor": True},
        {"name": f"{destination} Viewpoint", "category": "nature", "rating": 4.5, "cost": 50, "duration": 60, "location": destination, "lat": 0, "lon": 0, "is_indoor": False},
        {"name": f"Street Food Lane", "category": "food", "rating": 4.3, "cost": 200, "duration": 60, "location": destination, "lat": 0, "lon": 0, "is_indoor": False},
    ]
    return base_places
