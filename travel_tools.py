"""TripMind AI - Módulo de Ferramentas (Compatibilidade).

Reexporta as funções de domínio e serviços para manter compatibilidade
com scripts anteriores.
"""

from src.agent.tools_registry import (
    calcular_orcamento_viagem as calculate_travel_budget,
    consultar_previsao_tempo as get_weather,
    converter_moeda as convert_currency,
    gerar_checklist_mala as generate_packing_list,
)

__all__ = [
    "get_weather",
    "calculate_travel_budget",
    "convert_currency",
    "generate_packing_list",
]