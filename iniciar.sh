#!/usr/bin/env bash
# ====================================================================
# TripMind AI - Script de Inicializacao Automatica (Linux Mint / Ubuntu)
# ====================================================================

echo "[INFO] Iniciando TripMind AI no Linux Mint..."

# 1. Verifica se o Python 3 esta instalado
if ! command -v python3 &> /dev/null; then
    echo "[ERRO] Python 3 nao foi encontrado. Por favor, instale com: sudo apt update && sudo apt install python3 python3-venv python3-pip"
    exit 1
fi

# 2. Cria o ambiente virtual (.venv) se nao existir
if [ ! -d ".venv" ]; then
    echo "[1/3] Criando ambiente virtual (.venv)..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "[AVISO] Nao foi possivel criar o venv. Tentando instalar pacote do sistema..."
        sudo apt update && sudo apt install -y python3-venv
        python3 -m venv .venv
    fi
fi

# 3. Ativa o ambiente virtual
source .venv/bin/activate

# 4. Instala ou atualiza as dependencias
echo "[2/3] Verificando dependencias do projeto..."
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

# 5. Verifica se o .env existe
if [ ! -f ".env" ]; then
    echo "[AVISO] Arquivo .env nao encontrado. Copiando de .env.example..."
    cp .env.example .env
    echo "[DICA] Lembre-se de adicionar sua GEMINI_API_KEY no arquivo .env!"
fi

# 6. Executa a aplicacao Streamlit
echo "[3/3] Abrindo TripMind AI no navegador em http://localhost:8501..."
streamlit run app.py
