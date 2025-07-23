# coolcli/panels.py
from rich.panel import Panel
from rich.text import Text

def user_input_panel(command: str, width: int = None) -> Panel:
    from rich.text import Text
    kwargs = {}
    if width is not None:
        kwargs["width"] = width
    return Panel(
        Text(f"> {command}", style="bold white"),
        border_style="cyan",
        title="saxoflow",
        title_align="left",
        padding=(0, 1),
        expand=False,
        **kwargs
    )

def output_panel(renderable, border_style="cyan", icon=None) -> Panel:
    """
    Wraps output (can be Text, Markdown, etc.) in a styled panel.
    Optionally adds an icon in the title.
    """
    icon_text = f"{icon} " if icon else ""
    return Panel(
        renderable,
        border_style=border_style,
        title=f"{icon_text}output",
        title_align="left",
        padding=(1, 2),        # More padding for output
        expand=True
    )

def error_panel(message: str) -> Panel:
    """
    Error panel with red border and icon.
    """
    return Panel(
        Text(f"❌ {message}", style="bold yellow"),
        border_style="red",
        title="error",
        title_align="left",
        padding=(1, 2),
        expand=True
    )

def ai_panel(renderable) -> Panel:
    """
    For future: panel for AI/assistant output.
    """
    return Panel(
        renderable,
        border_style="magenta",
        title="🤖 ai agent",
        title_align="left",
        padding=(1, 2),
        expand=True
    )

# Optionally add more: log_panel, info_panel, etc.
