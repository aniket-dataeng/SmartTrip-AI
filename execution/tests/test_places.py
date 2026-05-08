"""
Tests for places service curated data and filtering.
"""

import pytest
from execution.places_service import _get_curated_places, _generate_generic_places


class TestCuratedPlaces:
    """Validate curated place data and filtering."""

    def test_bangalore_returns_places(self):
        places = _get_curated_places("Bangalore", ["cafes"])
        assert len(places) > 0
        names = [p["name"] for p in places]
        assert "Third Wave Coffee" in names

    def test_interest_filtering_prioritizes(self):
        places = _get_curated_places("Bangalore", ["cafes"])
        # Cafes should come first
        assert places[0]["category"] in ["cafe", "brewery"]

    def test_photography_interests(self):
        places = _get_curated_places("Bangalore", ["photography"])
        categories = [p["category"] for p in places[:3]]
        assert any(
            c in ["park", "garden", "landmark", "palace"]
            for c in categories
        )

    def test_hyderabad_data(self):
        places = _get_curated_places("Hyderabad", ["food"])
        names = [p["name"] for p in places]
        assert "Paradise Biryani" in names

    def test_unknown_city_returns_generic(self):
        places = _get_curated_places("Timbuktu", ["nature"])
        assert len(places) > 0
        # Generic places have the city name in them
        assert any("Timbuktu" in p["name"] for p in places)


class TestGenericPlaces:
    """Validate generic place generation for unknown cities."""

    def test_generates_six_places(self):
        places = _generate_generic_places("Pune", ["history"])
        assert len(places) == 6

    def test_includes_destination_name(self):
        places = _generate_generic_places("Kolkata", ["food"])
        has_name = any("Kolkata" in p["name"] for p in places)
        assert has_name

    def test_all_have_required_keys(self):
        places = _generate_generic_places("Delhi", ["shopping"])
        for p in places:
            assert "name" in p
            assert "category" in p
            assert "cost" in p
            assert "lat" in p
            assert "lon" in p
