"""Camada de Serviços & Adaptadores Externos do TripMind AI.

Contém clientes de APIs de terceiros (Open-Meteo, yFinance, Tavily).
"""

from src.services.currency_service import get_currency_rate
from src.services.search_service import get_search_tool
from src.services.weather_service import fetch_weather_forecast

__all__ = [
    "fetch_weather_forecast",
    "get_currency_rate",
    "get_search_tool",
]
