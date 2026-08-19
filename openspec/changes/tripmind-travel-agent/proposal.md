# Proposal: TripMind Travel Agent

## Why

Projeto da disciplina de IA (prazo: **1 semana**): desenvolver um chatbot/agente de IA para planejamento de viagens. O usuário informa destino, dias, orçamento e interesses, e o agente monta um roteiro dia a dia adaptado ao clima, com pesquisa em tempo real, estimativa de custos, checklist de mala e dicas culturais.

Base disponível: scripts do professor (`scripts/`) usando `agno` + `Groq (llama-3.3-70b-versatile)` + `TavilyTools` + `YFinanceTools` + tools customizadas em Python.

Contexto adicional:
- O professor sugeriu o uso da **Gemini API** como modelo (também como auxílio/correção).
- Nenhuma chave de API configurada ainda (Groq, Tavily, Gemini).
- Prazo reduzido de 2 para **1 semana** — escopo precisa ser priorizado.

## What Changes

Nova capability no repositório: um agente roteirista de viagens.

1. **Agente core** (`agno` + LLM) com instruções em português:
   - Roteiro dia a dia (Manhã/Tarde/Noite) adaptado ao clima:
     - Chuva → atrações cobertas (museus, cafés, shoppings)
     - Sol → praias, parques, passeios ao ar livre
   - Dicas culturais: viagem internacional → etiquetas, gorjetas, expressões; nacional → pratos típicos, gírias, segurança.

2. **Tools customizadas** (padrão do `script04.py`):
   - `calculate_travel_budget(days, travelers, profile, currency)` — estimativa por categoria (Alimentação, Passeios, Transporte Local, Emergência) para perfis Econômico/Moderado/Luxo.
   - `generate_packing_list(weather_forecast, days, trip_type)` — checklist de mala com base no clima.
   - `get_weather(city, days)` — previsão via **Open-Meteo** (gratuito, sem chave), com fallback em Tavily.

3. **Tools prontas do agno**:
   - `TavilyTools` — busca em tempo real de atrações, eventos e restaurantes.
   - `YFinanceTools` — conversão de moedas via pares `XXX=BRL` (ex: `USD=BRL`).

4. **Modelo:** `gemini-3.5-flash` (Gemini API, sugestão do professor, chave gratuita via Google AI Studio) como principal, com Groq (`llama-3.3-70b-versatile`) como alternativa/fallback.

5. **Interface:** Streamlit — formulário de entrada + chat de ajustes + exibição do roteiro em cards. *(Decidido pelo usuário em 19/08/2026.)*

## Implementation Plan

1. Setup do ambiente: venv, dependências (`requirements.txt` + `google-genai` + `streamlit`), template `.env`.
2. Obtenção das chaves de API (Gemini AI Studio, Tavily, Groq).
3. Implementação das tools customizadas (clima, orçamento, mala).
4. Montagem do agente com instruções e teste por CLI (padrão `script04.py`).
5. Interface Streamlit integrada ao agente.
6. Testes ponta a ponta, refinamento e README.

## Changes to Existing Capabilities

- Nenhuma capability existente é alterada; `scripts/` permanece como referência de estudo.
- `requirements.txt` ganha dependências novas: `google-genai`, `streamlit` (e `duckduckgo-search` se o fallback de busca for necessário).
