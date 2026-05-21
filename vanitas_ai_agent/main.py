"""CLI entrypoint for vanitas_ai_agent."""

from __future__ import annotations

import argparse

from vanitas_ai_agent.agent import VanitasAgent
from vanitas_ai_agent.config import Settings
from vanitas_ai_agent.gui import launch_gui


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="vanitas_ai_agent CLI")
    parser.add_argument("prompt", nargs="?", help="Natural language instruction for the agent")
    parser.add_argument("--gui", action="store_true", help="Launch Tkinter GUI")
    return parser


def interactive_loop(agent: VanitasAgent) -> None:
    print("vanitas_ai_agent interactive mode. Type 'exit' to quit.")
    while True:
        user_input = input("\nYou> ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("Bye!")
            return
        if not user_input:
            continue
        print(f"Agent> {agent.process(user_input)}")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.gui:
        launch_gui()
        return

    settings = Settings.from_env()
    agent = VanitasAgent(settings)

    if args.prompt:
        print(agent.process(args.prompt))
    else:
        interactive_loop(agent)


if __name__ == "__main__":
    main()
