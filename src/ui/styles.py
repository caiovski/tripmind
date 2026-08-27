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

/* Estilização da Sidebar Dark Minimalista */
section[data-testid="stSidebar"] {
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
   CONVERSAS SALVAS ESTILO CHATGPT (SEM CARD + HOVER EFFECT)
   ======================================================= */

.chatgpt-sidebar-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: #94a3b8;
    margin-bottom: 10px;
    letter-spacing: 0.02em;
    display: flex;
    align-items: center;
    gap: 4px;
}

/* Linha da conversa salva */
div[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] {
    position: relative;
    border-radius: 8px !important;
    padding: 2px 4px !important;
    margin-bottom: 2px !important;
    transition: background-color 0.15s ease !important;
    border: none !important;
    background: transparent !important;
    box-shadow: none !important;
}

/* Hover na linha: fundo cinza escuro sutil como no ChatGPT */
div[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"]:hover {
    background-color: rgba(255, 255, 255, 0.08) !important;
}

/* Botão de título da conversa (puro texto, alinhado à esquerda) */
div[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] button {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: #e2e8f0 !important;
    text-align: left !important;
    justify-content: flex-start !important;
    padding: 6px 8px !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    border-radius: 6px !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    white-space: nowrap !important;
    width: 100% !important;
}

div[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] button:hover {
    color: #ffffff !important;
}

/* Animação Marquee de rotação de texto no hover quando o nome for longo */
div[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"]:hover button p {
    display: inline-block !important;
    white-space: nowrap !important;
    animation: marquee-scroll 4.5s ease-in-out infinite alternate !important;
}

@keyframes marquee-scroll {
    0% {
        transform: translateX(0%);
    }
    30% {
        transform: translateX(0%);
    }
    100% {
        transform: translateX(-40%);
    }
}

/* Botão de 3 pontinhos (Popover): Oculto por padrão, surge suave no hover */
div[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] div[data-testid="stPopover"] {
    opacity: 0;
    transition: opacity 0.2s ease-in-out;
}

div[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"]:hover div[data-testid="stPopover"] {
    opacity: 1;
}

/* Estilo do botão de 3 pontos */
div[data-testid="stSidebar"] div[data-testid="stPopover"] button {
    background: transparent !important;
    border: none !important;
    color: #94a3b8 !important;
    font-size: 1.15rem !important;
    font-weight: 700 !important;
    padding: 2px 6px !important;
    justify-content: center !important;
    box-shadow: none !important;
}

div[data-testid="stSidebar"] div[data-testid="stPopover"] button:hover {
    color: #ffffff !important;
    background: rgba(255, 255, 255, 0.12) !important;
    border-radius: 4px !important;
}

/* Indicador de conversa ativa */
.active-chat-indicator {
    color: #38bdf8 !important;
    font-weight: 600 !important;
}
</style>
"""


def apply_custom_styles() -> str:
    """Retorna a tag de estilos para injeção no Streamlit."""
    return MODERN_CSS
