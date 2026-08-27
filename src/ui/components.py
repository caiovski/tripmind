from typing import Any, Callable, Dict, List, Optional
import streamlit as st
from src.config.settings import Settings
from src.services.pdf_service import generate_itinerary_pdf
from src.services.session_history_service import (
    delete_session,
    list_sessions,
    rename_session,
)


def render_header(settings: Settings) -> None:
    """Renderiza o cabeçalho profissional com badges de status de infraestrutura."""
    provider_name = "Gemini 3.6 Flash" if settings.model_provider != "groq" else "Groq (GPT-OSS 120B)"
    tavily_status = "Ativo" if settings.has_tavily else "Base de Conhecimento"
    tavily_dot = "online" if settings.has_tavily else "neutral"

    st.markdown(
        f"""
        <div class="tripmind-header">
            <h1 class="tripmind-title">TripMind AI</h1>
            <p class="tripmind-subtitle">
                Sistema Autônomo de Planejamento e Roteirização de Viagens
            </p>
            <div class="badge-container">
                <span class="status-badge">
                    <span class="status-dot online"></span>
                    LLM: {provider_name}
                </span>
                <span class="status-badge">
                    <span class="status-dot info"></span>
                    Clima: Open-Meteo API
                </span>
                <span class="status-badge">
                    <span class="status-dot {tavily_dot}"></span>
                    Pesquisa Web: {tavily_status}
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_cards(
    destination: str,
    days: int,
    travelers: int,
    profile: str,
    trip_type: str,
    periodo_str: str = "",
) -> None:
    """Renderiza cartões com resumo dos parâmetros de viagem configurados."""
    profile_labels = {
        "economico": "Econômico (Mochilão)",
        "moderado": "Moderado / Conforto",
        "luxo": "Luxo / Premium",
    }
    type_labels = {
        "cidade": "Urbano / Cultural",
        "praia": "Praia e Litoral",
        "natureza": "Natureza e Ecoturismo",
        "neve": "Inverno / Neve",
    }

    sub_periodo = f"{days} dia(s)"
    if periodo_str:
        sub_periodo += f" · {periodo_str}"
    sub_periodo += f" · {travelers} viajante(s)"

    st.markdown(
        f"""
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-card-title">Destino & Duração</div>
                <div class="metric-card-value">{destination or "Personalizado"}</div>
                <div class="metric-card-sub">{sub_periodo}</div>
            </div>
            <div class="metric-card">
                <div class="metric-card-title">Perfil de Gastos</div>
                <div class="metric-card-value">{profile_labels.get(profile, profile.capitalize())}</div>
                <div class="metric-card-sub">Cálculo determinístico em BRL</div>
            </div>
            <div class="metric-card">
                <div class="metric-card-title">Estilo da Viagem</div>
                <div class="metric-card-value">{type_labels.get(trip_type, trip_type.capitalize())}</div>
                <div class="metric-card-sub">Adaptado às condições meteorológicas</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_quick_prompts(on_prompt_selected: Callable[[str], None]) -> None:
    """Renderiza botões de ação rápida para testar no chat com 1 clique."""
    st.markdown('<div class="quick-prompts-label">Ações Rápidas:</div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("Opção mais econômica", use_container_width=True):
            on_prompt_selected("Poderia sugerir opções mais econômicas de alimentação e passeios no roteiro?")
    with col2:
        if st.button("Alternativas para chuva", use_container_width=True):
            on_prompt_selected("Quais alternativas cobertas (museus, centros culturais ou cafés) você recomenda caso chova?")
    with col3:
        if st.button("Restaurantes típicos", use_container_width=True):
            on_prompt_selected("Recomende 3 restaurantes ou pratos locais imperdíveis para esse destino.")
    with col4:
        if st.button("Checklist de bagagem", use_container_width=True):
            on_prompt_selected("Quais itens essenciais e cuidados especiais devo ter ao fazer a mala para este destino?")


def render_download_section(content: str, destination: str, trip_info: Optional[Dict[str, Any]] = None) -> None:
    """Renderiza botões para baixar o roteiro diagramado em PDF ou Markdown."""
    if not content:
        return

    dest_slug = (destination or "roteiro").lower().replace(" ", "_").replace(",", "")
    col_pdf, col_md = st.columns(2)

    with col_pdf:
        try:
            pdf_bytes = generate_itinerary_pdf(content, trip_info)
            st.download_button(
                label="Baixar Roteiro em PDF (.pdf)",
                data=pdf_bytes,
                file_name=f"tripmind_{dest_slug}.pdf",
                mime="application/pdf",
                use_container_width=True,
                help="Baixar documento PDF diagramado com mapa mental estrutural e roteiro completo.",
            )
        except Exception as exc:
            st.error(f"Erro ao gerar PDF: {exc}")

    with col_md:
        st.download_button(
            label="Baixar em Markdown (.md)",
            data=content,
            file_name=f"tripmind_{dest_slug}.md",
            mime="text/markdown",
            use_container_width=True,
            help="Exportar o texto em formato Markdown.",
        )


def render_saved_conversations_sidebar(
    current_session_id: Optional[str],
    on_select_session: Callable[[str], None],
    on_new_session: Callable[[], None],
) -> None:
    """Renderiza o histórico de conversas no estilo ChatGPT (sem cards, hover suave e menu de 3 pontos)."""
    st.markdown('<div class="chatgpt-sidebar-title">Recentes ▾</div>', unsafe_allow_html=True)

    if st.button("+ Nova Viagem", use_container_width=True):
        on_new_session()

    sessions = list_sessions()
    if not sessions:
        st.caption("Nenhuma conversa recente.")
        return

    for s in sessions[:15]:
        sess_id = s["id"]
        sess_title = s.get("title") or "Viagem"
        is_active = (sess_id == current_session_id)
        btn_label = f"{'▸ ' if is_active else ''}{sess_title}"

        # Layout sem card estilo ChatGPT: título com rolagem no hover e botão ⋮ flutuante
        col_title, col_opts = st.columns([5.2, 1.1])

        with col_title:
            if st.button(btn_label, key=f"sess_btn_{sess_id}", use_container_width=True):
                on_select_session(sess_id)

        with col_opts:
            with st.popover("⋮", use_container_width=True):
                st.caption("Opções da Conversa")
                new_title = st.text_input(
                    "Renomear",
                    value=sess_title,
                    key=f"rename_input_{sess_id}",
                    placeholder="Novo nome...",
                )
                if st.button("Salvar nome", key=f"save_rename_{sess_id}", use_container_width=True):
                    rename_session(sess_id, new_title)
                    st.rerun()

                st.divider()
                if st.button("Excluir conversa", key=f"del_btn_{sess_id}", type="secondary", use_container_width=True):
                    delete_session(sess_id)
                    if is_active:
                        on_new_session()
                    else:
                        st.rerun()
