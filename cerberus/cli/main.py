#!/usr/bin/env python3
"""
Cerberus CLI Entry Point

Command-line interface for Cerberus services.
"""

import sys
import argparse
from cerberus.services import (
    hash_text, hash_file, verify_hash,
    base64_encode, base64_decode, url_encode, url_decode,
    html_encode, html_decode, hex_encode, hex_decode,
    rot13_encode_text, morse_encode_text,
    generate_php_webshell, generate_reverse_shell,
    get_sql_injection_payloads, get_xss_payloads,
    is_tor_running, get_installation_instructions,
)


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


def cmd_encode(args):
    """Encode command."""
    if args.type == 'base64':
        result = base64_encode(args.text)
    elif args.type == 'url':
        result = url_encode(args.text)
    elif args.type == 'html':
        result = html_encode(args.text)
    elif args.type == 'hex':
        result = hex_encode(args.text)
    elif args.type == 'rot13':
        result = rot13_encode_text(args.text)
    elif args.type == 'morse':
        result = morse_encode_text(args.text)
    else:
        print(f"Unknown encoding: {args.type}")
        sys.exit(1)
    print(result)


def cmd_decode(args):
    """Decode command."""
    if args.type == 'base64':
        result = base64_decode(args.text)
    elif args.type == 'url':
        result = url_decode(args.text)
    elif args.type == 'html':
        result = html_decode(args.text)
    elif args.type == 'hex':
        result = hex_decode(args.text)
    elif args.type == 'rot13':
        result = rot13_encode_text(args.text)  # ROT13 is self-inverse
    else:
        print(f"Unknown decoding: {args.type}")
        sys.exit(1)
    
    if result:
        print(result)
    else:
        print("Error decoding")
        sys.exit(1)


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


def cmd_tor(args):
    """Tor-related commands."""
    if args.action == 'status':
        running = is_tor_running()
        print(f"Tor running: {'Yes ✓' if running else 'No ✗'}")
    elif args.action == 'install':
        print(get_installation_instructions())


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Cerberus - Cybersecurity Companion',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  cerberus hash "hello world"
  cerberus encode base64 "hello"
  cerberus decode base64 "aGVsbG8="
  cerberus payload webshell
  cerberus payload sqli
  cerberus tor status
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Hash command
    hash_parser = subparsers.add_parser('hash', help='Generate hash')
    hash_parser.add_argument('text', help='Text to hash')
    hash_parser.add_argument('-a', '--algorithm', default='sha256', 
                           choices=['md5', 'sha1', 'sha256', 'sha512', 'blake2'],
                           help='Hash algorithm')
    hash_parser.add_argument('-f', '--file', action='store_true', help='Hash file')
    hash_parser.set_defaults(func=cmd_hash)
    
    # Verify command
    verify_parser = subparsers.add_parser('verify', help='Verify hash')
    verify_parser.add_argument('text', help='Text to verify')
    verify_parser.add_argument('hash', help='Hash to verify against')
    verify_parser.add_argument('-a', '--algorithm', default='sha256',
                             choices=['md5', 'sha1', 'sha256', 'sha512', 'blake2'],
                             help='Hash algorithm')
    verify_parser.set_defaults(func=cmd_verify)
    
    # Encode command
    encode_parser = subparsers.add_parser('encode', help='Encode text')
    encode_parser.add_argument('type', choices=['base64', 'url', 'html', 'hex', 'rot13', 'morse'],
                              help='Encoding type')
    encode_parser.add_argument('text', help='Text to encode')
    encode_parser.set_defaults(func=cmd_encode)
    
    # Decode command
    decode_parser = subparsers.add_parser('decode', help='Decode text')
    decode_parser.add_argument('type', choices=['base64', 'url', 'html', 'hex', 'rot13'],
                              help='Decoding type')
    decode_parser.add_argument('text', help='Text to decode')
    decode_parser.set_defaults(func=cmd_decode)
    
    # Payload command
    payload_parser = subparsers.add_parser('payload', help='Generate payload')
    payload_parser.add_argument('type', choices=['webshell', 'reverse', 'sqli', 'xss'],
                              help='Payload type')
    payload_parser.add_argument('-v', '--variant', type=int, default=0, help='Webshell variant')
    payload_parser.add_argument('-s', '--shell', default='python', help='Shell type')
    payload_parser.add_argument('--lhost', default='10.10.10.10', help='Listen host')
    payload_parser.add_argument('--port', type=int, default=4444, help='Listen port')
    payload_parser.set_defaults(func=cmd_payload)
    
    # Tor command
    tor_parser = subparsers.add_parser('tor', help='Tor network operations')
    tor_parser.add_argument('action', choices=['status', 'install'], help='Action')
    tor_parser.set_defaults(func=cmd_tor)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == '__main__':
    main()
