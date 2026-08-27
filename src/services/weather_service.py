from datetime import datetime
from functools import lru_cache
import json
from typing import Any, Dict
import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

DIAS_SEMANA_PT = [
    "segunda-feira",
    "terça-feira",
    "quarta-feira",
    "quinta-feira",
    "sexta-feira",
    "sábado",
    "domingo",
]

WMO_WEATHER_CODES: Dict[int, str] = {
    0: "Céu limpo e ensolarado",
    1: "Predominantemente limpo",
    2: "Parcialmente nublado",
    3: "Nublado",
    45: "Nevoeiro denso",
    48: "Nevoeiro com geada",
    51: "Garoa leve",
    53: "Garoa moderada",
    55: "Garoa forte",
    61: "Chuva fraca",
    63: "Chuva moderada",
    65: "Chuva forte",
    71: "Neve fraca",
    73: "Neve moderada",
    75: "Neve intensa",
    80: "Pancada de chuva fraca",
    81: "Pancada de chuva moderada",
    82: "Pancada de chuva torrencial",
    95: "Tempestade com trovoadas",
    96: "Tempestade com granizo leve",
    99: "Tempestade severa com granizo",
}


@lru_cache(maxsize=32)
def _cached_weather_json(city: str, days: int) -> str:
    """Faz requisição rápida com cache para evitar chamadas duplicadas."""
    # 1. Geocodificação rápida
    geo_res = requests.get(
        GEOCODING_URL,
        params={"name": city, "count": 1, "language": "pt", "format": "json"},
        timeout=5,
    )
    geo_res.raise_for_status()
    geo_data = geo_res.json()

    results = geo_data.get("results")
    if not results:
        return json.dumps({
            "erro": f"Localização '{city}' não encontrada. Tente com estado/país."
        })

    place = results[0]
    safe_days = min(max(int(days), 1), 16)

    # 2. Previsão
    params = {
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "daily": "weathercode,temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "timezone": "auto",
        "forecast_days": safe_days,
    }

    forecast_res = requests.get(FORECAST_URL, params=params, timeout=5)
    forecast_res.raise_for_status()
    daily = forecast_res.json().get("daily", {})

    forecast_list = []
    for i, date_str in enumerate(daily.get("time", [])):
        code = daily["weathercode"][i]
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            dia_semana = DIAS_SEMANA_PT[dt.weekday()]
            data_formatada = dt.strftime("%d/%m/%Y")
            rotulo_dia = f"{data_formatada} ({dia_semana})"
        except Exception:
            rotulo_dia = date_str
            data_formatada = date_str
            dia_semana = ""

        forecast_list.append({
            "dia": rotulo_dia,
            "data": data_formatada,
            "dia_semana": dia_semana,
            "condicao": WMO_WEATHER_CODES.get(code, f"Código {code}"),
            "temp_max_c": daily["temperature_2m_max"][i],
            "temp_min_c": daily["temperature_2m_min"][i],
            "prob_chuva_pct": daily["precipitation_probability_max"][i],
        })

    return json.dumps({
        "cidade": f"{place.get('name')}, {place.get('country', '')}".strip(", "),
        "pais": place.get("country_code", "BR"),
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "dias_solicitados": safe_days,
        "previsao": forecast_list,
    }, ensure_ascii=False)



def fetch_weather_forecast(city: str, days: int = 5, timeout: int = 5) -> Dict[str, Any]:
    """Consulta a API gratuita do Open-Meteo para obter a previsão do tempo."""
    try:
        data_str = _cached_weather_json(city.strip().lower(), int(days))
        return json.loads(data_str)
    except Exception as exc:
        return {"erro": f"Não foi possível obter clima para '{city}': {str(exc)}"}
