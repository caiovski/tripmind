import os

import streamlit as st

from agent import build_agent

st.set_page_config(page_title="TripMind AI", layout="wide")

st.title("TripMind AI")
st.caption("Seu assistente roteirista de viagens inteligente")


def get_agent():
    if st.session_state.get("agent") is None:
        st.session_state.agent = build_agent()
    return st.session_state.agent


def run_agent(prompt: str):
    if st.session_state.get("agent") is None:
        st.warning("Preencha o formulário ao lado e clique em 'Gerar roteiro' antes de conversar.")
        return

    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Consultando clima, pesquisando atrações e calculando orçamento..."):
            response = get_agent().run(prompt)
        content = response.content
        st.markdown(content)
    st.session_state.messages.append({"role": "assistant", "content": content})


def build_trip_prompt(form: dict) -> str:
    partes = [
        f"Monte um roteiro de viagem completo para {form['destino']}",
        f"com {form['dias']} dia(s) e {form['viajantes']} viajante(s).",
        f"Perfil de gastos: {form['estilo']}.",
    ]
    if form["interesses"]:
        partes.append(f"Interesses: {', '.join(form['interesses'])}.")
    partes.append(f"Tipo de viagem: {form['tipo']}.")
    if form["orcamento"]:
        partes.append(f"Orçamento total disponível: R$ {form['orcamento']}.")
    partes.append(
        "Siga o fluxo: clima (get_weather), pesquisa de atrações, roteiro dia a dia "
        "(Manhã/Tarde/Noite adaptado ao clima), orçamento (calculate_travel_budget), "
        "checklist de mala (generate_packing_list) e dicas culturais e de moeda."
    )
    return " ".join(partes)


with st.sidebar:
    st.header("Nova viagem")
    destino = st.text_input("Destino", value="", placeholder="Ex: Lisboa, Portugal")
    dias = st.slider("Duração (dias)", 1, 14, 5)
    viajantes = st.number_input("Viajantes", 1, 10, 1)
    estilo = st.selectbox("Perfil de gastos", ["economico", "moderado", "luxo"], index=1)
    tipo = st.selectbox("Tipo de viagem", ["cidade", "praia", "natureza", "neve"])
    interesses = st.multiselect(
        "Interesses",
        ["Gastronomia", "Cultura e história", "Praia e lazer", "Natureza e trilhas", "Vida noturna", "Compras"],
    )
    orcamento = st.number_input("Orçamento total (R$, opcional)", min_value=0, value=0, step=100)

    if st.button("Gerar roteiro", type="primary", use_container_width=True):
        form = {
            "destino": destino,
            "dias": dias,
            "viajantes": viajantes,
            "estilo": estilo,
            "tipo": tipo,
            "interesses": interesses,
            "orcamento": orcamento,
        }
        st.session_state.agent = build_agent()
        st.session_state.messages = []
        run_agent(build_trip_prompt(form))

    st.divider()
    provider = os.getenv("MODEL_PROVIDER", "gemini")
    modelo = "Gemini 3.5 Flash" if provider != "groq" else "Groq (Llama 3.3 70B)"
    st.caption(f"Modelo ativo: {modelo}")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ajuste seu roteiro: ex: deixe o dia 2 mais econômico..."):
    run_agent(prompt)