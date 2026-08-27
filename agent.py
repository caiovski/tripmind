"""TripMind AI - Interface de Linha de Comando (CLI).

Permite interagir e testar o agente diretamente pelo terminal.
Comando para execução:
    python agent.py
"""

import os
import sys

# Configura encoding UTF-8 no terminal Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from src.agent.agent_factory import create_travel_agent


def run_cli() -> None:
    """Executa o loop interativo no terminal."""
    print("=" * 60)
    print("TripMind AI — Agente Roteirista de Viagens (Modo CLI)")
    print("=" * 60)
    print("Digite 'sair' ou pressione CTRL+C para encerrar.\n")

    try:
        agent = create_travel_agent()
    except Exception as exc:
        print(f"[ERRO] Falha ao inicializar o agente: {exc}")
        sys.exit(1)

    while True:
        try:
            prompt = input("\nVocê: ").strip()
            if not prompt:
                continue
            if prompt.lower() in ("sair", "exit", "quit"):
                print("\nAté mais e boa viagem!")
                break

            print("\nTripMind pensando...")
            agent.print_response(prompt)

        except KeyboardInterrupt:
            print("\n\nSessão encerrada.")
            break
        except Exception as exc:
            print(f"\n[AVISO] Erro durante a execução: {exc}")


if __name__ == "__main__":
    run_cli()