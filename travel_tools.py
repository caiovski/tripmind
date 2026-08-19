import json
from datetime import date

import requests
import yfinance as yf

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

WMO_CODES = {
    0: "Céu limpo",
    1: "Predominantemente limpo",
    2: "Parcialmente nublado",
    3: "Nublado",
    45: "Nevoeiro",
    48: "Nevoeiro com geada",
    51: "Garoa fraca",
    53: "Garoa",
    55: "Garoa forte",
    61: "Chuva fraca",
    63: "Chuva",
    65: "Chuva forte",
    71: "Neve fraca",
    73: "Neve",
    75: "Neve forte",
    80: "Pancada de chuva fraca",
    81: "Pancada de chuva",
    82: "Pancada de chuva forte",
    95: "Tempestade",
    96: "Tempestade com granizo",
    99: "Tempestade forte com granizo",
}

BUDGET_TABLE = {
    "economico": {"alimentacao": 60, "passeios": 40, "transporte": 30, "emergencia_pct": 0.10},
    "moderado": {"alimentacao": 150, "passeios": 100, "transporte": 70, "emergencia_pct": 0.10},
    "luxo": {"alimentacao": 400, "passeios": 300, "transporte": 200, "emergencia_pct": 0.15},
}


def get_weather(city: str, days: int = 5) -> str:
    """Busca a previsão do tempo de uma cidade para os próximos dias.

    Args:
        city (str): Nome da cidade (ex: "Varginha", "Lisboa, Portugal").
        days (int): Quantos dias de previsão (1 a 16).

    Returns:
        str: JSON com localização e a previsão diária (condição, máx, mín,
        probabilidade de chuva), usada para montar roteiros e malas.
    """
    geo = requests.get(
        GEOCODING_URL,
        params={"name": city, "count": 1, "language": "pt", "format": "json"},
        timeout=15,
    )
    geo.raise_for_status()
    results = geo.json().get("results")
    if not results:
        return json.dumps({"error": f"Não encontrei a cidade '{city}'. Tente com mais detalhes (ex: Lisboa, Portugal)."}, ensure_ascii=False)

    place = results[0]
    params = {
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "daily": "weathercode,temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "timezone": "auto",
        "forecast_days": min(max(days, 1), 16),
    }
    resp = requests.get(FORECAST_URL, params=params, timeout=15)
    resp.raise_for_status()
    daily = resp.json()["daily"]

    forecast = []
    for i, day in enumerate(daily["time"]):
        code = daily["weathercode"][i]
        forecast.append(
            {
                "dia": day,
                "condicao": WMO_CODES.get(code, f"Código {code}"),
                "temp_max_c": daily["temperature_2m_max"][i],
                "temp_min_c": daily["temperature_2m_min"][i],
                "prob_chuva_pct": daily["precipitation_probability_max"][i],
            }
        )

    return json.dumps(
        {
            "cidade": f"{place.get('name')}, {place.get('country', '')}",
            "pais": place.get("country_code"),
            "latitude": place["latitude"],
            "longitude": place["longitude"],
            "previsao": forecast,
        },
        ensure_ascii=False,
        indent=2,
    )


def calculate_travel_budget(days: int, travelers: int = 1, profile: str = "moderado") -> str:
    """Estima o custo total da viagem em reais (BRL) por categoria.

    Args:
        days (int): Quantidade de dias da viagem.
        travelers (int): Quantidade de viajantes.
        profile (str): Perfil de gastos: "economico", "moderado" ou "luxo".

    Returns:
        str: JSON com custo diário e total por categoria (Alimentação,
        Passeios, Transporte local) e reserva de emergência.
    """
    profile = (profile or "moderado").lower().strip()
    table = BUDGET_TABLE.get(profile)
    if not table:
        return json.dumps({"error": f"Perfil inválido '{profile}'. Use: economico, moderado ou luxo."}, ensure_ascii=False)

    dias = max(int(days), 1)
    viajantes = max(int(travelers), 1)

    alimentacao = table["alimentacao"] * dias * viajantes
    passeios = table["passeios"] * dias * viajantes
    transporte = table["transporte"] * dias * viajantes
    subtotal = alimentacao + passeios + transporte
    emergencia = round(subtotal * table["emergencia_pct"])
    total = subtotal + emergencia

    return json.dumps(
        {
            "perfil": profile,
            "dias": dias,
            "viajantes": viajantes,
            "moeda": "BRL",
            "categorias": {
                "alimentacao_brl": alimentacao,
                "passeios_brl": passeios,
                "transporte_local_brl": transporte,
                "emergencia_brl": emergencia,
            },
            "subtotal_brl": subtotal,
            "total_brl": total,
        },
        ensure_ascii=False,
        indent=2,
    )


def convert_currency(amount: float, from_currency: str = "USD") -> str:
    """Converte um valor em moeda estrangeira para reais (BRL) usando a cotação atual.

    Args:
        amount (float): Valor a converter.
        from_currency (str): Código ISO da moeda (ex: USD, EUR, GBP, JPY).

    Returns:
        str: JSON com a cotação usada e o valor convertido em reais.
    """
    from_currency = (from_currency or "USD").upper()
    try:
        ticker = yf.Ticker(f"{from_currency}BRL=X")
        hist = ticker.history(period="1d")
        if not hist.empty:
            rate = float(hist["Close"].iloc[-1])
            converted = round(float(amount) * rate, 2)
            return json.dumps(
                {"moeda_origem": from_currency, "cotacao_brl": rate, "valor_original": float(amount), "valor_em_brl": converted},
                ensure_ascii=False,
                indent=2,
            )
        ticker = yf.Ticker(f"BRL{from_currency}=X")
        hist = ticker.history(period="1d")
        if not hist.empty:
            rate = 1 / float(hist["Close"].iloc[-1])
            converted = round(float(amount) * rate, 2)
            return json.dumps(
                {"moeda_origem": from_currency, "cotacao_brl": rate, "valor_original": float(amount), "valor_em_brl": converted},
                ensure_ascii=False,
                indent=2,
            )
        return json.dumps({"error": f"Não encontrei cotação para '{from_currency}BRL=X'."}, ensure_ascii=False)
    except Exception as exc:
        return json.dumps({"error": f"Falha ao obter cotação: {exc}"}, ensure_ascii=False)


def generate_packing_list(weather_json: str, days: int = 5, trip_type: str = "cidade") -> str:
    """Gera um checklist de mala baseado na previsão do tempo e no tipo de viagem.

    Args:
        weather_json (str): JSON de previsão retornado por get_weather.
        days (int): Duração da viagem em dias.
        trip_type (str): "praia", "cidade", "natureza" ou "neve".

    Returns:
        str: JSON com categorias e itens de bagagem.
    """
    try:
        weather = json.loads(weather_json)
        forecast = weather.get("previsao", [])
    except Exception:
        return json.dumps({"error": "Previsão do tempo inválida. Chame get_weather antes."}, ensure_ascii=False)

    trip_type = (trip_type or "cidade").lower().strip()
    dias = max(int(days), 1)
    dias_chuva = sum(1 for d in forecast if d.get("prob_chuva_pct", 0) >= 50)
    dias_frio = sum(1 for d in forecast if d.get("temp_max_c", 30) <= 15)
    dias_calor = sum(1 for d in forecast if d.get("temp_max_c", 20) >= 30)
    temp_max = max((d.get("temp_max_c", 0) for d in forecast), default=20)

    itens = {
        "documentos_e_dinheiro": [
            "Documento de identidade / passaporte",
            "Cartão de crédito e débito",
            "Dinheiro em espécie (moeda local)",
            "Cartão SUS / plano de saúde e receitas",
            "Passagens e reservas impressas ou no celular",
        ],
        "tecnologia": [
            "Celular com carregador",
            "Carregador portátil (power bank)",
            "Fones de ouvido",
            "Adaptador de tomada" if weather.get("pais") not in (None, "BR") else "Fita e adaptador simples",
        ],
        "higiene_e_saude": [
            "Kit de higiene (escova, pasta, desodorante)",
            "Protetor solar" if temp_max >= 25 else "Hidratante para a pele",
            "Repelente",
            "Medicamentos pessoais e kit primeiros socorros",
            "Máscara de dormir e protetor auricular",
        ],
    }

    roupas = ["Roupas íntimas (uma por dia + 1 extra)"]
    if trip_type == "praia":
        roupas += ["Roupa de banho (2 peças)", "Canga/toalha de praia", "Camisas leves e shorts", "Chinelo e sandália", "Óculos de sol e chapéu"]
    elif trip_type == "neve":
        roupas += ["Casaco térmico impermeável", "Calça de neve", "Luvas, gorro e cachecol", "Meias grossas", "Botas impermeáveis"]
    elif trip_type == "natureza":
        roupas += ["Roupas leves e confortáveis", "Tênis de trilha", "Corta-vento ou jaqueta leve", "Boné", "Mochila de hidratação"]
    else:
        roupas += ["Roupas confortáveis para o dia", "Uma roupa social para a noite", "Tênis casual", "Casaco leve ou jaqueta"]

    if dias_chuva > 0:
        roupas.append("Guarda-chuva compacto e capa de chuva")
    if dias_frio > 0:
        roupas.append("Casaco quente e cachecol")
    if dias_calor > 0:
        roupas.append("Roupas de tecido leve e boné")

    itens["roupas"] = roupas
    itens["resumo_clima"] = {
        "dias_chuva": dias_chuva,
        "dias_frio": dias_frio,
        "dias_calor": dias_calor,
        "temp_max_c": temp_max,
    }

    return json.dumps(itens, ensure_ascii=False, indent=2)