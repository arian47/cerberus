"""
Cerberus Core Module
Formatting helpers, colors, and shared utilities
"""

import os
import sys

# ============================================================
# FORMATTING HELPERS
# ============================================================

class Colors:
    """ANSI color codes for terminal output"""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"
    
    # Background colors
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_BLUE = "\033[44m"
    BG_YELLOW = "\033[43m"


def box_title(title: str, width: int = 60) -> str:
    """Create a boxed title"""
    padding = (width - len(title) - 2) // 2
    return f"\n{'═' * width}\n{' ' * padding}{title}\n{'═' * width}"


def box_subtitle(title: str, width: int = 60) -> str:
    """Create a boxed subtitle"""
    return f"{'─' * width}\n  {title}\n{'─' * width}"


def menu_option(num: str, text: str, description: str = "") -> str:
    """Format a menu option nicely"""
    if description:
        return f"  {Colors.CYAN}[{num}]{Colors.RESET} {text:<25} - {Colors.GRAY}{description}{Colors.RESET}"
    return f"  {Colors.CYAN}[{num}]{Colors.RESET} {text}"


def status_indicator(available: bool) -> str:
    """Return colored status indicator"""
    if available:
        return f"{Colors.GREEN}✓{Colors.RESET}"
    return f"{Colors.RED}✗{Colors.RESET}"


def separator(width: int = 60, char: str = "─") -> str:
    """Create a separator line"""
    return char * width


def header(text: str, width: int = 60) -> str:
    """Create a centered header"""
    padding = (width - len(text)) // 2
    return f"\n{' ' * padding}{Colors.BOLD}{text}{Colors.RESET}"


def print_boxed(title: str, width: int = 60):
    """Print a boxed title"""
    print(box_title(title, width))


def print_subtitle(title: str, width: int = 60):
    """Print a subtitle with separator"""
    print(box_subtitle(title, width))


# ============================================================
# CONFIGURATION
# ============================================================

def load_env():
    """Load environment variables from .env file"""
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()


# Load environment on import
load_env()


# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GOOGLE_MODEL = os.getenv("GOOGLE_MODEL", "gemini-2.5-flash")
GOOGLE_ENDPOINT = os.getenv("GOOGLE_ENDPOINT", "https://generativelanguage.googleapis.com/v1beta/models")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT", "https://api.openai.com/v1/chat/completions")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")
ANTHROPIC_ENDPOINT = os.getenv("ANTHROPIC_ENDPOINT", "https://api.anthropic.com/v1/messages")

XAI_API_KEY = os.getenv("XAI_API_KEY", "")
XAI_MODEL = os.getenv("XAI_MODEL", "grok-3")
XAI_ENDPOINT = os.getenv("XAI_ENDPOINT", "https://api.x.ai/v1/chat/completions")

MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY", "")
MINIMAX_MODEL = os.getenv("MINIMAX_MODEL", "MiniMax-M2.5")
MINIMAX_ENDPOINT = os.getenv("MINIMAX_ENDPOINT", "https://api.minimax.io/v1/chat/completions")


# ============================================================
# EXPORTS
# ============================================================

__all__ = [
    "Colors",
    "box_title",
    "box_subtitle",
    "menu_option",
    "status_indicator",
    "separator",
    "header",
    "print_boxed",
    "print_subtitle",
    "load_env",
    "GOOGLE_API_KEY",
    "GOOGLE_MODEL",
    "GOOGLE_ENDPOINT",
    "OPENAI_API_KEY",
    "OPENAI_MODEL",
    "OPENAI_ENDPOINT",
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_MODEL",
    "ANTHROPIC_ENDPOINT",
    "XAI_API_KEY",
    "XAI_MODEL",
    "XAI_ENDPOINT",
    "MINIMAX_API_KEY",
    "MINIMAX_MODEL",
    "MINIMAX_ENDPOINT",
]
