# Replan Trip

## Goal
Dynamically rebuild an existing itinerary when real-world conditions change, minimizing disruption.

## Inputs
- **current_itinerary** (Itinerary): The existing plan
- **event** (ReplanEvent): What triggered the replan
  - `type`: `"weather"`, `"closure"`, `"budget_exceeded"`, `"user_preference"`
  - `details`: Human-readable description
  - `affected_day`: Which day index is impacted (optional, defaults to current)

## Scripts
1. `execution/weather_service.py` — Check live weather conditions
2. `execution/replan_engine.py` — Send existing plan + event to Gemini for rebuild
3. `execution/gemini_client.py` — AI reasoning for swap decisions

## Output
Updated `Itinerary` with:
- `changes_summary`: What was swapped and why
- `reasoning`: Chain-of-thought explanation
- Only affected days are modified; rest stays intact

## Replan Strategies
| Trigger | Strategy |
|---|---|
| Rain/Storm | Swap outdoor → indoor (museums, malls, cafés) |
| Attraction closed | Next-best alternative in same category |
| Budget exceeded | Cheaper alternatives, free attractions |
| User preference shift | Re-rank remaining activities by new priority |

## Edge Cases
- **All alternatives also affected**: Suggest rest day or travel to nearby city
- **Budget already at zero**: Only suggest free activities
- **Last day of trip**: Prioritize must-see items that were missed
