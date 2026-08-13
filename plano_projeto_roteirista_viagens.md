# ✈️ Plano do Projeto: TripMind AI — Assistente Roteirista de Viagens Inteligente

> **Resumo da Ideia e Arquitetura para o Projeto de IA I**  
> *Data do Registro: 13/08/2026*  
> *Prazo estimado de desenvolvimento: 2 semanas*

---

## 🎯 1. Objetivo do Projeto

Desenvolver um **Agente de IA Autônomo e Interativo** focado no planejamento de viagens personalizadas. O sistema recebe as preferências do usuário (destino, dias, orçamento, interesses) e utiliza ferramentas externas para buscar clima, eventos locais, estimar custos, sugerir bagagem e fornecer dicas culturais e financeiras.

---

## 🛠️ 2. Stack Tecnológica

* **Modelo de Linguagem (LLM):** Groq API (`llama-3.3-70b-versatile`) — Respostas ultrarrápidas em milissegundos.
* **Framework de Agentes:** `agno` (Python) — Utilizando o padrão do repositório base (`scripts/`).
* **Pesquisa Web:** `TavilyTools` (Busca em tempo real de atrações, clima e eventos).
* **Backend:** FastAPI (Python).
* **Frontend:** Interface Web moderna (HTML5, CSS3, JavaScript) ou Streamlit.

---

## 🧩 3. Funcionalidades & Ferramentas do Agente (*Tools*)

1. **🗺️ Roteiro Adaptativo Dia a Dia:**
   - Monta a programação (Manhã, Tarde, Noite).
   - Leva em consideração o clima: dias chuvosos recebem atrações cobertas (museus, cafés); dias ensolarados recebem praias, parques e passeios ao ar livre.

2. **🌐 Pesquisa em Tempo Real (`TavilyTools`):**
   - Busca pontos turísticos atualizados, eventos sazonais e recomendações de restaurantes bem avaliados.

3. **💱 Conversor de Moedas & Dicas Culturais/Regionais (Lógica Adaptativa):**
   - **Se for viagem internacional:** Converte valores para a moeda local/BRL e fornece dicas de **etiquetas culturais** (ex: gorjetas, costumes locais, transporte público, expressões úteis).
   - **Se for viagem nacional (Brasil):** Destaca pratos típicos regionais, gírias locais, recomendações de segurança e cultura da região.

4. **🧮 Calculadora de Orçamento (`calculate_travel_budget`):**
   - Estima os custos por categoria (Alimentação, Passeios, Transporte Local, Emergência) divididos entre os perfis: *Econômico (Mochilão)*, *Moderado* ou *Luxo*.

5. **🧳 Checklist de Mala Inteligente (`generate_packing_list`):**
   - Cria uma lista de bagagem personalizada baseada no clima previsto e estilo da viagem.

---

## 📐 4. Arquitetura do Sistema

```
┌────────────────────────────────────────────────────────┐
│             INTERFACE WEB (Frontend HTML/JS)           │
│   • Formulário de Destino, Dias, Orçamento e Estilo    │
│   • Exibição de Roteiro em Cards e Chat de Ajustes     │
└───────────────────────────┬────────────────────────────┘
                            │ Requisições HTTP (POST /api/plan)
                            ▼
┌────────────────────────────────────────────────────────┐
│                   BACKEND (FastAPI)                    │
│   • Recebe os dados, gerencia a sessão e chama o Agente│
└───────────────────────────┬────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│              AGENTE AGNO + GROQ (Python)               │
│   • Modelo: Groq (Llama 3.3 70B)                       │
│   • Tools:                                             │
│       - Tavily (Busca Web / Clima)                     │
│       - CurrencyConverter & CulturalTips               │
│       - BudgetCalculator                               │
│       - PackingListGenerator                           │
└────────────────────────────────────────────────────────┘
```

---

## 🚀 5. Próximos Passos (Para a próxima sessão)

1. Criar a estrutura base do projeto Python organizando a API FastAPI.
2. Implementar as funções customizadas Python (*Tools*) no `agno`.
3. Criar a interface Web em HTML/CSS/JS com visual escuro/moderno.
4. Testar o agente com Groq API Key.

---
*Backup gerado automaticamente pelo assistente Gemini para salvar o planejamento do aluno.*
