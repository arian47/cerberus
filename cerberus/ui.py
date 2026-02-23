"""
Cerberus Premium UI Module
Rich-powered terminal UI for a modern, premium CLI experience
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.style import Style
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.prompt import Prompt, Confirm, PromptBase
from rich.live import Live
from rich.layout import Layout
from rich.align import Align
from rich.box import Box, DOUBLE, ROUNDED, SIMPLE
from rich.theme import Theme
from rich.color import Color
from rich.color_triplet import ColorTriplet

# Custom theme for Cerberus
custom_theme = Theme({
    "red": "#ff4757",
    "green": "#2ed573", 
    "yellow": "#ffa502",
    "blue": "#1e90ff",
    "magenta": "#ff6b81",
    "cyan": "#00d2d3",
    "white": "#ffffff",
    "gray": "#747d8c",
    "bold": "bold",
    "bright_red": "#ff4757",
    "bright_green": "#7bed9f",
    "bright_yellow": "#eccc68",
})

console = Console(theme=custom_theme)


def print_header(title: str = "CERBERUS", subtitle: str = "Cybersecurity Companion v1.0.0"):
    """Print a fancy header with gradient effect"""
    header = Table(box=None, pad_edge=False)
    header.add_column(justify="center")
    
    title_text = Text()
    title_text.append("█" * 60 + "\n", style="bold cyan")
    title_text.append(f"  {title}  \n", style="bold magenta")
    title_text.append(f"  {subtitle}\n", style="dim gray")
    title_text.append("█" * 60, style="bold cyan")
    
    console.print(Panel(title_text, box=DOUBLE, border_style="cyan", padding=(0, 0)))


def print_menu(title: str, options: list, descriptions: list = None, footers: list = None):
    """
    Print a premium styled menu
    
    Args:
        title: Menu title
        options: List of option numbers/letters
        descriptions: Optional list of descriptions (parallel to options)
        footers: Optional footer options like [b] BACK, [q] QUIT
    """
    table = Table(box=None, show_header=False, padding=(0, 2))
    table.add_column(style="cyan", width=4)
    table.add_column(style="white")
    
    for i, opt in enumerate(options):
        desc = descriptions[i] if descriptions and i < len(descriptions) else ""
        table.add_row(f"[bold cyan][{opt}][/bold cyan]", f"{opt} - {desc}" if desc else f"{opt}")
    
    # Build the panel content
    content = Text()
    content.append(f"{title}\n", style="bold yellow")
    content.append("─" * 50 + "\n", style="dim")
    
    for i, opt in enumerate(options):
        desc = descriptions[i] if descriptions and i < len(descriptions) else ""
        if desc:
            content.append(f"  [{opt}] ", style="cyan bold")
            content.append(f"{desc}\n", style="white")
        else:
            content.append(f"  [{opt}]\n", style="cyan bold")
    
    if footers:
        content.append("─" * 50 + "\n", style="dim")
        for footer in footers:
            content.append(f"  {footer}\n", style="dim gray")
    
    console.print(Panel(content, box=ROUNDED, border_style="cyan", padding=(1, 2)))


def print_submenu(title: str, options: list, descriptions: list = None):
    """Print a submenu with back/quit options"""
    footers = ["[b] BACK - Return to Main Menu", "[q] QUIT - Exit Cerberus"]
    print_menu(title, options, descriptions, footers)


def print_success(message: str):
    """Print success message"""
    console.print(f"[bold green]✓[/bold green] [green]{message}[/green]")


def print_error(message: str):
    """Print error message"""
    console.print(f"[bold red]✗[/bold red] [red]{message}[/red]")


def print_warning(message: str):
    """Print warning message"""
    console.print(f"[bold yellow]⚠[/bold yellow] [yellow]{message}[/yellow]")


def print_info(message: str):
    """Print info message"""
    console.print(f"[bold blue]ℹ[/bold blue] [blue]{message}[/blue]")


def print_header_box(title: str, width: int = 60):
    """Print a header box"""
    title_text = Text(f" {title} ", style="bold cyan")
    console.print(Panel(title_text, box=DOUBLE, border_style="cyan", padding=(0, 1)))


def print_model_table(models: dict, available: list = None):
    """Print a table of available models"""
    table = Table(title="[bold]Available Models[/bold]", box=ROUNDED)
    table.add_column("#", style="cyan", justify="right", width=4)
    table.add_column("Model", style="white")
    table.add_column("Vendor", style="magenta", justify="center")
    table.add_column("Status", justify="center")
    
    for key, model in models.items():
        status = "✓" if key in (available or []) else "✗"
        status_style = "green" if status == "✓" else "red"
        
        table.add_row(
            f"[cyan]{key}[/cyan]",
            model["name"],
            model["vendor"],
            f"[{status_style}]{status}[/{status_style}]"
        )
    
    console.print(table)


def print_payload_table(payloads: dict):
    """Print a table of payloads"""
    table = Table(title="[bold]Available Payloads[/bold]", box=ROUNDED)
    table.add_column("#", style="cyan", justify="right", width=4)
    table.add_column("Payload", style="white")
    table.add_column("Preview", style="gray")
    
    for i, (key, payload) in enumerate(payloads.items(), 1):
        preview = payload[:45] + "..." if len(payload) > 45 else payload
        table.add_row(
            f"[cyan]{i}[/cyan]",
            key,
            preview
        )
    
    console.print(table)


def print_api_keys_table():
    """Print API keys configuration table"""
    from cerberus import (
        GOOGLE_API_KEY, GOOGLE_MODEL,
        OPENAI_API_KEY, OPENAI_MODEL,
        ANTHROPIC_API_KEY, ANTHROPIC_MODEL,
        XAI_API_KEY, XAI_MODEL,
        MINIMAX_API_KEY, MINIMAX_MODEL
    )
    
    table = Table(title="[bold]API Keys Configuration[/bold]", box=ROUNDED)
    table.add_column("Provider", style="cyan", justify="center")
    table.add_column("Status", justify="center")
    table.add_column("Model", style="white")
    
    apis = [
        ("Google", GOOGLE_API_KEY, GOOGLE_MODEL),
        ("OpenAI", OPENAI_API_KEY, OPENAI_MODEL),
        ("Anthropic", ANTHROPIC_API_KEY, ANTHROPIC_MODEL),
        ("xAI", XAI_API_KEY, XAI_MODEL),
        ("MiniMax", MINIMAX_API_KEY, MINIMAX_MODEL),
    ]
    
    for provider, key, model in apis:
        status = "✓ Configured" if key else "✗ Not Set"
        status_style = "green" if key else "red"
        model_display = model if key else "(not set)"
        
        table.add_row(
            provider,
            f"[{status_style}]{status}[/{status_style}]",
            model_display
        )
    
    console.print(table)


def get_input(prompt_text: str = "Select", default: str = "") -> str:
    """Get input with styled prompt"""
    if default:
        result = Prompt.ask(f"[bold cyan]{prompt_text} >[/bold cyan] [dim]({default})[/dim]")
    else:
        result = Prompt.ask(f"[bold cyan]{prompt_text} >[/bold cyan]")
    return result.strip()


def get_user_input(prompt_text: str = "Select", default: str = "") -> str:
    """Get user input - alias for get_input"""
    return get_input(prompt_text, default)


def get_yes_no(prompt_text: str) -> bool:
    """Get yes/no confirmation"""
    return Confirm.ask(f"[bold cyan]{prompt_text}[/bold cyan]")


def print_loading(message: str = "Loading"):
    """Create a loading spinner context"""
    return Progress(
        SpinnerColumn(style="cyan"),
        TextColumn("[progress.description]{task.description}", style="cyan"),
        console=console,
        transient=True
    )


def create_progress():
    """Create a progress bar"""
    return Progress(
        SpinnerColumn(style="cyan"),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=None, complete_style="cyan"),
        TaskProgressColumn(),
        console=console,
        transient=True
    )


def clear_screen():
    """Clear the terminal screen"""
    console.clear()


def pause(message: str = "Press Enter to continue..."):
    """Pause for user input"""
    console.print(f"\n[dim]{message}[/dim]")
    input()


# ============================================================
# LEGACY COMPATIBILITY FUNCTIONS
# ============================================================

def box_title(title: str, width: int = 60) -> str:
    """Legacy function - returns string (for compatibility)"""
    return f"\n{'═' * width}\n{title}\n{'═' * width}"


def status_indicator(available: bool) -> str:
    """Legacy function - returns string (for compatibility)"""
    return "✓" if available else "✗"


def separator(width: int = 60, char: str = "─") -> str:
    """Legacy function - returns string (for compatibility)"""
    return char * width
