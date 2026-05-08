"""
Tests for budget optimizer and route optimizer.
"""

import pytest
from execution.models import TripInput, DateRange, TravelStyle
from execution.budget_optimizer import allocate_budget, check_budget_health
from execution.route_optimizer import optimize_route, build_route_summary


class TestBudgetOptimizer:
    """Validate budget allocation logic."""

    def _make_trip(self, budget=10000, style=TravelStyle.MODERATE):
        return TripInput(
            destination="Bangalore",
            budget=budget,
            dates=DateRange(start="2026-05-10", end="2026-05-12"),
            interests=["cafes"],
            travel_style=style,
        )

    def test_even_split_across_days(self):
        result = allocate_budget(self._make_trip(9000), num_days=3)
        assert result["per_day"] == 3000
        assert result["total"] == 9000

    def test_category_ratios_moderate(self):
        result = allocate_budget(self._make_trip(10000), num_days=1)
        cats = result["categories"]
        assert cats["activities"] == 3500  # 35% of 10000
        assert cats["food"] == 3000       # 30%

    def test_tight_budget_flag(self):
        result = allocate_budget(self._make_trip(2000), num_days=3)
        assert result["is_tight"] is True

    def test_comfortable_budget_flag(self):
        result = allocate_budget(self._make_trip(15000), num_days=3)
        assert result["is_tight"] is False

    def test_zero_days_raises(self):
        with pytest.raises(ValueError):
            allocate_budget(self._make_trip(), num_days=0)

    def test_budget_health_ok(self):
        h = check_budget_health(5000, 10000)
        assert h["status"] == "ok"
        assert h["remaining"] == 5000

    def test_budget_health_warning(self):
        h = check_budget_health(8600, 10000)
        assert h["status"] == "warning"

    def test_budget_health_exceeded(self):
        h = check_budget_health(11000, 10000)
        assert h["status"] == "exceeded"
        assert h["remaining"] == 0


class TestRouteOptimizer:
    """Validate nearest-neighbor routing."""

    def test_single_location(self):
        locs = [{"name": "A", "lat": 0, "lon": 0}]
        result = optimize_route(locs)
        assert len(result) == 1

    def test_three_locations_ordered(self):
        # B is closer to A than C, so A→B→C
        locs = [
            {"name": "A", "lat": 0.0, "lon": 0.0},
            {"name": "C", "lat": 1.0, "lon": 1.0},
            {"name": "B", "lat": 0.1, "lon": 0.1},
        ]
        result = optimize_route(locs)
        names = [r["name"] for r in result]
        assert names == ["A", "B", "C"]

    def test_build_route_summary(self):
        s = build_route_summary(["Cubbon Park", "MG Road", "Lalbagh"])
        assert s == "Cubbon Park → MG Road → Lalbagh"

    def test_build_route_summary_empty(self):
        assert build_route_summary([]) == "No route"
