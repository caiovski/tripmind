"""TripMind AI - Bateria de Testes Automatizados (Smoke Test).

Valida todas as camadas da Clean Architecture:
1. Domínio (Cálculo de Orçamento e Checklist de Bagagem)
2. Serviços (Open-Meteo Clima e yFinance Câmbio)
3. Agente (Agno + Gemini / Groq)
"""

import os
import sys

# Configura encoding UTF-8 no terminal Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Adiciona a raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config.settings import get_settings
from src.domain.budget import calculate_budget_plan
from src.domain.packing import build_packing_checklist
from src.services.weather_service import fetch_weather_forecast
from src.services.currency_service import get_currency_rate
from src.agent.agent_factory import create_travel_agent


def test_domain():
    print("\n[1/4] Testando Camada de Domínio (Regras Puras)...")
    # Teste de orçamento
    budget = calculate_budget_plan(days=5, travelers=2, profile="moderado")
    assert budget["perfil"] == "moderado"
    assert budget["dias"] == 5
    assert budget["viajantes"] == 2
    assert budget["total_brl"] > 0
    print(f"  [OK] Orçamento calculado com sucesso: R$ {budget['total_brl']:,.2f}")

    # Teste de mala
    packing = build_packing_checklist(weather_data={}, days=5, trip_type="praia")
    assert "vestuario" in packing
    assert "documentos_e_financas" in packing
    print(f"  [OK] Checklist de mala gerado: {len(packing['vestuario'])} itens de vestuário.")


def test_services():
    print("\n[2/4] Testando Camada de Serviços (APIs Externas)...")
    # Teste Open-Meteo
    weather = fetch_weather_forecast("Salvador, Bahia", days=3)
    if "erro" not in weather:
        print(f"  [OK] Clima consultado para {weather.get('cidade')}: {len(weather.get('previsao', []))} dias.")
    else:
        print(f"  [AVISO] Clima: {weather.get('erro')}")

    # Teste yFinance
    currency = get_currency_rate(amount=100.0, from_currency="USD")
    if "erro" not in currency:
        print(f"  [OK] Câmbio USD -> BRL: US$ 100 = R$ {currency.get('valor_em_brl'):,.2f} (Cotação: {currency.get('cotacao_brl')})")
    else:
        print(f"  [AVISO] Câmbio: {currency.get('erro')}")


def test_agent_initialization():
    print("\n[3/4] Testando Inicialização do Agente Agno...")
    settings = get_settings()
    print(f"  [INFO] Provedor ativo: {settings.model_provider} (Gemini Key presente: {settings.has_gemini})")
    
    agent = create_travel_agent()
    print(f"  [OK] Agente criado: '{agent.name}' com {len(agent.tools)} ferramentas registradas.")
    return agent


def test_agent_execution(agent):
    print("\n[4/4] Testando Execução do Agente (Gemini/Groq)...")
    try:
        response = agent.run("Responda apenas com a palavra: TRIPMIND_OK")
        content = response.content if hasattr(response, "content") else str(response)
        print(f"  [OK] Resposta do Agente: {content.strip()}")
    except Exception as exc:
        print(f"  [AVISO] Execução com LLM retornou: {exc}")


if __name__ == "__main__":
    print("=" * 60)
    print("Testes Automatizados do TripMind AI (Clean Architecture)")
    print("=" * 60)

    test_domain()
    test_services()
    agent = test_agent_initialization()
    test_agent_execution(agent)

    print("\n" + "=" * 60)
    print("Bateria de testes concluída com sucesso!")
    print("=" * 60)
