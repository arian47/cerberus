#!/usr/bin/env python3
"""
Cerberus Network Scanner Module
Cross-platform network scanning capabilities
"""

import subprocess
import socket
import argparse
import concurrent.futures
from datetime import datetime
from pathlib import Path

# Try importing optional dependencies
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


class NetworkScanner:
    """Cross-platform network scanner"""
    
    def __init__(self):
        self.results = []
    
    def check_tool(self, tool_name):
        """Check if tool is installed"""
        try:
            result = subprocess.run(
                ["which", tool_name],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except:
            return False
    
    def nmap_scan(self, target, ports="1-1000", flags=""):
        """Run nmap scan"""
        if not self.check_tool("nmap"):
            return {"error": "nmap not installed"}
        
        cmd = ["nmap"]
        if flags:
            cmd.extend(flags.split())
        cmd.extend(["-p", ports, target])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            return {
                "tool": "nmap",
                "target": target,
                "ports": ports,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None
            }
        except Exception as e:
            return {"error": str(e)}
    
    def masscan_scan(self, target, ports="1-10000", rate="10000"):
        """Run masscan scan"""
        if not self.check_tool("masscan"):
            return {"error": "masscan not installed"}
        
        cmd = ["masscan", "-p", ports, "--rate", rate, target]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            return {
                "tool": "masscan",
                "target": target,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None
            }
        except Exception as e:
            return {"error": str(e)}
    
    def port_scan(self, target, ports=None, timeout=1):
        """Pure Python port scanner (no external tools needed)"""
        if ports is None:
            ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 993, 995, 3306, 3389, 5432, 8080, 8443]
        
        results = {
            "target": target,
            "open_ports": [],
            "timestamp": datetime.now().isoformat()
        }
        
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            try:
                result = sock.connect_ex((target, port))
                if result == 0:
                    results["open_ports"].append({
                        "port": port,
                        "service": self._get_service(port)
                    })
            except:
                pass
            finally:
                sock.close()
        
        return results
    
    def _get_service(self, port):
        """Get common service name for port"""
        services = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
            53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
            443: "HTTPS", 445: "SMB", 993: "IMAPS", 995: "POP3S",
            3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
            8080: "HTTP-Alt", 8443: "HTTPS-Alt"
        }
        return services.get(port, "Unknown")
    
    def subdomain_enum(self, domain, wordlist=None):
        """Enumerate subdomains (requires external tools)"""
        results = {"domain": domain, "subdomains": []}
        
        # Check for subfinder
        if self.check_tool("subfinder"):
            try:
                result = subprocess.run(
                    ["subfinder", "-d", domain, "-silent"],
                    capture_output=True, text=True, timeout=60
                )
                results["subdomains"] = result.stdout.strip().split("\n")
            except:
                pass
        
        # Check for amass
        if self.check_tool("amass") and not results["subdomains"]:
            try:
                result = subprocess.run(
                    ["amass", "enum", "-d", domain],
                    capture_output=True, text=True, timeout=120
                )
                results["subdomains"] = result.stdout.strip().split("\n")
            except:
                pass
        
        return results
    
    def reverse_dns(self, ip_range):
        """Reverse DNS lookup"""
        # Simple implementation
        results = []
        try:
            hostname = socket.gethostbyaddr(ip_range)
            results.append({"ip": ip_range, "hostname": hostname[0]})
        except:
            pass
        return results
    
    def whois(self, domain):
        """Whois lookup"""
        if not REQUESTS_AVAILABLE:
            return {"error": "requests library not available"}
        
        try:
            # Simple whois via API
            import json
            resp = requests.get(f"https://whois.freeaiapi.xyz/api?domain={domain}", timeout=10)
            if resp.status_code == 200:
                return resp.json()
        except Exception as e:
            return {"error": str(e)}
        
        return {"error": "Whois lookup failed"}


def main():
    """CLI Entry Point"""
    parser = argparse.ArgumentParser(description="Cerberus Network Scanner")
    parser.add_argument("target", help="Target IP or domain")
    parser.add_argument("--scan", choices=["nmap", "masscan", "basic"], default="basic",
                       help="Scan type")
    parser.add_argument("--ports", type=str, default="1-1000",
                       help="Port range (e.g., 1-1000, 80,443)")
    parser.add_argument("--subdomains", action="store_true",
                       help="Enumerate subdomains")
    parser.add_argument("--whois", action="store_true",
                       help="Whois lookup")
    parser.add_argument("--rate", type=str, default="10000",
                       help="Masscan rate")
    
    args = parser.parse_args()
    
    scanner = NetworkScanner()
    
    print(f"=== Cerberus Network Scanner ===")
    print(f"Target: {args.target}")
    print(f"Scan: {args.scan}\n")
    
    if args.scan == "nmap":
        result = scanner.nmap_scan(args.target, args.ports)
        print(result.get("output", result.get("error", "N/A")))
    
    elif args.scan == "masscan":
        result = scanner.masscan_scan(args.target, args.ports, args.rate)
        print(result.get("output", result.get("error", "N/A")))
    
    else:  # basic
        result = scanner.port_scan(args.target)
        print(f"Open ports found: {len(result['open_ports'])}")
        for port in result["open_ports"]:
            print(f"  ✓ {port['port']} ({port['service']})")
    
    if args.subdomains:
        print("\n--- Subdomain Enumeration ---")
        subs = scanner.subdomain_enum(args.target)
        print(f"Found {len(subs['subdomains'])} subdomains")
        for s in subs["subdomains"][:10]:
            print(f"  • {s}")
    
    if args.whois:
        print("\n--- Whois ---")
        whois = scanner.whois(args.target)
        print(whois)


if __name__ == "__main__":
    main()
