# Generate Itinerary

## Goal
Generate a personalized, day-wise travel itinerary optimized for budget, time, and user preferences.

## Inputs
- **destination** (str): City/region name
- **budget** (int): Total trip budget in ₹
- **dates** (dict): `{ start: "YYYY-MM-DD", end: "YYYY-MM-DD" }`
- **interests** (list[str]): e.g., `["cafes", "photography", "temples"]`
- **travel_style** (str, optional): `"budget"`, `"moderate"`, `"luxury"` — defaults to `"moderate"`

## Scripts
1. `execution/places_service.py` — Fetch real attractions for the destination
2. `execution/budget_optimizer.py` — Allocate budget across days and categories
3. `execution/itinerary_engine.py` — Send context to Gemini, parse structured output
4. `execution/route_optimizer.py` — Order activities per day by proximity

## Output
Structured JSON `Itinerary` object:
```json
{
  "destination": "Bangalore",
  "days": [
    {
      "date": "2026-05-10",
      "theme": "Café Hopping & Street Photography",
      "activities": [...],
      "total_cost": 3200,
      "route_summary": "Indiranagar → Koramangala → Cubbon Park"
    }
  ],
  "total_cost": 9500,
  "summary": "3-day Bangalore trip focused on cafés and photography...",
  "alternatives": [...]
}
```

## Edge Cases
- **Budget too low**: Return a warning + best-effort plan with free attractions
- **No matching attractions**: Broaden interest categories, suggest nearby alternatives
- **Single-day trip**: Pack morning/afternoon/evening slots tightly
- **Unknown destination**: Return error with suggestion to check spelling
