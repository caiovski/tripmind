from typing import Optional
from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.groq import Groq

from src.agent.prompts import TRIPMIND_SYSTEM_PROMPT
from src.agent.tools_registry import get_agent_tools
from src.config.settings import Settings, get_settings


def create_travel_agent(
    settings: Optional[Settings] = None,
    override_provider: Optional[str] = None,
    debug: Optional[bool] = None,
) -> Agent:
    """Fábrica para instanciar e configurar o Agente TripMind com Agno."""
    cfg = settings or get_settings()
    provider = (override_provider or cfg.model_provider).strip().lower()
    is_debug = debug if debug is not None else cfg.debug_mode

    # Seleção do modelo de linguagem (LLM)
    if provider == "groq" and cfg.has_groq:
        model = Groq(
            id=cfg.groq_model_id,
            api_key=cfg.groq_api_key,
        )
    else:
        # Padrão: Gemini 3.6 Flash
        model = Gemini(
            id=cfg.gemini_model_id,
            api_key=cfg.gemini_api_key,
            retries=1,
            delay_between_retries=1.0,
        )

    tools = get_agent_tools()

    return Agent(
        name="TripMind AI",
        model=model,
        tools=tools,
        instructions=TRIPMIND_SYSTEM_PROMPT,
        markdown=True,
        debug_mode=is_debug,
    )
