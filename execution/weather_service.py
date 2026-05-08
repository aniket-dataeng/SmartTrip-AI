"""
Weather service for SmartTrip-AI.
Fetches weather forecasts to trigger replanning events.
Falls back to mock data if no API key is configured.
"""

import os
import httpx
from dotenv import load_dotenv
from execution.models import WeatherInfo

load_dotenv()

_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
_BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"


async def get_forecast(
    destination: str,
    dates: list[str],
) -> list[WeatherInfo]:
    """
    Fetch weather forecast for a destination.
    Uses OpenWeatherMap if API key exists, else returns mock data.

    Args:
        destination: City name
        dates: List of date strings (YYYY-MM-DD)

    Returns:
        List of WeatherInfo for each requested date
    """
    if _API_KEY:
        return await _fetch_live(destination, dates)
    return _mock_forecast(destination, dates)


async def _fetch_live(
    destination: str,
    dates: list[str],
) -> list[WeatherInfo]:
    """Call OpenWeatherMap API for real forecasts."""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(
                _BASE_URL,
                params={
                    "q": destination,
                    "appid": _API_KEY,
                    "units": "metric",
                    "cnt": 40,  # 5-day forecast in 3h intervals
                },
            )
            resp.raise_for_status()
            data = resp.json()

        date_set = set(dates)
        forecasts = []
        seen_dates = set()

        for item in data.get("list", []):
            date_str = item["dt_txt"].split(" ")[0]
            if date_str in date_set and date_str not in seen_dates:
                seen_dates.add(date_str)
                weather = item["weather"][0]
                main = item["main"]
                is_rainy = weather["main"].lower() in (
                    "rain", "drizzle", "thunderstorm",
                )
                forecasts.append(WeatherInfo(
                    date=date_str,
                    condition=weather["main"],
                    temp_celsius=round(main["temp"], 1),
                    is_rainy=is_rainy,
                    description=weather["description"],
                ))

        return forecasts

    except Exception as e:
        # Graceful fallback to mock on API failure
        print(f"Weather API error: {e}, using mock data")
        return _mock_forecast(destination, dates)


def _mock_forecast(
    destination: str,
    dates: list[str],
) -> list[WeatherInfo]:
    """Generate realistic mock weather data for demo purposes."""
    import random
    random.seed(hash(destination))

    conditions = [
        ("Clear", "clear sky", False),
        ("Clouds", "scattered clouds", False),
        ("Rain", "light rain", True),
        ("Clear", "sunny", False),
        ("Clouds", "overcast clouds", False),
    ]

    forecasts = []
    for i, date in enumerate(dates):
        cond = conditions[i % len(conditions)]
        forecasts.append(WeatherInfo(
            date=date,
            condition=cond[0],
            temp_celsius=round(25 + random.uniform(-5, 10), 1),
            is_rainy=cond[2],
            description=cond[1],
        ))

    return forecasts
