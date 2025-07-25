"""
Interactive command‑line interface for the SaxoFlow project.

"""

import json
import os
import time
from typing import Any, Dict, List, Optional

from rich.console import Console
from rich.text import Text
from rich.markdown import Markdown
from coolcli.banner import print_banner
from coolcli.commands import handle_command
from coolcli.panels import user_input_panel, ai_panel
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory

# Global console used throughout the CLI
console = Console()

# Session state. These globals are mutated by various command handlers.
# A list of conversation entries. Each entry is a dict with keys:
#   user: str – the user's prompt
#   assistant: Union[str, Text, Markdown] – the assistant's response
conversation_history: List[Dict[str, Any]] = []
# A list of attachments for the current session. Each attachment is a dict
# with keys 'name' and 'content'. For large files only the name is stored
# when saving and loading sessions.
attachments: List[Dict[str, Any]] = []
# Persistent system prompt applied to all future AI responses
system_prompt: str = ""
# Generation configuration. These settings can be tweaked via `/set`.
config: Dict[str, Any] = {
    "model": "placeholder",
    "temperature": 0.7,
    "top_k": 1,
    "top_p": 1.0,
}


def clear_terminal() -> None:
    """Clear the user's terminal window using OS appropriate commands."""
    os.system("cls" if os.name == "nt" else "clear")


def attach_file(path: str) -> Text:
    """Attach a local file to the current conversation.

    If the path does not exist or is missing, an error message is
    returned. Otherwise the file's binary content is read and stored
    alongside its base filename. Attachments are not persisted across
    sessions when reloaded to avoid bloating JSON files.
    """
    if not path:
        return Text("❌ Attach command requires a file path.", style="bold red")
    if not os.path.isfile(path):
        return Text(f"❌ File not found: {path}", style="bold red")
    try:
        with open(path, "rb") as f:
            content = f.read()
        attachments.append({"name": os.path.basename(path), "content": content})
        return Text(f"📎 Attached {os.path.basename(path)}", style="cyan")
    except Exception as exc:
        return Text(f"❌ Failed to attach file: {exc}", style="bold red")


def save_session(filename: str) -> Text:
    """Persist the current session to a JSON file.

    The resulting file will contain the conversation history (user and
    assistant messages), a list of attachment names, the system prompt
    and the current configuration. The attachment contents themselves
    are omitted for brevity. If no filename is provided, a default
    ``session.json`` is used.
    """
    if not filename:
        filename = "session.json"
    data = {
        "conversation_history": conversation_history,
        "attachments": [{"name": att["name"]} for att in attachments],
        "system_prompt": system_prompt,
        "config": config,
    }
    try:
        with open(filename, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
        return Text(f"Session saved to {filename}", style="cyan")
    except Exception as exc:
        return Text(f"❌ Failed to save session: {exc}", style="bold red")


def load_session(filename: str) -> Text:
    """Load a previously saved session from a JSON file.

    The conversation history, attachments, system prompt and config are
    restored from the file. Attachment contents are not reloaded for
    safety; only their names are recorded.
    """
    if not filename:
        return Text("❌ Load command requires a filename.", style="bold red")
    if not os.path.isfile(filename):
        return Text(f"❌ Session file not found: {filename}", style="bold red")
    global conversation_history, attachments, system_prompt, config
    try:
        with open(filename, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        conversation_history = data.get("conversation_history", [])
        attachments = []
        for att in data.get("attachments", []):
            attachments.append({"name": att["name"], "content": b""})
        system_prompt = data.get("system_prompt", "")
        # merge config preserving unknown keys
        loaded_config = data.get("config", {})
        config.update(loaded_config)
        return Text(f"📂 Session loaded from {filename}", style="cyan")
    except Exception as exc:
        return Text(f"❌ Failed to load session: {exc}", style="bold red")


def export_markdown(filename: str) -> Text:
    """Export the current conversation to a Markdown file.

    Each user and assistant turn will become its own section. The
    persistent system prompt is included at the top if present. When no
    filename is provided ``conversation.md`` is used.
    """
    if not filename:
        filename = "conversation.md"
    try:
        with open(filename, "w", encoding="utf-8") as fh:
            if system_prompt:
                fh.write(f"## System Prompt\n\n{system_prompt}\n\n")
            for turn in conversation_history:
                fh.write(f"### User\n\n{turn['user']}\n\n")
                assistant_msg = turn.get("assistant", "")
                # Flatten Text or Markdown to plain text if necessary
                if isinstance(assistant_msg, (Text, Markdown)):
                    assistant_str = assistant_msg.plain if isinstance(assistant_msg, Text) else assistant_msg.text
                else:
                    assistant_str = str(assistant_msg)
                fh.write(f"### Assistant\n\n{assistant_str}\n\n")
        return Text(f"📄 Conversation exported to {filename}", style="cyan")
    except Exception as exc:
        return Text(f"❌ Failed to export conversation: {exc}", style="red")


def get_stats() -> Text:
    """Compute and return approximate token statistics for the session."""
    total_tokens = 0
    for turn in conversation_history:
        total_tokens += len(turn.get("user", "").split())
        assistant_msg = turn.get("assistant", "")
        # If assistant_msg is Text or Markdown, convert to string for splitting
        if isinstance(assistant_msg, (Text, Markdown)):
            assistant_str = assistant_msg.plain if isinstance(assistant_msg, Text) else assistant_msg.text
        else:
            assistant_str = str(assistant_msg)
        total_tokens += len(assistant_str.split())
    return Text(f"🧮 Approx token count: {total_tokens} (ignoring attachments)", style="light cyan")


def set_system_prompt(prompt: str) -> Text:
    """Set or clear the persistent system prompt for the session."""
    global system_prompt
    system_prompt = prompt.strip()
    if system_prompt:
        return Text("💡 System prompt set.", style="cyan")
    return Text("🗑️ System prompt cleared.", style="yellow")


def clear_history() -> Text:
    """Erase all conversation history and attachments."""
    conversation_history.clear()
    attachments.clear()
    return Text("Conversation history and attachments cleared.", style="light cyan")


def list_models() -> Text:
    """Return a list of available models. Placeholder implementation."""
    models = ["placeholder-model-1", "placeholder-model-2"]
    return Text("Available models:\n- " + "\n- ".join(models), style="light cyan")


def update_config(param: str, value: str) -> Text:
    """Update generation configuration parameters."""
    try:
        key = param.strip().lower()
        if key == "temperature":
            config["temperature"] = float(value)
        elif key == "top_k":
            config["top_k"] = int(value)
        elif key == "top_p":
            config["top_p"] = float(value)
        else:
            return Text(f"❌ Unknown config parameter: {param}", style="red")
        return Text(f"⚙️ Updated {param} to {value}", style="cyan")
    except Exception as exc:
        return Text(f"❌ Failed to update config: {exc}", style="red")


def simulate_ai_response(prompt: str) -> str:
    """
    Placeholder AI response generator.

    In a real implementation this function would call into the SaxoFlow
    backend or an external model. To illustrate streaming behaviour and
    attachments/system prompt awareness, the returned string echoes
    the user's prompt along with contextual information.
    """
    response = f"I received your message: '{prompt}'. (AI response placeholder)"
    if attachments:
        response += "\n\nAttached file(s): " + ", ".join(att["name"] for att in attachments)
    if system_prompt:
        response += f"\n\nSystem prompt: {system_prompt}"
    return response


def process_command(cmd: str) -> Optional[Any]:
    """
    Dispatch a slash command and return a renderable.

    Commands beginning with a slash (`/`) are intercepted here and may
    modify the global session state. For `/help` we delegate to
    ``handle_command`` defined in ``commands.py``. Returns ``None`` for
    commands that signal termination.
    """
    parts = cmd.strip().split(maxsplit=1)
    keyword = parts[0].lower()
    arg = parts[1].strip() if len(parts) > 1 else ""
    # Help is forwarded to handle_command so that the Markdown stays in one place
    if keyword in ["/help", "help"]:
        return handle_command("/help", console)
    elif keyword in ["/quit", "quit"]:
        return None
    elif keyword in ["/simulate", "simulate"]:
        return Text("Running simulation... (placeholder)", style="cyan")
    elif keyword in ["/synth", "synth"]:
        return Text("Running synthesis... (placeholder)", style="cyan")
    elif keyword in ["/ai", "ai"]:
        return Text("AI agent feature coming soon!", style="bold blue")
    elif keyword in ["/attach", "attach"]:
        return attach_file(arg)
    elif keyword in ["/save", "save"]:
        return save_session(arg)
    elif keyword in ["/load", "load"]:
        return load_session(arg)
    elif keyword in ["/export", "export"]:
        return export_markdown(arg)
    elif keyword in ["/stats", "stats"]:
        return get_stats()
    elif keyword in ["/system", "system"]:
        return set_system_prompt(arg)
    elif keyword in ["/clear", "clear"]:
        return clear_history()
    elif keyword in ["/models", "models"]:
        return list_models()
    elif keyword in ["/set", "set"]:
        if "=" in arg:
            param, val = arg.split("=", 1)
            return update_config(param, val)
        else:
            return Text("❌ Usage: /set &lt;parameter&gt;=&lt;value&gt;", style="red")
    else:
        # Unknown commands are routed through handle_command for a generic error
        return handle_command(cmd, console)


def main() -> None:
    """
    Entry point for the SaxoFlow CLI.

    This function sets up the prompt history, prints the banner and
    startup tips, then enters an infinite loop reading user input.
    It re‑renders the entire conversation each turn to accommodate
    dynamic terminal resizing. Commands are processed via
    ``process_command``; normal input is passed to ``simulate_ai_response``
    after a brief delay to simulate streaming.
    """
    cli_history = InMemoryHistory()
    session = PromptSession(history=cli_history)

    # Print the welcome banner and tips once at startup
    clear_terminal()
    print_banner(console)
    panel_width = int(console.width * 0.75)
    console.print(user_input_panel(
        "Welcome to SaxoFlow CLI! Take your first step toward mastering digital design and verification.",
        width=panel_width,
    ))
    console.print("")
    tips = Text(
        "Tips for getting started:\n"
        "1. Ask questions, edit files, or run commands.\n"
        "2. Be specific for the best results.\n"
        "3. Use /help to see available commands.\n"
        "4. Type /quit to exit the CLI.\n",
        style="rgb(255,215,0)",
    )
    console.print(tips)
    console.print("")

    while True:
        # Dynamically calculate panel width in case the terminal was resized
        panel_width = int(console.width * 0.75)
        # Render the conversation history
        for entry in conversation_history:
            # user turn
            upanel = user_input_panel(entry.get("user", ""), width=panel_width)
            console.print(upanel)
            # assistant turn
            assistant_msg = entry.get("assistant")
            if assistant_msg:
                # Convert strings to Text
                if isinstance(assistant_msg, str):
                    assistant_renderable = Text(assistant_msg)
                else:
                    assistant_renderable = assistant_msg
                opanel = ai_panel(assistant_renderable)
                console.print(opanel)
            console.print("")  # spacing between turns

        # Read user input
        try:
            user_input = session.prompt("> ")
        except (EOFError, KeyboardInterrupt):
            console.print("[cyan]Until next time, may your timing constraints always be met and your logic always latch-free.[/cyan]")
            break
        user_input = user_input.strip()
        if not user_input:
            # Re‑display the header if the user just presses Enter
            clear_terminal()
            print_banner(console)
            panel_width = int(console.width * 0.75)
            console.print(user_input_panel(
                "Welcome to SaxoFlow CLI! Take your first step toward mastering digital design and verification.",
                width=panel_width,
            ))
            console.print(tips)
            console.print("")
            continue

        # Handle slash commands
        if user_input.startswith("/") or user_input.lower().startswith("help"):
            renderable = process_command(user_input)
            if renderable is None:
                console.print("[cyan]Until next time, may your timing constraints always be met and your logic always latch-free.[/cyan]")
                break
            # Append the command and its output to the conversation history
            conversation_history.append({"user": user_input, "assistant": renderable})
        else:
            # Normal conversation – send to the AI
            conversation_history.append({"user": user_input})
            # Show a spinner while generating the response
            with console.status("[yellow]Thinking...", spinner="dots") as status:
                # Sleep for a moment to emulate latency and streaming
                time.sleep(1)
                response = simulate_ai_response(user_input)
            conversation_history[-1]["assistant"] = response

        # After each interaction, clear and re‑render everything
        clear_terminal()
        print_banner(console)
        panel_width = int(console.width * 0.75)
        console.print(user_input_panel(
            "Welcome to SaxoFlow CLI! Take your first step toward mastering digital design and verification.",
            width=panel_width,
        ))
        console.print(tips)
        console.print("")