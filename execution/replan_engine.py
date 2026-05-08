"""
Dynamic replanning engine for SmartTrip-AI.
Rebuilds itinerary when real-world conditions change.
"""

from execution.gemini_client import generate_json
from execution.models import (
    Itinerary, ReplanEvent, ReplanResult, ReplanTrigger,
)


def _build_replan_system_prompt() -> str:
    """System prompt for the replanning AI."""
    return """You are SmartTrip-AI's replanning engine.
Given an existing travel itinerary and a disruption event, you must rebuild the affected parts.

CORE PRINCIPLES:
- MINIMIZE disruption: only change what's necessary
- EXPLAIN every change with clear reasoning
- MAINTAIN budget constraints — never exceed the original budget
- PRESERVE the traveller's interests and priorities
- Prefer NEARBY alternatives to reduce travel time

For weather events: swap outdoor → indoor activities of similar interest
For closures: find the next-best alternative in the same category
For budget overruns: replace expensive activities with cheaper/free ones
For preference changes: re-rank remaining activities by new priority

Return valid JSON:
{
  "destination": "string",
  "days": [...same structure as original itinerary...],
  "total_cost": 0,
  "summary": "updated summary reflecting changes",
  "budget_remaining": 0,
  "alternatives": [...],
  "travel_tips": [...],
  "changes_summary": ["Changed X to Y because Z", ...],
  "reasoning": "Detailed explanation of the replanning logic"
}"""


def _build_replan_prompt(
    itinerary: Itinerary,
    event: ReplanEvent,
) -> str:
    """Build the replanning prompt with full context."""
    # Serialize current itinerary for context
    days_text = ""
    for day in itinerary.days:
        activities_text = "\n".join(
            f"    - {a.name} (₹{a.cost}, {a.duration_minutes}min, "
            f"{a.category}, {'indoor' if a.is_indoor else 'outdoor'})"
            for a in day.activities
        )
        days_text += (
            f"\n  Day {day.day_number} ({day.date}) — {day.theme}:\n"
            f"{activities_text}\n"
            f"    Route: {day.route_summary}\n"
            f"    Day cost: ₹{day.total_cost}\n"
        )

    affected = (
        f"Day {event.affected_day + 1}"
        if event.affected_day is not None
        else "Auto-detect affected day(s)"
    )

    return f"""CURRENT ITINERARY for {itinerary.destination}:
{days_text}
Total spent: ₹{itinerary.total_cost}
Budget remaining: ₹{itinerary.budget_remaining}
Original budget: ₹{itinerary.total_cost + itinerary.budget_remaining}

--- DISRUPTION EVENT ---
Type: {event.trigger.value}
Details: {event.details}
Affected: {affected}

Rebuild the itinerary. Only modify what's necessary.
Keep the same date range and maintain budget ≤ ₹{itinerary.total_cost + itinerary.budget_remaining}."""


async def replan_itinerary(
    itinerary: Itinerary,
    event: ReplanEvent,
) -> ReplanResult:
    """
    Replan an itinerary in response to a disruption event.

    Args:
        itinerary: The current itinerary
        event: What triggered the replan

    Returns:
        ReplanResult with updated itinerary, changes list, and reasoning
    """
    system_prompt = _build_replan_system_prompt()
    user_prompt = _build_replan_prompt(itinerary, event)

    # Use Flash for fast replanning (speed matters for live updates)
    raw = generate_json(
        prompt=user_prompt,
        system_instruction=system_prompt,
        use_pro=False,
        temperature=0.5,  # Lower temp for more focused changes
    )

    # Parse the updated itinerary
    from execution.itinerary_engine import _parse_itinerary
    original_budget = itinerary.total_cost + itinerary.budget_remaining
    updated = _parse_itinerary(raw, original_budget)

    return ReplanResult(
        updated_itinerary=updated,
        changes_summary=raw.get("changes_summary", ["Itinerary updated"]),
        reasoning=raw.get(
            "reasoning",
            "The itinerary was adjusted to accommodate the disruption.",
        ),
    )
