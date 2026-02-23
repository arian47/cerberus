"""
Cerberus CLI Renderer Service

Microservice for CLI UI rendering and interaction.
Handles menus, panels, tables, and user input.
"""

from typing import List, Dict, Optional, Any
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich import box
import sys
import os


class CLIRenderer:
    """
    Service for CLI UI rendering and user interaction.
    Handles menus, panels, tables, and input prompts.
    """
    
    def __init__(self, console: Console = None):
        """Initialize CLI renderer with optional console."""
        self.console = console or Console()
    
    # ==================== Menu Functions ====================
    
    def print_header(self, title: str = "CERBERUS", subtitle: str = "") -> None:
        """Print application header."""
        from rich.text import Text
        from rich.align import Align
        
        header = Text()
        header.append(f" {title} ", style="bold cyan")
        if subtitle:
            header.append(f"  |  {subtitle}", style="dim")
        
        self.console.print(Align.center(header))
        self.console.print()
    
    def print_main_menu(self, title: str = "Main Menu") -> None:
        """Print main menu options."""
        from rich.align import Align
        
        menu_items = [
            ("1", "Hash Tools", "Generate and verify hashes"),
            ("2", "Encoder/Decoder", "Various encoding methods"),
            ("3", "LLM Connectors", "Connect to AI models"),
            ("4", "Payload Generator", "Generate attack payloads"),
            ("5", "OSINT Tools", "Reconnaissance tools"),
            ("6", "Red Team Tools", "Post-exploitation tools"),
            ("7", "Security Issues", "Find vulnerabilities"),
            ("8", "Advanced Attacks", "Complex attack vectors"),
            ("9", "API Keys", "Manage API keys"),
            ("Q", "Quit", "Exit the application"),
        ]
        
        table = Table(box=box.ROUNDED, show_header=False, padding=(0, 2))
        table.add_column("Option", style="cyan bold", width=6)
        table.add_column("Menu Item", style="white")
        table.add_column("Description", style="dim")
        
        for option, item, desc in menu_items:
            table.add_row(option, item, desc)
        
        self.console.print(Panel(
            table,
            title=f"[bold cyan]{title}[/bold cyan]",
            border_style="cyan",
            box=box.ROUNDED
        ))
    
    def print_submenu(self, title: str, items: List[tuple], back: bool = True) -> None:
        """Print a submenu with items."""
        table = Table(box=box.ROUNDED, show_header=False, padding=(0, 2))
        table.add_column("Option", style="cyan bold", width=6)
        table.add_column("Menu Item", style="white")
        table.add_column("Description", style="dim")
        
        for option, item, desc in items:
            table.add_row(option, item, desc)
        
        if back:
            table.add_row("B", "Back", "Return to main menu")
        
        self.console.print(Panel(
            table,
            title=f"[bold cyan]{title}[/bold cyan]",
            border_style="cyan",
            box=box.ROUNDED
        ))
    
    def print_panel(self, title: str, content: str = None, style: str = "cyan") -> None:
        """Print a panel with title and content."""
        if content:
            self.console.print(Panel(
                content,
                title=f"[bold {style}]{title}[/bold {style}]",
                border_style=style,
                box=box.ROUNDED
            ))
        else:
            self.console.print(Panel(
                title=f"[bold {style}]{title}[/bold {style}]",
                border_style=style,
                box=box.ROUNDED
            ))
    
    # ==================== Output Functions ====================
    
    def print_success(self, msg: str) -> None:
        """Print success message."""
        self.console.print(f"[bold green]✓[/bold green] {msg}")
    
    def print_error(self, msg: str) -> None:
        """Print error message."""
        self.console.print(f"[bold red]✗[/bold red] {msg}")
    
    def print_warning(self, msg: str) -> None:
        """Print warning message."""
        self.console.print(f"[bold yellow]⚠[/bold yellow] {msg}")
    
    def print_info(self, msg: str) -> None:
        """Print info message."""
        self.console.print(f"[bold blue]ℹ[/bold blue] {msg}")
    
    def print_debug(self, msg: str) -> None:
        """Print debug message."""
        if os.getenv("DEBUG"):
            self.console.print(f"[dim]DEBUG:[/dim] {msg}")
    
    # ==================== Table Functions ====================
    
    def print_model_table(self, models: Dict, available: List = None) -> None:
        """Print AI model table."""
        table = Table(box=box.ROUNDED, show_header=True, header_style="bold cyan")
        table.add_column("#", width=4, style="cyan")
        table.add_column("Model", style="white")
        table.add_column("Vendor", style="green")
        table.add_column("Status", style="yellow")
        
        for num, info in models.items():
            status = "✓ Available" if available and num in available else "✗ Not configured"
            table.add_row(num, info.get("name", "Unknown"), info.get("vendor", "Unknown"), status)
        
        self.console.print(table)
    
    def print_api_keys(self, api_keys: Dict) -> None:
        """Print API keys status table."""
        table = Table(box=box.ROUNDED, show_header=True, header_style="bold cyan")
        table.add_column("Provider", style="cyan")
        table.add_column("Status", style="yellow")
        table.add_column("Key (first 8 chars)", style="white")
        
        for provider, key in api_keys.items():
            status = "✓ Configured" if key else "✗ Not set"
            key_preview = key[:8] + "..." if key else "-"
            table.add_row(provider.capitalize(), status, key_preview)
        
        self.console.print(Panel(
            table,
            title="[bold cyan]API Keys Status[/bold cyan]",
            border_style="cyan",
            box=box.ROUNDED
        ))
    
    def print_results_table(self, results: List[Dict], title: str = "Results") -> None:
        """Print results in a table format."""
        if not results:
            self.print_warning("No results to display")
            return
        
        # Get all keys from first result
        keys = list(results[0].keys())
        
        table = Table(box=box.ROUNDED, show_header=True, header_style="bold cyan")
        for key in keys:
            table.add_column(key.capitalize(), style="white")
        
        for result in results:
            table.add_row(*[str(result.get(k, "")) for k in keys])
        
        self.console.print(Panel(
            table,
            title=f"[bold cyan]{title}[/bold cyan]",
            border_style="cyan",
            box=box.ROUNDED
        ))
    
    # ==================== Input Functions ====================
    
    def get_input(self, prompt_text: str = "Select", default: str = "") -> str:
        """Get user input with prompt."""
        if default:
            result = Prompt.ask(f"[cyan]{prompt_text}[/cyan]", default=default)
        else:
            result = Prompt.ask(f"[cyan]{prompt_text}[/cyan]")
        return result.strip()
    
    def get_yes_no(self, prompt_text: str) -> bool:
        """Get yes/no confirmation."""
        return Confirm.ask(f"[cyan]{prompt_text}[/cyan]")
    
    def pause(self) -> None:
        """Pause for user input."""
        Prompt.ask("[dim]Press Enter to continue...[/dim]", default="")
    
    # ==================== Formatters ====================
    
    def box_title(self, title: str, width: int = 60) -> str:
        """Create boxed title string."""
        return f"┌{'─' * (width - 2)}┐\n│ {title.center(width - 4)} │\n└{'─' * (width - 2)}┘"
    
    def menu_option(self, num: str, text: str, description: str = "") -> str:
        """Format menu option."""
        if description:
            return f"[cyan]{num:>2}.[/cyan] {text:<20} - {description}"
        return f"[cyan]{num:>2}.[/cyan] {text}"
    
    def status_indicator(self, available: bool) -> str:
        """Get status indicator."""
        return "[green]✓[/green]" if available else "[red]✗[/red]"
    
    def separator(self, width: int = 60, char: str = "─") -> str:
        """Create separator string."""
        return char * width


# ==================== Module-level singleton ====================

_renderer = None

def get_renderer(console: Console = None) -> CLIRenderer:
    """Get CLI renderer singleton."""
    global _renderer
    if _renderer is None:
        _renderer = CLIRenderer(console)
    return _renderer


# ==================== Module-level convenience functions ====================

def print_header(title: str = "CERBERUS", subtitle: str = "") -> None:
    """Print application header."""
    get_renderer().print_header(title, subtitle)

def print_main_menu(title: str = "Main Menu") -> None:
    """Print main menu."""
    get_renderer().print_main_menu(title)

def print_submenu(title: str, items: list, back: bool = True) -> None:
    """Print submenu."""
    get_renderer().print_submenu(title, items, back)

def print_panel(title: str, content: str = None, style: str = "cyan") -> None:
    """Print panel."""
    get_renderer().print_panel(title, content, style)

def print_success(msg: str) -> None:
    """Print success message."""
    get_renderer().print_success(msg)

def print_error(msg: str) -> None:
    """Print error message."""
    get_renderer().print_error(msg)

def print_warning(msg: str) -> None:
    """Print warning message."""
    get_renderer().print_warning(msg)

def print_info(msg: str) -> None:
    """Print info message."""
    get_renderer().print_info(msg)

def print_model_table(models: dict, available: list = None) -> None:
    """Print model table."""
    get_renderer().print_model_table(models, available)

def print_api_keys(api_keys: dict) -> None:
    """Print API keys."""
    get_renderer().print_api_keys(api_keys)

def get_input(prompt_text: str = "Select") -> str:
    """Get user input."""
    return get_renderer().get_input(prompt_text)

def get_yes_no(prompt_text: str) -> bool:
    """Get yes/no."""
    return get_renderer().get_yes_no(prompt_text)

def pause() -> None:
    """Pause."""
    get_renderer().pause()

def box_title(title: str, width: int = 60) -> str:
    """Format box title."""
    return get_renderer().box_title(title, width)

def menu_option(num: str, text: str, description: str = "") -> str:
    """Format menu option."""
    return get_renderer().menu_option(num, text, description)

def status_indicator(available: bool) -> str:
    """Get status indicator."""
    return get_renderer().status_indicator(available)

def separator(width: int = 60, char: str = "─") -> str:
    """Create separator."""
    return get_renderer().separator(width, char)
