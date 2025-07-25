from rich.markdown import Markdown
from rich.text import Text

def handle_command(cmd: str, console):
    """
    Parse and return a help or placeholder renderable for built‑in commands.

    This function primarily exists to provide a simple help panel for the CLI.
    Complex commands (attachments, saving sessions, etc.) are handled
    directly in the shell. When the user types `/help` or `help`, a rich
    Markdown renderable describing all available commands is returned. Other
    recognised commands return placeholder text indicating that the feature
    has been invoked. Unknown commands yield a friendly error message.
    """
    cmd = cmd.strip()
    lowered = cmd.lower()

    if lowered in ["/help", "help"]:
        # Extended help including new features inspired by Gemini CLI
        return Markdown(
            """### Available Commands

- **/help** — Show this help
- **/exit** — Exit the CLI
- **/simulate** — Run simulation
- **/synth** — Run synthesis
- **/ai** — Use AI agent _(coming soon)_
- **/attach &lt;path&gt;** — Attach a file to the current conversation
- **/save &lt;file&gt;** — Save your current session to a JSON file
- **/load &lt;file&gt;** — Load a session from a JSON file
- **/export &lt;file&gt;** — Export the conversation to a Markdown file
- **/stats** — Show approximate token statistics for the current session
- **/system &lt;prompt&gt;** — Set a persistent system prompt
- **/clear** — Clear the current conversation and attachments
- **/models** — List available AI models (placeholder)
- **/set &lt;parameter&gt;=&lt;value&gt;** — Adjust generation parameters (e.g. temperature)

Commands beginning with `/` are parsed by the shell and may modify the
state of your session (e.g. attachments, system prompts, configuration).
If you type something that doesn't start with `/`, it will be sent to the
underlying AI for processing.
"""
        )
    # Provide placeholders for simple built‑in commands so that unit tests
    # expecting Text output continue to work. The actual implementation of
    # these commands lives in the shell.
    elif lowered.startswith("/simulate") or lowered.startswith("simulate"):
        return Text("Running simulation... (placeholder)", style="light cyan")
    elif lowered.startswith("/synth") or lowered.startswith("synth"):
        return Text("Running synthesis... (placeholder)", style="light cyan")
    elif lowered.startswith("/ai") or lowered.startswith("ai"):
        return Text("AI agent feature coming soon!", style="bold blue")
    elif lowered in ["/quit", "quit"]:
        return None
    else:
        # For unknown commands, return a composed Text prompting the user to use /help
        return Text(
            "❌ Unknown command. Type ",
            style="bold yellow",
        ) + Text(
            "/help",
            style="bold cyan",
        ) + Text(
            " to see available commands.",
            style="bold yellow",
        )
