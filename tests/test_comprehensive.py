#!/usr/bin/env python3
"""
Cerberus Comprehensive Test Suite
Tests for all modules including encoder, hash tools, redteam, OSINT, and more
"""

import pytest
import os
import sys
import base64
import urllib.parse
import html
import hashlib
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ============================================================
# ENCODER MODULE TESTS
# ============================================================

class TestEncoderModule:
    """Test encoder module functions"""
    
    def test_base64_encode_decode_roundtrip(self):
        """Test Base64 encode/decode roundtrip"""
        from cerberus.modules.encoder import base64_encode_text, base64_decode_text
        original = "Hello World! 你好世界"
        encoded = base64_encode_text(original)
        decoded = base64_decode_text(encoded)
        assert decoded == original
        
    def test_url_encode_decode_roundtrip(self):
        """Test URL encode/decode roundtrip"""
        from cerberus.modules.encoder import url_encode_text, url_decode_text
        original = "hello world&foo=bar&特殊字符"
        encoded = url_encode_text(original)
        decoded = url_decode_text(encoded)
        assert decoded == original
        
    def test_html_encode_decode_roundtrip(self):
        """Test HTML encode/decode roundtrip"""
        from cerberus.modules.encoder import html_encode_text, html_decode_text
        original = "<script>alert('test')</script>"
        encoded = html_encode_text(original)
        decoded = html_decode_text(encoded)
        assert decoded == original
        
    def test_hex_encode_decode_roundtrip(self):
        """Test hex encode/decode roundtrip"""
        from cerberus.modules.encoder import hex_encode_text, hex_decode_text
        original = "Hello"
        encoded = hex_encode_text(original)
        decoded = hex_decode_text(encoded)
        assert decoded == original
        
    def test_base64_decode_invalid_returns_none(self):
        """Test Base64 decode with invalid input returns None or error"""
        from cerberus.modules.encoder import base64_decode_text
        result = base64_decode_text("!!!invalid!!!")
        assert result is None or "Error" in str(result) or "Invalid" in str(result)
        
    def test_hex_decode_invalid_returns_none(self):
        """Test hex decode with invalid input returns None or error"""
        from cerberus.modules.encoder import hex_decode_text
        result = hex_decode_text("!!!nothex!!!")
        assert result is None or "Error" in str(result) or "Invalid" in str(result)


# ============================================================
# HASH TOOLS MODULE TESTS
# ============================================================

class TestHashToolsModule:
    """Test hash tools module functions"""
    
    def test_md5_hash_known_input(self):
        """Test MD5 with known input"""
        from cerberus.modules.hash_tools import generate_hash_md5
        result = generate_hash_md5("hello")
        assert result == "5d41402abc4b2a76b9719d911017c592"
        
    def test_sha256_hash_known_input(self):
        """Test SHA256 with known input"""
        from cerberus.modules.hash_tools import generate_hash_sha256
        result = generate_hash_sha256("hello")
        assert result == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
        
    def test_sha512_hash_known_input(self):
        """Test SHA512 with known input"""
        from cerberus.modules.hash_tools import generate_hash_sha512
        result = generate_hash_sha512("hello")
        expected = hashlib.sha512(b"hello").hexdigest()
        assert result == expected

    def test_hash_unicode_input(self):
        """Test hash with unicode input"""
        from cerberus.modules.hash_tools import generate_hash_md5
        result = generate_hash_md5("你好")
        assert len(result) == 32
        
    def test_hash_empty_string(self):
        """Test hash with empty string"""
        from cerberus.modules.hash_tools import generate_hash_md5
        result = generate_hash_md5("")
        assert result == "d41d8cd98f00b204e9800998ecf8427e"


# ============================================================
# CORE MODULE TESTS
# ============================================================

class TestCoreModule:
    """Test core module functions"""
    
    def test_box_title_format(self):
        """Test box_title creates correct format"""
        from cerberus.core import box_title
        result = box_title("Test")
        assert "Test" in result
        assert "═" in result
        
    def test_box_title_custom_width(self):
        """Test box_title with custom width"""
        from cerberus.core import box_title
        result = box_title("Test", width=40)
        lines = result.strip().split('\n')
        assert len(lines[0]) == 40
        
    def test_menu_option_format(self):
        """Test menu_option formatting"""
        from cerberus.core import menu_option
        result = menu_option("1", "Test")
        assert "1" in result
        assert "Test" in result
        
    def test_status_indicator_formats(self):
        """Test status_indicator with both True and False"""
        from cerberus.core import status_indicator
        true_result = status_indicator(True)
        false_result = status_indicator(False)
        # Should have some indication of status
        assert true_result != false_result
        
    def test_separator_formats(self):
        """Test separator with defaults and custom"""
        from cerberus.core import separator
        default_result = separator()
        custom_result = separator(width=30, char="*")
        assert len(default_result) == 60
        assert len(custom_result) == 30
        assert "*" in custom_result


# ============================================================
# CONNECTOR TESTS
# ============================================================

class TestConnectors:
    """Test API connectors initialization"""
    
    def test_google_connector_init(self):
        """Test Google connector initialization"""
        from cerberus.connectors import GeminiConnector
        connector = GeminiConnector()
        assert connector.model is not None
        
    def test_openai_connector_init(self):
        """Test OpenAI connector initialization"""
        from cerberus.connectors import OpenAIConnector
        connector = OpenAIConnector()
        assert connector.model is not None
        
    def test_anthropic_connector_init(self):
        """Test Anthropic connector initialization"""
        from cerberus.connectors import AnthropicConnector
        connector = AnthropicConnector()
        assert connector.model is not None
        
    def test_xai_connector_init(self):
        """Test xAI connector initialization"""
        from cerberus.connectors import GrokConnector
        connector = GrokConnector()
        assert connector.model is not None
        
    def test_models_dict_populated(self):
        """Test models dictionary is populated"""
        from cerberus.connectors import MODELS
        assert len(MODELS) > 0
        
    def test_models_have_required_fields(self):
        """Test each model has required fields"""
        from cerberus.connectors import MODELS
        required_fields = ["name", "vendor"]
        for key, model in MODELS.items():
            for field in required_fields:
                assert field in model, f"Model {key} missing {field}"


# ============================================================
# API KEY TESTS (Environment Variable Compliance)
# ============================================================

class TestAPIKeysCompliance:
    """Test API keys are loaded from environment variables (RULES.md compliance)"""
    
    def test_api_keys_defined_in_main_module(self):
        """Test API keys are defined in cerberus.py (main module)"""
        # Import from the main cerberus.py file
        import importlib.util
        spec = importlib.util.spec_from_file_location("cerberus_main", 
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "cerberus.py"))
        cerberus_main = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cerberus_main)
        
        assert hasattr(cerberus_main, 'GOOGLE_API_KEY')
        assert hasattr(cerberus_main, 'OPENAI_API_KEY')
        assert hasattr(cerberus_main, 'ANTHROPIC_API_KEY')
        
    def test_api_keys_are_strings(self):
        """Test API keys are strings"""
        import importlib.util
        spec = importlib.util.spec_from_file_location("cerberus_main", 
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "cerberus.py"))
        cerberus_main = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cerberus_main)
        
        assert isinstance(cerberus_main.GOOGLE_API_KEY, str)
        assert isinstance(cerberus_main.OPENAI_API_KEY, str)
        assert isinstance(cerberus_main.ANTHROPIC_API_KEY, str)
        
    def test_api_keys_loaded_from_env(self):
        """Test API keys match environment variables"""
        import importlib.util
        spec = importlib.util.spec_from_file_location("cerberus_main", 
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "cerberus.py"))
        cerberus_main = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cerberus_main)
        
        # Should be empty string if not set, or value from env
        assert cerberus_main.GOOGLE_API_KEY == os.getenv("GOOGLE_API_KEY", "")
        assert cerberus_main.OPENAI_API_KEY == os.getenv("OPENAI_API_KEY", "")
        assert cerberus_main.ANTHROPIC_API_KEY == os.getenv("ANTHROPIC_API_KEY", "")


# ============================================================
# MODULE IMPORT TESTS
# ============================================================

class TestModuleImports:
    """Test all modules can be imported"""
    
    def test_encoder_module_imports(self):
        """Test encoder module imports"""
        from cerberus.modules import encoder
        assert hasattr(encoder, 'base64_encode_text')
        assert hasattr(encoder, 'base64_decode_text')
        
    def test_hash_tools_module_imports(self):
        """Test hash tools module imports"""
        from cerberus.modules import hash_tools
        assert hasattr(hash_tools, 'generate_hash_md5')
        assert hasattr(hash_tools, 'generate_hash_sha256')
        
    def test_core_module_imports(self):
        """Test core module imports"""
        from cerberus import core
        assert hasattr(core, 'box_title')
        assert hasattr(core, 'menu_option')
        
    def test_connectors_module_imports(self):
        """Test connectors module imports"""
        from cerberus import connectors
        assert hasattr(connectors, 'GeminiConnector')
        assert hasattr(connectors, 'OpenAIConnector')


# ============================================================
# REDTEAM MODULE TESTS
# ============================================================

class TestRedTeamModule:
    """Test redteam module"""
    
    def test_redteam_module_imports(self):
        """Test redteam module can be imported"""
        from cerberus.modules import redteam
        assert redteam is not None
        
    def test_redteam_has_functions(self):
        """Test redteam module has expected functions"""
        from cerberus.modules import redteam
        # Check for key functions (actual names may vary)
        assert hasattr(redteam, 'module_redteam') or hasattr(redteam, 'redteam')


# ============================================================
# OSINT MODULE TESTS
# ============================================================

class TestOSINTModule:
    """Test OSINT module"""
    
    def test_osint_module_imports(self):
        """Test OSINT module can be imported"""
        from cerberus.modules import osint
        assert osint is not None


# ============================================================
# TOOLS MODULE TESTS
# ============================================================

class TestToolsModule:
    """Test tools module"""
    
    def test_tools_module_imports(self):
        """Test tools module can be imported"""
        from cerberus.modules import tools
        assert tools is not None


# ============================================================
# VISUAL/UI TESTS
# ============================================================

class TestVisualUI:
    """Test visual/UI elements"""
    
    def test_rich_console_available(self):
        """Test Rich console is available"""
        try:
            from rich.console import Console
            console = Console()
            assert console is not None
        except ImportError:
            pytest.skip("Rich not installed")
            
    def test_rich_panels_available(self):
        """Test Rich panels are available"""
        try:
            from rich.panel import Panel
            from rich.console import Console
            console = Console()
            panel = Panel("Test", title="Test Panel")
            assert panel is not None
        except ImportError:
            pytest.skip("Rich not installed")
            
    def test_rich_tables_available(self):
        """Test Rich tables are available"""
        try:
            from rich.table import Table
            table = Table(title="Test Table")
            assert table is not None
        except ImportError:
            pytest.skip("Rich not installed")


# ============================================================
# RUN TESTS
# ============================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
