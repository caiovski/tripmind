import re
from datetime import date, timedelta
from typing import Any, Dict, List, Optional
import streamlit as st

from src.agent.agent_factory import create_travel_agent
from src.config.settings import get_settings
from src.services.session_history_service import (
    create_new_session,
    load_session,
    save_session,
)
from src.ui.components import (
    render_download_section,
    render_header,
    render_metric_cards,
    render_quick_prompts,
    render_saved_conversations_sidebar,
)
from src.ui.styles import apply_custom_styles


def parse_budget_input(val_str: str) -> float:
    """Converte entrada de texto livre de orçamento em valor numérico float."""
    if not val_str:
        return 0.0
    cleaned = re.sub(r"[^\d,\.]", "", str(val_str)).strip()
    if not cleaned:
        return 0.0
    if "," in cleaned:
        cleaned = cleaned.replace(".", "").replace(",", ".")
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def init_session_state() -> None:
    """Inicializa variáveis necessárias no estado da sessão do Streamlit."""
    if "session_id" not in st.session_state:
        st.session_state.session_id = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "agent" not in st.session_state:
        st.session_state.agent = None
    if "trip_info" not in st.session_state:
        st.session_state.trip_info = None
    if "last_assistant_content" not in st.session_state:
        st.session_state.last_assistant_content = ""
    if "selected_provider" not in st.session_state:
        st.session_state.selected_provider = "gemini"
    if "pending_prompt" not in st.session_state:
        st.session_state.pending_prompt = None


def get_active_agent(provider: Optional[str] = None):
    """Retorna o agente ativo da sessão ou cria um novo com o provedor selecionado."""
    active_prov = provider or st.session_state.get("selected_provider", "gemini")
    if st.session_state.agent is None:
        st.session_state.agent = create_travel_agent(override_provider=active_prov)
    return st.session_state.agent


def sync_save_current_session(default_title: Optional[str] = None) -> None:
    """Salva a sessão atual na memória local da sessão."""
    if not st.session_state.session_id:
        new_sess = create_new_session(
            destination=default_title or (st.session_state.trip_info.get("destino", "") if st.session_state.trip_info else "Conversa"),
            trip_info=st.session_state.trip_info,
        )
        st.session_state.session_id = new_sess["id"]

    existing = load_session(st.session_state.session_id)
    if existing and existing.get("title") and existing.get("title") not in ("Conversa", "Nova Viagem"):
        title = existing["title"]
    elif st.session_state.trip_info and st.session_state.trip_info.get("destino"):
        dest = st.session_state.trip_info.get("destino", "")
        days = st.session_state.trip_info.get("dias", "")
        title = f"{dest} ({days}d)" if days else dest
    else:
        title = (default_title or "Conversa")[:28]

    session_data = {
        "id": st.session_state.session_id,
        "title": title,
        "trip_info": st.session_state.trip_info or {},
        "messages": st.session_state.messages,
        "last_assistant_content": st.session_state.last_assistant_content,
        "provider": st.session_state.selected_provider,
    }
    save_session(session_data)


def switch_to_session(session_id: str) -> None:
    """Carrega uma sessão salva para a interface ativa."""
    session_data = load_session(session_id)
    if session_data:
        st.session_state.session_id = session_id
        st.session_state.messages = session_data.get("messages", [])
        st.session_state.trip_info = session_data.get("trip_info", None)
        st.session_state.last_assistant_content = session_data.get("last_assistant_content", "")
        st.session_state.selected_provider = session_data.get("provider", "gemini")
        st.session_state.agent = create_travel_agent(override_provider=st.session_state.selected_provider)
        st.session_state.pending_prompt = None
        st.rerun()


def start_new_conversation() -> None:
    """Inicia uma nova conversa limpa na sessão."""
    st.session_state.session_id = None
    st.session_state.messages = []
    st.session_state.trip_info = None
    st.session_state.last_assistant_content = ""
    st.session_state.pending_prompt = None
    st.session_state.agent = create_travel_agent(override_provider=st.session_state.selected_provider)
    st.rerun()


DIAS_SEMANA_NOMES = [
    "segunda-feira",
    "terça-feira",
    "quarta-feira",
    "quinta-feira",
    "sexta-feira",
    "sábado",
    "domingo",
]


def build_contextual_prompt(user_prompt: str, history: List[Dict[str, str]], trip_info: Optional[Dict[str, Any]]) -> str:
    """Constrói prompt enriquecido com o contexto da viagem e histórico recente de turnos."""
    context_blocks: List[str] = []

    hoje_obj = date.today()
    hoje_str = f"{hoje_obj.strftime('%d/%m/%Y')} ({DIAS_SEMANA_NOMES[hoje_obj.weekday()]})"
    context_blocks.append(f"[DATA ATUAL DE REFERÊNCIA: {hoje_str}]")

    # 1. Dados estruturados da viagem (se disponíveis)
    if trip_info and trip_info.get("destino"):
        context_blocks.append(
            f"[CONTEXTO DA VIAGEM ATIVA:\n"
            f"- Destino: {trip_info.get('destino')}\n"
            f"- Duração: {trip_info.get('dias')} dia(s) (Período: {trip_info.get('periodo_str', 'Não informado')})\n"
            f"- Viajantes: {trip_info.get('viajantes', 1)}\n"
            f"- Perfil de Gastos: {trip_info.get('estilo', 'moderado')}\n"
            f"- Estilo da Viagem: {trip_info.get('tipo', 'cidade')}\n"
            f"- Orçamento Estipulado: R$ {trip_info.get('orcamento', 0):,.2f}]"
        )


    # 2. Histórico recente de mensagens anteriores da conversa
    if history:
        context_blocks.append("[HISTÓRICO DA CONVERSA ANTERIOR:]")
        for turn in history[-4:]:  # Mantém os últimos 4 turnos para alta velocidade e contexto preciso
            role_tag = "Usuário" if turn["role"] == "user" else "TripMind"
            text_content = turn["content"]
            if len(text_content) > 800:
                text_content = text_content[:800] + " ... [trecho omitido]"
            context_blocks.append(f"{role_tag}: {text_content}")

    context_blocks.append(
        f"[NOVA MENSAGEM DO USUÁRIO]:\n{user_prompt}\n\n"
        f"(Mantenha total coerência com o destino e perfil já estabelecidos.)"
    )

    return "\n\n".join(context_blocks)


def execute_agent_prompt(prompt_text: str) -> None:
    """Executa o prompt no agente mantendo a memória contextual e resiliência a fallback."""
    # Salva mensagem original no histórico visual
    st.session_state.messages.append({"role": "user", "content": prompt_text})

    with st.chat_message("user"):
        st.markdown(prompt_text)

    # Constrói o prompt enriquecido com a memória dos turnos anteriores
    prior_history = st.session_state.messages[:-1]
    enriched_prompt = build_contextual_prompt(
        user_prompt=prompt_text,
        history=prior_history,
        trip_info=st.session_state.trip_info,
    )

    with st.chat_message("assistant"):
        with st.spinner("TripMind gerando sua resposta..."):
            agent = get_active_agent()
            try:
                response = agent.run(enriched_prompt)
                content = response.content if hasattr(response, "content") else str(response)

                if '"code": 429' in content or "RESOURCE_EXHAUSTED" in content:
                    raise RuntimeError("Gemini 429 Quota Exceeded")

            except Exception as exc:
                err_str = str(exc)
                if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str or "Quota" in err_str or "QuotaFailure" in err_str:
                    st.warning("[Fallback Ativado] Alternando para Groq Cloud...")
                    fallback_agent = create_travel_agent(override_provider="groq")
                    st.session_state.agent = fallback_agent
                    st.session_state.selected_provider = "groq"
                    response = fallback_agent.run(enriched_prompt)
                    content = response.content if hasattr(response, "content") else str(response)
                else:
                    content = f"Não foi possível completar o planejamento: {err_str}"

        st.markdown(content)

    st.session_state.messages.append({"role": "assistant", "content": content})
    st.session_state.last_assistant_content = content

    first_title = prompt_text.replace("Por favor,", "").replace("Monte um roteiro", "").replace("Olá", "").replace("TripMind", "").strip(" ,:.-*#")
    sync_save_current_session(default_title=first_title[:26] if first_title else "Viagem")
    st.rerun()


def build_trip_prompt(form_data: Dict[str, Any]) -> str:
    """Constrói o prompt estruturado a partir dos dados do formulário."""
    partes: List[str] = [
        f"Monte um roteiro de viagem completo e detalhado para **{form_data['destino']}**.",
        f"Duração: **{form_data['dias']} dia(s)**",
    ]

    if form_data.get("periodo_str"):
        partes.append(f"(Período: {form_data['periodo_str']})")

    partes.append(
        f"para **{form_data['viajantes']} pessoa(s)**. "
        f"Perfil: **{form_data['estilo']}**. "
        f"Estilo: **{form_data['tipo']}**."
    )

    if form_data.get("interesses"):
        partes.append(f"Interesses: {', '.join(form_data['interesses'])}.")

    if form_data.get("orcamento", 0) > 0:
        partes.append(f"Orçamento limite: R$ {form_data['orcamento']:,.2f}.")

    partes.append(
        "\nConsulte o clima diário, calcule os custos e apresente o roteiro estruturado por turnos com checklist."
    )

    return " ".join(partes)


def main() -> None:
    """Função principal da interface Streamlit."""
    st.set_page_config(
        page_title="TripMind AI — Assistente de Viagens",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    init_session_state()
    settings = get_settings()

    # Aplica CSS moderno customizado
    st.markdown(apply_custom_styles(), unsafe_allow_html=True)

    # Renderiza Cabeçalho estilizado
    render_header(settings)

    if not settings.has_gemini and not settings.has_groq:
        st.error(
            "⚠️ **Nenhuma chave de API encontrada no arquivo `.env`!**\n\n"
            "Crie ou edite o arquivo `.env` na raiz do projeto contendo:\n"
            "```env\nGEMINI_API_KEY=sua_chave_aqui\nGROQ_API_KEY=sua_chave_aqui\n```"
        )

    # --- BARRA LATERAL (SIDEBAR) ---
    with st.sidebar:
        # Formulário Opcional / Assistente de Roteiro Rápido
        with st.expander("Assistente de Roteiro (Opcional)", expanded=False):
            st.caption("Preencha para enviar um prompt estruturado ou digite diretamente no chat:")

            destino = st.text_input(
                "Destino",
                value="",
                placeholder="Ex: Salvador, Bahia ou Lisboa, Portugal",
            )

            hoje = date.today()
            datas_selecionadas = st.date_input(
                "Período (Ida e Volta)",
                value=(hoje, hoje + timedelta(days=5)),
                min_value=hoje,
                format="DD/MM/YYYY",
            )

            if isinstance(datas_selecionadas, (tuple, list)) and len(datas_selecionadas) == 2:
                data_ida, data_volta = datas_selecionadas
                calc_dias = max((data_volta - data_ida).days, 1)
                periodo_str = f"{data_ida.strftime('%d/%m/%Y')} ({DIAS_SEMANA_NOMES[data_ida.weekday()]}) a {data_volta.strftime('%d/%m/%Y')} ({DIAS_SEMANA_NOMES[data_volta.weekday()]})"
            elif isinstance(datas_selecionadas, (tuple, list)) and len(datas_selecionadas) == 1:
                data_ida = datas_selecionadas[0]
                calc_dias = 1
                periodo_str = f"{data_ida.strftime('%d/%m/%Y')} ({DIAS_SEMANA_NOMES[data_ida.weekday()]})"
            else:
                calc_dias = 5
                periodo_str = ""


            viajantes = st.number_input(
                "Viajantes",
                min_value=1,
                max_value=10,
                value=1,
                step=1,
            )

            estilo = st.selectbox(
                "Perfil de Gastos",
                options=["economico", "moderado", "luxo"],
                format_func=lambda x: {
                    "economico": "Econômico (Mochilão)",
                    "moderado": "Moderado / Confortável",
                    "luxo": "Luxo / Premium",
                }[x],
                index=1,
            )

            tipo = st.selectbox(
                "Estilo da Viagem",
                options=["cidade", "praia", "natureza", "neve"],
                format_func=lambda x: {
                    "cidade": "Cidade / Urbano",
                    "praia": "Praia e Litoral",
                    "natureza": "Natureza e Trilhas",
                    "neve": "Neve e Inverno",
                }[x],
                index=0,
            )

            interesses = st.multiselect(
                "Interesses",
                options=[
                    "Gastronomia típica",
                    "Cultura, história e museus",
                    "Praia e passeios ao ar livre",
                    "Natureza, trilhas e ecoturismo",
                    "Vida noturna e bares",
                    "Compras e feiras locais",
                ],
                default=["Gastronomia típica", "Cultura, história e museus"],
            )

            orcamento_str = st.text_input(
                "Orçamento estimado (R$, opcional)",
                value="",
                placeholder="Ex: 3500",
            )
            orcamento_valor = parse_budget_input(orcamento_str)

            if st.button("Enviar ao Chat", type="primary", use_container_width=True):
                if not destino.strip():
                    st.error("Informe o destino no formulário.")
                else:
                    form_data = {
                        "destino": destino.strip(),
                        "dias": calc_dias,
                        "periodo_str": periodo_str,
                        "viajantes": viajantes,
                        "estilo": estilo,
                        "tipo": tipo,
                        "interesses": interesses,
                        "orcamento": orcamento_valor,
                    }
                    new_sess = create_new_session(destination=destino.strip(), trip_info=form_data)
                    st.session_state.session_id = new_sess["id"]
                    st.session_state.agent = create_travel_agent(override_provider=st.session_state.selected_provider)
                    st.session_state.messages = []
                    st.session_state.trip_info = form_data
                    st.session_state.last_assistant_content = ""

                    # Agenda o prompt para ser executado no container principal de chat
                    st.session_state.pending_prompt = build_trip_prompt(form_data)
                    st.rerun()

        st.divider()

        # Histórico de Conversas Salvas
        render_saved_conversations_sidebar(
            current_session_id=st.session_state.session_id,
            on_select_session=switch_to_session,
            on_new_session=start_new_conversation,
        )

        st.divider()

        # Informações do Sistema
        st.markdown("#### Informações do Sistema")
        provedor_opcoes = ["gemini", "groq"]
        provedor_idx = 0 if st.session_state.selected_provider == "gemini" else 1
        novo_provedor = st.selectbox(
            "Modelo de IA",
            options=provedor_opcoes,
            index=provedor_idx,
            format_func=lambda x: "Google Gemini 3.6 Flash" if x == "gemini" else "Groq Cloud (GPT-OSS 120B)",
        )
        if novo_provedor != st.session_state.selected_provider:
            st.session_state.selected_provider = novo_provedor
            st.session_state.agent = create_travel_agent(override_provider=novo_provedor)

        llm_nome = "Gemini 3.6 Flash" if st.session_state.selected_provider == "gemini" else "Groq (GPT-OSS 120B)"
        st.caption(f"LLM Ativo: {llm_nome}")

    # --- ÁREA PRINCIPAL (MAIN CONTENT) ---
    if st.session_state.trip_info and st.session_state.trip_info.get("destino"):
        info = st.session_state.trip_info
        render_metric_cards(
            destination=info.get("destino", ""),
            days=info.get("dias", 5),
            travelers=info.get("viajantes", 1),
            profile=info.get("estilo", "moderado"),
            trip_type=info.get("tipo", "cidade"),
            periodo_str=info.get("periodo_str", ""),
        )

    # Exibe histórico de mensagens do chat ou mensagem de boas-vindas
    if not st.session_state.messages and not st.session_state.pending_prompt:
        st.info(
            "**TripMind AI — Assistente de Viagens**\n\n"
            "Converse diretamente com o TripMind no campo abaixo para planejar sua viagem "
            "(ex: *'Monte um roteiro de 5 dias em Lisboa em outubro com foco em história e gastronomia'*) "
            "ou utilize o **Assistente de Roteiro (Opcional)** na barra lateral."
        )
    else:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if st.session_state.last_assistant_content:
            st.divider()
            current_dest = st.session_state.trip_info.get("destino", "roteiro") if st.session_state.trip_info else "roteiro"
            render_download_section(
                st.session_state.last_assistant_content,
                current_dest,
                st.session_state.trip_info,
            )
            render_quick_prompts(lambda p: execute_agent_prompt(p))

    # Processa prompt pendente (vindo do formulário na sidebar ou ação rápida)
    if st.session_state.pending_prompt:
        prompt_to_run = st.session_state.pending_prompt
        st.session_state.pending_prompt = None
        execute_agent_prompt(prompt_to_run)

    # Input de chat no rodapé (Totalmente livre e com memória contínua)
    if user_prompt := st.chat_input("Pergunte qualquer coisa ou peça ajustes para o TripMind..."):
        execute_agent_prompt(user_prompt)


if __name__ == "__main__":
    main()
