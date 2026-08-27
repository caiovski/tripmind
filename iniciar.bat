@echo off
REM ====================================================================
REM TripMind AI - Script de Inicializacao Automatica (Windows)
REM ====================================================================

title TripMind AI

echo ===================================================
echo   TripMind AI - Assistente Roteirista de Viagens
echo ===================================================

REM 1. Verifica ambiente virtual existente
if exist "%USERPROFILE%\.venvs\tripmind\Scripts\activate.bat" (
    echo [INFO] Utilizando ambiente virtual em %USERPROFILE%\.venvs\tripmind...
    call "%USERPROFILE%\.venvs\tripmind\Scripts\activate.bat"
) else (
    if not exist ".venv" (
        echo [1/3] Criando ambiente virtual .venv local...
        python -m venv .venv
    )
    echo [2/3] Ativando ambiente virtual .venv...
    call .venv\Scripts\activate.bat
    echo [3/3] Verificando dependencias...
    pip install -r requirements.txt --quiet
)

REM 2. Executa a aplicacao Streamlit
echo.
echo Iniciando interface web em http://localhost:8501 ...
streamlit run app.py

pause
