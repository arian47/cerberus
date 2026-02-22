"""
Cerberus Integration Tests
Test full module integration and API connectors
"""

import pytest
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ============================================================
# CONNECTOR TESTS
# ============================================================

class TestConnectors:
    """Test API connectors"""
    
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
        
    def test_models_dict(self):
        """Test models dictionary is populated"""
        from cerberus.connectors import MODELS
        assert len(MODELS) > 0
        assert "1" in MODELS
        assert MODELS["1"]["name"] is not None


# ============================================================
# CONFIGURATION TESTS
# ============================================================

class TestConfiguration:
    """Test configuration and environment loading"""
    
    def test_core_exports(self):
        """Test core module exports"""
        from cerberus import core
        assert hasattr(core, 'Colors')
        assert hasattr(core, 'box_title')
        assert hasattr(core, 'menu_option')
        assert hasattr(core, 'separator')
        
    def test_api_keys_loaded(self):
        """Test API keys can be loaded from environment"""
        from cerberus.core import (
            GOOGLE_API_KEY, GOOGLE_MODEL, GOOGLE_ENDPOINT,
            OPENAI_API_KEY, OPENAI_MODEL,
            ANTHROPIC_API_KEY, ANTHROPIC_MODEL,
            XAI_API_KEY, XAI_MODEL,
            MINIMAX_API_KEY, MINIMAX_MODEL,
        )
        # These should all be strings (can be empty)
        assert isinstance(GOOGLE_API_KEY, str)
        assert isinstance(GOOGLE_MODEL, str)
        assert isinstance(GOOGLE_ENDPOINT, str)
        assert isinstance(OPENAI_API_KEY, str)
        assert isinstance(ANTHROPIC_API_KEY, str)
        assert isinstance(XAI_API_KEY, str)
        assert isinstance(MINIMAX_API_KEY, str)


# ============================================================
# MODULE IMPORT TESTS
# ============================================================

class TestModuleImports:
    """Test all modules can be imported"""
    
    def test_import_encoder(self):
        """Test encoder module imports"""
        from cerberus.modules import encoder
        assert hasattr(encoder, 'module_encoder')
        
    def test_import_hash_tools(self):
        """Test hash tools module imports"""
        from cerberus.modules import hash_tools
        assert hasattr(hash_tools, 'module_hash_tools')
        
    def test_import_osint(self):
        """Test osint module imports"""
        from cerberus.modules import osint
        assert hasattr(osint, 'module_osint')
        
    def test_import_redteam(self):
        """Test redteam module imports"""
        from cerberus.modules import redteam
        assert hasattr(redteam, 'module_redteam')
        
    def test_import_tools(self):
        """Test tools module imports"""
        from cerberus.modules import tools
        assert hasattr(tools, 'module_tools')
        
    def test_import_payload_generator(self):
        """Test payload generator module imports"""
        from cerberus.modules import payload_generator
        assert hasattr(payload_generator, 'module_payload_generator')
        
    def test_import_advanced_attacks(self):
        """Test advanced attacks module imports"""
        from cerberus.modules import advanced_attacks
        assert hasattr(advanced_attacks, 'module_advanced_attacks')


# ============================================================
# MAIN ENTRY POINT TEST
# ============================================================

class TestMainEntry:
    """Test main cerberus.py entry point"""
    
    def test_main_imports(self):
        """Test cerberus.py can be imported"""
        # Import from root cerberus.py, not cerberus package
        import importlib.util
        spec = importlib.util.spec_from_file_location("cerberus_main", 
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "cerberus.py"))
        cerberus_main = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cerberus_main)
        # Should have MENU_OPTIONS defined
        assert hasattr(cerberus_main, 'MENU_OPTIONS')
        assert 'Cerberus' in cerberus_main.MENU_OPTIONS
        
    def test_colors_class(self):
        """Test Colors class has required attributes"""
        from cerberus import Colors
        assert hasattr(Colors, 'RED')
        assert hasattr(Colors, 'GREEN')
        assert hasattr(Colors, 'BLUE')
        assert hasattr(Colors, 'CYAN')
        assert hasattr(Colors, 'RESET')
        assert hasattr(Colors, 'BOLD')


# ============================================================
# RUN TESTS
# ============================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
