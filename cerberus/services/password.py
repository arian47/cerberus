"""
Cerberus Password Service

Microservice for password generation and security utilities.
"""

import random
import string
import secrets
import hashlib
from typing import List, Optional, Dict
import re


class PasswordService:
    """
    Service for password generation and security analysis.
    """
    
    # Common password patterns to check
    COMMON_PASSWORDS = [
        "password", "123456", "12345678", "qwerty", "abc123",
        "monkey", "1234567", "letmein", "trustno1", "dragon",
        "baseball", "iloveyou", "master", "sunshine", "ashley",
        "bailey", "passw0rd", "shadow", "123123", "654321",
        "superman", "qazwsx", "michael", "football", "password1",
        "password123", "welcome", "welcome1", "admin", "login"
    ]
    
    # Character sets
    LOWERCASE = string.ascii_lowercase
    UPPERCASE = string.ascii_uppercase
    DIGITS = string.digits
    SPECIAL = string.punctuation
    
    def __init__(self):
        """Initialize password service."""
        pass
    
    # ==================== Password Generation ====================
    
    def generate_password(self, length: int = 16, use_uppercase: bool = True,
                         use_digits: bool = True, use_special: bool = True,
                         exclude_ambiguous: bool = False) -> str:
        """
        Generate a secure random password.
        
        Args:
            length: Password length
            use_uppercase: Include uppercase letters
            use_digits: Include digits
            use_special: Include special characters
            exclude_ambiguous: Exclude ambiguous characters (0, O, l, 1, etc.)
            
        Returns:
            Generated password
        """
        # Build character pool
        chars = self.LOWERCASE
        if use_uppercase:
            chars += self.UPPERCASE
        if use_digits:
            chars += self.DIGITS
        if use_special:
            chars += self.SPECIAL
        
        # Remove ambiguous characters if requested
        if exclude_ambiguous:
            ambiguous = '0O1lI'
            chars = ''.join(c for c in chars if c not in ambiguous)
        
        # Generate password using secrets module for cryptographic strength
        password = ''.join(secrets.choice(chars) for _ in range(length))
        
        # Ensure at least one character from each requested set
        password = self._ensure_char_types(password, use_uppercase, use_digits, use_special, chars)
        
        return password
    
    def _ensure_char_types(self, password: str, use_uppercase: bool, 
                          use_digits: bool, use_special: bool, chars: str) -> str:
        """Ensure password contains at least one of each requested character type."""
        password = list(password)
        
        if use_uppercase and not any(c in self.UPPERCASE for c in password):
            pos = secrets.randbelow(len(password))
            password[pos] = secrets.choice(self.UPPERCASE)
        
        if use_digits and not any(c in self.DIGITS for c in password):
            pos = secrets.randbelow(len(password))
            password[pos] = secrets.choice(self.DIGITS)
        
        if use_special and not any(c in self.SPECIAL for c in password):
            pos = secrets.randbelow(len(password))
            password[pos] = secrets.choice(self.SPECIAL)
        
        return ''.join(password)
    
    def generate_passphrase(self, words: int = 4, separator: str = '-',
                           capitalize: bool = True) -> str:
        """
        Generate a passphrase from random words.
        
        Args:
            words: Number of words
            separator: Separator between words
            capitalize: Capitalize first letter of each word
            
        Returns:
            Generated passphrase
        """
        # Common words list (simplified - in production use EFF wordlist)
        wordlist = [
            "apple", "banana", "cherry", "dragon", "eagle", "falcon",
            "garden", "harbor", "island", "jungle", "knight", "lemon",
            "mountain", "night", "ocean", "planet", "queen", "river",
            "sunset", "thunder", "umbrella", "valley", "winter", "yellow",
            "zebra", "anchor", "bridge", "castle", "desert", "forest",
            "glacier", "horizon", "ivory", "jasper", "kingdom", "lavender",
            "meadow", "nebula", "orchid", "phoenix", "quartz", "rainbow",
            "silver", "tiger", "universe", "voyage", "wizard", "crystal"
        ]
        
        selected = [secrets.choice(wordlist) for _ in range(words)]
        
        if capitalize:
            selected = [word.capitalize() for word in selected]
        
        return separator.join(selected)
    
    # ==================== Password Analysis ====================
    
    def check_password_strength(self, password: str) -> Dict[str, any]:
        """
        Analyze password strength.
        
        Args:
            password: Password to analyze
            
        Returns:
            Dict with strength analysis
        """
        result = {
            'score': 0,
            'strength': 'weak',
            'suggestions': [],
            'entropy': 0,
            'length': len(password),
        }
        
        # Length scoring
        if len(password) >= 16:
            result['score'] += 30
        elif len(password) >= 12:
            result['score'] += 20
        elif len(password) >= 8:
            result['score'] += 10
        
        # Character variety
        has_lower = bool(re.search(r'[a-z]', password))
        has_upper = bool(re.search(r'[A-Z]', password))
        has_digit = bool(re.search(r'\d', password))
        has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
        
        if has_lower:
            result['score'] += 10
        if has_upper:
            result['score'] += 10
        if has_digit:
            result['score'] += 10
        if has_special:
            result['score'] += 20
        
        # Check for common passwords
        if password.lower() in self.COMMON_PASSWORDS:
            result['score'] = 0
            result['suggestions'].append("This is a commonly used password")
        
        # Check for patterns
        if self._has_repeated_chars(password):
            result['score'] -= 10
            result['suggestions'].append("Avoid repeated characters")
        
        if self._has_sequential_chars(password):
            result['score'] -= 10
            result['suggestions'].append("Avoid sequential characters")
        
        # Calculate entropy
        charset_size = 0
        if has_lower:
            charset_size += 26
        if has_upper:
            charset_size += 26
        if has_digit:
            charset_size += 10
        if has_special:
            charset_size += 32
        
        if charset_size > 0:
            result['entropy'] = len(password) * (charset_size ** 0.5)
        
        # Determine strength
        if result['score'] >= 70:
            result['strength'] = 'strong'
        elif result['score'] >= 40:
            result['strength'] = 'medium'
        else:
            result['strength'] = 'weak'
        
        return result
    
    def _has_repeated_chars(self, password: str) -> bool:
        """Check if password has repeated characters."""
        for i in range(len(password) - 2):
            if password[i] == password[i+1] == password[i+2]:
                return True
        return False
    
    def _has_sequential_chars(self, password: str) -> bool:
        """Check if password has sequential characters."""
        sequences = ['abcdefghijklmnopqrstuvwxyz', '0123456789', 'qwertyuiop', 'asdfghjkl', 'zxcvbnm']
        lower = password.lower()
        
        for seq in sequences:
            for i in range(len(seq) - 2):
                if seq[i:i+3] in lower:
                    return True
        return False
    
    def is_password_compromised(self, password: str) -> bool:
        """
        Check if password has been compromised (using SHA1 prefix).
        Uses Have I Been Pwned API.
        
        Args:
            password: Password to check
            
        Returns:
            True if compromised
        """
        try:
            import requests
            
            # Hash password with SHA1
            sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
            prefix = sha1_hash[:5]
            suffix = sha1_hash[5:]
            
            # Check against HIBP API
            response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}", 
                                   timeout=10)
            
            if response.status_code == 200:
                hashes = response.text.splitlines()
                for h in hashes:
                    if h.split(':')[0] == suffix:
                        return True
            
            return False
        except Exception:
            return False
    
    # ==================== Hash Lookup ====================
    
    def hash_lookup(self, hash_value: str, hash_type: str = 'md5') -> Optional[str]:
        """
        Look up hash in online databases.
        
        Args:
            hash_value: Hash to look up
            hash_type: Hash type (md5, sha1, sha256)
            
        Returns:
            Plain text if found, None otherwise
        """
        # This would require API integration
        # For now, return None
        return None
    
    # ==================== Password Generation Variants ====================
    
    def generate_pin(self, length: int = 4) -> str:
        """Generate a numeric PIN."""
        return ''.join(secrets.choice(self.DIGITS) for _ in range(length))
    
    def generate_api_key(self, length: int = 32) -> str:
        """Generate an API key."""
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    def generate_secure_token(self, length: int = 32) -> str:
        """Generate a secure random token."""
        return secrets.token_urlsafe(length)


# ==================== Module-level functions ====================

_service = None

def get_service() -> PasswordService:
    """Get password service instance."""
    global _service
    if _service is None:
        _service = PasswordService()
    return _service

def generate_password(length: int = 16, use_uppercase: bool = True,
                     use_digits: bool = True, use_special: bool = True,
                     exclude_ambiguous: bool = False) -> str:
    """Generate a secure password."""
    return get_service().generate_password(length, use_uppercase, use_digits, use_special, exclude_ambiguous)

def generate_passphrase(words: int = 4, separator: str = '-',
                        capitalize: bool = True) -> str:
    """Generate a passphrase."""
    return get_service().generate_passphrase(words, separator, capitalize)

def check_password_strength(password: str) -> Dict:
    """Check password strength."""
    return get_service().check_password_strength(password)

def is_password_compromised(password: str) -> bool:
    """Check if password is compromised."""
    return get_service().is_password_compromised(password)

def hash_lookup(hash_value: str, hash_type: str = 'md5') -> Optional[str]:
    """Look up hash."""
    return get_service().hash_lookup(hash_value, hash_type)

def generate_pin(length: int = 4) -> str:
    """Generate PIN."""
    return get_service().generate_pin(length)

def generate_api_key(length: int = 32) -> str:
    """Generate API key."""
    return get_service().generate_api_key(length)

def generate_secure_token(length: int = 32) -> str:
    """Generate secure token."""
    return get_service().generate_secure_token(length)
