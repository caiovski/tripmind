import os

from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.groq import Groq
from agno.tools.tavily import TavilyTools
from dotenv import load_dotenv

from travel_tools import calculate_travel_budget, convert_currency, generate_packing_list, get_weather

load_dotenv()


def _dummy_web_search(query: str) -> str:
    """Busca na web quando o Tavily não está configurado.

    Args:
        query (str): Termo de busca.

    Returns:
        str: Aviso de que a busca não está disponível.
    """
    return "Busca web não disponível (TAVILY_API_KEY não configurada). Use seu conhecimento e a previsão do tempo."

INSTRUCTIONS = """Você é o TripMind, um assistente roteirista de viagens em português do Brasil.

Seu trabalho é montar roteiros de viagem personalizados e interativos. SEMPRE siga este fluxo:

1. CLIMA: chame get_weather(cidade, dias) para saber a previsão dos dias da viagem.
2. PESQUISA: use TavilyTools para buscar atrações, eventos sazonais e restaurantes bem avaliados
   no destino (em português).
3. ROTEIRO: monte a programação dia a dia em Manhã / Tarde / Noite, adaptando ao clima:
   - Dia chuvoso ou frio: museus, cafés, shoppings, exposições, spas (atrações cobertas).
   - Dia ensolarado e quente: praias, parques, trilhas, passeios ao ar livre.
   Intercale também um ritmo razoável (não encha o dia) e respeite os interesses do viajante.
4. ORÇAMENTO: chame calculate_travel_budget(dias, viajantes, perfil) e inclua os valores no roteiro.
5. MALA: chame generate_packing_list com o JSON do clima e o tipo de viagem (praia, cidade, natureza ou neve).
6. MOEDA E CULTURA:
   - Viagem internacional: use convert_currency para mostrar custos em reais e dê dicas de etiqueta
     cultural (gorjetas, costumes, transporte público, expressões úteis).
   - Viagem nacional (Brasil): destaque pratos típicos regionais, gírias locais e recomendações de segurança.

REGRAS:
- Responda sempre em português do Brasil, com formatação markdown e tabelas quando útil.
- Seja conciso e organizado: seções claras com cabeçalhos (##), sem repetir informações.
- Se o usuário pedir ajustes no roteiro, aplique as mudanças mantendo as demais partes.
- Se algum dado (clima, cotações) não puder ser obtido, avise e continue com o que tiver."""


def build_agent(debug: bool = False) -> Agent:
    provider = os.getenv("MODEL_PROVIDER", "gemini").strip().lower()
    if provider == "groq":
        model = Groq(id="llama-3.3-70b-versatile")
    else:
        model = Gemini(id="gemini-3.5-flash", retries=3, delay_between_retries=6.0)

    tools = [
        get_weather,
        calculate_travel_budget,
        convert_currency,
        generate_packing_list,
    ]
    if os.getenv("TAVILY_API_KEY"):
        tools.append(TavilyTools())
    else:
        tools.append(_dummy_web_search)

    return Agent(
        model=model,
        tools=tools,
        instructions=INSTRUCTIONS,
        markdown=True,
        debug_mode=debug,
    )


if __name__ == "__main__":
    agent = build_agent()
    print("=== TripMind CLI (CTRL+C para sair) ===")
    while True:
        mensagem = input("\nVocê: ")
        if mensagem.strip().lower() in ("sair", "exit", "quit"):
            break
        agent.print_response(mensagem)