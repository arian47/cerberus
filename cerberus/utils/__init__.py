"""
Cerberus Utils Package

Common utility functions for the Cerberus application.
"""

import os
import re
import hashlib
from typing import Optional, List, Dict, Any
from pathlib import Path


# ==================== File Utilities ====================

def ensure_dir(path: str) -> bool:
    """
    Ensure a directory exists, create if it doesn't.
    
    Args:
        path: Directory path to ensure
        
    Returns:
        True if directory exists or was created, False on error
    """
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error creating directory: {e}")
        return False


def read_file(file_path: str, binary: bool = False) -> Optional[Any]:
    """
    Read a file safely.
    
    Args:
        file_path: Path to file to read
        binary: Whether to read in binary mode
        
    Returns:
        File contents as string/bytes or None on error
    """
    try:
        mode = 'rb' if binary else 'r'
        with open(file_path, mode) as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


def write_file(file_path: str, content: Any, binary: bool = False) -> bool:
    """
    Write content to a file safely.
    
    Args:
        file_path: Path to file to write
        content: Content to write
        binary: Whether to write in binary mode
        
    Returns:
        True on success, False on error
    """
    try:
        mode = 'wb' if binary else 'w'
        with open(file_path, mode) as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error writing file: {e}")
        return False


def get_file_hash(file_path: str, algorithm: str = 'sha256') -> Optional[str]:
    """
    Calculate hash of a file.
    
    Args:
        file_path: Path to file
        algorithm: Hash algorithm (md5, sha1, sha256, sha512)
        
    Returns:
        Hex digest of file hash or None on error
    """
    try:
        hash_obj = hashlib.new(algorithm)
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    except Exception as e:
        print(f"Error hashing file: {e}")
        return None


def list_files(directory: str, pattern: str = "*", recursive: bool = False) -> List[str]:
    """
    List files in a directory.
    
    Args:
        directory: Directory to list
        pattern: Glob pattern to match
        recursive: Whether to search recursively
        
    Returns:
        List of file paths
    """
    try:
        path = Path(directory)
        if recursive:
            return [str(f) for f in path.rglob(pattern) if f.is_file()]
        return [str(f) for f in path.glob(pattern) if f.is_file()]
    except Exception as e:
        print(f"Error listing files: {e}")
        return []


# ==================== Validation Utilities ====================

def is_valid_url(url: str) -> bool:
    """
    Validate if a string is a valid URL.
    
    Args:
        url: URL string to validate
        
    Returns:
        True if valid URL, False otherwise
    """
    url_pattern = re.compile(
        r'^https?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return bool(url_pattern.match(url))


def is_valid_email(email: str) -> bool:
    """
    Validate if a string is a valid email address.
    
    Args:
        email: Email string to validate
        
    Returns:
        True if valid email, False otherwise
    """
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    return bool(email_pattern.match(email))


def is_valid_ip(ip: str) -> bool:
    """
    Validate if a string is a valid IP address.
    
    Args:
        ip: IP string to validate
        
    Returns:
        True if valid IP, False otherwise
    """
    ipv4_pattern = re.compile(
        r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'
        r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
    return bool(ipv4_pattern.match(ip))


def is_valid_domain(domain: str) -> bool:
    """
    Validate if a string is a valid domain name.
    
    Args:
        domain: Domain string to validate
        
    Returns:
        True if valid domain, False otherwise
    """
    domain_pattern = re.compile(
        r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)*'
        r'[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$')
    return bool(domain_pattern.match(domain))


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename by removing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')
    # Limit length
    if len(filename) > 255:
        filename = filename[:255]
    return filename


# ==================== String Utilities ====================

def truncate_string(text: str, max_length: int = 80, suffix: str = "...") -> str:
    """
    Truncate a string to a maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated string
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def extract_urls(text: str) -> List[str]:
    """
    Extract all URLs from text.
    
    Args:
        text: Text to extract URLs from
        
    Returns:
        List of URLs
    """
    url_pattern = re.compile(r'https?://[^\s<>"{}|\\^`\[\]]+')
    return url_pattern.findall(text)


def extract_emails(text: str) -> List[str]:
    """
    Extract all email addresses from text.
    
    Args:
        text: Text to extract emails from
        
    Returns:
        List of email addresses
    """
    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    return email_pattern.findall(text)


def extract_ips(text: str) -> List[str]:
    """
    Extract all IP addresses from text.
    
    Args:
        text: Text to extract IPs from
        
    Returns:
        List of IP addresses
    """
    ip_pattern = re.compile(
        r'\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
        r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
        r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
        r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b')
    return ip_pattern.findall(text)


def normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace in text.
    
    Args:
        text: Text to normalize
        
    Returns:
        Text with normalized whitespace
    """
    return ' '.join(text.split())


# ==================== Network Utilities ====================

def parse_url(url: str) -> Optional[Dict[str, str]]:
    """
    Parse URL into components.
    
    Args:
        url: URL to parse
        
    Returns:
        Dict with scheme, host, port, path, query or None on error
    """
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return {
            'scheme': parsed.scheme,
            'host': parsed.hostname or '',
            'port': parsed.port or 0,
            'path': parsed.path,
            'query': parsed.query,
            'fragment': parsed.fragment,
        }
    except Exception:
        return None


def build_url(scheme: str = "http", host: str = "", port: int = 0, 
              path: str = "", query: str = "") -> str:
    """
    Build URL from components.
    
    Args:
        scheme: URL scheme (http, https)
        host: Hostname
        port: Port number
        path: Path
        query: Query string
        
    Returns:
        Built URL
    """
    url = f"{scheme}://{host}"
    if port:
        url += f":{port}"
    if path:
        url += path
    if query:
        url += f"?{query}"
    return url


# ==================== Config Utilities ====================

def load_env_file(env_file: str = ".env") -> Dict[str, str]:
    """
    Load environment variables from a .env file.
    
    Args:
        env_file: Path to .env file
        
    Returns:
        Dict of environment variables
    """
    env_vars = {}
    try:
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        env_vars[key.strip()] = value.strip().strip('"').strip("'")
    except Exception as e:
        print(f"Error loading .env file: {e}")
    return env_vars


def get_env_with_prefix(prefix: str) -> Dict[str, str]:
    """
    Get environment variables with a specific prefix.
    
    Args:
        prefix: Prefix to filter by
        
    Returns:
        Dict of matching environment variables
    """
    return {k: v for k, v in os.environ.items() if k.startswith(prefix)}


# ==================== Time Utilities ====================

def format_timestamp(timestamp: float = None, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format a timestamp.
    
    Args:
        timestamp: Unix timestamp (default: current time)
        fmt: Format string
        
    Returns:
        Formatted timestamp
    """
    import datetime
    if timestamp is None:
        dt = datetime.datetime.now()
    else:
        dt = datetime.datetime.fromtimestamp(timestamp)
    return dt.strftime(fmt)


def get_time_diff(start: float, end: float = None) -> str:
    """
    Get human-readable time difference.
    
    Args:
        start: Start timestamp
        end: End timestamp (default: current time)
        
    Returns:
        Human-readable time difference
    """
    import datetime
    if end is None:
        end = datetime.datetime.now().timestamp()
    
    diff = end - start
    if diff < 1:
        return f"{diff * 1000:.0f}ms"
    elif diff < 60:
        return f"{diff:.1f}s"
    elif diff < 3600:
        return f"{diff / 60:.1f}m"
    else:
        return f"{diff / 3600:.1f}h"
