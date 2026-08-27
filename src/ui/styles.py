"""Estilos visuais modernos e elegantes para a interface Streamlit do TripMind AI."""

MODERN_CSS = """
<style>
/* Importação de fontes modernas */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Header principal estilizado */
.tripmind-header {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 24px;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.3);
}

.tripmind-title {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(90deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 12px;
}

.tripmind-subtitle {
    color: #94a3b8;
    font-size: 0.95rem;
    margin-top: 6px;
    margin-bottom: 12px;
}

/* Badges de status no header */
.badge-container {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 10px;
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    display: inline-block;
}

.status-dot.online {
    background-color: #10b981;
    box-shadow: 0 0 8px #10b981;
}

.status-dot.neutral {
    background-color: #94a3b8;
}

.status-dot.info {
    background-color: #38bdf8;
    box-shadow: 0 0 8px #38bdf8;
}

.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 5px 12px;
    border-radius: 6px;
    font-size: 0.78rem;
    font-weight: 500;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    color: #e2e8f0;
    letter-spacing: 0.02em;
}

/* Cards de Resumo Rápido */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 14px;
    margin-bottom: 20px;
}

.metric-card {
    background: rgba(30, 41, 59, 0.7);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 16px;
    transition: transform 0.2s ease, border-color 0.2s ease;
}

.metric-card:hover {
    transform: translateY(-2px);
    border-color: rgba(56, 189, 248, 0.3);
}

.metric-card-title {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #94a3b8;
    margin-bottom: 6px;
}

.metric-card-value {
    font-size: 1.25rem;
    font-weight: 700;
    color: #f8fafc;
}

.metric-card-sub {
    font-size: 0.8rem;
    color: #64748b;
    margin-top: 4px;
}

/* Atalhos rápidos / Sugestões de chat */
.quick-prompts-label {
    font-size: 0.8rem;
    font-weight: 600;
    color: #94a3b8;
    margin-top: 16px;
    margin-bottom: 8px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Estilização da Sidebar Dark */
section[data-testid="stSidebar"],
[data-testid="stSidebar"] {
    background-color: #0b1120 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.06);
}

/* Divisores sutis */
hr {
    border-color: rgba(255, 255, 255, 0.08) !important;
}

/* Botões primários com gradiente */
button[kind="primary"] {
    background: linear-gradient(135deg, #0284c7 0%, #4f46e5 100%) !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}

button[kind="primary"]:hover {
    box-shadow: 0 4px 15px rgba(2, 132, 199, 0.4) !important;
    transform: scale(1.01) !important;
}

/* Ajustes nas mensagens de chat */
[data-testid="stChatMessage"] {
    background-color: rgba(30, 41, 59, 0.5) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 14px !important;
    padding: 16px !important;
    margin-bottom: 12px !important;
}

[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    background-color: rgba(15, 23, 42, 0.8) !important;
    border-color: rgba(56, 189, 248, 0.2) !important;
}

/* =======================================================
   OCULTA O ÍCONE PISCANDO/STATUS AO LADO DO STOP NO TOPO
   ======================================================= */

div[data-testid="stStatusWidget"] svg,
div[data-testid="stStatusWidget"] [data-testid="stStatusWidgetStatus"],
div[data-testid="stStatusWidget"] [class*="StatusWidget_status"],
div[data-testid="stStatusWidget"] [class*="stStatusWidget"] > svg,
div[data-testid="stStatusWidget"] img,
div[data-testid="stStatusWidget"] [role="img"],
header[data-testid="stHeader"] [data-testid="stStatusWidget"] svg,
header[data-testid="stHeader"] [data-testid="stStatusWidget"] [class*="status"],
header[data-testid="stHeader"] [data-testid="stStatusWidget"] > div:first-child:not(:has(button)) {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    width: 0px !important;
    height: 0px !important;
    pointer-events: none !important;
}


/* =======================================================
   ESTILIZAÇÃO DOS BOTÕES '+' (VERDE) E '-' (VERMELHO)
   ======================================================= */

button[data-testid="stNumberInputStepUp"]:hover,
button[data-testid="stNumberInputStepUp"]:active,
button[data-testid="stNumberInputStepUp"]:focus {
    background-color: #10b981 !important;
    color: #ffffff !important;
    border-color: #059669 !important;
    box-shadow: 0 0 10px rgba(16, 185, 129, 0.5) !important;
}

button[data-testid="stNumberInputStepDown"]:hover,
button[data-testid="stNumberInputStepDown"]:active,
button[data-testid="stNumberInputStepDown"]:focus {
    background-color: #ef4444 !important;
    color: #ffffff !important;
    border-color: #dc2626 !important;
    box-shadow: 0 0 10px rgba(239, 68, 68, 0.5) !important;
}

/* =======================================================
   SIDEBAR RECENTES ESTILO CHATGPT (SLIM, COMPACTO E ELEGANTE)
   ======================================================= */

.chatgpt-sidebar-title {
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    color: #94a3b8 !important;
    margin-top: 6px !important;
    margin-bottom: 4px !important;
    padding-left: 2px !important;
    letter-spacing: 0.03em !important;
    text-transform: uppercase;
}

/* Linha da conversa: altura slim de 32px, sem borda */
section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 0px 4px !important;
    margin-bottom: 2px !important;
    margin-top: 0px !important;
    min-height: 32px !important;
    height: 32px !important;
    transition: background-color 0.12s ease !important;
    box-shadow: none !important;
    display: flex !important;
    align-items: center !important;
}

section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"]:hover {
    background-color: #212121 !important;
}

/* Remove completamente bordas, fundos e paddings excessivos */
section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] button,
section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] div.stButton > button,
section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] div[data-testid="stPopover"] > button,
section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] div[data-testid="stPopover"] button {
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    border-color: transparent !important;
    box-shadow: none !important;
    outline: none !important;
    margin: 0 !important;
    padding: 0px 4px !important;
    height: 30px !important;
    min-height: 30px !important;
    line-height: 30px !important;
}

/* Botão do Título da Conversa (Alinhado à esquerda e para cima) */
section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="column"]:first-child button {
    color: #ececf1 !important;
    text-align: left !important;
    justify-content: flex-start !important;
    font-size: 0.85rem !important;
    font-weight: 400 !important;
    width: 100% !important;
    padding-left: 2px !important;
    overflow: hidden !important;
    white-space: nowrap !important;
    text-overflow: ellipsis !important;
}

section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="column"]:first-child button p {
    margin: 0 !important;
    padding: 0 !important;
    line-height: 30px !important;
    font-size: 0.85rem !important;
}

section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"]:hover [data-testid="column"]:first-child button {
    color: #ffffff !important;
}

/* Animação Marquee no hover quando o nome for longo */
section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"]:hover [data-testid="column"]:first-child button p {
    display: inline-block !important;
    white-space: nowrap !important;
    animation: marquee-scroll 4s ease-in-out infinite alternate !important;
}

@keyframes marquee-scroll {
    0% { transform: translateX(0%); }
    25% { transform: translateX(0%); }
    100% { transform: translateX(-35%); }
}

/* Popover dos 3 pontinhos: Invisível por padrão, surge no hover */
section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="stPopover"] {
    opacity: 0 !important;
    transition: opacity 0.15s ease-in-out !important;
    display: flex !important;
    align-items: center !important;
    justify-content: flex-end !important;
}

section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"]:hover [data-testid="stPopover"],
section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="stPopover"]:focus-within {
    opacity: 1 !important;
}

/* Botão dos 3 pontinhos horizontais compactos */
section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="column"]:last-child button {
    color: #9ca3af !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.5px !important;
    white-space: nowrap !important;
    justify-content: center !important;
    display: flex !important;
    align-items: center !important;
}

section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="column"]:last-child button p {
    margin: 0 !important;
    line-height: 1 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.5px !important;
}

section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="column"]:last-child button:hover {
    color: #ffffff !important;
}

/* Remove a seta chevron do popover */
section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="stPopover"] button svg,
section[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] [data-testid="stPopover"] svg {
    display: none !important;
    visibility: hidden !important;
    width: 0px !important;
    height: 0px !important;
}

/* =======================================================
   POPOVER DROPDOWN MENU ESTILO CHATGPT
   ======================================================= */

div[data-testid="stPopoverBody"] {
    background-color: #202123 !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 8px !important;
    padding: 8px 10px !important;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.7) !important;
    max-width: 220px !important;
    min-width: 190px !important;
}

div[data-testid="stPopoverBody"] input {
    background-color: #121214 !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 6px !important;
    color: #ffffff !important;
    font-size: 0.82rem !important;
    padding: 4px 8px !important;
    height: 30px !important;
}

div[data-testid="stPopoverBody"] button {
    background-color: rgba(255, 255, 255, 0.08) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 6px !important;
    color: #ececf1 !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    padding: 2px 8px !important;
    height: 28px !important;
    min-height: 28px !important;
    transition: background-color 0.15s ease !important;
}

div[data-testid="stPopoverBody"] button:hover {
    background-color: rgba(255, 255, 255, 0.18) !important;
    color: #ffffff !important;
}
</style>
"""


def apply_custom_styles() -> str:
    """Retorna a tag de estilos para injeção no Streamlit."""
    return MODERN_CSS
