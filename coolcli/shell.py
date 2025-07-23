import os
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from coolcli.banner import print_banner
from coolcli.commands import handle_command

console = Console()
history = []

def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def main():
    style = Style.from_dict({
        "prompt": "bold cyan",
        "": "white"
    })
    session = PromptSession()

    clear_terminal()
    print_banner(console)
    # Initial dummy panel
    console.print(Panel("[bold white]Welcome to [magenta]SaxoFlow CLI[/magenta][/bold white]", border_style="magenta"))

    while True:
        # Print full history (as Rich panels)
        for user_panel, response_panel in history:
            console.print(user_panel)
            if response_panel:
                console.print(response_panel)

        # Input at the bottom
        user_input = session.prompt("> ", style=style)
        user_input = user_input.strip()
        if not user_input:
            continue

        # User input as panel
        user_panel = Panel(
            Text(user_input, style="bold cyan"),
            border_style="bright_blue",
            title="saxoflow",
            title_align="left",
            padding=(0, 1)
        )

        # Get response as panel (from handle_command)
        from io import StringIO
        temp_out = StringIO()
        local_console = Console(file=temp_out, force_terminal=True, color_system="truecolor", width=100)
        handle_command(user_input, local_console)
        output_text = temp_out.getvalue().strip()
        temp_out.close()

        # Output panel only if output_text
        response_panel = None
        if output_text:
            response_panel = Panel(
                output_text,
                border_style="yellow" if "Unknown command" in output_text else "green",
                padding=(0, 1)
            )

        # Save both to history
        history.append((user_panel, response_panel))

        if user_input in ["/quit", "/exit"]:
            console.print("[bold green]Goodbye![/bold green]")
            break

        # Prepare next prompt (clear and print history again)
        clear_terminal()
        print_banner(console)
        console.print(Panel("[bold white]Welcome to [magenta]SaxoFlow CLI[/magenta][/bold white]", border_style="magenta"))
