"""
Cerberus Test Suite
Tests for core functionality and modules
"""

import base64
import urllib.parse
import html
import hashlib
import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from modules directly (test the pure functions)
from cerberus.modules.encoder import (
    base64_encode_text,
    base64_decode_text,
    url_encode_text,
    url_decode_text,
    html_encode_text,
    html_decode_text,
    hex_encode_text,
    hex_decode_text,
)
from cerberus.modules.hash_tools import (
    generate_hash_md5,
    generate_hash_sha256,
    generate_hash_sha512,
)
from cerberus.core import (
    box_title,
    menu_option,
    status_indicator,
    separator,
)


# ============================================================
# CORE FUNCTION TESTS
# ============================================================

class TestCoreFunctions:
    """Test core utility functions"""
    
    def test_box_title(self):
        """Test box_title creates correct format"""
        result = box_title("Test Title")
        assert "Test Title" in result
        assert "═" in result
        
    def test_box_title_custom_width(self):
        """Test box_title with custom width"""
        result = box_title("Test", width=40)
        assert "Test" in result
        # Account for leading newline in split
        lines = result.strip().split('\n')
        assert len(lines[0]) == 40
        
    def test_menu_option_basic(self):
        """Test menu_option basic formatting"""
        result = menu_option("1", "Test Option")
        assert "1" in result
        assert "Test Option" in result
        
    def test_menu_option_with_description(self):
        """Test menu_option with description"""
        result = menu_option("1", "Test", "Description")
        assert "1" in result
        assert "Test" in result
        assert "Description" in result
        
    def test_status_indicator_true(self):
        """Test status_indicator with True"""
        result = status_indicator(True)
        assert "✓" in result or "True" in result
        
    def test_status_indicator_false(self):
        """Test status_indicator with False"""
        result = status_indicator(False)
        assert "✗" in result or "False" in result
        
    def test_separator_default(self):
        """Test separator with defaults"""
        result = separator()
        assert len(result) == 60
        assert "─" in result
        
    def test_separator_custom(self):
        """Test separator with custom parameters"""
        result = separator(width=30, char="*")
        assert len(result) == 30
        assert "*" in result


# ============================================================
# ENCODER MODULE TESTS
# ============================================================

class TestEncoderModule:
    """Test encoder module functions"""
    
    def test_base64_encode(self):
        """Test Base64 encoding"""
        result = base64_encode_text("Hello World")
        expected = base64.b64encode(b"Hello World").decode()
        assert result == expected
        
    def test_base64_decode(self):
        """Test Base64 decoding"""
        result = base64_decode_text("SGVsbG8gV29ybGQ=")
        assert result == "Hello World"
        
    def test_base64_decode_invalid(self):
        """Test Base64 decode with invalid input"""
        result = base64_decode_text("!!!invalid!!!")
        assert result is None or "Error" in str(result)
        
    def test_url_encode(self):
        """Test URL encoding"""
        result = url_encode_text("hello world&foo=bar")
        assert "hello%20world" in result
        assert "%26" in result  # & encoded
        
    def test_url_decode(self):
        """Test URL decoding"""
        result = url_decode_text("hello%20world%26foo%3Dbar")
        assert result == "hello world&foo=bar"
        
    def test_html_encode(self):
        """Test HTML encoding"""
        result = html_encode_text("<script>alert('xss')</script>")
        assert "&lt;" in result
        assert "&gt;" in result
        # Single quotes are encoded as &#x27; not &quot;
        assert "&#x27;" in result or "&quot;" in result
        
    def test_html_decode(self):
        """Test HTML decoding"""
        result = html_decode_text("&lt;script&gt;alert(&#x27;xss&#x27;)&lt;/script&gt;")
        assert "<script>" in result
        assert "alert" in result
        
    def test_hex_encode(self):
        """Test hex encoding"""
        result = hex_encode_text("Hello")
        assert result == "48656c6c6f"
        
    def test_hex_decode(self):
        """Test hex decoding"""
        result = hex_decode_text("48656c6c6f")
        assert result == "Hello"
        
    def test_hex_decode_invalid(self):
        """Test hex decode with invalid input"""
        result = hex_decode_text("!!!nothex!!!")
        assert result is None or "Error" in str(result)


# ============================================================
# HASH TOOLS MODULE TESTS
# ============================================================

class TestHashToolsModule:
    """Test hash tools module functions"""
    
    def test_generate_hash_md5(self):
        """Test MD5 hash generation"""
        result = generate_hash_md5("Hello World")
        expected = hashlib.md5(b"Hello World").hexdigest()
        assert result == expected
        assert len(result) == 32
        
    def test_generate_hash_sha256(self):
        """Test SHA256 hash generation"""
        result = generate_hash_sha256("Hello World")
        expected = hashlib.sha256(b"Hello World").hexdigest()
        assert result == expected
        assert len(result) == 64
        
    def test_generate_hash_sha512(self):
        """Test SHA512 hash generation"""
        result = generate_hash_sha512("Hello World")
        expected = hashlib.sha512(b"Hello World").hexdigest()
        assert result == expected
        assert len(result) == 128
        
    def test_hash_empty_string(self):
        """Test hash of empty string"""
        result = generate_hash_md5("")
        expected = hashlib.md5(b"").hexdigest()
        assert result == expected
        
    def test_hash_unicode(self):
        """Test hash of unicode string"""
        result = generate_hash_md5("Hello 世界")
        expected = hashlib.md5("Hello 世界".encode()).hexdigest()
        assert result == expected
        
    def test_hash_consistency(self):
        """Test hash consistency (same input = same output)"""
        text = "Test String"
        result1 = generate_hash_sha256(text)
        result2 = generate_hash_sha256(text)
        assert result1 == result2


# ============================================================
# EDGE CASES AND ERROR HANDLING
# ============================================================

class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_empty_string_base64(self):
        """Test Base64 with empty string"""
        result = base64_encode_text("")
        assert result == "" or result is not None
        
    def test_empty_string_hash(self):
        """Test hash with empty string"""
        result = generate_hash_md5("")
        assert result == hashlib.md5(b"").hexdigest()
        
    def test_very_long_string(self):
        """Test with very long string"""
        long_string = "a" * 10000
        result = generate_hash_sha256(long_string)
        assert len(result) == 64
        
    def test_special_characters(self):
        """Test with special characters"""
        special = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
        result = base64_encode_text(special)
        assert result is not None
        decoded = base64_decode_text(result)
        assert decoded == special


# ============================================================
# RUN TESTS
# ============================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
