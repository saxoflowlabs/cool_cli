# coolcli/commands.py
def handle_command(cmd, console):
    if cmd.strip() == "help":
        console.print("""
[bold cyan]Available Commands:[/bold cyan]
help         Show this help
exit         Exit the CLI
simulate      Run simulation
synth         Run synthesis
ai            Use AI agent (future)
        """)
    elif cmd.startswith("simulate"):
        console.print("[green]Running simulation (placeholder)...[/green]")
    elif cmd.startswith("synth"):
        console.print("[green]Running synthesis (placeholder)...[/green]")
    else:
        console.print("[yellow]Unknown command. Type /help.[/yellow]")
