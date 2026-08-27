from typing import Any, Dict

# Tabela base de diárias por pessoa em BRL
BUDGET_DAILY_RATES: Dict[str, Dict[str, float]] = {
    "economico": {
        "alimentacao": 60.0,
        "passeios": 40.0,
        "transporte": 30.0,
        "emergencia_pct": 0.10,
    },
    "moderado": {
        "alimentacao": 150.0,
        "passeios": 100.0,
        "transporte": 70.0,
        "emergencia_pct": 0.10,
    },
    "luxo": {
        "alimentacao": 400.0,
        "passeios": 300.0,
        "transporte": 200.0,
        "emergencia_pct": 0.15,
    },
}


def calculate_budget_plan(
    days: int,
    travelers: int = 1,
    profile: str = "moderado"
) -> Dict[str, Any]:
    """Calcula determinística e matematicamente o orçamento de viagem.

    Regra de negócio pura: não faz chamadas a LLM e nem a rede.

    Args:
        days (int): Quantidade de dias da viagem (mínimo 1).
        travelers (int): Quantidade de viajantes (mínimo 1).
        profile (str): "economico", "moderado" ou "luxo".

    Returns:
        Dict[str, Any]: Detalhamento dos custos por categoria e totais em BRL.
    """
    normalized_profile = (profile or "moderado").lower().strip()
    rate_table = BUDGET_DAILY_RATES.get(normalized_profile, BUDGET_DAILY_RATES["moderado"])

    safe_days = max(int(days), 1)
    safe_travelers = max(int(travelers), 1)

    alimentacao = round(rate_table["alimentacao"] * safe_days * safe_travelers, 2)
    passeios = round(rate_table["passeios"] * safe_days * safe_travelers, 2)
    transporte = round(rate_table["transporte"] * safe_days * safe_travelers, 2)
    subtotal = round(alimentacao + passeios + transporte, 2)

    emergencia = round(subtotal * rate_table["emergencia_pct"], 2)
    total = round(subtotal + emergencia, 2)
    diaria_media_por_pessoa = round(total / (safe_days * safe_travelers), 2)

    return {
        "perfil": normalized_profile,
        "dias": safe_days,
        "viajantes": safe_travelers,
        "moeda": "BRL",
        "categorias": {
            "alimentacao_brl": alimentacao,
            "passeios_brl": passeios,
            "transporte_local_brl": transporte,
            "emergencia_brl": emergencia,
        },
        "subtotal_brl": subtotal,
        "total_brl": total,
        "diaria_media_por_pessoa_brl": diaria_media_por_pessoa,
    }
