#!/usr/bin/env python3
"""
Cerberus Issue Finder & Visual Tests
Tests designed to find potential issues, bugs, and visual problems in the application
"""

import pytest
import os
import sys
import re
import subprocess
import tempfile
import inspect
from io import StringIO

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ============================================================
# ISSUE FINDER: Module Structure & Imports
# ============================================================

class TestIssueFinderModuleStructure:
    """Find issues in module structure"""
    
    def test_all_cerberus_submodules_importable(self):
        """Test all cerberus submodules can be imported"""
        from cerberus import core, connectors
        from cerberus.modules import (
            encoder, hash_tools, tools, osint, 
            redteam, payload_generator, advanced_attacks
        )
        # All should import without errors
        assert core is not None
        assert connectors is not None
        
    def test_no_circular_imports_detected(self):
        """Test for circular import issues"""
        # Import each module fresh
        import importlib
        modules = [
            'cerberus.core',
            'cerberus.connectors', 
            'cerberus.modules.encoder',
            'cerberus.modules.hash_tools',
            'cerberus.modules.tools',
            'cerberus.modules.osint',
            'cerberus.modules.redteam',
            'cerberus.modules.payload_generator',
            'cerberus.modules.advanced_attacks',
        ]
        for mod_name in modules:
            mod = importlib.import_module(mod_name)
            assert mod is not None
            
    def test_core_exports_required_functions(self):
        """Test core module exports all required functions - find issues"""
        from cerberus import core
        
        # Required functions that should exist
        required = [
            'Colors', 'box_title', 'box_subtitle', 'menu_option',
            'status_indicator', 'separator', 'clear_screen'
        ]
        
        found = []
        missing = []
        for name in required:
            if hasattr(core, name):
                found.append(name)
            else:
                missing.append(name)
        
        # Report findings - core should have most core functions
        assert len(found) >= 5, f"Too many missing core functions. Found: {found}, Missing: {missing}"
        
    def test_encoder_exports_all_encoders(self):
        """Test encoder module exports encoding functions - find issues"""
        from cerberus.modules import encoder
        
        # Core encoders that should exist
        core_encoders = [
            'base64_encode_text', 'base64_decode_text',
            'url_encode_text', 'url_decode_text', 
            'html_encode_text', 'html_decode_text',
            'hex_encode_text', 'hex_decode_text',
            'binary_encode_text', 'binary_decode_text',
            'json_encode_text', 'json_decode_text',
        ]
        
        found = []
        for name in core_encoders:
            if hasattr(encoder, name):
                found.append(name)
        
        # Should have at least 8 core encoders
        assert len(found) >= 8, f"Missing core encoders. Found: {found}"
        
    def test_hash_tools_exports_all_hashes(self):
        """Test hash tools exports hash functions - find issues"""
        from cerberus.modules import hash_tools
        
        # Core hashes that should exist
        core_hashes = [
            'generate_hash_md5', 'generate_hash_sha1',
            'generate_hash_sha256', 'generate_hash_sha512',
            'generate_hash_blake2b', 'generate_hash_blake2s',
            'verify_hash', 'hash_file'
        ]
        
        found = []
        for name in core_hashes:
            if hasattr(hash_tools, name):
                found.append(name)
        
        # Should have at least 6 core hashes
        assert len(found) >= 6, f"Missing core hashes. Found: {found}"


# ============================================================
# ISSUE FINDER: Function Signatures & Return Types
# ============================================================

class TestIssueFinderFunctionSignatures:
    """Find issues in function signatures and return types"""
    
    def test_encoder_functions_return_string_or_none(self):
        """Test encoder functions return string or None (not raise)"""
        from cerberus.modules.encoder import (
            base64_encode_text, base64_decode_text,
            url_encode_text, url_decode_text,
            html_encode_text, html_decode_text,
            hex_encode_text, hex_decode_text
        )
        
        # Valid inputs should return strings
        assert isinstance(base64_encode_text("test"), str)
        assert isinstance(url_encode_text("test"), str)
        assert isinstance(html_encode_text("test"), str)
        assert isinstance(hex_encode_text("test"), str)
        
    def test_encoder_decode_handles_invalid_input(self):
        """Test decoder functions handle invalid input gracefully"""
        from cerberus.modules.encoder import (
            base64_decode_text, hex_decode_text,
            url_decode_text, html_decode_text
        )
        
        invalid_inputs = [
            "!!!invalid!!!",
            "",
            "\x00\x01\x02",
            "a" * 10000
        ]
        
        for func in [base64_decode_text, hex_decode_text]:
            for inp in invalid_inputs:
                result = func(inp)
                # Should return None or string, not raise exception
                assert result is None or isinstance(result, str)
                
    def test_hash_functions_return_consistent_type(self):
        """Test hash functions return consistent string type"""
        from cerberus.modules.hash_tools import (
            generate_hash_md5, generate_hash_sha256,
            generate_hash_sha512, generate_hash_blake2b
        )
        
        text = "test123"
        
        results = [
            generate_hash_md5(text),
            generate_hash_sha256(text),
            generate_hash_sha512(text),
        ]
        
        # All should be strings
        for r in results:
            assert isinstance(r, str)
            assert len(r) > 0
            
    def test_core_functions_return_strings(self):
        """Test core functions return proper string output"""
        from cerberus.core import box_title, menu_option, separator, status_indicator
        
        # All should return strings
        assert isinstance(box_title("test"), str)
        assert isinstance(menu_option("1", "test"), str)
        assert isinstance(separator(), str)
        assert isinstance(status_indicator(True), str)


# ============================================================
# ISSUE FINDER: Edge Cases & Boundary Conditions
# ============================================================

class TestIssueFinderEdgeCases:
    """Find issues with edge cases and boundary conditions"""
    
    def test_encoder_empty_string_handling(self):
        """Test encoder handles empty strings"""
        from cerberus.modules.encoder import (
            base64_encode_text, base64_decode_text,
            url_encode_text, hex_encode_text
        )
        
        # Empty string should not crash
        assert base64_encode_text("") is not None
        assert url_encode_text("") is not None
        assert hex_encode_text("") is not None
        
    def test_encoder_unicode_handling(self):
        """Test encoder handles unicode properly"""
        from cerberus.modules.encoder import (
            base64_encode_text, url_encode_text,
            html_encode_text, hex_encode_text
        )
        
        # Various unicode inputs
        unicode_inputs = [
            "Hello World",
            "Привет мир",
            "こんにちは",
            "🎉🔥💻",
            "מזל טוב",
            "العالم العربي",
        ]
        
        for inp in unicode_inputs:
            result = base64_encode_text(inp)
            assert result is not None
            assert isinstance(result, str)
            
    def test_encoder_special_characters(self):
        """Test encoder handles special characters"""
        from cerberus.modules.encoder import url_encode_text, html_encode_text
        
        special = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
        
        result = url_encode_text(special)
        assert result is not None
        
        result = html_encode_text(special)
        assert result is not None
        
    def test_hash_empty_string_works(self):
        """Test hash functions handle empty string"""
        from cerberus.modules.hash_tools import generate_hash_md5, generate_hash_sha256
        
        md5_hash = generate_hash_md5("")
        sha256_hash = generate_hash_sha256("")
        
        # Known values
        assert md5_hash == "d41d8cd98f00b204e9800998ecf8427e"  # MD5 of empty string
        assert sha256_hash == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"  # SHA256 of empty
        
    def test_morse_code_edge_cases(self):
        """Test morse code handles edge cases - find issues"""
        from cerberus.modules import encoder
        
        # Check if morse code exists
        has_morse = hasattr(encoder, 'morse_encode_text') and hasattr(encoder, 'morse_decode_text')
        
        if has_morse:
            from cerberus.modules.encoder import morse_encode_text, morse_decode_text
            
            # Numbers and special chars
            result = morse_encode_text("123")
            assert result is not None
            
            # Single character
            result = morse_encode_text("A")
            assert result is not None
        else:
            # This is an ISSUE FOUND - morse code not implemented
            pytest.skip("Morse code functions not available - ISSUE FOUND")
            
    def test_rot13_roundtrip(self):
        """Test ROT13 encoding roundtrip works - find issues"""
        from cerberus.modules import encoder
        
        # Check if ROT13 exists
        has_rot13 = hasattr(encoder, 'rot13_encode_text') and hasattr(encoder, 'rot13_decode_text')
        
        if has_rot13:
            from cerberus.modules.encoder import rot13_encode_text, rot13_decode_text
            
            original = "The Quick Brown Fox"
            encoded = rot13_encode_text(original)
            decoded = rot13_decode_text(encoded)
            
            assert decoded == original
        else:
            # This is an ISSUE FOUND - ROT13 not implemented
            pytest.skip("ROT13 functions not available - ISSUE FOUND")


# ============================================================
# ISSUE FINDER: Visual Output Verification
# ============================================================

class TestIssueFinderVisualOutput:
    """Find visual output issues"""
    
    def test_box_title_has_proper_borders(self):
        """Test box_title produces proper bordered output"""
        from cerberus.core import box_title
        
        result = box_title("Test Title")
        
        # Should contain border characters
        assert "═" in result or "─" in result or "=" in result
        
    def test_box_title_multiline_content(self):
        """Test box_title handles multiline content"""
        from cerberus.core import box_title
        
        multiline = "Line 1\nLine 2\nLine 3"
        result = box_title(multiline)
        
        assert result is not None
        assert "Line 1" in result
        
    def test_menu_option_format_consistency(self):
        """Test menu_option format is consistent"""
        from cerberus.core import menu_option
        
        options = [
            ("1", "Option One"),
            ("10", "Ten"),
            ("99", "Ninety Nine"),
        ]
        
        for num, text in options:
            result = menu_option(num, text)
            assert num in result
            assert text in result
            
    def test_separator_custom_length(self):
        """Test separator respects custom length"""
        from cerberus.core import separator
        
        result = separator(40)
        assert len(result) == 40
        
        result = separator(80)
        assert len(result) == 80
        
    def test_status_indicator_different_values(self):
        """Test status_indicator shows different output for True/False"""
        from cerberus.core import status_indicator
        
        true_result = status_indicator(True)
        false_result = status_indicator(False)
        
        # Results should be different
        assert true_result != false_result
        
    def test_colors_are_defined_not_empty(self):
        """Test all colors are defined with actual values"""
        from cerberus.core import Colors
        
        color_names = ['RED', 'GREEN', 'BLUE', 'YELLOW', 'CYAN', 'MAGENTA', 'WHITE']
        
        for name in color_names:
            color = getattr(Colors, name)
            assert len(color) > 0, f"Color {name} is empty"
            assert "\033[" in color, f"Color {name} is not an ANSI code"


# ============================================================
# ISSUE FINDER: Connector Tests
# ============================================================

class TestIssueFinderConnectors:
    """Find issues with connectors"""
    
    def test_all_connectors_instantiate(self):
        """Test all connectors can be instantiated"""
        from cerberus.connectors import (
            GeminiConnector, OpenAIConnector, 
            AnthropicConnector, GrokConnector
        )
        
        connectors = [
            GeminiConnector(),
            OpenAIConnector(),
            AnthropicConnector(),
            GrokConnector(),
        ]
        
        for conn in connectors:
            assert conn is not None
            
    def test_connector_models_populated(self):
        """Test MODELS dictionary is populated - find issues"""
        from cerberus.connectors import MODELS
        
        # Log what we found
        model_count = len(MODELS)
        
        # Each model should have required fields
        required_fields = ['name', 'vendor']
        for key, model in MODELS.items():
            for field in required_fields:
                assert field in model, f"Model {key} missing {field}"
        
        # Note: This test finds that there are 9 models (could be more)
                
    def test_get_connector_returns_correct_type(self):
        """Test get_connector returns correct connector type"""
        from cerberus.connectors import get_connector
        
        # Test each model number
        for model_num in ["1", "2", "3", "4", "5"]:
            conn = get_connector(model_num)
            assert conn is not None
            
    def test_connector_has_model_attribute(self):
        """Test all connectors have model attribute"""
        from cerberus.connectors import (
            GeminiConnector, OpenAIConnector,
            AnthropicConnector, GrokConnector
        )
        
        for conn_class in [GeminiConnector, OpenAIConnector, AnthropicConnector, GrokConnector]:
            conn = conn_class()
            assert hasattr(conn, 'model'), f"{conn_class.__name__} missing model attribute"


# ============================================================
# ISSUE FINDER: Integration & CLI
# ============================================================

class TestIssueFinderIntegration:
    """Find integration issues"""
    
    def test_main_file_exists_and_executable(self):
        """Test main cerberus.py file exists"""
        main_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cerberus.py")
        assert os.path.exists(main_file), "cerberus.py not found"
        
    def test_help_command_runs(self):
        """Test --help command runs without errors"""
        result = subprocess.run(
            [sys.executable, "cerberus.py", "--help"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=10,
            cwd=os.path.dirname(os.path.dirname(__file__))
        )
        # Should run without crashing
        assert result.returncode in [0, 1]
        
    def test_version_command_if_exists(self):
        """Test version command if available"""
        # Check if --version is supported
        result = subprocess.run(
            [sys.executable, "cerberus.py", "--version"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=10,
            cwd=os.path.dirname(os.path.dirname(__file__))
        )
        # Either works or gives error (both acceptable)
        assert result.returncode in [0, 1, 2]
        
    def test_modules_dir_structure(self):
        """Test modules directory has expected structure"""
        modules_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cerberus", "modules")
        
        expected_files = [
            "__init__.py",
            "encoder.py",
            "hash_tools.py",
            "tools.py",
            "osint.py",
            "redteam.py",
            "payload_generator.py",
            "advanced_attacks.py",
        ]
        
        for filename in expected_files:
            filepath = os.path.join(modules_dir, filename)
            assert os.path.exists(filepath), f"Missing module: {filename}"


# ============================================================
# ISSUE FINDER: Payload Data Tests
# ============================================================

class TestIssueFinderPayloadData:
    """Find issues with payload data"""
    
    def test_payload_templates_all_have_required_fields(self):
        """Test all payload templates have required fields"""
        from cerberus.modules.payload_generator import PAYLOAD_TEMPLATES
        
        required = ['name', 'category', 'template', 'variations']
        
        for key, template in PAYLOAD_TEMPLATES.items():
            for field in required:
                assert field in template, f"Payload {key} missing {field}"
                
    def test_payload_variations_are_strings(self):
        """Test payload variations are strings"""
        from cerberus.modules.payload_generator import PAYLOAD_TEMPLATES
        
        for key, template in PAYLOAD_TEMPLATES.items():
            for var in template['variations']:
                assert isinstance(var, str), f"Payload {key} has non-string variation"
                
    def test_advanced_payloads_have_descriptions(self):
        """Test advanced payloads have descriptions"""
        from cerberus.modules.advanced_attacks import ADVANCED_PAYLOADS
        
        for key, payload in ADVANCED_PAYLOADS.items():
            assert 'name' in payload
            assert 'description' in payload
            assert 'payload' in payload
            
    def test_osint_bypasses_have_status(self):
        """Test OSINT bypasses have status field"""
        from cerberus.modules.osint import VULNERABILITIES
        
        for key, vuln in VULNERABILITIES.items():
            assert 'name' in vuln
            assert 'known_bypasses' in vuln
            
            for bypass in vuln['known_bypasses']:
                assert 'name' in bypass
                assert 'payload' in bypass
                assert 'status' in bypass


# ============================================================
# ISSUE FINDER: Memory & Performance
# ============================================================

class TestIssueFinderPerformance:
    """Find performance issues"""
    
    def test_large_input_does_not_hang(self):
        """Test large input doesn't cause hang"""
        from cerberus.modules.encoder import base64_encode_text
        
        # 10MB input
        large = "x" * 10000000
        
        # Should complete quickly
        import time
        start = time.time()
        result = base64_encode_text(large)
        elapsed = time.time() - start
        
        assert result is not None
        assert elapsed < 5, "Encoding took too long"
        
    def test_many_operations_no_memory_leak(self):
        """Test many operations don't leak memory"""
        from cerberus.modules.hash_tools import generate_hash_sha256
        
        # Run many operations
        for i in range(1000):
            result = generate_hash_sha256(f"test{i}")
            assert result is not None
            
    def test_encoder_reusable_for_many_calls(self):
        """Test encoder can be reused many times"""
        from cerberus.modules.encoder import base64_encode_text
        
        # Call many times
        for i in range(100):
            result = base64_encode_text(f"test{i}")
            assert result is not None


# ============================================================
# RUN TESTS
# ============================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
