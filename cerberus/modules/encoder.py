"""
Cerberus Encoder Module
Encoding and decoding utilities for security testing
"""

import base64
import urllib.parse
import html
import binascii
from typing import Optional

from ..core import Colors, box_title, menu_option, separator


# ============================================================
# MODULE FUNCTIONS
# ============================================================

def module_encoder():
    """Encoder/decoder module"""
    print(box_title("ENCODER - Encode/Decode Utilities"))
    
    print(f"""
{Colors.BOLD}Select an option:{Colors.RESET}
{menu_option('1', 'Base64 Encode', 'Encode text to Base64')}
{menu_option('2', 'Base64 Decode', 'Decode Base64 to text')}
{menu_option('3', 'URL Encode', 'URL encode text')}
{menu_option('4', 'URL Decode', 'URL decode text')}
{menu_option('5', 'HTML Encode', 'HTML entity encode')}
{menu_option('6', 'HTML Decode', 'HTML entity decode')}
{menu_option('7', 'Hex Encode', 'Encode text to hexadecimal')}
{menu_option('8', 'Hex Decode', 'Decode hexadecimal to text')}
{menu_option('9', 'Unicode Encode', 'Unicode escape sequences')}
{menu_option('10', 'ASCII Table', 'View ASCII character table')}
{menu_option('q', 'Back', 'Return to main menu')}
    """)
    
    choice = input(f"{Colors.CYAN}Select > {Colors.RESET}").strip().lower()
    
    if choice == "q":
        return
    elif choice == "1":
        base64_encode()
    elif choice == "2":
        base64_decode()
    elif choice == "3":
        url_encode()
    elif choice == "4":
        url_decode()
    elif choice == "5":
        html_encode()
    elif choice == "6":
        html_decode()
    elif choice == "7":
        hex_encode()
    elif choice == "8":
        hex_decode()
    elif choice == "9":
        unicode_encode()
    elif choice == "10":
        ascii_table()
    else:
        print(f"{Colors.RED}Invalid selection{Colors.RESET}")
    
    input(f"\n{Colors.GRAY}Press Enter to continue...{Colors.RESET}")


def base64_encode():
    """Encode text to Base64"""
    print(box_title("BASE64 ENCODE"))
    
    print(f"\n{Colors.CYAN}Enter text to encode:{Colors.RESET}")
    text = input(f"{Colors.YELLOW}> {Colors.RESET}").strip()
    
    if not text:
        print(f"{Colors.RED}Empty input!{Colors.RESET}")
        return
    
    encoded = base64.b64encode(text.encode()).decode()
    
    print(f"\n{Colors.BOLD}Base64 Encoded:{Colors.RESET}")
    print(separator(60))
    print(encoded)


def base64_decode():
    """Decode Base64 to text"""
    print(box_title("BASE64 DECODE"))
    
    print(f"\n{Colors.CYAN}Enter Base64 to decode:{Colors.RESET}")
    text = input(f"{Colors.YELLOW}> {Colors.RESET}").strip()
    
    if not text:
        print(f"{Colors.RED}Empty input!{Colors.RESET}")
        return
    
    try:
        decoded = base64.b64decode(text.encode()).decode()
        print(f"\n{Colors.BOLD}Decoded:{Colors.RESET}")
        print(separator(60))
        print(decoded)
    except Exception as e:
        print(f"\n{Colors.RED}Decode error: {e}{Colors.RESET}")


def url_encode():
    """URL encode text"""
    print(box_title("URL ENCODE"))
    
    print(f"\n{Colors.CYAN}Enter text to URL encode:{Colors.RESET}")
    text = input(f"{Colors.YELLOW}> {Colors.RESET}").strip()
    
    if not text:
        print(f"{Colors.RED}Empty input!{Colors.RESET}")
        return
    
    encoded = urllib.parse.quote(text)
    
    print(f"\n{Colors.BOLD}URL Encoded:{Colors.RESET}")
    print(separator(60))
    print(encoded)


def url_decode():
    """URL decode text"""
    print(box_title("URL DECODE"))
    
    print(f"\n{Colors.CYAN}Enter URL encoded text:{Colors.RESET}")
    text = input(f"{Colors.YELLOW}> {Colors.RESET}").strip()
    
    if not text:
        print(f"{Colors.RED}Empty input!{Colors.RESET}")
        return
    
    try:
        decoded = urllib.parse.unquote(text)
        print(f"\n{Colors.BOLD}Decoded:{Colors.RESET}")
        print(separator(60))
        print(decoded)
    except Exception as e:
        print(f"\n{Colors.RED}Decode error: {e}{Colors.RESET}")


def html_encode():
    """HTML encode text"""
    print(box_title("HTML ENCODE"))
    
    print(f"\n{Colors.CYAN}Enter text to HTML encode:{Colors.RESET}")
    text = input(f"{Colors.YELLOW}> {Colors.RESET}").strip()
    
    if not text:
        print(f"{Colors.RED}Empty input!{Colors.RESET}")
        return
    
    encoded = html.escape(text)
    
    print(f"\n{Colors.BOLD}HTML Encoded:{Colors.RESET}")
    print(separator(60))
    print(encoded)


def html_decode():
    """HTML decode text"""
    print(box_title("HTML DECODE"))
    
    print(f"\n{Colors.CYAN}Enter HTML encoded text:{Colors.RESET}")
    text = input(f"{Colors.YELLOW}> {Colors.RESET}").strip()
    
    if not text:
        print(f"{Colors.RED}Empty input!{Colors.RESET}")
        return
    
    try:
        decoded = html.unescape(text)
        print(f"\n{Colors.BOLD}Decoded:{Colors.RESET}")
        print(separator(60))
        print(decoded)
    except Exception as e:
        print(f"\n{Colors.RED}Decode error: {e}{Colors.RESET}")


def hex_encode():
    """Encode text to hexadecimal"""
    print(box_title("HEX ENCODE"))
    
    print(f"\n{Colors.CYAN}Enter text to encode:{Colors.RESET}")
    text = input(f"{Colors.YELLOW}> {Colors.RESET}").strip()
    
    if not text:
        print(f"{Colors.RED}Empty input!{Colors.RESET}")
        return
    
    encoded = text.encode().hex()
    
    print(f"\n{Colors.BOLD}Hex Encoded:{Colors.RESET}")
    print(separator(60))
    print(encoded)


def hex_decode():
    """Decode hexadecimal to text"""
    print(box_title("HEX DECODE"))
    
    print(f"\n{Colors.CYAN}Enter hex to decode:{Colors.RESET}")
    text = input(f"{Colors.YELLOW}> {Colors.RESET}").strip()
    
    if not text:
        print(f"{Colors.RED}Empty input!{Colors.RESET}")
        return
    
    try:
        decoded = bytes.fromhex(text).decode()
        print(f"\n{Colors.BOLD}Decoded:{Colors.RESET}")
        print(separator(60))
        print(decoded)
    except Exception as e:
        print(f"\n{Colors.RED}Decode error: {e}{Colors.RESET}")


def unicode_encode():
    """Unicode escape sequences"""
    print(box_title("UNICODE ENCODE"))
    
    print(f"\n{Colors.CYAN}Enter text to Unicode encode:{Colors.RESET}")
    text = input(f"{Colors.YELLOW}> {Colors.RESET}").strip()
    
    if not text:
        print(f"{Colors.RED}Empty input!{Colors.RESET}")
        return
    
    encoded = ''.join(f'\\u{ord(c):04x}' for c in text)
    
    print(f"\n{Colors.BOLD}Unicode Encoded:{Colors.RESET}")
    print(separator(60))
    print(encoded)


def ascii_table():
    """Display ASCII table"""
    print(box_title("ASCII CHARACTER TABLE"))
    print(separator(60))
    
    print(f"\n{Colors.BOLD}Control Characters (0-31):{Colors.RESET}")
    control = {
        0: "NUL", 1: "SOH", 2: "STX", 3: "ETX", 4: "EOT", 5: "ENQ",
        6: "ACK", 7: "BEL", 8: "BS", 9: "TAB", 10: "LF", 11: "VT",
        12: "FF", 13: "CR", 14: "SO", 15: "SI", 16: "DLE", 17: "DC1",
        18: "DC2", 19: "DC3", 20: "DC4", 21: "NAK", 22: "SYN", 23: "ETB",
        24: "CAN", 25: "EM", 26: "SUB", 27: "ESC", 28: "FS", 29: "GS",
        30: "RS", 31: "US"
    }
    for i in range(32):
        print(f"  {i:3d} (0x{i:02x}): {control.get(i, '')}")
    
    print(f"\n{Colors.BOLD}Printable Characters (32-126):{Colors.RESET}")
    for i in range(32, 127, 8):
        row = []
        for j in range(i, min(i + 8, 127)):
            char = chr(j) if j >= 32 else "."
            row.append(f"{j:3d}: {char}")
        print("  " + "  | ".join(row))
    
    print(f"\n{Colors.BOLD}127: DEL{Colors.RESET}")


__all__ = ["module_encoder"]
