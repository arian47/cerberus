#!/usr/bin/env python3
"""
Cerberus Module Functionality Tests
Tests for tools, payload_generator, advanced_attacks, osint modules
"""

import pytest
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ============================================================
# TOOLS MODULE TESTS
# ============================================================

class TestToolsModule:
    """Test tools module functionality"""
    
    def test_tools_module_imports(self):
        """Test tools module can be imported"""
        from cerberus.modules import tools
        assert tools is not None
        
    def test_tools_module_has_module_tools_function(self):
        """Test tools module has module_tools function"""
        from cerberus.modules.tools import module_tools
        assert callable(module_tools)
        
    def test_tools_exports_module_tools(self):
        """Test tools module exports"""
        from cerberus.modules.tools import __all__
        assert "module_tools" in __all__


# ============================================================
# PAYLOAD GENERATOR MODULE TESTS
# ============================================================

class TestPayloadGeneratorModule:
    """Test payload generator module"""
    
    def test_payload_generator_imports(self):
        """Test payload generator module can be imported"""
        from cerberus.modules import payload_generator
        assert payload_generator is not None
        
    def test_payload_templates_defined(self):
        """Test PAYLOAD_TEMPLATES is defined"""
        from cerberus.modules.payload_generator import PAYLOAD_TEMPLATES
        assert len(PAYLOAD_TEMPLATES) > 0
        
    def test_payload_template_structure(self):
        """Test payload template has correct structure"""
        from cerberus.modules.payload_generator import PAYLOAD_TEMPLATES
        first_key = list(PAYLOAD_TEMPLATES.keys())[0]
        template = PAYLOAD_TEMPLATES[first_key]
        
        assert "name" in template
        assert "category" in template
        assert "template" in template
        assert "variations" in template
        
    def test_xss_payload_exists(self):
        """Test XSS payload template exists"""
        from cerberus.modules.payload_generator import PAYLOAD_TEMPLATES
        assert "1" in PAYLOAD_TEMPLATES
        assert PAYLOAD_TEMPLATES["1"]["name"] == "XSS Payload"
        
    def test_sql_injection_payload_exists(self):
        """Test SQL injection payload template exists"""
        from cerberus.modules.payload_generator import PAYLOAD_TEMPLATES
        assert "2" in PAYLOAD_TEMPLATES
        assert "SQL" in PAYLOAD_TEMPLATES["2"]["name"]
        
    def test_command_injection_payload_exists(self):
        """Test command injection payload template exists"""
        from cerberus.modules.payload_generator import PAYLOAD_TEMPLATES
        assert "3" in PAYLOAD_TEMPLATES
        assert PAYLOAD_TEMPLATES["3"]["category"] == "System"
        
    def test_all_payloads_have_variations(self):
        """Test all payloads have variations"""
        from cerberus.modules.payload_generator import PAYLOAD_TEMPLATES
        for key, template in PAYLOAD_TEMPLATES.items():
            assert "variations" in template
            assert len(template["variations"]) > 0


# ============================================================
# ADVANCED ATTACKS MODULE TESTS
# ============================================================

class TestAdvancedAttacksModule:
    """Test advanced attacks module"""
    
    def test_advanced_attacks_imports(self):
        """Test advanced attacks module can be imported"""
        from cerberus.modules import advanced_attacks
        assert advanced_attacks is not None
        
    def test_advanced_payloads_defined(self):
        """Test ADVANCED_PAYLOADS is defined"""
        from cerberus.modules.advanced_attacks import ADVANCED_PAYLOADS
        assert len(ADVANCED_PAYLOADS) > 0
        
    def test_dan_mode_payload_exists(self):
        """Test DAN mode payload exists"""
        from cerberus.modules.advanced_attacks import ADVANCED_PAYLOADS
        assert "1" in ADVANCED_PAYLOADS
        assert "DAN" in ADVANCED_PAYLOADS["1"]["name"]
        
    def test_advanced_payload_structure(self):
        """Test advanced payload has correct structure"""
        from cerberus.modules.advanced_attacks import ADVANCED_PAYLOADS
        first_key = list(ADVANCED_PAYLOADS.keys())[0]
        payload = ADVANCED_PAYLOADS[first_key]
        
        assert "name" in payload
        assert "description" in payload
        assert "payload" in payload
        
    def test_roleplay_jailbreak_exists(self):
        """Test roleplay jailbreak exists"""
        from cerberus.modules.advanced_attacks import ADVANCED_PAYLOADS
        assert "2" in ADVANCED_PAYLOADS
        assert "Role Play" in ADVANCED_PAYLOADS["2"]["name"]
        
    def test_cot_injection_exists(self):
        """Test chain of thought injection exists"""
        from cerberus.modules.advanced_attacks import ADVANCED_PAYLOADS
        assert "3" in ADVANCED_PAYLOADS
        assert "Chain" in ADVANCED_PAYLOADS["3"]["name"]


# ============================================================
# OSINT MODULE TESTS
# ============================================================

class TestOSINTModule:
    """Test OSINT module"""
    
    def test_osint_module_imports(self):
        """Test OSINT module can be imported"""
        from cerberus.modules import osint
        assert osint is not None
        
    def test_vulnerabilities_database_defined(self):
        """Test VULNERABILITIES database is defined"""
        from cerberus.modules.osint import VULNERABILITIES
        assert len(VULNERABILITIES) > 0
        
    def test_vulnerability_structure(self):
        """Test vulnerability entry has correct structure"""
        from cerberus.modules.osint import VULNERABILITIES
        first_key = list(VULNERABILITIES.keys())[0]
        vuln = VULNERABILITIES[first_key]
        
        assert "name" in vuln
        assert "known_bypasses" in vuln
        assert len(vuln["known_bypasses"]) > 0
        
    def test_bypass_structure(self):
        """Test bypass entry has correct structure"""
        from cerberus.modules.osint import VULNERABILITIES
        first_key = list(VULNERABILITIES.keys())[0]
        bypasses = VULNERABILITIES[first_key]["known_bypasses"]
        
        first_bypass = bypasses[0]
        assert "name" in first_bypass
        assert "payload" in first_bypass
        assert "status" in first_bypass
        
    def test_minimax_vulnerabilities_exist(self):
        """Test MiniMax vulnerabilities are defined"""
        from cerberus.modules.osint import VULNERABILITIES
        assert "minimax-2.5" in VULNERABILITIES
        
    def test_gemini_vulnerabilities_exist(self):
        """Test Gemini vulnerabilities are defined"""
        from cerberus.modules.osint import VULNERABILITIES
        assert "gemini-2.5-flash" in VULNERABILITIES
        
    def test_osint_module_functions_exist(self):
        """Test OSINT module has required functions"""
        from cerberus.modules import osint
        assert hasattr(osint, 'module_osint')


# ============================================================
# MODULE INTEGRATION TESTS
# ============================================================

class TestModuleIntegration:
    """Test module integration"""
    
    def test_all_modules_importable(self):
        """Test all modules can be imported"""
        from cerberus.modules import encoder
        from cerberus.modules import hash_tools
        from cerberus.modules import tools
        from cerberus.modules import osint
        from cerberus.modules import redteam
        from cerberus.modules import payload_generator
        from cerberus.modules import advanced_attacks
        
        assert encoder is not None
        assert hash_tools is not None
        assert tools is not None
        assert osint is not None
        assert redteam is not None
        assert payload_generator is not None
        assert advanced_attacks is not None
        
    def test_core_module_integrates_with_all(self):
        """Test core module integrates with all modules"""
        from cerberus import core
        from cerberus.modules import encoder
        from cerberus.modules import tools
        
        # Core exports should be usable
        assert hasattr(core, 'Colors')
        assert hasattr(core, 'box_title')
        assert hasattr(core, 'menu_option')


# ============================================================
# ENCODER EDGE CASE TESTS
# ============================================================

class TestEncoderEdgeCases:
    """Additional encoder edge case tests"""
    
    def test_base64_with_padding(self):
        """Test Base64 handles various padding"""
        from cerberus.modules.encoder import base64_encode_text, base64_decode_text
        
        test_cases = ["a", "ab", "abc", "abcd"]
        for case in test_cases:
            encoded = base64_encode_text(case)
            decoded = base64_decode_text(encoded)
            assert decoded == case
            
    def test_url_special_characters(self):
        """Test URL encoding handles special characters"""
        from cerberus.modules.encoder import url_encode_text
        
        # Various special characters
        result = url_encode_text("hello world&foo=bar#hash")
        assert "%20" in result  # space
        assert "%26" in result  # &
        assert "%3D" in result  # =
        assert "%23" in result  # #
        
    def test_html_all_entities(self):
        """Test HTML encoding handles all entities"""
        from cerberus.modules.encoder import html_encode_text
        
        # Test all major HTML entities
        test = "<>&'\""
        result = html_encode_text(test)
        
        assert "&lt;" in result
        assert "&gt;" in result
        assert "&amp;" in result
        
    def test_hex_case_insensitivity(self):
        """Test hex encoding/decoding is case insensitive"""
        from cerberus.modules.encoder import hex_encode_text, hex_decode_text
        
        result1 = hex_decode_text("48656c6c6f")
        result2 = hex_decode_text("48656C6C6F")
        
        assert result1 == result2 == "Hello"


# ============================================================
# HASH TOOLS EDGE CASE TESTS
# ============================================================

class TestHashToolsEdgeCases:
    """Additional hash tools edge case tests"""
    
    def test_all_hash_algorithms_available(self):
        """Test all hash algorithms are available"""
        from cerberus.modules.hash_tools import (
            generate_hash_md5,
            generate_hash_sha256,
            generate_hash_sha512,
        )
        
        text = "test"
        
        assert generate_hash_md5(text) is not None
        assert generate_hash_sha256(text) is not None
        assert generate_hash_sha512(text) is not None
        
    def test_blake2_hashes_available(self):
        """Test BLAKE2 hashes are available"""
        from cerberus.modules.hash_tools import (
            generate_hash_blake2b,
            generate_hash_blake2s,
        )
        
        text = "test"
        
        # These may or may not exist depending on implementation
        try:
            result_b = generate_hash_blake2b(text)
            assert result_b is not None
            assert len(result_b) == 128  # blake2b hex length (64 bytes = 128 hex chars)
        except AttributeError:
            pytest.skip("blake2b not available")
            
    def test_hash_output_consistency(self):
        """Test hash output is consistent"""
        from cerberus.modules.hash_tools import generate_hash_sha256
        
        text = "consistency_test"
        
        result1 = generate_hash_sha256(text)
        result2 = generate_hash_sha256(text)
        
        assert result1 == result2
        
    def test_different_texts_different_hashes(self):
        """Test different inputs produce different hashes"""
        from cerberus.modules.hash_tools import generate_hash_sha256
        
        hash1 = generate_hash_sha256("text1")
        hash2 = generate_hash_sha256("text2")
        
        assert hash1 != hash2


# ============================================================
# CONNECTOR TESTS - EXTENDED
# ============================================================

class TestConnectorExtended:
    """Extended connector tests"""
    
    def test_all_connectors_instantiable(self):
        """Test all connectors can be instantiated"""
        from cerberus.connectors import (
            GeminiConnector,
            OpenAIConnector,
            AnthropicConnector,
            GrokConnector,
        )
        
        connectors = [
            GeminiConnector,
            OpenAIConnector,
            AnthropicConnector,
            GrokConnector,
        ]
        
        for conn_class in connectors:
            conn = conn_class()
            assert conn is not None
            
    def test_models_dict_has_all_vendors(self):
        """Test MODELS has all expected vendors"""
        from cerberus.connectors import MODELS
        
        vendors = set()
        for model in MODELS.values():
            vendors.add(model.get('vendor', ''))
            
        expected = {'Google', 'OpenAI', 'Anthropic', 'xAI', 'MiniMax'}
        assert expected.issubset(vendors)
        
    def test_get_connector_function(self):
        """Test get_connector function works"""
        from cerberus.connectors import get_connector
        
        # Test with valid model number
        conn = get_connector("1")  # Google
        assert conn is not None


# ============================================================
# CORE EXTENDED TESTS
# ============================================================

class TestCoreExtended:
    """Extended core tests"""
    
    def test_colors_all_defined(self):
        """Test all colors are defined"""
        from cerberus.core import Colors
        
        expected_colors = ['RESET', 'BOLD', 'RED', 'GREEN', 'YELLOW', 'BLUE', 'CYAN', 'MAGENTA', 'WHITE', 'GRAY']
        
        for color in expected_colors:
            assert hasattr(Colors, color), f"Missing color: {color}"
            
    def test_box_subtitle_function(self):
        """Test box_subtitle function exists"""
        from cerberus.core import box_subtitle
        
        result = box_subtitle("Test Subtitle")
        assert "Test Subtitle" in result
        
    def test_status_indicator_true_format(self):
        """Test status_indicator True format"""
        from cerberus.core import status_indicator
        
        result = status_indicator(True)
        # Should indicate success/positive
        assert result is not None
        
    def test_status_indicator_false_format(self):
        """Test status_indicator False format"""
        from cerberus.core import status_indicator
        
        result = status_indicator(False)
        # Should indicate failure/negative
        assert result is not None


# ============================================================
# RUN TESTS
# ============================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
