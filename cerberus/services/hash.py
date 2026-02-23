"""
Cerberus Hash Service

Microservice for hash generation, verification, and analysis.
Supports multiple hash algorithms including MD5, SHA-1, SHA-256, etc.
"""

import hashlib
import hmac
import os
from typing import Optional, Dict, List


class HashService:
    """
    Service for hash operations.
    Provides hash generation, verification, and file hashing.
    """
    
    # Supported hash algorithms
    SUPPORTED_ALGORITHMS = [
        'md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512',
        'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512',
        'blake2b', 'blake2s', 'shake_128', 'shake_256'
    ]
    
    # Algorithm info
    ALGORITHM_INFO = {
        'md5': {'name': 'MD5', 'length': 32, 'security': 'Low'},
        'sha1': {'name': 'SHA-1', 'length': 40, 'security': 'Low'},
        'sha224': {'name': 'SHA-224', 'length': 56, 'security': 'Medium'},
        'sha256': {'name': 'SHA-256', 'length': 64, 'security': 'High'},
        'sha384': {'name': 'SHA-384', 'length': 96, 'security': 'High'},
        'sha512': {'name': 'SHA-512', 'length': 128, 'security': 'High'},
        'sha3_224': {'name': 'SHA3-224', 'length': 56, 'security': 'High'},
        'sha3_256': {'name': 'SHA3-256', 'length': 64, 'security': 'High'},
        'sha3_384': {'name': 'SHA3-384', 'length': 96, 'security': 'High'},
        'sha3_512': {'name': 'SHA3-512', 'length': 128, 'security': 'High'},
        'blake2b': {'name': 'BLAKE2b', 'length': 128, 'security': 'High'},
        'blake2s': {'name': 'BLAKE2s', 'length': 64, 'security': 'High'},
    }
    
    def __init__(self):
        """Initialize the hash service."""
        self.algorithms = self.SUPPORTED_ALGORITHMS.copy()
    
    def hash_text(self, text: str, algorithm: str = 'sha256') -> Optional[str]:
        """
        Generate hash for given text.
        
        Args:
            text: Input text to hash
            algorithm: Hash algorithm to use
            
        Returns:
            Hexadecimal hash string or None if error
        """
        algorithm = algorithm.lower()
        
        if algorithm not in self.algorithms:
            return None
            
        try:
            hasher = hashlib.new(algorithm)
            hasher.update(text.encode('utf-8'))
            return hasher.hexdigest()
        except Exception:
            return None
    
    def hash_file(self, file_path: str, algorithm: str = 'sha256') -> Optional[str]:
        """
        Generate hash for a file.
        
        Args:
            file_path: Path to the file
            algorithm: Hash algorithm to use
            
        Returns:
            Hexadecimal hash string or None if error
        """
        algorithm = algorithm.lower()
        
        if algorithm not in self.algorithms:
            return None
            
        if not os.path.exists(file_path):
            return None
            
        try:
            hasher = hashlib.new(algorithm)
            with open(file_path, 'rb') as f:
                while chunk := f.read(8192):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception:
            return None
    
    def verify_hash(self, text: str, hash_to_verify: str, algorithm: str = 'sha256') -> bool:
        """
        Verify text against a hash.
        
        Args:
            text: Input text to verify
            hash_to_verify: Hash to compare against
            algorithm: Hash algorithm used
            
        Returns:
            True if hash matches, False otherwise
        """
        computed = self.hash_text(text, algorithm)
        if computed is None:
            return False
        return hmac.compare_digest(computed.lower(), hash_to_verify.lower())
    
    def get_algorithm_info(self, algorithm: str) -> Optional[Dict]:
        """
        Get information about a hash algorithm.
        
        Args:
            algorithm: Hash algorithm name
            
        Returns:
            Dictionary with algorithm info or None
        """
        return self.ALGORITHM_INFO.get(algorithm.lower())
    
    def list_algorithms(self) -> List[str]:
        """Get list of supported algorithms."""
        return self.algorithms.copy()
    
    def compare_hashes(self, hash1: str, hash2: str) -> bool:
        """
        Compare two hashes (timing-safe).
        
        Args:
            hash1: First hash
            hash2: Second hash
            
        Returns:
            True if hashes match
        """
        return hmac.compare_digest(hash1.lower(), hash2.lower())
    
    def generate_password_hash(self, password: str, salt: Optional[str] = None) -> Dict[str, str]:
        """
        Generate a secure password hash with salt.
        
        Args:
            password: Password to hash
            salt: Optional salt (generated if not provided)
            
        Returns:
            Dictionary with hash, salt, and algorithm
        """
        if salt is None:
            salt = os.urandom(32).hex()
            
        # Use PBKDF2-HMAC-SHA256
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        
        return {
            'hash': key.hex(),
            'salt': salt,
            'algorithm': 'pbkdf2_sha256'
        }
    
    def verify_password(self, password: str, password_hash: str, salt: str, 
                       algorithm: str = 'pbkdf2_sha256') -> bool:
        """
        Verify a password against a stored hash.
        
        Args:
            password: Password to verify
            password_hash: Stored hash
            salt: Salt used
            algorithm: Algorithm used
            
        Returns:
            True if password matches
        """
        if algorithm == 'pbkdf2_sha256':
            key = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                salt.encode('utf-8'),
                100000
            )
            return hmac.compare_digest(key.hex(), password_hash)
        return False


# Module-level convenience functions
_service = HashService()

def hash_text(text: str, algorithm: str = 'sha256') -> Optional[str]:
    """Generate hash for text."""
    return _service.hash_text(text, algorithm)

def hash_file(file_path: str, algorithm: str = 'sha256') -> Optional[str]:
    """Generate hash for file."""
    return _service.hash_file(file_path, algorithm)

def verify_hash(text: str, hash_to_verify: str, algorithm: str = 'sha256') -> bool:
    """Verify text against hash."""
    return _service.verify_hash(text, hash_to_verify, algorithm)

def get_algorithm_info(algorithm: str) -> Optional[Dict]:
    """Get algorithm info."""
    return _service.get_algorithm_info(algorithm)
