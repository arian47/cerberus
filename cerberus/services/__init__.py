"""
Cerberus Services Package

Microservices architecture for the Cerberus Cybersecurity Companion.
Each service is a self-contained module for specific functionality.
"""

# LLM Service
from cerberus.services.llm import (
    LLMService,
    LLMConnector,
    get_connector,
    get_available_models,
    is_model_available,
    call_model,
    MODELS,
)

# Hash Service
from cerberus.services.hash import (
    HashService,
    hash_text,
    hash_file,
    verify_hash,
    get_algorithm_info,
)

# Encoder Service
from cerberus.services.encoder import (
    EncoderService,
    base64_encode,
    base64_decode,
    url_encode,
    url_decode,
    html_encode,
    html_decode,
    hex_encode,
    hex_decode,
    binary_encode_text,
    binary_decode_text,
    json_encode_text,
    json_decode_text,
    rot13_encode_text,
    rot13_decode_text,
    morse_encode_text,
    morse_decode_text,
    unicode_encode,
    unicode_decode,
    ascii_table_generate,
)

# Payload Service
from cerberus.services.payloads import (
    PayloadService,
    generate_php_webshell,
    generate_reverse_shell,
    get_sql_injection_payloads,
    get_xss_payloads,
    encode_payload,
)

# Tor Service
from cerberus.services.tor import (
    TorService,
    get_service,
    is_tor_running,
    get_session,
    get_onion_session,
    check_ip,
    ensure_tor_running,
    get_installation_instructions,
    renew_tor_ip,
    get_tor_info,
    create_config_with_control_port,
    start_tor_with_config,
    enable_control_port,
)

# Password Service
from cerberus.services.password import (
    PasswordService,
    get_service as get_password_service,
    generate_password,
    generate_passphrase,
    check_password_strength,
    is_password_compromised,
    hash_lookup,
    generate_pin,
    generate_api_key,
    generate_secure_token,
)

# Network Scanner Service
from cerberus.services.network import (
    NetworkScannerService,
    get_service as get_network_service,
    scan_port,
    scan_ports,
    scan_common_ports,
    scan_port_range,
    ping_host,
    scan_network,
    detect_service,
    get_banner,
    reverse_dns,
    dns_lookup,
    get_local_ip,
    get_hostname,
)

# Vulnerability Database Service
from cerberus.services.vulnerability import (
    VulnerabilityService,
    get_service as get_vulnerability_service,
    get_vulnerabilities_for_model,
    get_all_vulnerable_models,
    search_vulnerabilities,
    get_vulnerabilities_by_category,
    get_vulnerabilities_by_severity,
    get_cve_info,
    get_cwe_info,
    get_statistics,
)

# Red Team Service
from cerberus.services.redteam import (
    RedTeamService,
    get_service as get_redteam_service,
    get_payloads,
    get_payload,
    add_payload,
    analyze_response,
    check_bypass,
    test_model_all_payloads,
    test_all_models,
    generate_report,
)

__all__ = [
    # LLM
    "LLMService",
    "LLMConnector", 
    "get_connector",
    "get_available_models",
    "is_model_available",
    "call_model",
    "MODELS",
    # Hash
    "HashService",
    "hash_text",
    "hash_file",
    "verify_hash",
    "get_algorithm_info",
    # Encoder
    "EncoderService",
    "base64_encode",
    "base64_decode",
    "url_encode",
    "url_decode",
    "html_encode",
    "html_decode",
    "hex_encode",
    "hex_decode",
    "binary_encode_text",
    "binary_decode_text",
    "json_encode_text",
    "json_decode_text",
    "rot13_encode_text",
    "rot13_decode_text",
    "morse_encode_text",
    "morse_decode_text",
    "unicode_encode",
    "unicode_decode",
    "ascii_table_generate",
    # Payloads
    "PayloadService",
    "generate_php_webshell",
    "generate_reverse_shell",
    "get_sql_injection_payloads",
    "get_xss_payloads",
    "encode_payload",
    # Tor
    "TorService",
    "get_service",
    "is_tor_running",
    "get_session",
    "get_onion_session",
    "check_ip",
    "ensure_tor_running",
    "get_installation_instructions",
    "renew_tor_ip",
    "get_tor_info",
    # Password
    "PasswordService",
    "get_password_service",
    "generate_password",
    "generate_passphrase",
    "check_password_strength",
    "is_password_compromised",
    "hash_lookup",
    "generate_pin",
    "generate_api_key",
    "generate_secure_token",
    # Network
    "NetworkScannerService",
    "get_network_service",
    "scan_port",
    "scan_ports",
    "scan_common_ports",
    "scan_port_range",
    "ping_host",
    "scan_network",
    "detect_service",
    "get_banner",
    "reverse_dns",
    "dns_lookup",
    "get_local_ip",
    "get_hostname",
    # Vulnerability
    "VulnerabilityService",
    "get_vulnerability_service",
    "get_vulnerabilities_for_model",
    "get_all_vulnerable_models",
    "search_vulnerabilities",
    "get_vulnerabilities_by_category",
    "get_vulnerabilities_by_severity",
    "get_cve_info",
    "get_cwe_info",
    "get_statistics",
    # Red Team
    "RedTeamService",
    "get_redteam_service",
    "get_payloads",
    "get_payload",
    "add_payload",
    "analyze_response",
    "check_bypass",
    "test_model_all_payloads",
    "test_all_models",
    "generate_report",
]
