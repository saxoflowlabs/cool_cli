from rich.markdown import Markdown
from rich.text import Text

def handle_command(cmd: str, console):
    cmd = cmd.strip().lower()

    if cmd in ["/help", "help"]:
        return Markdown(
            """### Available Commands

- **/help** — Show this help
- **/exit** — Exit the CLI
- **/simulate** — Run simulation
- **/synth** — Run synthesis
- **/ai** — Use AI agent _(coming soon)_"""
        )
    elif cmd.startswith("/simulate") or cmd.startswith("simulate"):
        return Text("✅ Running simulation... (placeholder)", style="green")
    elif cmd.startswith("/synth") or cmd.startswith("synth"):
        return Text("🏗️ Running synthesis... (placeholder)", style="green")
    elif cmd.startswith("/ai") or cmd.startswith("ai"):
        return Text("🤖 AI agent feature coming soon!", style="bold blue")
    elif cmd in ["/exit", "exit", "/quit", "quit"]:
        return None
    else:
        # For error, just return colored/styled Text, NOT a Panel
        return Text(
            "❌ Unknown command. Type ",
            style="bold yellow"
        ) + Text(
            "/help",
            style="bold cyan"
        ) + Text(
            " to see available commands.",
            style="bold yellow"
        )
