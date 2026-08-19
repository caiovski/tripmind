# TripMind AI — Assistente Roteirista de Viagens

Agente de IA que monta roteiros de viagem personalizados: clima, atrações, orçamento, checklist de mala e dicas culturais.

## Pré-requisitos

- Python 3.12+
- Chaves de API (opcionais, mas recomendadas):
  - `GEMINI_API_KEY` — [Google AI Studio](https://aistudio.google.com) (essencial, tier gratuito)
  - `TAVILY_API_KEY` — [Tavily](https://app.tavily.com) (pesquisa web em tempo real)
  - `GROQ_API_KEY` — [Groq](https://console.groq.com) (modelo alternativo)

## Instalação

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r scripts/requirements.txt
cp .env.example .env   # preencha as chaves
```

## Execução

Interface web (Streamlit):

```bash
streamlit run app.py
```

Teste por linha de comando:

```bash
python agent.py
```

## Configuração (`.env`)

| Variável | Descrição |
|----------|-----------|
| `GEMINI_API_KEY` | Chave do Gemini (modelo padrão: `gemini-3.5-flash`) |
| `TAVILY_API_KEY` | Ativa a pesquisa web; sem ela o agente segue sem busca |
| `GROQ_API_KEY` | Chave do Groq (usada se `MODEL_PROVIDER=groq`) |
| `MODEL_PROVIDER` | `gemini` (padrão) ou `groq` |

## Arquitetura

```
app.py (Streamlit) → agent.py (agno) → tools
                                        ├─ get_weather (Open-Meteo, sem chave)
                                        ├─ calculate_travel_budget (determinístico)
                                        ├─ convert_currency (yfinance)
                                        ├─ generate_packing_list (determinístico)
                                        └─ TavilyTools (busca web, se chave presente)
```

## Funcionalidades

- Roteiro dia a dia (Manhã/Tarde/Noite) adaptado ao clima: chuva/frio → atrações cobertas; sol → atividades ao ar livre
- Pesquisa em tempo real de atrações, eventos e restaurantes (Tavily)
- Orçamento por perfil (Econômico/Moderado/Luxo) calculado por função determinística
- Conversão de moeda para BRL (yfinance)
- Checklist de mala baseado no clima e tipo de viagem (praia, cidade, natureza, neve)
- Dicas culturais: internacional → etiqueta, gorjetas, expressões; nacional → pratos típicos, gírias, segurança

## Projeto de disciplina

Proposta e design: `openspec/changes/tripmind-travel-agent/`