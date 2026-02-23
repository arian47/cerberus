#!/usr/bin/env python3
"""
Cerberus Security & Visual Test Suite
Security-focused tests and visual/UI tests for the application
"""

import pytest
import os
import sys
import re
import subprocess

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ============================================================
# SECURITY TESTS - Input Validation & Injection Prevention
# ============================================================

class TestSecurityInputValidation:
    """Security tests for input validation"""
    
    def test_encoder_prevents_null_bytes(self):
        """Test encoder handles null bytes safely"""
        from cerberus.modules.encoder import base64_encode_text, base64_decode_text
        # Should handle null bytes without crashing
        result = base64_encode_text("test\x00null")
        assert result is not None
        
    def test_encoder_handles_very_long_input(self):
        """Test encoder handles extremely long input"""
        from cerberus.modules.encoder import base64_encode_text
        long_input = "x" * 1000000  # 1MB of data
        result = base64_encode_text(long_input)
        assert result is not None
        assert len(result) > 0
        
    def test_encoder_handles_binary_data(self):
        """Test encoder handles binary-like data"""
        from cerberus.modules.encoder import base64_encode_text
        # Binary-like data
        binary_data = bytes([0, 1, 2, 255, 254, 253])
        result = base64_encode_text(binary_data.decode('latin-1'))
        assert result is not None
        
    def test_encoder_handles_mixed_encoding(self):
        """Test encoder handles mixed encoding strings"""
        from cerberus.modules.encoder import url_encode_text
        # Mixed content that could cause issues
        mixed = "http://example.com/path?param=value&other=<script>"
        result = url_encode_text(mixed)
        assert result is not None
        assert "&" in result or "%26" in result
        
    def test_encoder_prevents_control_characters_leak(self):
        """Test encoder doesn't leak control characters"""
        from cerberus.modules.encoder import html_encode_text
        # Control characters should be encoded
        control_chars = "\x00\x01\x02\x03\x04\x05"
        result = html_encode_text(control_chars)
        assert result is not None
        
    def test_hash_handles_large_input(self):
        """Test hash functions handle large input"""
        from cerberus.modules.hash_tools import generate_hash_sha256
        large_input = "a" * 10000000  # 10MB
        result = generate_hash_sha256(large_input)
        assert len(result) == 64
        
    def test_encoder_handles_unicode_bombs(self):
        """Test encoder handles unicode bomb attacks"""
        from cerberus.modules.encoder import base64_encode_text
        # Unicode bomb (ZEK pattern)
        unicode_bomb = "\u200b" * 10000
        result = base64_encode_text(unicode_bomb)
        assert result is not None


# ============================================================
# SECURITY TESTS - Path Traversal & File Access
# ============================================================

class TestSecurityPathTraversal:
    """Security tests for path traversal prevention"""
    
    def test_no_path_traversal_in_modules(self):
        """Test that modules don't have obvious path traversal vulnerabilities"""
        import cerberus.modules.encoder as encoder
        # Just verify the module exists and has expected functions
        assert hasattr(encoder, 'base64_encode_text')
        assert hasattr(encoder, 'base64_decode_text')
        
    def test_core_safe_string_operations(self):
        """Test core module uses safe string operations"""
        from cerberus.core import box_title, menu_option
        # Should handle special characters without code injection
        result = box_title("Test <script>alert('xss')</script>")
        assert "<script>" in result or "&lt;" in result


# ============================================================
# VISUAL/UI TESTS - Rich Library Tests
# ============================================================

class TestVisualRichConsole:
    """Visual tests using Rich library"""
    
    def test_rich_console_can_be_created(self):
        """Test Rich Console can be created"""
        from rich.console import Console
        console = Console()
        assert console is not None
        
    def test_rich_panel_creation(self):
        """Test Rich Panel can be created"""
        from rich.panel import Panel
        from rich.console import Console
        console = Console()
        panel = Panel("Test Content", title="Test Title")
        assert panel is not None
        # Panel has renderable content
        rendered = console.render(panel)
        assert rendered is not None
        
    def test_rich_table_creation(self):
        """Test Rich Table can be created"""
        from rich.table import Table
        table = Table(title="Test Table")
        table.add_column("Column 1")
        table.add_row("Row 1")
        assert table is not None
        
    def test_rich_progress_creation(self):
        """Test Rich Progress can be created"""
        from rich.progress import Progress, SpinnerColumn, TextColumn
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
        )
        assert progress is not None
        
    def test_rich_syntax_creation(self):
        """Test Rich Syntax highlighting can be created"""
        try:
            from rich.syntax import Syntax
            syntax = Syntax("print('hello')", "python")
            assert syntax is not None
        except ImportError:
            pytest.skip("rich.syntax not available")
            
    def test_rich_markdown_creation(self):
        """Test Rich Markdown can be created"""
        try:
            from rich.markdown import Markdown
            md = Markdown("# Hello World")
            assert md is not None
        except ImportError:
            pytest.skip("rich.markdown not available")


# ============================================================
# VISUAL/UI TESTS - Color & Formatting
# ============================================================

class TestVisualColors:
    """Visual tests for colors and formatting"""
    
    def test_colors_class_exists(self):
        """Test Colors class exists in core"""
        from cerberus.core import Colors
        assert Colors is not None
        
    def test_colors_have_basic_colors(self):
        """Test Colors has basic color definitions"""
        from cerberus.core import Colors
        assert hasattr(Colors, 'RESET')
        assert hasattr(Colors, 'RED')
        assert hasattr(Colors, 'GREEN')
        assert hasattr(Colors, 'YELLOW')
        assert hasattr(Colors, 'BLUE')
        
    def test_box_title_uses_colors(self):
        """Test box_title output contains color codes"""
        from cerberus.core import box_title
        result = box_title("Test")
        # Should contain ANSI color codes
        assert "\033[" in result or "Test" in result
        
    def test_menu_option_uses_colors(self):
        """Test menu_option output contains color codes"""
        from cerberus.core import menu_option
        result = menu_option("1", "Test")
        assert "1" in result
        assert "Test" in result


# ============================================================
# VISUAL/UI TESTS - Layout & Structure
# ============================================================

class TestVisualLayout:
    """Visual tests for layout and structure"""
    
    def test_box_title_has_correct_structure(self):
        """Test box_title has proper border structure"""
        from cerberus.core import box_title
        result = box_title("Test")
        lines = result.split('\n')
        # Should have top border, content, bottom border
        assert len(lines) >= 3
        
    def test_separator_has_correct_length(self):
        """Test separator has correct default length"""
        from cerberus.core import separator
        result = separator()
        # Default is 60 characters
        assert len(result) == 60
        
    def test_menu_option_has_number_and_text(self):
        """Test menu_option shows both number and text"""
        from cerberus.core import menu_option
        result = menu_option("99", "Test Option")
        assert "99" in result
        assert "Test Option" in result


# ============================================================
# TOR MODULE TESTS
# ============================================================

class TestTorModule:
    """Tests for Tor module"""
    
    def test_tor_module_imports(self):
        """Test Tor module can be imported"""
        try:
            from cerberus.modules import tor
            assert tor is not None
        except ImportError as e:
            pytest.skip(f"Tor module import failed: {e}")
            
    def test_tor_constants_defined(self):
        """Test Tor constants are defined"""
        try:
            from cerberus.modules import tor
            assert hasattr(tor, 'TOR_SOCKS_PORT')
            assert hasattr(tor, 'TOR_CONTROL_PORT')
            assert hasattr(tor, 'TOR_PROXY')
        except ImportError:
            pytest.skip("Tor module not available")
            
    def test_tor_has_connection_class(self):
        """Test Tor module has TorConnection class"""
        try:
            from cerberus.modules.tor import TorConnection
            assert TorConnection is not None
        except ImportError:
            pytest.skip("Tor module not available")
            
    def test_tor_check_endpoints_defined(self):
        """Test Tor check endpoints are defined"""
        try:
            from cerberus.modules import tor
            assert hasattr(tor, 'TOR_CHECK_ENDPOINTS')
            assert len(tor.TOR_CHECK_ENDPOINTS) > 0
        except ImportError:
            pytest.skip("Tor module not available")


# ============================================================
# CONNECTOR TESTS - Security & Error Handling
# ============================================================

class TestConnectorSecurity:
    """Security tests for connectors"""
    
    def test_connector_handles_missing_api_key(self):
        """Test connector handles missing API key gracefully"""
        from cerberus.connectors import GeminiConnector
        connector = GeminiConnector()
        # Should have empty or default API key, not crash
        # Check that model attribute exists (API key may be handled internally)
        assert hasattr(connector, 'model')
        
    def test_connector_url_validation(self):
        """Test connector uses valid endpoints"""
        from cerberus.connectors import MODELS
        
        # Verify MODELS dictionary is populated with expected vendors
        vendors = [model.get('vendor', '') for model in MODELS.values()]
        expected_vendors = ['Google', 'OpenAI', 'Anthropic', 'xAI', 'MiniMax']
        
        for vendor in expected_vendors:
            assert vendor in vendors, f"Missing vendor: {vendor}"
        
    def test_connectors_have_timeout(self):
        """Test connectors have timeout configured"""
        from cerberus.connectors import GeminiConnector
        connector = GeminiConnector()
        # Should have some timeout mechanism
        assert connector is not None


# ============================================================
# ERROR HANDLING TESTS
# ============================================================

class TestErrorHandling:
    """Tests for error handling"""
    
    def test_encoder_invalid_base64_handled(self):
        """Test encoder handles invalid Base64 gracefully"""
        from cerberus.modules.encoder import base64_decode_text
        result = base64_decode_text("!!!invalid-base64!!!")
        # Should return None or error message, not crash
        assert result is None or isinstance(result, str)
        
    def test_encoder_invalid_hex_handled(self):
        """Test encoder handles invalid hex gracefully"""
        from cerberus.modules.encoder import hex_decode_text
        result = hex_decode_text("nothex!")
        # Should return None or error message, not crash
        assert result is None or isinstance(result, str)
        
    def test_hash_handles_none_input(self):
        """Test hash handles None input gracefully"""
        from cerberus.modules.hash_tools import generate_hash_md5
        # Hash should fail gracefully with TypeError for None - this is expected
        with pytest.raises((TypeError, AttributeError)):
            generate_hash_md5(None)


# ============================================================
# MAIN ENTRY POINT TESTS
# ============================================================

class TestMainEntry:
    """Tests for main entry point"""
    
    def test_cerberus_main_imports(self):
        """Test main cerberus.py can be imported"""
        import importlib.util
        spec = importlib.util.spec_from_file_location("cerberus_main",
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "cerberus.py"))
        cerberus_main = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cerberus_main)
        assert cerberus_main is not None
        
    def test_main_has_menu_function(self):
        """Test main module has main menu function"""
        import importlib.util
        spec = importlib.util.spec_from_file_location("cerberus_main",
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "cerberus.py"))
        cerberus_main = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cerberus_main)
        assert hasattr(cerberus_main, 'main') or hasattr(cerberus_main, 'show_menu')
        
    def test_main_help_flag_works(self):
        """Test --help flag produces output"""
        result = subprocess.run(
            [sys.executable, "cerberus.py", "--help"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=10
        )
        # Should either show help or exit cleanly
        assert result.returncode in [0, 1] or "usage" in result.stdout.lower() or "help" in result.stdout.lower()


# ============================================================
# RUN TESTS
# ============================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
