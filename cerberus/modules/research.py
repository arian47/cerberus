#!/usr/bin/env python3
"""
Cerberus Security Tools Research Module
Researches and integrates new pentesting/Kali Linux tools
"""

import os
import json
import subprocess
import requests
from datetime import datetime
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
RESEARCH_DIR = BASE_DIR / "research_data"
TOOLS_DB = RESEARCH_DIR / "tools.json"

class SecurityToolsResearcher:
    """Research new security tools and update Cerberus"""
    
    def __init__(self):
        RESEARCH_DIR.mkdir(exist_ok=True)
        self.tools = self._load_tools()
    
    def _load_tools(self):
        """Load existing tools database"""
        if TOOLS_DB.exists():
            with open(TOOLS_DB, 'r') as f:
                return json.load(f)
        return {"tools": [], "last_updated": None}
    
    def _save_tools(self):
        """Save tools database"""
        self.tools["last_updated"] = datetime.now().isoformat()
        with open(TOOLS_DB, 'w') as f:
            json.dump(self.tools, f, indent=2)
    
    def get_kali_tools(self):
        """Get list of Kali Linux tools"""
        # Common Kali Linux tools by category
       kali_tools = {
            "Information Gathering": [
                {"name": "nmap", "desc": "Network scanner", "category": "recon"},
                {"name": "masscan", "desc": "Fast TCP scanner", "category": "recon"},
                {"name": "netdiscover", "desc": "ARP scanner", "category": "recon"},
                {"name": " Recon-ng", "desc": "Web reconnaissance", "category": "recon"},
                {"name": "theHarvester", "desc": "Email/subdomain harvester", "category": "recon"},
            ],
            "Vulnerability Analysis": [
                {"name": "nikto", "desc": "Web server scanner", "category": "vuln"},
                {"name": "nmap scripts", "desc": "NSE scripts", "category": "vuln"},
                {"name": "openvas", "desc": "Vulnerability scanner", "category": "vuln"},
                {"name": "nessus", "desc": "Commercial scanner", "category": "vuln"},
            ],
            "Exploitation Tools": [
                {"name": "metasploit", "desc": "Exploitation framework", "category": "exploit"},
                {"name": "searchsploit", "desc": "Exploit database", "category": "exploit"},
                {"name": "sqlmap", "desc": "SQL injection tool", "category": "exploit"},
                {"name": "hydra", "desc": "Password brute force", "category": "exploit"},
            ],
            "Wireless Attacks": [
                {"name": "aircrack-ng", "desc": "WiFi cracker", "category": "wireless"},
                {"name": "reaver", "desc": "WPS cracker", "category": "wireless"},
                {"name": "wifite", "desc": "Wireless auditor", "category": "wireless"},
            ],
            "Password Attacks": [
                {"name": "john", "desc": "John the Ripper", "category": "password"},
                {"name": "hashcat", "desc": "GPU password cracker", "category": "password"},
                {"name": "cewl", "desc": "Wordlist generator", "category": "password"},
                {"name": "crunch", "desc": "Wordlist generator", "category": "password"},
            ],
            "Reverse Engineering": [
                {"name": "ghidra", "desc": "SRE framework", "category": "re"},
                {"name": "radare2", "desc": "Binary analysis", "category": "re"},
                {"name": "objdump", "desc": "Disassembler", "category": "re"},
            ],
            "Web Applications": [
                {"name": "burpSuite", "desc": "Web proxy", "category": "web"},
                {"name": "zap", "desc": "OWASP ZAP", "category": "web"},
                {"name": "dirb", "desc": "Directory scanner", "category": "web"},
                {"name": "gobuster", "desc": "Directory/Subdomain", "category": "web"},
            ],
            "Forensics": [
                {"name": "autopsy", "desc": " forensics", "category": "forensics"},
                {"name": "volatility", "desc": "Memory forensics", "category": "forensics"},
                {"name": "binwalk", "desc": "Binary analysis", "category": "forensics"},
            ],
        }
        return kali_tools
    
    def check_tool_installed(self, tool_name):
        """Check if a tool is installed"""
        result = subprocess.run(
            ["which", tool_name.strip()],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    
    def scan_local_tools(self):
        """Scan for available security tools on system"""
        available = []
        all_tools = []
        
        for category, tools in self.get_kali_tools().items():
            for tool in tools:
                all_tools.append(tool)
                if self.check_tool_installed(tool["name"]):
                    tool["installed"] = True
                    available.append(tool)
                else:
                    tool["installed"] = False
        
        return {
            "available": available,
            "all_tools": all_tools,
            "total_available": len(available),
            "total_tools": len(all_tools)
        }
    
    def generate_tool_integration(self):
        """Generate tool integration code for Cerberus"""
        tools = self.scan_local_tools()
        
        # Generate module code
        module_code = '''"""
Auto-generated security tools integration
Generated: {timestamp}
"""
from .connectors import BaseConnector

TOOLS_AVAILABLE = {tools}

TOOL_COMMANDS = {commands}
'''.format(
            timestamp=datetime.now().isoformat(),
            tools=json.dumps([t["name"] for t in tools["available"]], indent=4),
            commands=json.dumps({t["name"]: t.get("desc", "") for t in tools["all_tools"]}, indent=4)
        )
        
        return module_code
    
    def run_research(self):
        """Run full research cycle"""
        print("=== Cerberus Security Tools Research ===")
        print(f"Time: {datetime.now().isoformat()}\n")
        
        # Scan local tools
        tools = self.scan_local_tools()
        print(f"Found {tools['total_available']}/{tools['total_tools']} tools installed")
        
        # Update database
        self.tools["tools"] = tools
        self._save_tools()
        
        print("\nAvailable tools:")
        for tool in tools["available"]:
            print(f"  ✓ {tool['name']} - {tool['desc']}")
        
        print("\nMissing tools:")
        missing = [t for t in tools["all_tools"] if not t.get("installed")]
        for tool in missing[:10]:  # Show first 10
            print(f"  ✗ {tool['name']}")
        
        print(f"\n=== Research Complete ===")
        return tools

def main():
    """Main entry point"""
    researcher = SecurityToolsResearcher()
    researcher.run_research()

if __name__ == "__main__":
    main()
