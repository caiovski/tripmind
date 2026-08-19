# Tasks: TripMind Travel Agent

## Setup

- [x] Criar venv e instalar dependências (`pip install -r scripts/requirements.txt`)
- [x] Adicionar dependências novas ao `requirements.txt`: `google-genai`, `streamlit`
- [x] Criar `.env` a partir de template com `GROQ_API_KEY`, `TAVILY_API_KEY`, `GEMINI_API_KEY`, `MODEL_PROVIDER`
- [ ] Obter chaves: Gemini (aistudio.google.com), Tavily (tavily.com), Groq (console.groq.com)

## Tools customizadas (módulo `travel_tools.py`)

- [x] Implementar `get_weather(city, days)` via Open-Meteo (sem chave)
- [x] Implementar `calculate_travel_budget(days, travelers, profile, currency)` (perfis Econômico/Moderado/Luxo; categorias: Alimentação, Passeios, Transporte Local, Emergência)
- [x] Implementar `generate_packing_list(weather_forecast, days, trip_type)` (checklist por clima: praia, frio, chuva, urbano)

## Agente (módulo `agent.py`)

- [x] Criar agente `agno` com modelo configurável (Gemini 3.5 Flash padrão, Groq fallback)
- [x] Registrar tools: `TavilyTools`, `YFinanceTools`, e as 3 tools customizadas
- [x] Escrever instruções em português: roteiro Manhã/Tarde/Noite, adaptação ao clima, lógica nacional vs internacional (moeda + dicas culturais), formatação markdown

## Teste CLI

- [x] Testar o agente por linha de comando (padrão `script04.py`): viagem internacional (ex: Lisboa)
- [x] Testar viagem nacional (ex: Salvador) e conferir lógica adaptativa
- [x] Validar orçamento e mala com saídas consistentes

## Interface Streamlit (`app.py`)

- [x] Formulário: destino, dias, orçamento, estilo, interesses
- [x] Exibição do roteiro em cards (markdown) e seções de orçamento/mala/dicas
- [x] Chat de ajustes conversando com o mesmo agente
- [x] Spinner/feedback durante chamadas longas de tools

## Finalização

- [ ] Teste ponta a ponta completo (formulário → roteiro → ajuste via chat)
- [ ] README com instruções de execução, variáveis de ambiente e demo
- [ ] Commitar mudanças
