from functools import lru_cache
from typing import Any, Dict
import yfinance as yf

# Cotações de referência instantâneas para evitar esperas de rede
FALLBACK_RATES: Dict[str, float] = {
    "USD": 5.40,
    "EUR": 5.90,
    "GBP": 7.00,
    "ARS": 0.0055,
    "JPY": 0.036,
    "CLP": 0.0058,
    "UYU": 0.13,
    "CAD": 3.95,
    "AUD": 3.55,
    "CHF": 6.10,
}


@lru_cache(maxsize=32)
def _fetch_live_rate(currency: str) -> float:
    """Busca cotação ao vivo com cache e timeout rápido."""
    ticker = yf.Ticker(f"{currency}BRL=X")
    hist = ticker.history(period="1d", timeout=3)
    if not hist.empty:
        return float(hist["Close"].iloc[-1])
    return FALLBACK_RATES.get(currency, 5.40)


def get_currency_rate(amount: float, from_currency: str = "USD") -> Dict[str, Any]:
    """Converte um valor em moeda estrangeira para reais (BRL) de forma ultrarrápida.

    Args:
        amount (float): Valor monetário na moeda de origem.
        from_currency (str): Código ISO da moeda (ex: "USD", "EUR", "GBP", "JPY", "ARS").

    Returns:
        Dict[str, Any]: Cotação e valor convertido em BRL.
    """
    currency = (from_currency or "USD").upper().strip()
    safe_amount = float(amount)

    if currency in ("BRL", "R$", "REAL"):
        return {
            "moeda_origem": "BRL",
            "cotacao_brl": 1.0,
            "valor_original": safe_amount,
            "valor_em_brl": safe_amount,
        }

    try:
        rate = _fetch_live_rate(currency)
    except Exception:
        rate = FALLBACK_RATES.get(currency, 5.40)

    return {
        "moeda_origem": currency,
        "cotacao_brl": round(rate, 4),
        "valor_original": safe_amount,
        "valor_em_brl": round(safe_amount * rate, 2),
    }
