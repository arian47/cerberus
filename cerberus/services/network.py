"""
Cerberus Network Scanner Service

Microservice for network scanning and reconnaissance.
"""

import socket
import concurrent.futures
from typing import List, Dict, Optional, Tuple
import struct
import random


class NetworkScannerService:
    """
    Service for network scanning and reconnaissance operations.
    """
    
    def __init__(self):
        """Initialize network scanner service."""
        self.common_ports = {
            21: "FTP",
            22: "SSH",
            23: "Telnet",
            25: "SMTP",
            53: "DNS",
            80: "HTTP",
            110: "POP3",
            143: "IMAP",
            443: "HTTPS",
            445: "SMB",
            993: "IMAPS",
            995: "POP3S",
            3306: "MySQL",
            3389: "RDP",
            5432: "PostgreSQL",
            5900: "VNC",
            8080: "HTTP-Proxy",
            8443: "HTTPS-Alt",
        }
    
    # ==================== Port Scanning ====================
    
    def scan_port(self, host: str, port: int, timeout: float = 2.0) -> bool:
        """
        Scan a single port on a host.
        
        Args:
            host: Target host IP or hostname
            port: Port number to scan
            timeout: Connection timeout
            
        Returns:
            True if port is open
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except Exception:
            return False
    
    def scan_ports(self, host: str, ports: List[int], 
                   timeout: float = 2.0, max_workers: int = 50) -> Dict[int, bool]:
        """
        Scan multiple ports on a host.
        
        Args:
            host: Target host
            ports: List of ports to scan
            timeout: Connection timeout
            max_workers: Max concurrent connections
            
        Returns:
            Dict mapping port to open status
        """
        results = {}
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_port = {
                executor.submit(self.scan_port, host, port, timeout): port 
                for port in ports
            }
            
            for future in concurrent.futures.as_completed(future_to_port):
                port = future_to_port[future]
                try:
                    results[port] = future.result()
                except Exception:
                    results[port] = False
        
        return results
    
    def scan_common_ports(self, host: str, timeout: float = 2.0) -> Dict[int, str]:
        """
        Scan common ports on a host.
        
        Args:
            host: Target host
            timeout: Connection timeout
            
        Returns:
            Dict of open ports to service names
        """
        port_list = list(self.common_ports.keys())
        results = self.scan_ports(host, port_list, timeout)
        
        return {
            port: self.common_ports[port] 
            for port, is_open in results.items() 
            if is_open
        }
    
    def scan_port_range(self, host: str, start_port: int, end_port: int,
                        timeout: float = 1.0, max_workers: int = 100) -> List[int]:
        """
        Scan a range of ports.
        
        Args:
            host: Target host
            start_port: Start port
            end_port: End port
            timeout: Connection timeout
            max_workers: Max concurrent connections
            
        Returns:
            List of open ports
        """
        ports = list(range(start_port, end_port + 1))
        results = self.scan_ports(host, ports, timeout, max_workers)
        
        return [port for port, is_open in results.items() if is_open]
    
    # ==================== Host Discovery ====================
    
    def ping_host(self, host: str, timeout: float = 3.0) -> bool:
        """
        Check if a host is reachable (ICMP ping).
        
        Args:
            host: Target host
            timeout: Timeout in seconds
            
        Returns:
            True if host is reachable
        """
        try:
            # Try ICMP ping
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            sock.settimeout(timeout)
            
            # Build ICMP packet
            packet_id = random.randint(1, 65535)
            seq = 1
            checksum = 0
            
            header = struct.pack('!BBHHH', 8, 0, checksum, packet_id, seq)
            data = b'Cerberus Ping'
            checksum = self._icmp_checksum(header + data)
            header = struct.pack('!BBHHH', 8, 0, checksum, packet_id, seq)
            
            sock.sendto(header + data, (host, 0))
            
            while True:
                rec_packet, addr = sock.recvfrom(1024)
                icmp_header = rec_packet[20:28]
                _, _, _, recv_id, _ = struct.unpack('!BBHHH', icmp_header)
                
                if recv_id == packet_id:
                    sock.close()
                    return True
                
        except Exception:
            pass
        
        # Fallback: try connecting to common ports
        for port in [80, 443, 22]:
            if self.scan_port(host, port, timeout=2.0):
                return True
        
        return False
    
    def _icmp_checksum(self, data: str) -> int:
        """Calculate ICMP checksum."""
        if len(data) % 2:
            data += b'\x00'
        
        checksum = 0
        for i in range(0, len(data), 2):
            word = (data[i] << 8) + data[i + 1]
            checksum += word
        
        checksum = (checksum >> 16) + (checksum & 0xffff)
        checksum += checksum >> 16
        return ~checksum & 0xffff
    
    def scan_network(self, subnet: str, timeout: float = 2.0) -> List[str]:
        """
        Scan a network subnet for live hosts.
        
        Args:
            subnet: Subnet in CIDR notation (e.g., "192.168.1.0/24")
            timeout: Timeout per host
            
        Returns:
            List of live hosts
        """
        # Parse subnet
        parts = subnet.split('/')
        if len(parts) != 2:
            return []
        
        base_ip = parts[0]
        prefix = int(parts[1])
        
        # Calculate network range
        ip_parts = base_ip.split('.')
        if len(ip_parts) != 4:
            return []
        
        base = int(ip_parts[0]) << 24 | int(ip_parts[1]) << 16 | int(ip_parts[2]) << 8 | int(ip_parts[3])
        mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
        
        network = base & mask
        broadcast = network | (~mask & 0xFFFFFFFF)
        
        hosts = []
        for ip in range(network + 1, broadcast):
            host = socket.inet_ntoa(struct.pack('!I', ip))
            if self.ping_host(host, timeout):
                hosts.append(host)
        
        return hosts
    
    # ==================== Service Detection ====================
    
    def detect_service(self, host: str, port: int) -> Optional[str]:
        """
        Detect service running on a port.
        
        Args:
            host: Target host
            port: Port number
            
        Returns:
            Service name or None
        """
        if port in self.common_ports:
            return self.common_ports[port]
        
        # Try banner grabbing
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3.0)
            sock.connect((host, port))
            
            # Send HTTP request on common web ports
            if port in [80, 8080, 443, 8443]:
                sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
            
            banner = sock.recv(1024).decode('utf-8', errors='ignore')
            sock.close()
            
            if banner:
                # Extract server header
                for line in banner.split('\n'):
                    if 'Server:' in line:
                        return line.split(':', 1)[1].strip()
                
                return banner[:50].strip()
                
        except Exception:
            pass
        
        return None
    
    def get_banner(self, host: str, port: int, timeout: float = 5.0) -> Optional[str]:
        """
        Grab banner from a service.
        
        Args:
            host: Target host
            port: Port number
            timeout: Connection timeout
            
        Returns:
            Banner string or None
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((host, port))
            
            # Try to receive banner
            banner = sock.recv(1024).decode('utf-8', errors='ignore')
            sock.close()
            
            return banner.strip() if banner else None
            
        except Exception:
            return None
    
    # ==================== DNS Operations ====================
    
    def reverse_dns(self, ip: str) -> Optional[str]:
        """
        Perform reverse DNS lookup.
        
        Args:
            ip: IP address
            
        Returns:
            Hostname or None
        """
        try:
            return socket.gethostbyaddr(ip)[0]
        except Exception:
            return None
    
    def dns_lookup(self, hostname: str) -> Optional[str]:
        """
        Perform DNS lookup.
        
        Args:
            hostname: Hostname to resolve
            
        Returns:
            IP address or None
        """
        try:
            return socket.gethostbyname(hostname)
        except Exception:
            return None
    
    def get_all_dns_records(self, hostname: str) -> Dict[str, List[str]]:
        """
        Get all DNS records for a hostname.
        
        Args:
            hostname: Hostname
            
        Returns:
            Dict of record types to values
        """
        import dns.resolver
        
        records = {}
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']
        
        for rtype in record_types:
            try:
                answers = dns.resolver.resolve(hostname, rtype)
                records[rtype] = [str(rdata) for rdata in answers]
            except Exception:
                pass
        
        return records
    
    # ==================== Network Info ====================
    
    def get_local_ip(self) -> str:
        """Get local IP address."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"
    
    def get_hostname(self) -> str:
        """Get local hostname."""
        return socket.gethostname()
    
    def get_fqdn(self) -> str:
        """Get fully qualified domain name."""
        return socket.getfqdn()


# ==================== Module-level functions ====================

_service = None

def get_service() -> NetworkScannerService:
    """Get network scanner service instance."""
    global _service
    if _service is None:
        _service = NetworkScannerService()
    return _service

def scan_port(host: str, port: int, timeout: float = 2.0) -> bool:
    """Scan a single port."""
    return get_service().scan_port(host, port, timeout)

def scan_ports(host: str, ports: List[int], timeout: float = 2.0) -> Dict[int, bool]:
    """Scan multiple ports."""
    return get_service().scan_ports(host, ports, timeout)

def scan_common_ports(host: str, timeout: float = 2.0) -> Dict[int, str]:
    """Scan common ports."""
    return get_service().scan_common_ports(host, timeout)

def scan_port_range(host: str, start_port: int, end_port: int) -> List[int]:
    """Scan port range."""
    return get_service().scan_port_range(host, start_port, end_port)

def ping_host(host: str, timeout: float = 3.0) -> bool:
    """Ping a host."""
    return get_service().ping_host(host, timeout)

def scan_network(subnet: str, timeout: float = 2.0) -> List[str]:
    """Scan network for live hosts."""
    return get_service().scan_network(subnet, timeout)

def detect_service(host: str, port: int) -> Optional[str]:
    """Detect service on port."""
    return get_service().detect_service(host, port)

def get_banner(host: str, port: int) -> Optional[str]:
    """Get service banner."""
    return get_service().get_banner(host, port)

def reverse_dns(ip: str) -> Optional[str]:
    """Reverse DNS lookup."""
    return get_service().reverse_dns(ip)

def dns_lookup(hostname: str) -> Optional[str]:
    """DNS lookup."""
    return get_service().dns_lookup(hostname)

def get_local_ip() -> str:
    """Get local IP."""
    return get_service().get_local_ip()

def get_hostname() -> str:
    """Get local hostname."""
    return get_service().get_hostname()
