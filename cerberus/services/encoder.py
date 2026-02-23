"""
Cerberus Encoder Service

Microservice for encoding and decoding operations.
Supports multiple encoding schemes including Base64, URL, HTML, Hex, etc.
"""

import base64
import urllib.parse
import html
import json
import codecs
import re
from typing import Optional, Dict, List


class EncoderService:
    """
    Service for encoding/decoding operations.
    Provides various encoding schemes for security testing.
    """
    
    # ROT13 lookup table
    _rot13_table = str.maketrans(
        'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
        'nopqrstuvwxyzabcdefghijklmNOPQRSTUVWXYZABCDEFGHIJKLM'
    )
    
    # Morse code mapping
    MORSE_CODE = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
        'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
        'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
        'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
        'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
        '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
        '8': '---..', '9': '----.', ' ': '/'
    }
    
    REVERSE_MORSE = {v: k for k, v in MORSE_CODE.items()}
    
    def __init__(self):
        """Initialize the encoder service."""
        pass
    
    # ==================== Base64 Operations ====================
    
    def base64_encode(self, text: str) -> str:
        """Encode text to Base64."""
        return base64.b64encode(text.encode('utf-8')).decode('ascii')
    
    def base64_decode(self, text: str) -> Optional[str]:
        """Decode Base64 to text."""
        try:
            return base64.b64decode(text.encode('ascii')).decode('utf-8')
        except Exception:
            return None
    
    # ==================== URL Operations ====================
    
    def url_encode(self, text: str) -> str:
        """URL encode text."""
        return urllib.parse.quote(text, safe='')
    
    def url_decode(self, text: str) -> Optional[str]:
        """URL decode text."""
        try:
            return urllib.parse.unquote(text)
        except Exception:
            return None
    
    # ==================== HTML Operations ====================
    
    def html_encode(self, text: str) -> str:
        """HTML encode text."""
        return html.escape(text)
    
    def html_decode(self, text: str) -> str:
        """HTML decode text."""
        return html.unescape(text)
    
    # ==================== Hex Operations ====================
    
    def hex_encode(self, text: str, separator: str = '') -> str:
        """Encode text to hex."""
        return separator.join(f'{ord(c):02x}' for c in text)
    
    def hex_decode(self, text: str, separator: str = '') -> Optional[str]:
        """Decode hex to text."""
        try:
            # Handle both with and without separator
            if separator:
                text = text.replace(separator, '')
            return codecs.decode(text, 'hex').decode('utf-8')
        except Exception:
            return None
    
    # ==================== Binary Operations ====================
    
    def binary_encode_text(self, text: str, separator: str = ' ') -> str:
        """Encode text to binary."""
        return separator.join(f'{ord(c):08b}' for c in text)
    
    def binary_decode_text(self, text: str, separator: str = ' ') -> Optional[str]:
        """Decode binary to text."""
        try:
            binaries = text.split(separator)
            return ''.join(chr(int(b, 2)) for b in binaries if b)
        except Exception:
            return None
    
    # ==================== JSON Operations ====================
    
    def json_encode_text(self, text: str) -> str:
        """JSON encode text."""
        return json.dumps(text)
    
    def json_decode_text(self, text: str) -> Optional[str]:
        """JSON decode text."""
        try:
            return json.loads(text)
        except Exception:
            return None
    
    # ==================== ROT13 Operations ====================
    
    def rot13_encode_text(self, text: str) -> str:
        """Encode text with ROT13."""
        return text.translate(self._rot13_table)
    
    def rot13_decode_text(self, text: str) -> str:
        """Decode ROT13 (same as encode)."""
        return text.translate(self._rot13_table)
    
    # ==================== Morse Code Operations ====================
    
    def morse_encode_text(self, text: str) -> str:
        """Encode text to Morse code."""
        return ' '.join(self.MORSE_CODE.get(c.upper(), c) for c in text)
    
    def morse_decode_text(self, text: str) -> Optional[str]:
        """Decode Morse code to text."""
        try:
            return ''.join(self.REVERSE_MORSE.get(c, c) for c in text.split())
        except Exception:
            return None
    
    # ==================== Unicode Operations ====================
    
    def unicode_encode(self, text: str) -> str:
        """Unicode escape text."""
        return '\\u' + '\\u'.join(f'{ord(c):04x}' for c in text)
    
    def unicode_decode(self, text: str) -> Optional[str]:
        """Unicode unescape text."""
        try:
            return text.encode('utf-8').decode('unicode_escape')
        except Exception:
            return None
    
    # ==================== ASCII Table ====================
    
    def ascii_table_generate(self, start: int = 33, end: int = 126) -> List[Dict]:
        """Generate ASCII table."""
        return [
            {'dec': i, 'hex': f'{i:02x}', 'oct': f'{i:03o}', 'char': chr(i)}
            for i in range(start, end + 1)
        ]
    
    # ==================== UUID Operations ====================
    
    def uuid_generate(self) -> str:
        """Generate a UUID."""
        import uuid
        return str(uuid.uuid4())
    
    # ==================== Hash-like Operations ====================
    
    def hash_encode(self, text: str, algorithm: str = 'md5') -> Optional[str]:
        """Hash encode (not cryptographic - just encoding)."""
        # This is different from hash service - it's for encoding
        import hashlib
        try:
            return hashlib.new(algorithm, text.encode()).hexdigest()
        except Exception:
            return None
    
    # ==================== Convenience Methods ====================
    
    def detect_encoding(self, text: str) -> Dict[str, Optional[str]]:
        """Attempt to detect what encoding was used."""
        results = {}
        
        # Try Base64
        if re.match(r'^[A-Za-z0-9+/]+=*$', text.strip()):
            decoded = self.base64_decode(text.strip())
            if decoded and all(c in printables for c in decoded):
                results['base64'] = decoded
        
        # Try URL encoded
        if '%' in text:
            decoded = self.url_decode(text)
            if decoded:
                results['url'] = decoded
        
        # Try hex
        if re.match(r'^[0-9a-fA-F]+$', text.replace(' ', '')):
            decoded = self.hex_decode(text.replace(' ', ''))
            if decoded:
                results['hex'] = decoded
        
        return results


# Module-level convenience functions
_service = EncoderService()

def base64_encode(text: str) -> str:
    """Encode text to Base64."""
    return _service.base64_encode(text)

def base64_decode(text: str) -> Optional[str]:
    """Decode Base64 to text."""
    return _service.base64_decode(text)

def url_encode(text: str) -> str:
    """URL encode text."""
    return _service.url_encode(text)

def url_decode(text: str) -> Optional[str]:
    """URL decode text."""
    return _service.url_decode(text)

def html_encode(text: str) -> str:
    """HTML encode text."""
    return _service.html_encode(text)

def html_decode(text: str) -> str:
    """HTML decode text."""
    return _service.html_decode(text)

def hex_encode(text: str, separator: str = '') -> str:
    """Encode text to hex."""
    return _service.hex_encode(text, separator)

def hex_decode(text: str, separator: str = '') -> Optional[str]:
    """Decode hex to text."""
    return _service.hex_decode(text, separator)

def binary_encode_text(text: str, separator: str = ' ') -> str:
    """Encode text to binary."""
    return _service.binary_encode_text(text, separator)

def binary_decode_text(text: str, separator: str = ' ') -> Optional[str]:
    """Decode binary to text."""
    return _service.binary_decode_text(text, separator)

def json_encode_text(text: str) -> str:
    """JSON encode text."""
    return _service.json_encode_text(text)

def json_decode_text(text: str) -> Optional[str]:
    """JSON decode text."""
    return _service.json_decode_text(text)

def rot13_encode_text(text: str) -> str:
    """Encode text with ROT13."""
    return _service.rot13_encode_text(text)

def rot13_decode_text(text: str) -> str:
    """Decode ROT13."""
    return _service.rot13_decode_text(text)

def morse_encode_text(text: str) -> str:
    """Encode text to Morse code."""
    return _service.morse_encode_text(text)

def morse_decode_text(text: str) -> Optional[str]:
    """Decode Morse code to text."""
    return _service.morse_decode_text(text)

def unicode_encode(text: str) -> str:
    """Unicode escape text."""
    return _service.unicode_encode(text)

def unicode_decode(text: str) -> Optional[str]:
    """Unicode unescape text."""
    return _service.unicode_decode(text)

def ascii_table_generate(start: int = 33, end: int = 126) -> List[Dict]:
    """Generate ASCII table."""
    return _service.ascii_table_generate(start, end)
