from typing import Any, Callable
from agno.tools.tavily import TavilyTools
from src.config.settings import get_settings


def _fallback_web_search(query: str) -> str:
    """Ferramenta de fallback quando a chave do Tavily não está presente."""
    return (
        "Busca web externa não configurada (TAVILY_API_KEY ausente). "
        "Utilize a previsão meteorológica obtida e sua ampla base de conhecimento sobre o destino."
    )


def get_search_tool() -> Any:
    """Retorna a ferramenta de busca apropriada (Tavily ou Fallback)."""
    settings = get_settings()
    if settings.has_tavily:
        try:
            return TavilyTools(api_key=settings.tavily_api_key)
        except Exception:
            return _fallback_web_search
    return _fallback_web_search
