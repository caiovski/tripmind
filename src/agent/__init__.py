"""Camada de Agente do TripMind AI.

Orquestra modelos de linguagem (Gemini/Groq), prompts e registro de ferramentas.
"""

from src.agent.agent_factory import create_travel_agent

__all__ = ["create_travel_agent"]
