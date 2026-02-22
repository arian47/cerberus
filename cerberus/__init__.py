"""
Cerberus - Cybersecurity Companion Package
The Three-Headed Hellhound of Security
"""

__version__ = "1.0.0"
__author__ = "Cerberus Team"

# Import main components for easy access
from .core import Colors, box_title, box_subtitle, menu_option, separator
from .connectors import get_connector, MODELS

__all__ = [
    "Colors",
    "box_title", 
    "box_subtitle",
    "menu_option",
    "separator",
    "get_connector",
    "MODELS",
]
