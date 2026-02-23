#!/usr/bin/env python3
"""
Cerberus CLI Entry Point

Command-line interface for Cerberus cybersecurity services.
All services are accessible via subcommands.
"""

import sys
import argparse

# Import all services
from cerberus.services import (
    # Encoding/Hashing
    hash_text, hash_file, verify_hash,
    base64_encode, base64_decode, url_encode, url_decode,
    html_encode, html_decode, hex_encode, hex_decode,
    rot13_encode_text, morse_encode_text,
    # Payloads
    generate_php_webshell, generate_reverse_shell,
    get_sql_injection_payloads, get_xss_payloads,
    # Tor
    is_tor_running, get_installation_instructions,
)

# Import additional services
try:
    from cerberus.services.scanner import NetworkScanner
    SCANNER_AVAILABLE = True
except ImportError:
    SCANNER_AVAILABLE = False

try:
    from cerberus.services.fuzzer import WebFuzzer
    FUZZER_AVAILABLE = True
except ImportError:
    FUZZER_AVAILABLE = False

try:
    from cerberus.services.exploit import ExploitFinder
    EXPLOIT_AVAILABLE = True
except ImportError:
    EXPLOIT_AVAILABLE = False

try:
    from cerberus.services.wifi import WiFiScanner
    WIFI_AVAILABLE = True
except ImportError:
    WIFI_AVAILABLE = False

try:
    from cerberus.services.forensics import ForensicsToolkit
    FORENSICS_AVAILABLE = True
except ImportError:
    FORENSICS_AVAILABLE = False

try:
    from cerberus.services.reporting import ReportGenerator
    REPORTING_AVAILABLE = True
except ImportError:
    REPORTING_AVAILABLE = False

try:
    from cerberus.modules.research import SecurityToolsResearcher
    RESEARCH_AVAILABLE = True
except ImportError:
    RESEARCH_AVAILABLE = False


# ============================================================
# Hash Commands
# ============================================================

def cmd_hash(args):
    """Hash command."""
    if args.file:
        result = hash_file(args.text, args.algorithm)
    else:
        result = hash_text(args.text, args.algorithm)
    
    if result:
        print(f"{args.algorithm.upper()}: {result}")
    else:
        print(f"Error hashing with {args.algorithm}")
        sys.exit(1)


def cmd_verify(args):
    """Verify hash command."""
    result = verify_hash(args.text, args.hash, args.algorithm)
    print(f"Verification: {'MATCH ✓' if result else 'NO MATCH ✗'}")


# ============================================================
# Encode/Decode Commands
# ============================================================

def cmd_encode(args):
    """Encode command."""
    encoders = {
        'base64': base64_encode,
        'url': url_encode,
        'html': html_encode,
        'hex': hex_encode,
        'rot13': rot13_encode_text,
        'morse': morse_encode_text,
    }
    
    if args.type in encoders:
        result = encoders[args.type](args.text)
        print(result)
    else:
        print(f"Unknown encoding: {args.type}")
        sys.exit(1)


def cmd_decode(args):
    """Decode command."""
    decoders = {
        'base64': base64_decode,
        'url': url_decode,
        'html': html_decode,
        'hex': hex_decode,
        'rot13': rot13_encode_text,  # ROT13 is self-inverse
    }
    
    if args.type in decoders:
        result = decoders[args.type](args.text)
        if result:
            print(result)
        else:
            print("Error decoding")
            sys.exit(1)
    else:
        print(f"Unknown decoding: {args.type}")
        sys.exit(1)


# ============================================================
# Payload Commands
# ============================================================

def cmd_payload(args):
    """Payload generation command."""
    if args.type == 'webshell':
        print(generate_php_webshell(args.variant))
    elif args.type == 'reverse':
        print(generate_reverse_shell(args.shell, args.lhost, args.port))
    elif args.type == 'sqli':
        for p in get_sql_injection_payloads():
            print(p)
    elif args.type == 'xss':
        for p in get_xss_payloads():
            print(p)


# ============================================================
# Tor Commands
# ============================================================

def cmd_tor(args):
    """Tor-related commands."""
    if args.action == 'status':
        running = is_tor_running()
        print(f"Tor running: {'Yes ✓' if running else 'No ✗'}")
    elif args.action == 'install':
        print(get_installation_instructions())


# ============================================================
# Network Scanner Commands
# ============================================================

def cmd_scan(args):
    """Network scanner command."""
    if not SCANNER_AVAILABLE:
        print("Scanner module not available")
        sys.exit(1)
    
    scanner = NetworkScanner()
    
    if args.scan_type == 'basic':
        result = scanner.port_scan(args.target, timeout=2)
        print(f"Open ports on {args.target}:")
        for port in result.get('open_ports', []):
            print(f"  ✓ {port['port']} ({port['service']})")
    elif args.scan_type == 'nmap':
        result = scanner.nmap_scan(args.target, args.ports)
        print(result.get('output', result.get('error', 'Error')))
    elif args.scan_type == 'subdomain':
        result = scanner.subdomain_enum(args.target)
        print(f"Subdomains found: {len(result.get('subdomains', []))}")
        for s in result.get('subdomains', [])[:10]:
            print(f"  • {s}")


# ============================================================
# Web Fuzzer Commands
# ============================================================

def cmd_fuzz(args):
    """Web fuzzer command."""
    if not FUZZER_AVAILABLE:
        print("Fuzzer module not available")
        sys.exit(1)
    
    fuzzer = WebFuzzer()
    
    if args.fuzz_type == 'dir':
        result = fuzzer.dir_scan(args.target)
        print(f"Directories found: {len(result.get('found', []))}")
        for p in result.get('found', [])[:20]:
            print(f"  ✓ {p}")
    elif args.fuzz_type == 'subdomain':
        result = fuzzer.subdomain_enum(args.target)
        print(f"Subdomains found: {len(result.get('found', []))}")
        for s in result.get('found', [])[:10]:
            print(f"  • {s}")
    elif args.fuzz_type == 'cms':
        result = fuzzer.cms_detect(args.target)
        print(f"CMS: {result.get('cms', 'Unknown')}")
        print(f"Version: {result.get('version', 'Unknown')}")
    elif args.fuzz_type == 'tech':
        result = fuzzer.tech_detect(args.target)
        print("Technologies:")
        for t in result.get('tech', []):
            print(f"  • {t}")


# ============================================================
# Exploit Finder Commands
# ============================================================

def cmd_exploit(args):
    """Exploit finder command."""
    if not EXPLOIT_AVAILABLE:
        print("Exploit module not available")
        sys.exit(1)
    
    finder = ExploitFinder()
    
    if args.exploit_type == 'search':
        result = finder.searchsploit_search(args.keyword)
        if 'error' in result:
            print(f"Error: {result['error']}")
        else:
            print(f"Results for '{args.keyword}':")
            for r in result.get('results', [])[:10]:
                print(f"  • {r}")
    elif args.exploit_type == 'cve':
        result = finder.search_cve(args.keyword)
        if 'error' in result:
            print(f"Error: {result['error']}")
        else:
            print(result)
    elif args.exploit_type == 'github':
        result = finder.github_exploits(args.keyword)
        if 'error' in result:
            print(f"Error: {result['error']}")
        else:
            print(f"GitHub exploits for '{args.keyword}':")
            for r in result.get('results', [])[:10]:
                print(f"  ★ {r['stars']} - {r['name']}")


# ============================================================
# WiFi Commands
# ============================================================

def cmd_wifi(args):
    """WiFi security command."""
    if not WIFI_AVAILABLE:
        print("WiFi module not available")
        sys.exit(1)
    
    wifi = WiFiScanner()
    
    if args.wifi_type == 'scan':
        result = wifi.airodump_scan(args.interface)
        if 'error' in result:
            print(f"Error: {result['error']}")
        else:
            print(f"Networks found: {result.get('count', 0)}")
            for net in result.get('networks', [])[:15]:
                print(f"  {net.get('ssid', 'Hidden')[:20]:20} | {net.get('bssid')} | PWR: {net.get('power')}")
    elif args.wifi_type == 'wps':
        result = wifi.wash_scan(args.interface)
        if 'error' in result:
            print(f"Error: {result['error']}")
        else:
            print("WPS-enabled networks:")
            for net in result.get('wps_networks', [])[:10]:
                print(f"  • {net.get('ssid')} | {net.get('bssid')}")


# ============================================================
# Forensics Commands
# ============================================================

def cmd_forensics(args):
    """Forensics command."""
    if not FORENSICS_AVAILABLE:
        print("Forensics module not available")
        sys.exit(1)
    
    forensics = ForensicsToolkit()
    
    if args.forensics_type == 'hash':
        result = forensics.file_hash(args.file)
        if 'error' in result:
            print(f"Error: {result['error']}")
        else:
            print(f"File: {result['file']}")
            print(f"Size: {result['size']} bytes")
            print(f"MD5:  {result['hashes']['md5']}")
            print(f"SHA1: {result['hashes']['sha1']}")
            print(f"SHA256: {result['hashes']['sha256']}")
    elif args.forensics_type == 'strings':
        result = forensics.strings_extract(args.file)
        print(f"Strings found: {len(result.get('strings', []))}")
        for s in result.get('strings', [])[:20]:
            print(f"  {s}")
    elif args.forensics_type == 'meta':
        result = forensics.metadata_extract(args.file)
        for k, v in result.items():
            print(f"{k}: {v}")
    elif args.forensics_type == 'hexdump':
        result = forensics.hexdump(args.file)
        print(result.get('hexdump', 'Error'))


# ============================================================
# Report Commands
# ============================================================

def cmd_report(args):
    """Report generator command."""
    if not REPORTING_AVAILABLE:
        print("Reporting module not available")
        sys.exit(1)
    
    if args.report_type == 'sample':
        from cerberus.services.reporting import create_sample_report
        report = create_sample_report()
        content = report.generate_markdown()
        if args.output:
            with open(args.output, 'w') as f:
                f.write(content)
            print(f"Report saved to {args.output}")
        else:
            print(content)
    elif args.report_type == 'create':
        # Create custom report
        report = ReportGenerator()
        report.set_metadata(title=args.title or "Security Assessment", target=args.target or "N/A")
        report.add_finding(args.severity, args.find_title, args.description)
        
        content = report.generate_markdown()
        if args.output:
            with open(args.output, 'w') as f:
                f.write(content)
            print(f"Report saved to {args.output}")
        else:
            print(content)


# ============================================================
# Research Commands
# ============================================================

def cmd_research(args):
    """Security tools research command."""
    if not RESEARCH_AVAILABLE:
        print("Research module not available")
        sys.exit(1)
    
    researcher = SecurityToolsResearcher()
    
    if args.research_type == 'list':
        tools = researcher.list_tools(category=args.category, available_only=args.installed)
        for tool in tools:
            status = "✓" if tool["installed"] else "✗"
            print(f"[{status}] {tool['name']} - {tool['desc']} ({tool['category']})")
    elif args.research_type == 'info':
        info = researcher.get_tool_info(args.tool)
        if info:
            print(f"\n=== {args.tool} ===")
            print(f"Description: {info['desc']}")
            print(f"Category: {info['category']}")
            print(f"Installed: {'Yes' if info['installed'] else 'No'}")
            print(f"Install: {info['install']}")
            print(f"Usage: {info['usage']}")
        else:
            print(f"Tool '{args.tool}' not found")
    elif args.research_type == 'scan':
        researcher.run_research()


# ============================================================
# Main Entry Point
# ============================================================

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Cerberus - Cybersecurity Companion',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available Services:
  hash/verify     - Generate and verify hashes
  encode/decode   - Encoding/decoding utilities
  payload         - Generate various payloads
  tor             - Tor network operations
  scan            - Network scanning
  fuzz            - Web fuzzing
  exploit         - Exploit finding
  wifi            - WiFi security
  forensics       - Digital forensics
  report          - Report generation
  research        - Security tools research

Examples:
  cerberus hash "hello world"
  cerberus encode base64 "hello"
  cerberus scan 192.168.1.1
  cerberus fuzz dir target.com
  cerberus exploit search wordpress
  cerberus wifi scan
  cerberus forensics hash file.exe
  cerberus research list --installed
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # ============== Hash ==============
    hash_parser = subparsers.add_parser('hash', help='Generate hash')
    hash_parser.add_argument('text', help='Text to hash')
    hash_parser.add_argument('-a', '--algorithm', default='sha256', 
                           choices=['md5', 'sha1', 'sha256', 'sha512', 'blake2'],
                           help='Hash algorithm')
    hash_parser.add_argument('-f', '--file', action='store_true', help='Hash file')
    hash_parser.set_defaults(func=cmd_hash)
    
    # ============== Verify ==============
    verify_parser = subparsers.add_parser('verify', help='Verify hash')
    verify_parser.add_argument('text', help='Text to verify')
    verify_parser.add_argument('hash', help='Hash to verify against')
    verify_parser.add_argument('-a', '--algorithm', default='sha256',
                             choices=['md5', 'sha1', 'sha256', 'sha512', 'blake2'],
                             help='Hash algorithm')
    verify_parser.set_defaults(func=cmd_verify)
    
    # ============== Encode ==============
    encode_parser = subparsers.add_parser('encode', help='Encode text')
    encode_parser.add_argument('type', choices=['base64', 'url', 'html', 'hex', 'rot13', 'morse'],
                              help='Encoding type')
    encode_parser.add_argument('text', help='Text to encode')
    encode_parser.set_defaults(func=cmd_encode)
    
    # ============== Decode ==============
    decode_parser = subparsers.add_parser('decode', help='Decode text')
    decode_parser.add_argument('type', choices=['base64', 'url', 'html', 'hex', 'rot13'],
                              help='Decoding type')
    decode_parser.add_argument('text', help='Text to decode')
    decode_parser.set_defaults(func=cmd_decode)
    
    # ============== Payload ==============
    payload_parser = subparsers.add_parser('payload', help='Generate payload')
    payload_parser.add_argument('type', choices=['webshell', 'reverse', 'sqli', 'xss'],
                              help='Payload type')
    payload_parser.add_argument('-v', '--variant', type=int, default=0, help='Webshell variant')
    payload_parser.add_argument('-s', '--shell', default='python', help='Shell type')
    payload_parser.add_argument('--lhost', default='10.10.10.10', help='Listen host')
    payload_parser.add_argument('--port', type=int, default=4444, help='Listen port')
    payload_parser.set_defaults(func=cmd_payload)
    
    # ============== Tor ==============
    tor_parser = subparsers.add_parser('tor', help='Tor network operations')
    tor_parser.add_argument('action', choices=['status', 'install'], help='Action')
    tor_parser.set_defaults(func=cmd_tor)
    
    # ============== Scanner ==============
    scan_parser = subparsers.add_parser('scan', help='Network scanning')
    scan_parser.add_argument('target', help='Target IP or domain')
    scan_parser.add_argument('--type', dest='scan_type', default='basic',
                           choices=['basic', 'nmap', 'subdomain'],
                           help='Scan type')
    scan_parser.add_argument('-p', '--ports', default='1-1000', help='Port range')
    scan_parser.set_defaults(func=cmd_scan)
    
    # ============== Fuzzer ==============
    fuzz_parser = subparsers.add_parser('fuzz', help='Web fuzzing')
    fuzz_parser.add_argument('target', help='Target URL or domain')
    fuzz_parser.add_argument('--type', dest='fuzz_type', default='dir',
                           choices=['dir', 'subdomain', 'cms', 'tech'],
                           help='Fuzz type')
    fuzz_parser.set_defaults(func=cmd_fuzz)
    
    # ============== Exploit ==============
    exploit_parser = subparsers.add_parser('exploit', help='Exploit finder')
    exploit_parser.add_argument('keyword', help='Search keyword or CVE ID')
    exploit_parser.add_argument('--type', dest='exploit_type', default='search',
                               choices=['search', 'cve', 'github'],
                               help='Search type')
    exploit_parser.set_defaults(func=cmd_exploit)
    
    # ============== WiFi ==============
    wifi_parser = subparsers.add_parser('wifi', help='WiFi security')
    wifi_parser.add_argument('interface', nargs='?', help='Wireless interface')
    wifi_parser.add_argument('--type', dest='wifi_type', default='scan',
                           choices=['scan', 'wps'],
                           help='WiFi action')
    wifi_parser.set_defaults(func=cmd_wifi)
    
    # ============== Forensics ==============
    forensics_parser = subparsers.add_parser('forensics', help='Digital forensics')
    forensics_parser.add_argument('file', help='Target file')
    forensics_parser.add_argument('--type', dest='forensics_type', default='hash',
                                 choices=['hash', 'strings', 'meta', 'hexdump'],
                                 help='Forensics action')
    forensics_parser.set_defaults(func=cmd_forensics)
    
    # ============== Report ==============
    report_parser = subparsers.add_parser('report', help='Report generator')
    report_parser.add_argument('--type', dest='report_type', default='sample',
                             choices=['sample', 'create'],
                             help='Report type')
    report_parser.add_argument('-o', '--output', help='Output file')
    report_parser.add_argument('--title', help='Report title')
    report_parser.add_argument('--target', help='Target assessed')
    report_parser.add_argument('--severity', default='medium', help='Finding severity')
    report_parser.add_argument('--find-title', default='Sample Finding', help='Finding title')
    report_parser.add_argument('--description', default='Description', help='Finding description')
    report_parser.set_defaults(func=cmd_report)
    
    # ============== Research ==============
    research_parser = subparsers.add_parser('research', help='Security tools research')
    research_parser.add_argument('--type', dest='research_type', default='list',
                               choices=['list', 'info', 'scan'],
                               help='Research action')
    research_parser.add_argument('-c', '--category', help='Filter by category')
    research_parser.add_argument('-i', '--installed', action='store_true', help='Show only installed')
    research_parser.add_argument('--tool', help='Get info on specific tool')
    research_parser.set_defaults(func=cmd_research)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == '__main__':
    main()
