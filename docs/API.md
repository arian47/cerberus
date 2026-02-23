# Cerberus API Documentation

## Overview

Cerberus is a cybersecurity companion tool with a microservices architecture. The application is organized into several packages:

- **cerberus.services** - Core microservices for specific functionality
- **cerberus.cli** - Command-line interface components
- **cerberus.utils** - Common utility functions
- **cerberus.modules** - Original module implementations

---

## Services Package (`cerberus.services`)

### Hash Service (`cerberus.services.hash`)

Provides hashing and verification functionality.

#### Classes

##### `HashService`

Main service class for hash operations.

**Methods:**

| Method | Description | Returns |
|--------|-------------|---------|
| `hash_text(text, algorithm)` | Hash a text string | `Optional[str]` |
| `hash_file(file_path, algorithm)` | Hash a file | `Optional[str]` |
| `verify_hash(text, hash_to_verify, algorithm)` | Verify a hash | `bool` |
| `get_supported_algorithms()` | List supported algorithms | `List[str]` |
| `generate_password_hash(password)` | Generate password hash | `str` |

#### Module Functions

```python
from cerberus.services import hash_text, hash_file, verify_hash, HashService

# Hash text
sha256_hash = hash_text("hello world", "sha256")

# Hash file
md5_hash = hash_file("malware.exe", "md5")

# Verify hash
is_valid = verify_hash("hello world", "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9", "sha256")
```

---

### Encoder Service (`cerberus.services.encoder`)

Provides encoding and decoding functionality.

#### Classes

##### `EncoderService`

Main service class for encoding operations.

**Methods:**

| Method | Description | Returns |
|--------|-------------|---------|
| `base64_encode(text)` | Base64 encode | `str` |
| `base64_decode(text)` | Base64 decode | `Optional[str]` |
| `url_encode(text)` | URL encode | `str` |
| `url_decode(text)` | URL decode | `Optional[str]` |
| `html_encode(text)` | HTML encode | `str` |
| `html_decode(text)` | HTML decode | `str` |
| `hex_encode(text)` | Hex encode | `str` |
| `hex_decode(text)` | Hex decode | `Optional[str]` |
| `binary_encode_text(text)` | Binary encode | `str` |
| `binary_decode_text(text)` | Binary decode | `Optional[str]` |
| `rot13_encode_text(text)` | ROT13 encode | `str` |
| `morse_encode_text(text)` | Morse code encode | `str` |
| `morse_decode_text(text)` | Morse code decode | `Optional[str]` |

#### Module Functions

```python
from cerberus.services import (
    base64_encode, base64_decode,
    url_encode, url_decode,
    html_encode, html_decode,
    hex_encode, hex_decode,
    rot13_encode_text,
    EncoderService
)

# Base64 encoding
encoded = base64_encode("secret message")
decoded = base64_decode(encoded)

# URL encoding
url_encoded = url_encode("hello world?")
url_decoded = url_decode(url_encoded)

# HTML encoding
html_encoded = html_encode("<script>alert('xss')</script>")
```

---

### LLM Service (`cerberus.services.llm`)

Provides connectivity to various Large Language Model providers.

#### Classes

##### `LLMService`

Main service class for LLM operations.

**Methods:**

| Method | Description | Returns |
|--------|-------------|---------|
| `get_available_models()` | Get models with API keys | `Dict` |
| `get_all_models()` | Get all models | `Dict` |
| `is_model_available(model_id)` | Check if model configured | `bool` |
| `get_connector(model_id)` | Get connector for model | `Optional[LLMConnector]` |
| `call_model(model_id, prompt, system_prompt)` | Call LLM | `Optional[str]` |

##### `LLMConnector` (Base Class)

Base class for all LLM connectors.

**Subclasses:**

- `GoogleConnector` - Google Gemini
- `OpenAIConnector` - OpenAI GPT models
- `AnthropicConnector` - Anthropic Claude
- `XAIConnector` - xAI Grok
- `MiniMaxConnector` - MiniMax models

#### Available Models

| ID | Model Name | Vendor |
|----|------------|--------|
| 1 | gemini-2.5-flash | Google |
| 2 | gemini-2.5-pro | Google |
| 3 | gpt-4o | OpenAI |
| 4 | gpt-4o-mini | OpenAI |
| 5 | claude-sonnet-4 | Anthropic |
| 6 | claude-4-opus | Anthropic |
| 7 | grok-3 | xAI |
| 8 | grok-4 | xAI |
| 9 | MiniMax-M2.5 | MiniMax |

#### Environment Variables

```bash
# Required API Keys
GOOGLE_API_KEY=your_google_key
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
XAI_API_KEY=your_xai_key
MINIMAX_API_KEY=your_minimax_key

# Optional: Override default models
GOOGLE_MODEL=gemini-2.5-flash
OPENAI_MODEL=gpt-4o
ANTHROPIC_MODEL=claude-4-opus
```

#### Usage

```python
from cerberus.services import get_connector, get_available_models, call_model

# Get available models
available = get_available_models()

# Get a specific connector
connector = get_connector("1")  # Google Gemini
if connector:
    response = connector.generate("Hello, how are you?")

# Or use the convenience function
response = call_model("3", "What is the capital of France?")
```

---

### Payload Service (`cerberus.services.payloads`)

Generates various offensive security payloads.

#### Classes

##### `PayloadService`

Main service class for payload generation.

**Methods:**

| Method | Description | Returns |
|--------|-------------|---------|
| `generate_php_webshell(variant)` | Generate PHP webshell | `str` |
| `generate_reverse_shell(shell_type, lhost, lport)` | Generate reverse shell | `str` |
| `generate_bind_shell(shell_type, port)` | Generate bind shell | `str` |
| `get_sql_injection_payloads()` | Get SQLi payloads | `List[str]` |
| `get_xss_payloads()` | Get XSS payloads | `List[str]` |
| `encode_payload(payload, encoding)` | Encode a payload | `str` |
| `generate_obfuscated_php(base_shell)` | Generate obfuscated PHP | `str` |
| `generate_file_upload_bypass(extension)` | Generate bypass techniques | `List[str]` |

#### Module Functions

```python
from cerberus.services import (
    generate_php_webshell,
    generate_reverse_shell,
    get_sql_injection_payloads,
    get_xss_payloads,
    encode_payload,
    PayloadService
)

# Generate PHP webshell
webshell = generate_php_webshell(0)

# Generate reverse shell
shell = generate_reverse_shell("python", "10.10.10.10", 4444)
shell = generate_reverse_shell("bash", "10.10.10.10", 4444)
shell = generate_reverse_shell("powershell", "10.10.10.10", 4444)

# Get payloads
sqli_payloads = get_sql_injection_payloads()
xss_payloads = get_xss_payloads()

# Encode payload
encoded = encode_payload(shell, "base64")
```

---

## CLI Package (`cerberus.cli`)

### Renderer Service (`cerberus.cli.renderers`)

Provides CLI UI rendering and user interaction.

#### Classes

##### `CLIRenderer`

Main renderer class for CLI components.

**Methods:**

| Method | Description |
|--------|-------------|
| `print_header(title, subtitle)` | Print application header |
| `print_main_menu(title)` | Print main menu |
| `print_submenu(title, items, back)` | Print submenu |
| `print_panel(title, content, style)` | Print panel |
| `print_success(msg)` | Print success message |
| `print_error(msg)` | Print error message |
| `print_warning(msg)` | Print warning message |
| `print_info(msg)` | Print info message |
| `print_model_table(models, available)` | Print AI model table |
| `print_api_keys(api_keys)` | Print API keys status |
| `get_input(prompt_text)` | Get user input |
| `get_yes_no(prompt_text)` | Get yes/no confirmation |
| `pause()` | Pause for user input |

#### Module Functions

```python
from cerberus.cli import (
    print_header,
    print_main_menu,
    print_panel,
    print_success,
    print_error,
    print_warning,
    print_info,
    get_input,
    get_yes_no,
    pause
)

# Print header
print_header("CERBERUS", "Cybersecurity Companion")

# Print menu
print_main_menu()

# Get input
choice = get_input("Select an option")

# Confirm
if get_yes_no("Continue?"):
    print_success("Confirmed!")
```

---

## Utils Package (`cerberus.utils`)

### File Utilities

```python
from cerberus.utils import (
    ensure_dir,
    read_file,
    write_file,
    get_file_hash,
    list_files
)

# Ensure directory exists
ensure_dir("./output")

# Read/Write files
content = read_file("data.txt")
write_file("output.txt", "content")

# Get file hash
sha256 = get_file_hash("malware.exe", "sha256")

# List files
files = list_files("./data", "*.txt")
```

### Validation Utilities

```python
from cerberus.utils import (
    is_valid_url,
    is_valid_email,
    is_valid_ip,
    is_valid_domain,
    sanitize_filename
)

# Validate inputs
is_valid_url("https://example.com")
is_valid_email("user@example.com")
is_valid_ip("192.168.1.1")
is_valid_domain("example.com")
sanitize_filename("file<>?.txt")  # "file__.txt"
```

### String Utilities

```python
from cerberus.utils import (
    truncate_string,
    extract_urls,
    extract_emails,
    extract_ips,
    normalize_whitespace
)

# Extract from text
urls = extract_urls("Visit https://example.com for more info")
emails = extract_emails("Contact admin@example.com")
ips = extract_ips("Server at 192.168.1.1")

# Transform
truncated = truncate_string("long text...", 10)  # "long te..."
normalized = normalize_whitespace("  multiple   spaces  ")  # "multiple spaces"
```

---

## Quick Reference

### Import All Services

```python
# Import everything
from cerberus.services import *
from cerberus.cli import *
from cerberus.utils import *
```

### Service Instantiation

```python
# Using service classes
hash_service = HashService()
encoder_service = EncoderService()
llm_service = LLMService()
payload_service = PayloadService()
cli_renderer = CLIRenderer()

# Using module-level functions (recommended)
result = hash_text("data", "sha256")
encoded = base64_encode("test")
response = call_model("1", "prompt")
```

---

## Environment Setup

Create a `.env` file in the project root:

```bash
# LLM API Keys
GOOGLE_API_KEY=your_google_key
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
XAI_API_KEY=your_xai_key
MINIMAX_API_KEY=your_minimax_key

# Optional: Debug mode
DEBUG=true
```
