"""
Tor Network Module for Cerberus
Provides Tor connectivity and anonymous browsing capabilities
"""

import socket
import requests
import time
import sys
import os
import subprocess
import shutil
import zipfile
import urllib.request
from typing import Optional, Dict, Any

# Try to import stem for Tor control
try:
    from stem import Signal
    from stem.control import Controller
    STEM_AVAILABLE = True
except ImportError:
    STEM_AVAILABLE = False

# Import Tor service for advanced features
try:
    from cerberus.services.tor import renew_tor_ip as service_renew_tor_ip
    TOR_SERVICE_AVAILABLE = True
except ImportError:
    TOR_SERVICE_AVAILABLE = False

# Try to import Rich for premium UI
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
    from rich import box
    RICH_AVAILABLE = True
    console = Console(force_terminal=True, no_color=False)
except Exception:
    RICH_AVAILABLE = False
    console = None

# Tor check endpoints
TOR_CHECK_ENDPOINTS = [
    ("https://check.torproject.org/api/ip", "json"),
    ("https://api.ipify.org?format=json", "json"),
    ("https://ifconfig.me/ip", "text"),
]

# Default Tor proxy settings
TOR_SOCKS_PORT = 9050
TOR_CONTROL_PORT = 9051
TOR_PROXY = f"socks5h://127.0.0.1:{TOR_SOCKS_PORT}"
TOR_CONTROL_PASSWORD = ""


def is_admin() -> bool:
    """Check if running with admin privileges"""
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


def check_chocolatey() -> bool:
    """Check if Chocolatey is installed"""
    return shutil.which("choco") is not None


def install_tor_windows() -> bool:
    """Install Tor on Windows automatically"""
    print_info("Installing Tor...")
    
    # Check for chocolatey
    if check_chocolatey():
        print_info("Using Chocolatey to install Tor...")
        try:
            result = subprocess.run(
                ["choco", "install", "tor", "-y"],
                capture_output=True,
                text=True,
                timeout=300
            )
            return result.returncode == 0
        except Exception as e:
            print_error(f"Chocolatey install failed: {e}")
    
    # Try direct download
    print_info("Attempting direct Tor download...")
    tor_url = "https://www.torproject.org/dist/torbrowser/13.5.6/tor-expert-bundle-windows-x86_64-13.5.6.tar.gz"
    
    # For now, show clear instructions
    print_warning("Automatic Tor installation not available")
    return False


def start_tor_service() -> bool:
    """Try to start Tor service automatically"""
    # Try to start Tor Windows service
    try:
        result = subprocess.run(
            ["sc", "start", "Tor"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            return True
    except Exception:
        pass
    
    # Try to find and run tor.exe
    tor_paths = [
        r"C:\Program Files\Tor Browser\Tor\tor.exe",
        r"C:\Program Files (x86)\Tor Browser\Tor\tor.exe",
        os.path.expanduser(r"~\AppData\Local\Tor Browser\Tor\tor.exe"),
    ]
    
    for tor_path in tor_paths:
        if os.path.exists(tor_path):
            try:
                # Start tor in background
                subprocess.Popen(
                    [tor_path, "--defaults-torrc", r"C:\Program Files\Tor Browser\TorBrowser\Data\Tor\torrc"],
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                time.sleep(3)
                return True
            except Exception:
                pass
    
    return False


def ensure_tor_running() -> Dict[str, Any]:
    """Ensure Tor is installed and running, install if needed"""
    result = {
        "success": False,
        "message": "",
        "installed": False,
        "started": False,
    }
    
    # Check if already running
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    is_running = sock.connect_ex(('127.0.0.1', TOR_SOCKS_PORT)) == 0
    sock.close()
    
    if is_running:
        result["success"] = True
        result["started"] = True
        result["message"] = "Tor is already running"
        return result
    
    # Check if Tor is installed
    tor_installed = False
    tor_exe_path = None
    tor_paths = [
        r"C:\Program Files\Tor Browser\Tor\tor.exe",
        r"C:\Program Files (x86)\Tor Browser\Tor\tor.exe",
        os.path.expanduser(r"~\AppData\Local\Tor Browser\Tor\tor.exe"),
    ]
    
    for path in tor_paths:
        if os.path.exists(path):
            tor_installed = True
            tor_exe_path = path
            break
    
    if not tor_installed:
        # Check if Tor is in PATH
        tor_in_path = shutil.which("tor")
        if tor_in_path:
            tor_installed = True
            tor_exe_path = tor_in_path
    
    if tor_installed and tor_exe_path:
        result["installed"] = True
        
        # Check if already running properly
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        is_running = sock.connect_ex(('127.0.0.1', TOR_SOCKS_PORT)) == 0
        sock.close()
        
        if is_running:
            # Tor is running on port but may not be properly configured
            # Try to stop it and restart with proper config
            print_info("Tor already running, restarting with proper configuration...")
            try:
                subprocess.run(["taskkill", "/F", "/IM", "tor.exe"], 
                             capture_output=True, timeout=5)
                time.sleep(2)
            except Exception:
                pass
            is_running = False
        
        # Try to start Tor
        print_info("Starting Tor service...")
        
        # Try Windows service first
        started = False
        try:
            svc_result = subprocess.run(
                ["sc", "query", "Tor"],
                capture_output=True,
                text=True
            )
            if svc_result.returncode == 0 and "RUNNING" not in svc_result.stdout:
                subprocess.run(["sc", "start", "Tor"], capture_output=True, timeout=10)
                time.sleep(3)
        except Exception:
            pass
        
        # Try starting Tor Browser directly if service didn't work
        if tor_exe_path and "Tor Browser" in tor_exe_path:
            try:
                subprocess.Popen(
                    [tor_exe_path, "--defaults-torrc", r"C:\Program Files\Tor Browser\TorBrowser\Data\Tor\torrc"],
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                time.sleep(5)
            except Exception:
                pass
        
        # Check if started now
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        is_running = sock.connect_ex(('127.0.0.1', TOR_SOCKS_PORT)) == 0
        sock.close()
        
        if is_running:
            result["success"] = True
            result["started"] = True
            result["message"] = "Tor installed and started successfully!"
            return result
        else:
            result["message"] = "Tor installed but failed to start. Please start Tor manually."
            return result
    
    # Tor not installed - try to install
    print_info("Tor not found. Attempting installation...")
    
    # Check if we have choco
    choco_available = check_chocolatey()
    
    if not choco_available:
        print_info("Chocolatey not found. Attempting to install...")
        # Try to install Chocolatey
        try:
            subprocess.run(
                ['powershell', '-Command', 
                 'Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString(\'https://community.chocolatey.org/install.ps1\'))'],
                capture_output=True,
                timeout=180
            )
            choco_available = check_chocolatey()
        except Exception as e:
            print_warning(f"Could not install Chocolatey: {e}")
    
    # Try to install Tor via Chocolatey
    if choco_available:
        print_info("Installing Tor via Chocolatey...")
        try:
            install_result = subprocess.run(
                ["choco", "install", "tor", "-y", "--no-progress"],
                capture_output=True,
                text=True,
                timeout=300
            )
            if install_result.returncode == 0:
                tor_installed = True
                print_success("Tor installed via Chocolatey!")
        except Exception as e:
            print_warning(f"Chocolatey install failed: {e}")
    
    # If still not installed, try direct download
    if not tor_installed:
        print_info("Attempting direct Tor download...")
        try:
            import tarfile
            
            # Download Tor expert bundle (portable version) - use correct URL
            tor_tar_url = "https://dist.torproject.org/torbrowser/15.0.6/tor-expert-bundle-windows-x86_64-15.0.6.tar.gz"
            temp_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Temp")
            tar_path = os.path.join(temp_dir, "tor.tar.gz")
            extract_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Tor")
            
            os.makedirs(temp_dir, exist_ok=True)
            os.makedirs(extract_dir, exist_ok=True)
            
            print_info("Downloading Tor (this may take a minute)...")
            
            # Download with progress
            def report_progress(block_num, block_size, total_size):
                if total_size > 0:
                    percent = min(100, int(block_num * block_size * 100 / total_size))
                    if block_num % 100 == 0:
                        print_info(f"Downloaded {percent}%...")
            
            urllib.request.urlretrieve(tor_tar_url, tar_path, reporthook=report_progress)
            print_success("Download complete!")
            
            if os.path.exists(tar_path) and os.path.getsize(tar_path) > 1000:
                print_info("Extracting Tor...")
                
                with tarfile.open(tar_path, 'r:gz') as tar_ref:
                    tar_ref.extractall(extract_dir)
                
                # Find tor.exe in extracted files
                for root, dirs, files in os.walk(extract_dir):
                    for f in files:
                        if f.lower() == "tor.exe":
                            tor_exe_path = os.path.join(root, f)
                            tor_installed = True
                            print_success(f"Tor extracted to: {tor_exe_path}")
                            break
                    if tor_installed:
                        break
            else:
                print_warning("Downloaded file appears invalid")
        except Exception as e:
            print_warning(f"Direct download failed: {e}")
    
    # If Tor is now installed, try to start it
    if tor_installed and tor_exe_path:
        result["installed"] = True
        print_info("Starting Tor...")
        
        try:
            # Try to start as service first
            try:
                subprocess.run(["sc", "start", "Tor"], capture_output=True, timeout=10)
                time.sleep(3)
            except Exception:
                pass
            
            # Check if running
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            is_running = sock.connect_ex(('127.0.0.1', TOR_SOCKS_PORT)) == 0
            sock.close()
            
            if is_running:
                # Tor is running on port but may not be properly configured
                # Try to stop it and restart with proper config
                print_info("Tor already running, restarting with proper configuration...")
                try:
                    # Try to stop existing Tor process
                    subprocess.run(["taskkill", "/F", "/IM", "tor.exe"], 
                                 capture_output=True, timeout=5)
                    time.sleep(2)
                except Exception:
                    pass
                
                is_running = False
            
            if not is_running and tor_exe_path:
                # Create a minimal torrc config for the Expert Bundle
                tor_dir = os.path.dirname(tor_exe_path)
                torrc_path = os.path.join(tor_dir, "torrc")
                
                # Write minimal config
                torrc_content = """# Minimal Tor configuration for Cerberus
SocksPort 9050
ControlPort 9051
DataDirectory {}\\Data\\Tor
Log notice stdout
""".format(os.path.expanduser("~\\AppData\\Local\\Tor"))
                
                try:
                    with open(torrc_path, 'w') as f:
                        f.write(torrc_content)
                except Exception:
                    pass
                
                # Try to start tor.exe directly with config
                try:
                    subprocess.Popen(
                        [tor_exe_path, "-f", torrc_path],
                        creationflags=subprocess.CREATE_NO_WINDOW,
                        cwd=tor_dir
                    )
                    time.sleep(10)  # Give more time for bootstrapping
                except Exception as e:
                    print_warning(f"Failed to start tor: {e}")
            
            # Final check
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            is_running = sock.connect_ex(('127.0.0.1', TOR_SOCKS_PORT)) == 0
            sock.close()
            
            if is_running:
                result["success"] = True
                result["started"] = True
                result["message"] = "Tor installed and started successfully!"
                return result
        except Exception as e:
            print_warning(f"Failed to start Tor: {e}")
    
    result["message"] = "Tor not installed. Please install Tor Browser from torproject.org"
    return result


def get_installation_instructions() -> str:
    """Get platform-specific installation instructions"""
    instructions = """
╭───────────────────────────────────────────────────────────╮
│                    TOR INSTALLATION                       │
╰───────────────────────────────────────────────────────────╯

WINDOWS:
  Option 1: Install via Chocolatey (recommended)
    1. Open PowerShell as Administrator
    2. Run: Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    3. Run: choco install tor -y
    4. Run: sc start Tor

  Option 2: Manual Installation
    1. Download Tor Browser from: https://www.torproject.org/download
    2. Install and run Tor Browser
    3. Tor will be available on port 9050

MAC:
  Option 1: Homebrew
    brew install tor
    brew services start tor

  Option 2: MacPorts
    sudo port install tor
    sudo launchctl load /Library/LaunchDaemons/org.macports.tor.plist

LINUX:
  Debian/Ubuntu:
    sudo apt update
    sudo apt install tor
    
  Fedora/RHEL:
    sudo dnf install tor
    
  Then start: sudo systemctl start tor
"""
    return instructions


# UI Helper functions
def print_panel(title: str, content: str = None, style: str = "cyan"):
    """Print a content panel with Rich"""
    if RICH_AVAILABLE:
        safe_title = title.replace("[", "[[").replace("]", "]]")
        if content:
            console.print(Panel(
                content,
                title=f"[bold]{safe_title}[/bold]",
                border_style=style,
                box=box.ROUNDED,
                padding=(1, 2)
            ))
        else:
            console.print(Panel(
                f"[bold]{safe_title}[/bold]",
                border_style=style,
                box=box.ROUNDED,
                padding=(1, 2)
            ))
    else:
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}\n")


def print_success(msg: str):
    """Print success message"""
    if RICH_AVAILABLE:
        console.print(f"[bold green]✓[/bold green] [green]{msg}[/green]")
    else:
        print(f"✓ {msg}")


def print_error(msg: str):
    """Print error message"""
    if RICH_AVAILABLE:
        console.print(f"[bold red]✗[/bold red] [red]{msg}[/red]")
    else:
        print(f"✗ {msg}")


def print_warning(msg: str):
    """Print warning message"""
    if RICH_AVAILABLE:
        console.print(f"[bold yellow]⚠[/bold yellow] [yellow]{msg}[/yellow]")
    else:
        print(f"⚠ {msg}")


def print_info(msg: str):
    """Print info message"""
    if RICH_AVAILABLE:
        console.print(f"[bold blue]ℹ[/bold blue] [blue]{msg}[/blue]")
    else:
        print(f"ℹ {msg}")


def print_submenu(title: str, items: list, back: bool = True):
    """Print a submenu"""
    if RICH_AVAILABLE:
        table = Table(box=None, show_header=False, pad_edge=False)
        table.add_column(style="cyan", width=6)
        table.add_column(style="white")
        
        for num, name, desc in items:
            table.add_row(
                f"[bold cyan][{num}][/bold cyan]",
                f"[bold]{name}[/bold]  [dim]-[dim]  {desc}"
            )
        
        console.print(Panel(
            table,
            title=f"[bold cyan]{title}[/bold cyan]",
            border_style="cyan",
            box=box.ROUNDED,
            padding=(1, 2)
        ))
        
        if back:
            console.print("\n[dim]  [b] BACK    - Return to Main Menu[/dim]")
            console.print("[dim]  [q] QUIT    - Exit Cerberus[/dim]\n")
    else:
        print(f"\n{'─'*60}")
        print(f"  {title}")
        print(f"{'─'*60}\n")
        for num, name, desc in items:
            print(f"  [{num}] {name:20} - {desc}")
        if back:
            print("\n  [b] BACK    - Return to Main Menu")
            print("  [q] QUIT    - Exit Cerberus\n")


def get_input(prompt_text: str) -> str:
    """Get user input"""
    if RICH_AVAILABLE:
        from rich.prompt import Prompt
        return Prompt.ask(f"[bold cyan]{prompt_text}[/bold cyan]").strip()
    else:
        return input(f"\n{prompt_text}: ").strip()


def pause():
    """Pause for user input"""
    if RICH_AVAILABLE:
        console.print("\n[dim]Press Enter to continue...[/dim]")
        input()
    else:
        input("\nPress Enter to continue...")


class TorConnection:
    """Manages Tor network connection"""
    
    def __init__(self):
        self.connected = False
        self.current_ip = None
        self.proxy_dict = {
            "http": TOR_PROXY,
            "https": TOR_PROXY,
        }
        self.controller = None
    
    def is_tor_running(self) -> bool:
        """Check if Tor daemon is running"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        try:
            result = sock.connect_ex(('127.0.0.1', TOR_SOCKS_PORT))
            sock.close()
            return result == 0
        except Exception:
            return False
    
    def check_ip_through_tor(self) -> Optional[str]:
        """Check IP through Tor network"""
        try:
            session = requests.Session()
            session.proxies = self.proxy_dict
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            response = session.get("https://check.torproject.org/api/ip", timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data.get('IP', None)
        except Exception as e:
            pass
        
        # Fallback method
        try:
            session = requests.Session()
            session.proxies = self.proxy_dict
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            response = session.get("https://api.ipify.org?format=json", timeout=10)
            if response.status_code == 200:
                return response.json().get('ip')
        except Exception:
            pass
        
        return None
    
    def get_tor_info(self) -> Dict[str, Any]:
        """Get detailed Tor network information"""
        info = {
            "running": self.is_tor_running(),
            "ip": None,
            "country": None,
            "city": None,
            "isp": None,
            "tor_exit": False,
        }
        
        if not info["running"]:
            return info
        
        # Check if IP goes through Tor
        try:
            session = requests.Session()
            session.proxies = self.proxy_dict
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            # Check Tor project API
            response = session.get("https://check.torproject.org/api/ip", timeout=10)
            if response.status_code == 200:
                data = response.json()
                info["ip"] = data.get('IP')
                info["tor_exit"] = data.get('IsTor', False)
            
            # Get location info
            if info["ip"]:
                geo_response = session.get(f"http://ip-api.com/json/{info['ip']}", timeout=10)
                if geo_response.status_code == 200:
                    geo_data = geo_response.json()
                    info["country"] = geo_data.get('country')
                    info["city"] = geo_data.get('city')
                    info["isp"] = geo_data.get('isp')
                    
        except Exception:
            pass
        
        return info
    
    def renew_tor_ip(self) -> bool:
        """Renew Tor IP (get new identity)"""
        if not STEM_AVAILABLE:
            return False
            
        try:
            if self.controller is None:
                self.controller = Controller.from_port(port=TOR_CONTROL_PORT)
            
            if self.controller.is_authenticated():
                self.controller.signal(Signal.NEWNYM)
                time.sleep(2)  # Wait for new circuit
                return True
        except Exception:
            pass
        
        return False
    
    def connect(self) -> Dict[str, Any]:
        """Connect to Tor network and get status"""
        result = {
            "success": False,
            "message": "",
            "ip": None,
            "running": False,
        }
        
        # Check if Tor is running
        result["running"] = self.is_tor_running()
        
        if not result["running"]:
            result["message"] = "Tor is not running. Please start Tor daemon."
            return result
        
        # Get IP through Tor
        ip = self.check_ip_through_tor()
        
        if ip:
            result["success"] = True
            result["ip"] = ip
            result["message"] = f"Connected to Tor network. IP: {ip}"
            self.connected = True
            self.current_ip = ip
        else:
            result["message"] = "Tor is running but couldn't verify connection"
        
        return result
    
    def disconnect(self) -> bool:
        """Disconnect from Tor (stops using Tor proxy)"""
        self.connected = False
        self.current_ip = None
        return True
    
    def get_session(self) -> requests.Session:
        """Get a requests session configured for Tor"""
        session = requests.Session()
        session.proxies = self.proxy_dict
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        return session


# Global Tor connection instance
tor_connection = TorConnection()


def module_tor():
    """Tor network module main function"""
    
    # Use local UI functions (defined at top of module)
    while True:
        # Clear console for dynamic refresh
        if RICH_AVAILABLE:
            console.clear()
        
        print_panel("TOR NETWORK", style="purple")
        
        # Show current status
        status = tor_connection.get_tor_info()
        
        # Display status using Rich if available
        if RICH_AVAILABLE:
            from rich.table import Table
            
            status_table = Table(box=None, show_header=False, pad_edge=False)
            status_table.add_column(style="cyan", width=20)
            status_table.add_column(style="white")
            
            status_table.add_row("Tor Daemon", "✓ Running" if status["running"] else "✗ Not Running")
            status_table.add_row("Current IP", status["ip"] or "Not connected")
            status_table.add_row("Exit Node", "✓ Yes" if status.get("tor_exit") else "✗ No")
            if status.get("country"):
                status_table.add_row("Location", f"{status['city']}, {status['country']}")
            if status.get("isp"):
                status_table.add_row("ISP", status['isp'])
            
            console.print(status_table)
        else:
            print(f"\n  Tor Daemon:     {'Running' if status['running'] else 'Not Running'}")
            print(f"  Current IP:     {status['ip'] or 'Not connected'}")
            print(f"  Exit Node:      {'Yes' if status.get('tor_exit') else 'No'}")
            if status.get("country"):
                print(f"  Location:       {status['city']}, {status['country']}")
            if status.get("isp"):
                print(f"  ISP:            {status['isp']}")
        
        print()
        
        # Premium menu items with icons
        items = [
            ("1", "⚡ Connect / Auto-Install", "Connect to Tor or install if needed"),
            ("2", "◎ Check Status", "Verify Tor connection"),
            ("3", "⟳ New Identity", "Get new Tor IP (renew)"),
            ("4", "◉ Details", "Show detailed connection info"),
            ("5", "⬡ Test Proxy", "Test Tor proxy with request"),
            ("6", "⬢ Install Tor", "Install Tor on this system"),
            ("7", "⚙ Enable Control Port", "Enable control port for New Identity"),
        ]
        
        print_submenu("Tor Options", items, back=False)
        
        choice = get_input("Select")
        
        if choice == "1":
            # Try to connect, auto-install if not running
            print("\nConnecting to Tor network...")
            result = tor_connection.connect()
            
            if not result["running"]:
                print_warning("Tor not running. Attempting auto-install...")
                install_result = ensure_tor_running()
                
                if install_result["success"]:
                    print_success(install_result["message"])
                    # Try to connect again
                    result = tor_connection.connect()
                else:
                    print_error(install_result["message"])
                    print()
                    print_info("Displaying installation instructions...")
                    print(get_installation_instructions())
            
            if result["success"]:
                print_success(result["message"])
            else:
                print_error(result["message"])
            
            pause()
            
        elif choice == "2":
            print("\nChecking Tor connection...")
            ip = tor_connection.check_ip_through_tor()
            if ip:
                print_success(f"Tor connection active! IP: {ip}")
            else:
                print_error("Not connected through Tor")
            pause()
            
        elif choice == "3":
            # Try service first, then stem library
            if TOR_SERVICE_AVAILABLE:
                print("\nRequesting new Tor identity...")
                if service_renew_tor_ip():
                    print_success("New Tor identity obtained!")
                    time.sleep(1)
                    new_ip = tor_connection.check_ip_through_tor()
                    if new_ip:
                        print(f"New IP: {new_ip}")
                else:
                    print_error("Failed to renew Tor identity")
                    print_warning("Tor control port is not enabled")
                    print()
                    print_info("Go to option 7 to enable the control port")
            elif not STEM_AVAILABLE:
                print_error("Stem library required for this feature")
                print("Install with: pip install stem")
            else:
                print("\nRequesting new Tor identity...")
                if tor_connection.renew_tor_ip():
                    print_success("New Tor identity obtained!")
                    time.sleep(1)
                    new_ip = tor_connection.check_ip_through_tor()
                    if new_ip:
                        print(f"New IP: {new_ip}")
                else:
                    print_error("Failed to renew Tor identity")
                    print_warning("Tor control port is not enabled")
                    print()
                    print_info("Go to option 7 to enable the control port")
            pause()
            
        elif choice == "4":
            print("\nFetching detailed Tor information...")
            info = tor_connection.get_tor_info()
            
            if RICH_AVAILABLE:
                from rich.table import Table
                
                details = Table(title="Tor Connection Details", box=None)
                details.add_column("Property", style="cyan")
                details.add_column("Value")
                
                details.add_row("Status", "Connected" if info["running"] else "Disconnected")
                details.add_row("IP Address", info["ip"] or "N/A")
                details.add_row("Tor Exit Node", "Yes" if info.get("tor_exit") else "No")
                details.add_row("Country", info.get("country") or "N/A")
                details.add_row("City", info.get("city") or "N/A")
                details.add_row("ISP", info.get("isp") or "N/A")
                details.add_row("SOCKS Port", str(TOR_SOCKS_PORT))
                details.add_row("Control Port", str(TOR_CONTROL_PORT))
                
                console.print(details)
            else:
                print("\n=== Tor Connection Details ===")
                print(f"  Status:         {'Connected' if info['running'] else 'Disconnected'}")
                print(f"  IP Address:     {info['ip'] or 'N/A'}")
                print(f"  Tor Exit Node:  {'Yes' if info.get('tor_exit') else 'No'}")
                print(f"  Country:        {info.get('country') or 'N/A'}")
                print(f"  City:           {info.get('city') or 'N/A'}")
                print(f"  ISP:            {info.get('isp') or 'N/A'}")
                print(f"  SOCKS Port:     {TOR_SOCKS_PORT}")
                print(f"  Control Port:   {TOR_CONTROL_PORT}")
            
            pause()
            
        elif choice == "5":
            print("\nTesting Tor proxy...")
            try:
                session = tor_connection.get_session()
                response = session.get("https://httpbin.org/ip", timeout=15)
                if response.status_code == 200:
                    print_success("Proxy test successful!")
                    print(f"Response: {response.json()}")
                else:
                    print_error(f"Proxy test failed: {response.status_code}")
            except Exception as e:
                print_error(f"Proxy test failed: {str(e)}")
            pause()
            
        elif choice == "6":
            print("\nInstalling Tor...")
            result = ensure_tor_running()
            
            if result["success"]:
                print_success(result["message"])
                print()
                print_info("Attempting to connect to Tor network...")
                connect_result = tor_connection.connect()
                if connect_result["success"]:
                    print_success(connect_result["message"])
                else:
                    print_warning(connect_result["message"])
            else:
                print_error(result["message"])
                print()
                print_info("Installation instructions:")
                print(get_installation_instructions())
            
            pause()
            
        elif choice == "7":
            print("\nEnabling Tor control port...")
            print_info("This will create a config with ControlPort enabled and restart Tor...")
            
            from cerberus.services.tor import enable_control_port, create_config_with_control_port
            
            # Try to enable control port
            if enable_control_port():
                print_success("Control port enabled! Tor has been restarted.")
                print_info("You can now use 'New Identity' feature.")
            else:
                # Try to create config and guide user
                config_path = create_config_with_control_port()
                if config_path:
                    print_warning(f"Config created at: {config_path}")
                    print()
                    print_info("To enable control port:")
                    print("  1. Stop Tor (close Tor Browser or tor service)")
                    print(f"  2. Start Tor with: tor -f \"{config_path}\"")
                    print("  3. Or add the following to your torrc:")
                    print("     ControlPort 9051")
                    print("     CookieAuthentication 1")
                else:
                    print_error("Failed to create config file")
            
            pause()
            
        elif choice.lower() == "b" or choice.lower() == "back":
            break
            
        elif choice.lower() == "q" or choice.lower() == "quit":
            sys.exit(0)
            
        else:
            print_error("Invalid selection")
            time.sleep(0.5)


# Utility function to get Tor-ready session
def get_tor_session() -> Optional[requests.Session]:
    """Get a requests session configured for Tor network"""
    if tor_connection.is_tor_running():
        return tor_connection.get_session()
    return None


if __name__ == "__main__":
    # Test module when run directly
    module_tor()
