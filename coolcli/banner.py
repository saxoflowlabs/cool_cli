# from rich.console import Console
# from rich.text import Text
# from rich.panel import Panel
# import pyfiglet

# def print_banner(console: Console):
#     ascii_art = pyfiglet.figlet_format("SaxoFlow", font="big")
    
#     # Apply a horizontal gradient
#     gradient_text = Text(ascii_art)
#     gradient_text.stylize("bold", 0, len(gradient_text))
#     gradient_text.stylize("color(27)", 0, len(gradient_text)//8)           # Blue
#     gradient_text.stylize("color(63)", len(gradient_text)//8, len(gradient_text)//4)
#     gradient_text.stylize("color(99)", len(gradient_text)//4, len(gradient_text)//2)
#     gradient_text.stylize("color(135)", len(gradient_text)//2, 5 * len(gradient_text)//8)
#     gradient_text.stylize("color(171)", 5 * len(gradient_text)//8, 3 * len(gradient_text)//4)
#     gradient_text.stylize("color(207)", 3 * len(gradient_text)//4, 7 * len(gradient_text)//8)
#     gradient_text.stylize("color(213)", 7 * len(gradient_text)//8, len(gradient_text))  # Pink
    
#     console.print(gradient_text)
#     console.print("[bold magenta]Welcome to SaxoFlow CLI! Type /help to get started.[/bold magenta]\n")

#     welcome_text = "[bold]Welcome to [magenta]SaxoFlow CLI[/magenta][/bold]"
#     console.print(Panel(welcome_text, style="bold white on black", border_style="magenta"))

from rich.console import Console
from rich.text import Text
from rich.panel import Panel
import pyfiglet
from coolcli.styling import SAXO_THEME

def print_banner(console: Console):
    ascii_art = pyfiglet.figlet_format("SaxoFlow", font="cybermedium")

    styled_art = Text(ascii_art)
    for i, color in enumerate(SAXO_THEME["logo_gradient"]):
        start = i * len(styled_art) // len(SAXO_THEME["logo_gradient"])
        end = (i + 1) * len(styled_art) // len(SAXO_THEME["logo_gradient"])
        styled_art.stylize(color, start, end)

    console.print(styled_art)
    console.print(Panel(
        "[bold green]*[/bold green] Welcome to [bold cyan]SaxoFlow CLI[/bold cyan]",
        border_style=SAXO_THEME["border"],
        style=SAXO_THEME["box"]
    ))
