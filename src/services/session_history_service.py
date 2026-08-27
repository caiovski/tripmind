import time
import uuid
from typing import Any, Dict, List, Optional
import streamlit as st


def get_sessions_dict() -> Dict[str, Dict[str, Any]]:
    """Obtém o dicionário de sessões armazenado na memória da sessão atual."""
    if "saved_conversations" not in st.session_state:
        st.session_state.saved_conversations = {}
    return st.session_state.saved_conversations


def create_new_session(destination: str = "", trip_info: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Cria uma nova sessão de conversa na memória local."""
    session_id = str(uuid.uuid4())[:8]
    title = destination.strip() if destination.strip() else "Nova Viagem"
    session_data = {
        "id": session_id,
        "title": title,
        "created_at": time.strftime("%d/%m %H:%M"),
        "trip_info": trip_info or {},
        "messages": [],
        "last_assistant_content": "",
        "provider": "gemini",
    }
    sessions = get_sessions_dict()
    sessions[session_id] = session_data
    return session_data


def save_session(session_data: Dict[str, Any]) -> None:
    """Atualiza a sessão na memória local."""
    session_id = session_data.get("id")
    if not session_id:
        return
    sessions = get_sessions_dict()
    sessions[session_id] = session_data


def load_session(session_id: str) -> Optional[Dict[str, Any]]:
    """Carrega uma sessão específica pelo ID a partir da memória."""
    sessions = get_sessions_dict()
    return sessions.get(session_id)


def list_sessions() -> List[Dict[str, Any]]:
    """Lista todas as sessões salvas na memória em ordem decrescente."""
    sessions = get_sessions_dict()
    items = []
    for s_id, data in sessions.items():
        items.append({
            "id": s_id,
            "title": data.get("title", "Viagem"),
            "created_at": data.get("created_at", ""),
            "destination": data.get("trip_info", {}).get("destino", ""),
        })
    items.reverse()
    return items


def rename_session(session_id: str, new_title: str) -> None:
    """Renomeia uma sessão salva na memória."""
    if not new_title.strip():
        return
    sessions = get_sessions_dict()
    if session_id in sessions:
        sessions[session_id]["title"] = new_title.strip()


def delete_session(session_id: str) -> None:
    """Remove uma sessão da memória local."""
    sessions = get_sessions_dict()
    if session_id in sessions:
        del sessions[session_id]
