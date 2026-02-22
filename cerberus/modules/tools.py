"""
Cerberus Tools Module
Utility tools for security testing
"""

from ..core import Colors, box_title, menu_option, separator


# ============================================================
# MODULE FUNCTIONS
# ============================================================

def module_tools():
    """Utility Tools Module"""
    print(box_title("UTILITY TOOLS"))
    
    print(f"""
{Colors.BOLD}Select a tool:{Colors.RESET}
{menu_option('1', 'Hash Generator', 'Generate hashes from text')}
{menu_option('2', 'Base64 Encoder/Decoder', 'Encode or decode Base64')}
{menu_option('3', 'URL Encoder', 'URL encode/decode strings')}
{menu_option('4', 'Password Generator', 'Generate secure passwords')}
{menu_option('5', 'Back', 'Return to main menu')}
{separator(60)}
    """)
    choice = input(f"{Colors.CYAN}Select > {Colors.RESET}").strip()
    if choice == "5":
        return
    print(f"\n{Colors.YELLOW}⚠️ Module under development{Colors.RESET}")
    input(f"\n{Colors.GRAY}Press Enter to continue...{Colors.RESET}")


__all__ = ["module_tools"]
