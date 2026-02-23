# Cerberus Architecture

## Overview

Cerberus follows a microservices architecture, separating concerns into distinct packages:

```
cerberus/
├── services/          # Core microservices (independent functionality)
│   ├── hash.py        # Hashing service
│   ├── encoder.py     # Encoding/decoding service
│   ├── llm.py         # LLM connectors service
│   ├── payloads.py    # Payload generation service
│   ├── tor.py         # Tor network connectivity
│   ├── password.py    # Password generation & security
│   ├── network.py     # Network scanning & reconnaissance
│   ├── vulnerability.py # Vulnerability database
│   └── redteam.py     # LLM vulnerability testing
├── cli/               # Command-line interface components
│   ├── __init__.py
│   └── renderers.py   # UI rendering service
├── utils/             # Common utilities
│   └── __init__.py    # File, validation, string utilities
├── modules/           # Original module implementations
│   ├── encoder.py     # Original encoder module
│   ├── hash_tools.py  # Original hash module
│   ├── connectors.py  # Original connectors module
│   ├── osint.py       # OSINT module
│   ├── redteam.py     # Red team module
│   ├── tools.py       # Tools module
│   ├── tor.py         # Tor module
│   ├── payload_generator.py
│   └── advanced_attacks.py
└── __init__.py
```

## Design Principles

### 1. Service Isolation
Each service is self-contained and can be imported independently:

```python
# Hash service works without any other imports
from cerberus.services import hash_text
result = hash_text("data", "sha256")
```

### 2. Consistent Interface
All services follow consistent patterns:
- Service class for complex operations
- Module-level functions for convenience
- Clear documentation and type hints

### 3. Backward Compatibility
Original modules in `cerberus/modules/` remain functional.
New services complement rather than replace.

### 4. Testability
Each service can be unit tested independently:
```python
from cerberus.services import HashService

def test_hash_service():
    service = HashService()
    result = service.hash_text("test", "sha256")
    assert result is not None
```

## Services

### Hash Service
- **File**: `cerberus/services/hash.py`
- **Purpose**: Generate and verify cryptographic hashes
- **Algorithms**: MD5, SHA1, SHA256, SHA512, BLAKE2

### Encoder Service
- **File**: `cerberus/services/encoder.py`
- **Purpose**: Encode/decode in various formats
- **Formats**: Base64, URL, HTML, Hex, Binary, ROT13, Morse

### LLM Service
- **File**: `cerberus/services/llm.py`
- **Purpose**: Connect to LLM providers
- **Providers**: Google, OpenAI, Anthropic, xAI, MiniMax

### Payload Service
- **File**: `cerberus/services/payloads.py`
- **Purpose**: Generate security payloads
- **Types**: Webshells, Reverse shells, SQLi, XSS

### Tor Service
- **File**: `cerberus/services/tor.py`
- **Purpose**: Tor network connectivity
- **Features**: Installation, service control, session management

### Password Service
- **File**: `cerberus/services/password.py`
- **Purpose**: Password generation & security
- **Features**: Password generation, strength analysis, PINs, tokens

### Network Service
- **File**: `cerberus/services/network.py`
- **Purpose**: Network scanning & reconnaissance
- **Features**: Port scanning, host discovery, DNS lookups

### Vulnerability Service
- **File**: `cerberus/services/vulnerability.py`
- **Purpose**: Vulnerability database
- **Features**: LLM bypass tracking, CVE/CWE information

### RedTeam Service
- **File**: `cerberus/services/redteam.py`
- **Purpose**: LLM vulnerability testing
- **Features**: Payload management, response analysis

## CLI Components

### Renderer Service
- **File**: `cerberus/cli/renderers.py`
- **Purpose**: Handle all CLI output and user input
- **Features**: Menus, panels, tables, prompts

## Utilities

### Common Utils
- **File**: `cerberus/utils/__init__.py`
- **Features**:
  - File operations (read, write, list)
  - Validation (URL, email, IP, domain)
  - String manipulation (extract, truncate)
  - Network utilities (parse/build URLs)

## Migration Guide

### Old Import Style (Still Works)
```python
from cerberus.modules.encoder import base64_encode
from cerberus.modules.hash_tools import generate_hash
```

### New Service Style (Recommended)
```python
from cerberus.services import base64_encode, hash_text

# Use services directly
result = hash_text("data", "sha256")
```

### Using Service Classes
```python
from cerberus.services import EncoderService, HashService

encoder = EncoderService()
hashing = HashService()

encoded = encoder.base64_encode("data")
hashed = hashing.hash_text("data", "sha256")
```

## Testing

Run tests for specific services:
```bash
# Test hash service
python -m pytest tests/ -k "hash"

# Test encoder service
python -m pytest tests/ -k "encoder"

# Test all
python -m pytest tests/
```

## Performance Considerations

- Services are stateless where possible
- Lazy loading of heavy dependencies
- Connection pooling for LLM services
- Efficient file hashing with chunked reading
