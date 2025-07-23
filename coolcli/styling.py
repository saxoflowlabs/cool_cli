# coolcli/styling.py
from rich.style import Style

SAXO_THEME = {
    "prompt": Style(color="green", bold=True),
    "logo_gradient": ["green", "bright_green", "cyan"],
    "info": Style(color="cyan"),
    "success": Style(color="green"),
    "warning": Style(color="yellow"),
    "error": Style(color="red", bold=True),
    "heading": Style(color="bright_cyan", bold=True),
    "box": "bold white on black",
    "border": "green",
}
