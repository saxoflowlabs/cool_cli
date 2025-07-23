import os
from rich.console import Console
from rich.text import Text
from coolcli.banner import print_banner
from coolcli.commands import handle_command
from coolcli.panels import user_input_panel
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory

console = Console()
history_renderables = []

def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def main():
    cli_history = InMemoryHistory()
    session = PromptSession(history=cli_history)

    # One-time welcome
    clear_terminal()
    print_banner(console)
    panel_width = int(console.width * 0.75)
    console.print(user_input_panel("Welcome to SaxoFlow CLI! Take your first step toward mastering digital design and verification.", width=panel_width))

    # Startup tips (Text, left-aligned)
    tips = Text(
        "Tips for getting started:\n"
        "1. Ask questions, edit files, or run commands.\n"
        "2. Be specific for the best results.\n"
        "3. Use /help to see available commands.\n"
        "4. Type /exit to quit the CLI.\n",
        style="violet"
    )
    console.print(tips)
    console.print("")  # spacer

    while True:
        # Print history (user panel + output)
        panel_width = int(console.width * 0.75)  # recalc in case window size changed
        for upanel, opanel in history_renderables:
            # Ensure all input panels are correct width
            if hasattr(upanel, "width"):
                upanel.width = panel_width
            console.print(upanel)
            if opanel:
                console.print(opanel)
            console.print("")  # space between interactions

        try:
            user_input = session.prompt("> ")
        except (EOFError, KeyboardInterrupt):
            console.print("[bold green]Goodbye![/bold green]")
            break

        user_input = user_input.strip()
        if not user_input:
            clear_terminal()
            print_banner(console)
            panel_width = int(console.width * 0.75)
            console.print(user_input_panel("Welcome to SaxoFlow CLI! Take your first step toward mastering digital design and verification.", width=panel_width))
            console.print(tips)
            console.print("")
            continue

        upanel = user_input_panel(user_input, width=panel_width)
        opanel = handle_command(user_input, console)
        history_renderables.append((upanel, opanel))

        if user_input in ["/quit", "/exit"]:
            console.print("[bold green]Goodbye![/bold green]")
            break

        # Clear and redraw everything
        clear_terminal()
        print_banner(console)
        panel_width = int(console.width * 0.75)
        console.print(user_input_panel("Welcome to SaxoFlow CLI! Take your first step toward mastering digital design and verification.", width=panel_width))
        console.print(tips)
        console.print("")

