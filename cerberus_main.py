#!/usr/bin/env python3
"""
Cerberus - Cybersecurity Companion v1.0.0
The Three-Headed Hellhound of Security

This is the main entry point. Core functionality has been modularized
into the 'cerberus' package for better maintainability.
"""

import sys
import os

# Add the parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import from the cerberus package
from cerberus.core import (
    Colors, box_title, box_subtitle, menu_option, separator,
    status_indicator, load_env
)
from cerberus.connectors import get_connector, get_available_models, MODELS
from cerberus.modules import (
    module_osint,
    module_redteam,
    module_tools,
    module_advanced_attacks,
    module_payload_generator,
    module_hash_tools,
    module_encoder,
)


# ============================================================
# CERBERUS ART & MENU
# ============================================================

CERBERUS_ART = """

                                      ██████████████
                                  ████             ████
                                ██                     ██
                              ██                         ██
                             ██                           ██
                            ██                             ██
                           ██                               ██
                          ██                                 ██
                          ██                                 ██
                         ██                                   ██
                         ██                                   ██
                        ██                                     ██
                        ██           ████████████            ██
                        ██       ████           ████        ██
                        ██     ██                   ██      ██
                         ██   ██                       ██   ██
                          ████                           ████
                                                      

    ████████╗██╗  ██╗███████╗    ██████╗  ██████╗ ████████╗███████╗██╗  ██╗
    ╚══██╔══╝██║  ██║██╔════╝    ██╔══██╗██╔═══██╗╚══██╔══╝██╔════╝██║  ██║
       ██║   ███████║█████╗      ██████╔╝██║   ██║   ██║   █████╗  ███████║
       ██║   ██╔══██║██╔══╝      ██╔══██╗██║   ██║   ██║   ██╔══╝  ██╔══██║
       ██║   ██║  ██║███████╗    ██║  ██║╚██████╔╝   ██║   ███████╗██║  ██║
       ╚═╝   ╚═╝  ╚═╝╚══════╝    ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝

    ███████╗ ██████╗  ██████╗ ████████╗    ██████╗ ██╗  ██╗ ██████╗ ███╗   ██╗
    ██╔════╝██╔═══██╗██╔═══██╗╚══██╔══╝    ██╔══██╗██║  ██║██╔═══██╗████╗  ██║
    █████╗  ██║   ██║██║   ██║   ██║       ██████╔╝███████║██║   ██║██╔██╗ ██║
    ██╔══╝  ██║   ██║██║   ██║   ██║       ██╔═══╝ ██╔══██║██║   ██║██║╚██╗██║
    ███████╗╚██████╔╝╚██████╔╝   ██║       ██║     ██║  ██║╚██████╔╝██║ ╚████║
    ╚══════╝ ╚═════╝  ╚═════╝    ╚═╝       ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝

""" + """
MAIN MENU - Cerberus Premium
════════════════════════════════════════════════════════════════════════════
  [1] OSINT MODULE          - Threat Intelligence & Research
  [2] RED TEAM              - LLM Vulnerability Testing  
  [3] VULNERABILITIES       - Known Vulnerabilities Database
  [4] VULNERABILITY SCAN    - Security Assessment
  [5] INTELLIGENCE          - News & Threat Feeds
  [6] TOOLS                 - Utility Tools
  [7] ADVANCED ATTACKS      - Premium Red Team Techniques
  [8] PAYLOAD GEN           - Custom Payload Generator
  [9] HASH TOOLS            - Hash Generator & Cracker
  [10] ENCODER              - Encode/Decode Utilities
  [11] SETTINGS             - Configuration
  [12] UPDATE               - Pull Latest Vulnerabilities
════════════════════════════════════════════════════════════════════════════
  [q] QUIT                  - Exit Cerberus
════════════════════════════════════════════════════════════════════════════"""


# ============================================================
# MAIN
# ============================================================

def main():
    """Main entry point for Cerberus"""
    while True:
        print(CERBERUS_ART)
        choice = input(f"{Colors.CYAN}Select > {Colors.RESET}").strip().lower()
        
        if choice == "1":
            module_osint()
        elif choice == "2":
            module_redteam()
        elif choice == "3":
            print(box_title("VULNERABILITIES DATABASE"))
            from cerberus.modules.osint import show_vulnerabilities
            show_vulnerabilities()
            input(f"\n{Colors.GRAY}Press Enter to continue...{Colors.RESET}")
        elif choice == "4":
            print(f"\n{Colors.YELLOW}⚠️ Vulnerability Scanner - Coming Soon{Colors.RESET}")
            input(f"\n{Colors.GRAY}Press Enter to continue...{Colors.RESET}")
        elif choice == "5":
            print(f"\n{Colors.YELLOW}⚠️ Intelligence Feeds - Coming Soon{Colors.RESET}")
            input(f"\n{Colors.GRAY}Press Enter to continue...{Colors.RESET}")
        elif choice == "6":
            module_tools()
        elif choice == "7":
            module_advanced_attacks()
        elif choice == "8":
            module_payload_generator()
        elif choice == "9":
            module_hash_tools()
        elif choice == "10":
            module_encoder()
        elif choice == "11":
            module_settings()
        elif choice == "12":
            print(f"\n{Colors.CYAN}🔄 Use: python3 auto_update.py --scan{Colors.RESET}")
            input(f"\n{Colors.GRAY}Press Enter to continue...{Colors.RESET}")
        elif choice == "q":
            print(f"\n{Colors.GREEN}{separator(50, '═')}{Colors.RESET}")
            print(f"{Colors.GREEN}🔒 Cerberus v1.0.0 - Stay Secure{Colors.RESET}")
            print(f"{Colors.GREEN}{separator(50, '═')}{Colors.RESET}")
            break
        else:
            print(f"\n{Colors.RED}⚠️ Invalid selection. Please try again.{Colors.RESET}")


def module_settings():
    """Settings module"""
    from cerberus.core import (
        GOOGLE_API_KEY, GOOGLE_MODEL,
        OPENAI_API_KEY, OPENAI_MODEL,
        ANTHROPIC_API_KEY, ANTHROPIC_MODEL,
        XAI_API_KEY, XAI_MODEL,
        MINIMAX_API_KEY, MINIMAX_MODEL,
    )
    
    print(box_title("SETTINGS"))
    
    print(f"""
{Colors.BOLD}API Keys Configuration:{Colors.RESET}
{separator(60)}
  {status_indicator(bool(GOOGLE_API_KEY))}  Google API:    {GOOGLE_MODEL if GOOGLE_API_KEY else '(not set)'}
  {status_indicator(bool(OPENAI_API_KEY))}  OpenAI API:    {OPENAI_MODEL if OPENAI_API_KEY else '(not set)'}
  {status_indicator(bool(ANTHROPIC_API_KEY))}  Anthropic API: {ANTHROPIC_MODEL if ANTHROPIC_API_KEY else '(not set)'}
  {status_indicator(bool(XAI_API_KEY))}  xAI API:       {XAI_MODEL if XAI_API_KEY else '(not set)'}
  {status_indicator(bool(MINIMAX_API_KEY))}  MiniMax API:   {MINIMAX_MODEL if MINIMAX_API_KEY else '(not set)'}
{separator(60)}

Edit the {Colors.CYAN}.env{Colors.RESET} file to configure API keys.
    """)
    input(f"\n{Colors.GRAY}Press Enter to continue...{Colors.RESET}")


if __name__ == "__main__":
    main()
