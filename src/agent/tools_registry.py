import json
from typing import Any, List

from src.domain.budget import calculate_budget_plan
from src.domain.packing import build_packing_checklist
from src.services.currency_service import get_currency_rate
from src.services.search_service import get_search_tool
from src.services.weather_service import fetch_weather_forecast


def consultar_previsao_tempo(cidade: str, dias: int = 5) -> str:
    """Consulta a previsão meteorológica de uma cidade para até 16 dias.

    Args:
        cidade (str): Nome da cidade de destino (ex: "Salvador", "Paris, França").
        dias (int): Quantidade de dias da previsão (1 a 16).

    Returns:
        str: JSON com temperaturas máximas, mínimas, condição do tempo e probabilidade de chuva.
    """
    data = fetch_weather_forecast(city=cidade, days=dias)
    return json.dumps(data, ensure_ascii=False, indent=2)


def calcular_orcamento_viagem(dias: int, viajantes: int = 1, perfil: str = "moderado") -> str:
    """Calcula matematicamente a estimativa de custos da viagem por categoria em Reais (BRL).

    Args:
        dias (int): Duração da viagem em dias.
        viajantes (int): Quantidade de pessoas.
        perfil (str): Perfil de gastos ("economico", "moderado" ou "luxo").

    Returns:
        str: JSON com custos de alimentação, passeios, transporte local e reserva de emergência.
    """
    data = calculate_budget_plan(days=dias, travelers=viajantes, profile=perfil)
    return json.dumps(data, ensure_ascii=False, indent=2)


def converter_moeda(valor: float, moeda_origem: str = "USD") -> str:
    """Converte um valor monetário estrangeiro para Reais (BRL) usando cotação de mercado.

    Args:
        valor (float): Quantidade monetária a ser convertida.
        moeda_origem (str): Código internacional da moeda (ex: "USD", "EUR", "GBP", "ARS", "JPY").

    Returns:
        str: JSON com a cotação utilizada e o valor final convertido em BRL.
    """
    data = get_currency_rate(amount=valor, from_currency=moeda_origem)
    return json.dumps(data, ensure_ascii=False, indent=2)


def gerar_checklist_mala(
    dados_clima_json: str,
    dias: int = 5,
    tipo_viagem: str = "cidade"
) -> str:
    """Gera uma lista inteligente de bagagem personalizada baseada no clima e tipo de viagem.

    Args:
        dados_clima_json (str): JSON com dados da previsão retornado por consultar_previsao_tempo.
        dias (int): Duração da viagem em dias.
        tipo_viagem (str): Estilo da viagem ("cidade", "praia", "natureza" ou "neve").

    Returns:
        str: JSON com itens organizados em vestuário, documentos, tecnologia e cuidados pessoais.
    """
    try:
        if isinstance(dados_clima_json, str):
            weather_data = json.loads(dados_clima_json)
        else:
            weather_data = dados_clima_json
    except Exception:
        weather_data = {}

    data = build_packing_checklist(weather_data=weather_data, days=dias, trip_type=tipo_viagem)
    return json.dumps(data, ensure_ascii=False, indent=2)


def get_agent_tools() -> List[Any]:
    """Reúne e retorna a lista completa de ferramentas para o Agente."""
    tools: List[Any] = [
        consultar_previsao_tempo,
        calcular_orcamento_viagem,
        converter_moeda,
        gerar_checklist_mala,
    ]

    search_tool = get_search_tool()
    if search_tool:
        tools.append(search_tool)

    return tools
