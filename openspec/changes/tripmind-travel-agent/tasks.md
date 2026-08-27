# Tasks: TripMind Travel Agent

## Setup & Portabilidade

- [x] Criar venv e instalar dependências (`pip install -r requirements.txt`)
- [x] Adicionar dependências universais no `requirements.txt` da raiz
- [x] Criar scripts de execução automática: `iniciar.sh` (Linux Mint) e `iniciar.bat` (Windows)
- [x] Configurar `.env` com `GEMINI_API_KEY`, `TAVILY_API_KEY`, `GROQ_API_KEY` e `MODEL_PROVIDER`

## Clean Architecture (`src/`)

- [x] **Configuração (`src/config/`)**: `settings.py` com dataclasses e validação de chaves
- [x] **Domínio Puro (`src/domain/`)**:
  - `budget.py`: cálculo determinístico de orçamento por pessoa/categoria em BRL
  - `packing.py`: regras de montagem de mala por limites climáticos e estilo de viagem
- [x] **Serviços & Adaptadores (`src/services/`)**:
  - `weather_service.py`: integração Open-Meteo API com geocoding e códigos WMO em português
  - `currency_service.py`: cotações e conversão para Real com yFinance
  - `search_service.py`: busca web em tempo real com Tavily e fallback gracioso
- [x] **Agente (`src/agent/`)**:
  - `prompts.py`: prompt estruturado em português com diretrizes claras dia a dia
  - `tools_registry.py`: conversão e documentação das tools para o Agno
  - `agent_factory.py`: fábrica do Agente Agno (Gemini 3.5 Flash padrão, Groq fallback)
- [x] **Apresentação & UI (`src/ui/`)**:
  - `styles.py`: tema dark moderno com CSS customizado
  - `components.py`: cabeçalho com badges, cards de métricas, quick prompts e exportação
  - `app.py`: interface interativa Streamlit com chat, formulário e atalhos rápidos

## Pontos de Entrada & Compatibilidade

- [x] `app.py`: ponto de entrada raiz para execução do Streamlit (`streamlit run app.py`)
- [x] `agent.py`: ponto de entrada CLI para interação via terminal (`python agent.py`)
- [x] `travel_tools.py`: módulo de reexportação para compatibilidade
- [x] `smoke_test.py`: bateria de testes automatizados ponta a ponta
- [x] `README.md`: documentação completa com arquitetura, funcionalidades e guias para Linux Mint e Windows

## Finalização

- [x] Validação automatizada ponta a ponta (4/4 testes aprovados)
- [x] Teste de compatibilidade e portabilidade
