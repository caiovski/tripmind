# Design: TripMind Travel Agent

## Context & Problem Statement

Prazo de 1 semana para entregar um agente de IA roteirista de viagens. A base do professor (scripts agno + Groq + tools) já valida o padrão. Restrições-chave:

- Chaves de API ainda não existem (Groq, Tavily, Gemini).
- Professor sugeriu Gemini API como modelo.
- Interface precisa ser rápida de construir → Streamlit.

## Goals

- Gerar roteiro diário personalizado (destino, dias, orçamento, interesses).
- Adaptar atividades ao clima (indoor vs outdoor).
- Pesquisar atrações/eventos/restaurantes em tempo real (Tavily).
- Calcular orçamento por perfil (Econômico/Moderado/Luxo).
- Gerar checklist de mala pelo clima.
- Converter moeda e dar dicas culturais (internacional vs nacional).
- Entregar em 1 semana, testável no dia da apresentação.

## Non-Goals

- Contas de usuário, login ou persistência (sessão única).
- Reservas, compras ou integração com agências.
- App mobile ou mapas interativos em tempo real.
- Suporte offline ou dados em cache.

## Architecture

```
┌───────────────────────────────────────────────┐
│          INTERFACE STREAMLIT (app.py)          │
│  • Formulário: destino, dias, orçamento,      │
│    estilo, interesses                          │
│  • Chat de ajustes + exibição do roteiro       │
└───────────────────────┬───────────────────────┘
                        │ sessão em memória
                        ▼
┌───────────────────────────────────────────────┐
│            AGENTE AGNO (agent.py)              │
│  Modelo: Gemini 3.5 Flash ou Groq (fallback)   │
│  Instruções: português, lógica adaptativa      │
└──┬─────────┬──────────┬───────────┬───────────┘
   │         │          │           │
   ▼         ▼          ▼           ▼
Tavily    Open-Meteo  YFinance    Tools próprias
(busca    (clima,     (câmbio     (orçamento,
web)      sem chave)  XXX=BRL)    mala)
```

## Tools Design

| Tool | Fonte | Responsabilidade | Tipo |
|------|-------|------------------|------|
| `TavilyTools` | agno | Atrações, eventos, restaurantes, dados gerais | Pronta |
| `get_weather(city, days)` | Open-Meteo API | Previsão por dia (temp, chuva, condição) | Custom |
| `convert_currency(amount, from_curr)` | YFinanceTools (`XXX=BRL`) | Conversão para BRL | Pronta |
| `calculate_travel_budget(...)` | Python puro | Estimativa por categoria × perfil | Custom |
| `generate_packing_list(...)` | Python puro | Checklist baseado no clima | Custom |

**Decisões de design:**

1. **Clima via Open-Meteo** (gratuito, sem chave, JSON simples) em vez de depender do Tavily para previsão — mais confiável e determinístico. Tavily fica para conteúdo turístico.
2. **Câmbio via YFinanceTools** (reuso do padrão `script03.py`, pares `USD=BRL`). Fallback: prompt ao LLM para valores aproximados.
3. **Orçamento e mala como funções determinísticas** (padrão `script04.py`) — o LLM decide quando chamá-las, mas o cálculo é exato e reproduzível.
4. **Modelo `gemini-3.5-flash` como principal** (chave gratuita AI Studio, sugestão do professor; rápido e otimizado para agentes/tools; modelos Pro viraram pagos em 04/2026). `agno.models.google.Gemini` exige o pacote `google-genai`. Groq `llama-3.3-70b-versatile` fica como constante de fallback configurável no `.env` (`MODEL_PROVIDER`).

## Data Flow (fluxo de uma sessão)

1. Usuário preenche formulário (destino, dias, orçamento, estilo, interesses).
2. Agente: busca clima (`get_weather`) → pesquisa atrações/eventos (`TavilyTools`).
3. Agente: monta roteiro dia a dia (Manhã/Tarde/Noite) adaptado ao clima.
4. Agente: chama `calculate_travel_budget` e `generate_packing_list`.
5. Agente: se internacional → `convert_currency` + dicas de etiqueta; se nacional → dicas regionais.
6. Streamlit renderiza roteiro em cards; usuário ajusta via chat (ex: "troque o dia 2 para algo mais econômico").

## Trade-offs Considerados

| Decisão | Escolhido | Alternativa descartada | Motivo |
|---------|-----------|------------------------|--------|
| Interface | Streamlit | Web custom (HTML/JS/FastAPI) | Prazo de 1 semana |
| Modelo | Gemini 3.5 Flash (fallback Groq) | Somente Groq | Sugestão do professor + cota gratuita + foco em agentes |
| Clima | Open-Meteo | Tavily | Precisão determinística, sem custo |
| Câmbio | YFinanceTools | Taxa fixa no código | Dados reais, reuso da base |

## Risco & Mitigação

- **Sem chave Tavily** → fallback `DuckDuckGoTools` (pacote `duckduckgo-search`) ou buscar com Open-Meteo + conhecimento do LLM.
- **Sem chave Gemini** → Groq (`llama-3.3-70b-versatile`) já é suficiente, o agno suporta ambos.
- **Demora das chamadas de tools no chat** → usar `st.spinner`/streaming e instruir o agente a responder de forma enxuta.
- **Alucinação em valores de custo** → orçamento é calculado por função determinística, não pelo LLM.
