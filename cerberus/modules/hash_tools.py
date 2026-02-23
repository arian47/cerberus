"""
Cerberus Hash Tools Module
Hash generation, verification, and cracking utilities
"""

import hashlib
import secrets
import string
from typing import Dict, Optional

from ..core import Colors, box_title, menu_option, separator


# ============================================================
# HASH ALGORITHMS
# ============================================================

HASH_ALGORITHMS = {
    "1": {"name": "MD5", "function": "md5", "length": 32},
    "2": {"name": "SHA1", "function": "sha1", "length": 40},
    "3": {"name": "SHA256", "function": "sha256", "length": 64},
    "4": {"name": "SHA512", "function": "sha512", "length": 128},
    "5": {"name": "BLAKE2b", "function": "blake2b", "length": 96},
    "6": {"name": "BLAKE2s", "function": "blake2s", "length": 56},
}


# ============================================================
# MODULE FUNCTIONS
# ============================================================

def module_hash_tools():
    """Hash tools module"""
    print(box_title("HASH TOOLS - Premium"))
    
    print(f"""
{Colors.BOLD}Select an option:{Colors.RESET}
{menu_option('1', 'Generate Hash', 'Create hash from text')}
{menu_option('2', 'Verify Hash', 'Verify text against hash')}
{menu_option('3', 'Hash Lookup', 'Search hash in online databases')}
{menu_option('4', 'Compare Hashes', 'Compare two hashes')}
{menu_option('5', 'Password Generator', 'Generate secure passwords')}
{menu_option('q', 'Back', 'Return to main menu')}
    """)
    
    choice = input(f"{Colors.CYAN}Select > {Colors.RESET}").strip().lower()
    
    if choice == "q":
        return
    elif choice == "1":
        generate_hash()
    elif choice == "2":
        verify_hash()
    elif choice == "3":
        hash_lookup()
    elif choice == "4":
        compare_hashes()
    elif choice == "5":
        password_generator()
    else:
        print(f"{Colors.RED}Invalid selection{Colors.RESET}")
    
    input(f"\n{Colors.GRAY}Press Enter to continue...{Colors.RESET}")


def generate_hash():
    """Generate hash from input"""
    print(box_title("GENERATE HASH"))
    
    print(f"\n{Colors.CYAN}Enter text to hash:{Colors.RESET}")
    text = input(f"{Colors.YELLOW}> {Colors.RESET}").strip()
    
    if not text:
        print(f"{Colors.RED}Empty input!{Colors.RESET}")
        return
    
    print(f"\n{Colors.BOLD}Hashes:{Colors.RESET}")
    print(separator(60))
    
    for key, algo in HASH_ALGORITHMS.items():
        hash_func = getattr(hashlib, algo["function"])
        result = hash_func(text.encode()).hexdigest()
        print(f"  {algo['name']:<12}: {result}")


def verify_hash():
    """Verify text against a hash"""
    print(box_title("VERIFY HASH"))
    
    print(f"\n{Colors.CYAN}Enter the original text:{Colors.RESET}")
    text = input(f"{Colors.YELLOW}> {Colors.RESET}").strip()
    
    print(f"\n{Colors.CYAN}Enter the hash to verify:{Colors.RESET}")
    target_hash = input(f"{Colors.YELLOW}> {Colors.RESET}").strip().lower()
    
    if not text or not target_hash:
        print(f"{Colors.RED}Empty input!{Colors.RESET}")
        return
    
    # Detect algorithm by hash length
    algo_name = None
    for key, algo in HASH_ALGORITHMS.items():
        if len(target_hash) == algo["length"]:
            algo_name = algo["name"]
            algo_func = algo["function"]
            break
    
    if not algo_name:
        print(f"{Colors.RED}Unknown hash format{Colors.RESET}")
        return
    
    hash_func = getattr(hashlib, algo_func)
    result = hash_func(text.encode()).hexdigest()
    
    if result == target_hash:
        print(f"\n{Colors.GREEN}✅ MATCH! The text matches the {algo_name} hash.{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}❌ NO MATCH! The text does not match the hash.{Colors.RESET}")
        print(f"  Expected: {result}")
        print(f"  Got:      {target_hash}")


def hash_lookup():
    """Search for hash in online databases"""
    print(box_title("HASH LOOKUP"))
    
    print(f"\n{Colors.CYAN}Enter hash to lookup:{Colors.RESET}")
    hash_value = input(f"{Colors.YELLOW}> {Colors.RESET}").strip()
    
    if not hash_value:
        print(f"{Colors.RED}Empty input!{Colors.RESET}")
        return
    
    print(f"\n{Colors.YELLOW}Note: Online hash lookup requires internet access{Colors.RESET}")
    print(f"  Hash: {hash_value[:40]}{'...' if len(hash_value) > 40 else ''}")
    print(f"\n{Colors.GRAY}This feature would query hash databases like:{Colors.RESET}")
    print(f"  • CrackStation")
    print(f"  • HashKiller")
    print(f"  • OnlineHashCrack")


def compare_hashes():
    """Compare two hashes"""
    print(box_title("COMPARE HASHES"))
    
    print(f"\n{Colors.CYAN}Enter first hash:{Colors.RESET}")
    hash1 = input(f"{Colors.YELLOW}> {Colors.RESET}").strip().lower()
    
    print(f"\n{Colors.CYAN}Enter second hash:{Colors.RESET}")
    hash2 = input(f"{Colors.YELLOW}> {Colors.RESET}").strip().lower()
    
    if not hash1 or not hash2:
        print(f"{Colors.RED}Empty input!{Colors.RESET}")
        return
    
    if hash1 == hash2:
        print(f"\n{Colors.GREEN}✅ HASHES MATCH!{Colors.RESET}")
    else:
        print(f"\n{Colors.RED}❌ HASHES DIFFER{Colors.RESET}")
        print(f"  Length diff: {abs(len(hash1) - len(hash2))} characters")


def password_generator():
    """Generate secure passwords"""
    print(box_title("PASSWORD GENERATOR"))
    
    try:
        length = int(input(f"\n{Colors.CYAN}Password length (default 16): {Colors.RESET}").strip() or "16")
    except ValueError:
        length = 16
    
    length = max(8, min(128, length))
    
    use_special = input(f"{Colors.CYAN}Include special characters? (y/n): {Colors.RESET}").strip().lower() == "y"
    
    # Character sets
    chars = string.ascii_letters + string.digits
    if use_special:
        chars += string.punctuation
    
    print(f"\n{Colors.BOLD}Generated Passwords:{Colors.RESET}")
    print(separator(60))
    
    for i in range(5):
        password = ''.join(secrets.choice(chars) for _ in range(length))
        print(f"  {i+1}. {password}")
    
    print(f"\n{Colors.GRAY}Tip: Use a password manager to store passwords securely{Colors.RESET}")


__all__ = [
    "module_hash_tools", 
    "HASH_ALGORITHMS",
    # Pure functions for testing
    "generate_hash_md5",
    "generate_hash_sha256", 
    "generate_hash_sha512",
    "generate_hash_sha1",
    "generate_hash_blake2b",
    "generate_hash_blake2s",
    "verify_hash",
    "hash_file",
]


# ============================================================
# PURE HASH FUNCTIONS (for testing)
# ============================================================

def generate_hash_md5(text: str) -> str:
    """Generate MD5 hash (pure function)"""
    return hashlib.md5(text.encode()).hexdigest()


def generate_hash_sha1(text: str) -> str:
    """Generate SHA1 hash (pure function)"""
    return hashlib.sha1(text.encode()).hexdigest()


def generate_hash_sha256(text: str) -> str:
    """Generate SHA256 hash (pure function)"""
    return hashlib.sha256(text.encode()).hexdigest()


def generate_hash_sha512(text: str) -> str:
    """Generate SHA512 hash (pure function)"""
    return hashlib.sha512(text.encode()).hexdigest()


def generate_hash_blake2b(text: str) -> str:
    """Generate BLAKE2b hash (pure function)"""
    return hashlib.blake2b(text.encode()).hexdigest()


def generate_hash_blake2s(text: str) -> str:
    """Generate BLAKE2s hash (pure function)"""
    return hashlib.blake2s(text.encode()).hexdigest()


def verify_hash(text: str, hash_to_verify: str, algorithm: str = "sha256") -> bool:
    """
    Verify a text against a hash (pure function)
    
    Args:
        text: The original text to verify
        hash_to_verify: The hash to verify against
        algorithm: The hash algorithm to use (md5, sha1, sha256, sha512, blake2b, blake2s)
    
    Returns:
        True if the hash matches, False otherwise
    """
    algorithm = algorithm.lower()
    
    # Map algorithm names to hashlib functions
    hash_functions = {
        "md5": hashlib.md5,
        "sha1": hashlib.sha1,
        "sha256": hashlib.sha256,
        "sha512": hashlib.sha512,
        "blake2b": hashlib.blake2b,
        "blake2s": hashlib.blake2s,
    }
    
    if algorithm not in hash_functions:
        return False
    
    try:
        computed_hash = hash_functions[algorithm](text.encode()).hexdigest()
        return computed_hash.lower() == hash_to_verify.lower()
    except Exception:
        return False


def hash_file(file_path: str, algorithm: str = "sha256") -> Optional[str]:
    """
    Generate hash of a file (pure function)
    
    Args:
        file_path: Path to the file to hash
        algorithm: The hash algorithm to use (md5, sha1, sha256, sha512, blake2b, blake2s)
    
    Returns:
        The hash as a hex string, or None if file cannot be read
    """
    algorithm = algorithm.lower()
    
    # Map algorithm names to hashlib functions
    hash_functions = {
        "md5": hashlib.md5,
        "sha1": hashlib.sha1,
        "sha256": hashlib.sha256,
        "sha512": hashlib.sha512,
        "blake2b": hashlib.blake2b,
        "blake2s": hashlib.blake2s,
    }
    
    if algorithm not in hash_functions:
        return None
    
    try:
        hash_obj = hash_functions[algorithm]()
        with open(file_path, 'rb') as f:
            # Read file in chunks to handle large files
            for chunk in iter(lambda: f.read(4096), b''):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    except Exception:
        return None
