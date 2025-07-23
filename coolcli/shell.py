import os
from prompt_toolkit import PromptSession
from rich.console import Console
from coolcli.banner import print_banner
from coolcli.commands import handle_command

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    console = Console()
    clear_terminal()  # 👈 clears the terminal on launch
    print_banner(console)

    session = PromptSession("[bold green]🧠 saxoflow λ[/bold green] ")

    while True:
        try:
            cmd = session.prompt()
            if cmd.strip() in ["/quit", "/exit"]:
                console.print("[bold green]Goodbye![/bold green]")
                break
            else:
                handle_command(cmd, console)
        except KeyboardInterrupt:
            console.print("\n[red]Interrupted. Type /quit to exit.[/red]")
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
