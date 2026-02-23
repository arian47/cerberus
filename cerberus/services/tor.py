"""
Cerberus Tor Service

Microservice for Tor network connectivity.
Provides session management, installation, and service control.
"""

import os
import sys
import subprocess
import time
import socket
from typing import Optional, Dict, Any
import requests


class TorService:
    """
    Service for Tor network operations.
    Handles Tor installation, service management, and session creation.
    """
    
    DEFAULT_SOCKS_PORT = 9050
    DEFAULT_CONTROL_PORT = 9051
    DEFAULT_HTTP_PORT = 8123
    
    def __init__(self, socks_port: int = None, control_port: int = None, http_port: int = None):
        """Initialize Tor service."""
        self.socks_port = socks_port or self.DEFAULT_SOCKS_PORT
        self.control_port = control_port or self.DEFAULT_CONTROL_PORT
        self.http_port = http_port or self.DEFAULT_HTTP_PORT
    
    # ==================== System Checks ====================
    
    def is_admin(self) -> bool:
        """Check if running with administrator privileges."""
        try:
            if sys.platform == 'win32':
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            else:
                return os.geteuid() == 0
        except Exception:
            return False
    
    def check_chocolatey(self) -> bool:
        """Check if Chocolatey is installed."""
        try:
            result = subprocess.run(
                ['choco', '--version'],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except Exception:
            return False
    
    # ==================== Installation ====================
    
    def install_tor_windows(self) -> bool:
        """Install Tor on Windows using Chocolatey."""
        if not self.check_chocolatey():
            print("Chocolatey is not installed. Please install it first.")
            return False
        
        try:
            print("Installing Tor...")
            result = subprocess.run(
                ['choco', 'install', 'tor', '-y'],
                capture_output=True,
                text=True,
                timeout=300
            )
            return result.returncode == 0
        except Exception as e:
            print(f"Error installing Tor: {e}")
            return False
    
    def install_tor(self) -> bool:
        """Install Tor based on platform."""
        if sys.platform == 'win32':
            return self.install_tor_windows()
        else:
            # Linux/macOS
            try:
                result = subprocess.run(
                    ['apt-get', 'install', '-y', 'tor'],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                return result.returncode == 0
            except Exception:
                return False
    
    # ==================== Service Control ====================
    
    def start_tor_service(self) -> bool:
        """Start Tor service."""
        try:
            if sys.platform == 'win32':
                result = subprocess.run(
                    ['sc', 'start', 'Tor'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                return result.returncode == 0
            else:
                result = subprocess.run(
                    ['service', 'tor', 'start'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                return result.returncode == 0
        except Exception as e:
            print(f"Error starting Tor: {e}")
            return False
    
    def stop_tor_service(self) -> bool:
        """Stop Tor service."""
        try:
            if sys.platform == 'win32':
                result = subprocess.run(
                    ['sc', 'stop', 'Tor'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                return result.returncode == 0
            else:
                result = subprocess.run(
                    ['service', 'tor', 'stop'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                return result.returncode == 0
        except Exception as e:
            print(f"Error stopping Tor: {e}")
            return False
    
    def is_tor_running(self) -> bool:
        """Check if Tor is running."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        try:
            result = sock.connect_ex(('127.0.0.1', self.socks_port))
            sock.close()
            return result == 0
        except Exception:
            return False
    
    # ==================== Session Management ====================
    
    def get_session(self, proxy_type: str = 'socks5') -> Optional[requests.Session]:
        """
        Get a requests session routed through Tor.
        
        Args:
            proxy_type: Type of proxy (socks5, socks4, http)
            
        Returns:
            Configured requests Session or None
        """
        if not self.is_tor_running():
            print("Tor is not running. Please start Tor first.")
            return None
        
        session = requests.Session()
        
        proxy = f"{proxy_type}://127.0.0.1:{self.socks_port}"
        session.proxies = {
            'http': proxy,
            'https': proxy,
        }
        
        # Set common headers
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        return session
    
    def get_onion_session(self) -> Optional[requests.Session]:
        """Get session optimized for .onion sites."""
        return self.get_session()
    
    # ==================== IP Verification ====================
    
    def check_ip(self, session: requests.Session = None) -> Optional[str]:
        """Check current IP address through Tor."""
        try:
            if session is None:
                session = self.get_session()
                if session is None:
                    return None
            
            response = session.get('https://httpbin.org/ip', timeout=30)
            if response.status_code == 200:
                data = response.json()
                return data.get('origin', '')
            return None
        except Exception as e:
            print(f"Error checking IP: {e}")
            return None
    
    def renew_tor_ip(self) -> bool:
        """
        Request a new Tor identity (new IP).
        
        Returns:
            True if successful
        """
        # Try multiple control ports commonly used by Tor
        control_ports = [
            self.control_port,           # Default (9051)
            9151,                        # Tor Browser
            9052,                        # Alternate
            9152,                        # Tor Browser alternate
        ]
        
        # Remove duplicates while preserving order
        control_ports = list(dict.fromkeys(control_ports))
        
        last_error = None
        for port in control_ports:
            try:
                from stem import Signal
                from stem.control import Controller
                
                with Controller.from_port(port=port) as controller:
                    controller.authenticate()
                    controller.signal(Signal.NEWNYM)
                    # Update the control port on successful connection
                    self.control_port = port
                    return True
            except ImportError:
                print("Stem library required for this feature")
                print("Install with: pip install stem")
                return False
            except Exception as e:
                last_error = str(e)
                continue
        
        # All ports failed
        print("Error: Could not connect to Tor control port")
        print("Make sure Tor is running with control port enabled:")
        print("  - Add 'ControlPort 9051' to your torrc file")
        print("  - Or use Tor Browser with 'Enable control port' setting")
        print(f"  - Tried ports: {', '.join(map(str, control_ports))}")
        if last_error:
            print(f"  - Last error: {last_error}")
        return False
    
    def get_tor_info(self) -> Dict[str, Any]:
        """Get detailed Tor connection information."""
        info = {
            'running': self.is_tor_running(),
            'socks_port': self.socks_port,
            'control_port': self.control_port,
        }
        
        if info['running']:
            session = self.get_session()
            if session:
                info['ip'] = self.check_ip(session)
        
        # Try to get stem info
        try:
            from stem import __version__ as stem_version
            info['stem_version'] = stem_version
        except ImportError:
            info['stem_version'] = None
        
        return info
    
    # ==================== Configuration ====================
    
    def ensure_tor_running(self) -> Dict[str, Any]:
        """
        Ensure Tor is running, install if needed.
        
        Returns:
            Dict with status and details
        """
        result = {
            'installed': False,
            'running': False,
            'ip': None,
            'message': ''
        }
        
        # Check if running
        if self.is_tor_running():
            result['running'] = True
            result['message'] = 'Tor is already running'
            session = self.get_session()
            if session:
                result['ip'] = self.check_ip(session)
            return result
        
        # Check if installed
        if sys.platform == 'win32':
            installed = self.check_chocolatey()
        else:
            import shutil
            installed = shutil.which('tor') is not None
        
        if not installed:
            result['message'] = 'Tor is not installed'
            return result
        
        # Try to start
        if self.start_tor_service():
            # Wait for Tor to start
            for _ in range(30):
                time.sleep(1)
                if self.is_tor_running():
                    result['installed'] = True
                    result['running'] = True
                    result['message'] = 'Tor started successfully'
                    session = self.get_session()
                    if session:
                        result['ip'] = self.check_ip(session)
                    return result
            
            result['message'] = 'Tor failed to start'
        else:
            result['message'] = 'Failed to start Tor service'
        
        return result
    
    # ==================== Installation Instructions ====================
    
    def get_installation_instructions(self) -> str:
        """Get platform-specific installation instructions."""
        if sys.platform == 'win32':
            return """
## Windows Installation

### Option 1: Chocolatey (Recommended)
```powershell
# Install Chocolatey first
Set-ExecutionPolicy Bypass -Scope Process -Force
iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

# Install Tor
choco install tor -y
```

### Option 2: Manual
1. Download Tor Browser from https://www.torproject.org
2. Install and run the Tor Expert Bundle
3. Configure the service to run automatically

### Option 3: Using Scoop
```powershell
scoop install tor
```
"""
        else:
            return """
## Linux Installation

### Debian/Ubuntu
```bash
sudo apt update
sudo apt install tor
sudo service tor start
```

### Fedora/RHEL
```bash
sudo dnf install tor
sudo systemctl enable --now tor
```

### macOS
```bash
brew install tor
brew services start tor
```
"""

    def create_config_with_control_port(self, config_path: str = None) -> str:
        """Create a Tor config file with control port enabled."""
        if config_path is None:
            # Use Tor data directory
            if sys.platform == 'win32':
                tor_data = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Tor', 'data')
            else:
                tor_data = os.path.expanduser("~/.tor")
            
            os.makedirs(tor_data, exist_ok=True)
            config_path = os.path.join(tor_data, 'torrc')
        
        # Get absolute paths
        if sys.platform == 'win32':
            tor_data = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Tor', 'data')
        else:
            tor_data = os.path.expanduser("~/.tor")
        
        config_content = f"""# Tor configuration with control port enabled
# Generated by Cerberus

# SOCKS proxy port
SOCKSPort 9050

# Control port - required for New Identity feature
ControlPort 9051

# Cookie authentication (more secure)
CookieAuthentication 1

# Data directory
DataDirectory {tor_data}

# GeoIP files (point to Tor Browser defaults if available)
GeoIPFile C:\\Users\\arian\\AppData\\Local\\Tor\\data\\geoip
GeoIPv6File C:\\Users\\arian\\AppData\\Local\\Tor\\data\\geoip6

# Log to stdout
Log notice stdout
"""
        
        try:
            with open(config_path, 'w') as f:
                f.write(config_content)
            return config_path
        except Exception as e:
            print(f"Error creating config: {e}")
            return ""

    def start_tor_with_config(self, config_path: str) -> bool:
        """Start Tor with a specific config file."""
        try:
            tor_exe = self._find_tor_executable()
            if not tor_exe:
                print("Tor executable not found")
                return False
            
            # Kill existing Tor process
            self.stop_tor_service()
            time.sleep(1)
            
            # Start Tor with config
            if sys.platform == 'win32':
                subprocess.Popen(
                    [tor_exe, '-f', config_path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            else:
                subprocess.Popen(
                    [tor_exe, '-f', config_path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            
            # Wait for Tor to start
            time.sleep(3)
            return self.is_tor_running()
        except Exception as e:
            print(f"Error starting Tor with config: {e}")
            return False

    def _find_tor_executable(self) -> Optional[str]:
        """Find Tor executable path."""
        possible_paths = []
        
        if sys.platform == 'win32':
            # Common Windows locations
            possible_paths = [
                r"C:\Program Files\Tor\tor.exe",
                r"C:\Program Files (x86)\Tor\tor.exe",
                os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Tor', 'tor', 'tor.exe'),
                os.path.join(os.environ.get('APPDATA', ''), 'tor', 'tor.exe'),
            ]
        else:
            # Unix-like systems
            possible_paths = [
                '/usr/bin/tor',
                '/usr/local/bin/tor',
                '/opt/homebrew/bin/tor',
            ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        # Try which command
        try:
            result = subprocess.run(['which', 'tor'], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass
        
        return None

    def enable_control_port(self) -> bool:
        """Try to enable control port on running Tor."""
        # Check if we can connect to control port first
        try:
            from stem.control import Controller
            with Controller.from_port(port=self.control_port) as controller:
                controller.authenticate()
                # Already connected, port is available
                return True
        except Exception:
            pass
        
        # Try to restart Tor with config that enables control port
        config_path = self.create_config_with_control_port()
        if config_path:
            return self.start_tor_with_config(config_path)
        
        return False


# ==================== Module-level functions ====================

_service = None

def get_service(socks_port: int = None, control_port: int = None, http_port: int = None) -> TorService:
    """Get Tor service instance."""
    global _service
    if _service is None:
        _service = TorService(socks_port, control_port, http_port)
    return _service

def is_tor_running() -> bool:
    """Check if Tor is running."""
    return get_service().is_tor_running()

def get_session(proxy_type: str = 'socks5') -> Optional[requests.Session]:
    """Get Tor session."""
    return get_service().get_session(proxy_type)

def get_onion_session() -> Optional[requests.Session]:
    """Get session for .onion sites."""
    return get_service().get_onion_session()

def check_ip(session: requests.Session = None) -> Optional[str]:
    """Check IP through Tor."""
    return get_service().check_ip(session)

def ensure_tor_running() -> Dict[str, Any]:
    """Ensure Tor is running."""
    return get_service().ensure_tor_running()

def get_installation_instructions() -> str:
    """Get installation instructions."""
    return get_service().get_installation_instructions()

def create_config_with_control_port(config_path: str = None) -> str:
    """Create a Tor config file with control port enabled."""
    return get_service().create_config_with_control_port(config_path)

def start_tor_with_config(config_path: str) -> bool:
    """Start Tor with a specific config file."""
    return get_service().start_tor_with_config(config_path)

def enable_control_port() -> bool:
    """Try to enable control port on running Tor."""
    return get_service().enable_control_port()

def renew_tor_ip() -> bool:
    """Request a new Tor identity (new IP)."""
    return get_service().renew_tor_ip()

def get_tor_info() -> Dict[str, Any]:
    """Get detailed Tor connection information."""
    return get_service().get_tor_info()
