#!/usr/bin/env python3
"""
Cerberus Security Tools Research Module - CROSS-PLATFORM
Works via CLI on any platform (Linux, macOS, Windows)
"""

import os
import sys
import json
import subprocess
import argparse
from datetime import datetime
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"
TOOLS_DB = DATA_DIR / "security_tools.json"

# Cross-platform security tools database
SECURITY_TOOLS = {
    # === EXISTING CATEGORIES ===
    "Information Gathering": {
        "nmap": {
            "desc": "Network scanner - discovers hosts/services",
            "install": "apt install nmap / brew install nmap / choco install nmap",
            "usage": "nmap -sV -sC target.com",
            "category": "recon"
        },
        "masscan": {
            "desc": "Fast TCP port scanner",
            "install": "apt install masscan / brew install masscan",
            "usage": "masscan -p1-65535 target.com --rate=10000",
            "category": "recon"
        },
        "netdiscover": {
            "desc": "ARP-based network discovery",
            "install": "apt install netdiscover",
            "usage": "netdiscover -r 192.168.1.0/24",
            "category": "recon"
        },
        "theHarvester": {
            "desc": "Email/subdomain harvester",
            "install": "pip install theHarvester",
            "usage": "theHarvester -d target.com -b all",
            "category": "recon"
        },
        "subfinder": {
            "desc": "Passive subdomain enumeration",
            "install": "go install -v github.com/projectdiscovery/subfinder/v2/...@latest",
            "usage": "subfinder -d target.com",
            "category": "recon"
        },
        "amass": {
            "desc": "Network mapping of attack surfaces",
            "install": "go install -v github.com/OWASP/Amass/v3/...@latest",
            "usage": "amass enum -d target.com",
            "category": "recon"
        },
        "knock": {
            "desc": "Port knock scanner",
            "install": "apt install knock",
            "usage": "knock target.com 1000 2000 3000",
            "category": "recon"
        },
        "zenmap": {
            "desc": "Nmap GUI",
            "install": "apt install zenmap",
            "usage": "zenmap target.com",
            "category": "recon"
        },
    },
    "Vulnerability Analysis": {
        "nikto": {
            "desc": "Web server vulnerability scanner",
            "install": "apt install nikto / brew install nikto",
            "usage": "nikto -h target.com",
            "category": "vuln"
        },
        "nuclei": {
            "desc": "Template-based vulnerability scanner",
            "install": "go install -v github.com/projectdiscovery/nuclei/v3/...@latest",
            "usage": "nuclei -u target.com",
            "category": "vuln"
        },
        "openvas": {
            "desc": "Full vulnerability scanner",
            "install": "apt install openvas",
            "usage": "openvas-start",
            "category": "vuln"
        },
    },
    "Exploitation": {
        "metasploit": {
            "desc": "Exploitation framework",
            "install": "apt install metasploit-framework / brew install metasploit",
            "usage": "msfconsole",
            "category": "exploit"
        },
        "sqlmap": {
            "desc": "SQL injection automation",
            "install": "apt install sqlmap / pip install sqlmap",
            "usage": "sqlmap -u target.com vuln param",
            "category": "exploit"
        },
        "searchsploit": {
            "desc": "Exploit-DB search tool",
            "install": "apt install exploitdb / brew install exploitdb",
            "usage": "searchsploit apache 2.4",
            "category": "exploit"
        },
        "hydra": {
            "desc": "Password brute-forcing tool",
            "install": "apt install hydra / brew install hydra",
            "usage": "hydra -L users.txt -P passwords.txt target.com ssh",
            "category": "exploit"
        },
    },
    "Wireless": {
        "aircrack-ng": {
            "desc": "WiFi security auditing",
            "install": "apt install aircrack-ng",
            "usage": "aircrack-ng capture.cap",
            "category": "wireless"
        },
        "wifite": {
            "desc": "Automated wireless auditor",
            "install": "apt install wifite / pip install wifite2",
            "usage": "wifite",
            "category": "wireless"
        },
    },
    "Password Attacks": {
        "hashcat": {
            "desc": "Fast password recovery",
            "install": "apt install hashcat / brew install hashcat",
            "usage": "hashcat -m 0 hashes.txt wordlist.txt",
            "category": "password"
        },
        "john": {
            "desc": "John the Ripper",
            "install": "apt install john / brew install john",
            "usage": "john hash.txt",
            "category": "password"
        },
        "cewl": {
            "desc": "Custom wordlist generator",
            "install": "apt install cewl / brew install cewl",
            "usage": "cewl target.com -m 6 -w wordlist.txt",
            "category": "password"
        },
    },
    "Web Applications": {
        "burpsuite": {
            "desc": "Web application security testing",
            "install": "Download from https://portswigger.net/burp",
            "usage": "java -jar burpsuite.jar",
            "category": "web"
        },
        "zap": {
            "desc": "OWASP ZAP proxy",
            "install": "apt install zaproxy / brew install owasp-zap",
            "usage": "zap.sh",
            "category": "web"
        },
        "gobuster": {
            "desc": "Directory/Subdomain fuzzing",
            "install": "go install github.com/OJ/gobuster/v3@latest",
            "usage": "gobuster dir -u target.com -w wordlist.txt",
            "category": "web"
        },
        "dirb": {
            "desc": "Web content scanner",
            "install": "apt install dirb",
            "usage": "dirb target.com",
            "category": "web"
        },
    },
    "Reverse Engineering": {
        "ghidra": {
            "desc": "Software reverse engineering",
            "install": "Download from https://ghidra-sre.org/",
            "usage": "ghidraRun",
            "category": "re"
        },
        "radare2": {
            "desc": "Command-line reverse engineering",
            "install": "apt install radare2 / brew install radare2",
            "usage": "r2 binary",
            "category": "re"
        },
        "objdump": {
            "desc": "Disassembler (part of binutils)",
            "install": "apt install binutils / brew install binutils",
            "usage": "objdump -d binary",
            "category": "re"
        },
    },
    "Forensics": {
        "autopsy": {
            "desc": "Digital forensics platform",
            "install": "apt install autopsy",
            "usage": "autopsy",
            "category": "forensics"
        },
        "volatility": {
            "desc": "Memory forensics framework",
            "install": "pip install volatility3",
            "usage": "volatility -f memdump.raw",
            "category": "forensics"
        },
        "binwalk": {
            "desc": "Binary analysis tool",
            "install": "apt install binwalk / pip install binwalk",
            "usage": "binwalk firmware.bin",
            "category": "forensics"
        },
    },
    "LLM Security": {
        "burp-suite": {
            "desc": "Web proxy for testing LLM apps",
            "install": "Download from PortSwigger",
            "usage": "Intercept and analyze LLM API calls",
            "category": "llm"
        },
        "payloads": {
            "desc": "LLM jailbreak payloads collection",
            "install": "git clone https://github.com/GeorgioMaia/llm-payloads",
            "usage": "Use for red teaming LLM applications",
            "category": "llm"
        },
    },
    # === NEW CATEGORIES ===
    "Cloud Security": {
        "awscli": {
            "desc": "AWS command line interface",
            "install": "pip install awscli",
            "usage": "aws s3 ls / aws ec2 describe-instances",
            "category": "cloud"
        },
        "azure-cli": {
            "desc": "Microsoft Azure CLI",
            "install": "curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash",
            "usage": "az vm list",
            "category": "cloud"
        },
        "gcloud": {
            "desc": "Google Cloud CLI",
            "install": "curl https://sdk.cloud.google.com | bash",
            "usage": "gcloud compute instances list",
            "category": "cloud"
        },
        "cloudmapper": {
            "desc": "AWS security visualization",
            "install": "pip install cloudmapper",
            "usage": "cloudmapper.py report --account myaccount",
            "category": "cloud"
        },
        "prowler": {
            "desc": "AWS security assessment",
            "install": "pip install prowler",
            "usage": "prowler aws",
            "category": "cloud"
        },
        "cloudfrunt": {
            "desc": "Find domain variants for cloud services",
            "install": "git clone https://github.com/dustinmiano/cloudfrunt",
            "usage": "python3 cloudfrunt.py -d example.com",
            "category": "cloud"
        },
    },
    "Mobile Security": {
        "adb": {
            "desc": "Android Debug Bridge",
            "install": "apt install adb / brew install adb",
            "usage": "adb devices / adb shell",
            "category": "mobile"
        },
        "apktool": {
            "desc": "Android APK decompiler",
            "install": "apt install apktool / brew install apktool",
            "usage": "apktool d app.apk",
            "category": "mobile"
        },
        "jadx": {
            "desc": "Dex to Java decompiler",
            "install": "Download from jadx.github.io",
            "usage": "jadx app.apk",
            "category": "mobile"
        },
        "drozer": {
            "desc": "Android security assessment",
            "install": "pip install drozer",
            "usage": "drozer console connect",
            "category": "mobile"
        },
        "frida": {
            "desc": "Dynamic instrumentation toolkit",
            "install": "pip install frida-tools",
            "usage": "frida -U -f com.app",
            "category": "mobile"
        },
    },
    "API Security": {
        "Postman": {
            "desc": "API testing platform",
            "install": "Download from postman.com",
            "usage": "GUI for API testing",
            "category": "api"
        },
        "insomnia": {
            "desc": "API design platform",
            "install": "apt install insomnia / brew install insomnia",
            "usage": "insomnia",
            "category": "api"
        },
        "swagger": {
            "desc": "API documentation tool",
            "install": "npm install -g swagger",
            "usage": "swagger project create",
            "category": "api"
        },
        "restler": {
            "desc": "REST API fuzzer",
            "install": "git clone Microsoft/restler-fuzzer",
            "usage": "python restler.py",
            "category": "api"
        },
    },
    "Social Engineering": {
        "setoolkit": {
            "desc": "Social-Engineer Toolkit",
            "install": "apt install set",
            "usage": "setoolkit",
            "category": "social"
        },
        "king-phisher": {
            "desc": "Phishing campaign tool",
            "install": "apt install king-phisher",
            "usage": "king-phisher",
            "category": "social"
        },
        "gophish": {
            "desc": "Open-source phishing framework",
            "install": "Download from getgophish.com",
            "usage": "./gophish",
            "category": "social"
        },
        "evilginx2": {
            "desc": "Man-in-the-middle proxy",
            "install": "go get -u github.com/kgretzky/evilginx2",
            "usage": "evilginx -p /path/to/phishlets",
            "category": "social"
        },
    },
    "Sniffing & Spoofing": {
        "wireshark": {
            "desc": "Network protocol analyzer",
            "install": "apt install wireshark / brew install wireshark",
            "usage": "wireshark",
            "category": "sniff"
        },
        "tcpdump": {
            "desc": "Command-line packet analyzer",
            "install": "apt install tcpdump / brew install tcpdump",
            "usage": "tcpdump -i eth0",
            "category": "sniff"
        },
        "ettercap": {
            "desc": "Man-in-the-middle tool",
            "install": "apt install ettercap-graphical",
            "usage": "ettercap -G",
            "category": "sniff"
        },
        "bettercap": {
            "desc": "Swiss army knife for network",
            "install": "go get -u github.com/bettercap/bettercap",
            "usage": "bettercap -X",
            "category": "sniff"
        },
        "dsniff": {
            "desc": "Network sniffing tools",
            "install": "apt install dsniff",
            "usage": "dsniff -i eth0",
            "category": "sniff"
        },
    },
    "Privilege Escalation": {
        "linpeas": {
            "desc": "Linux privilege escalation checker",
            "install": "curl -L https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh",
            "usage": "curl -L https://github.com/carlospolop/PEASS-ng/... | sh",
            "category": "privesc"
        },
        "linenum": {
            "desc": "Linux local enumeration",
            "install": "git clone https://github.com/rebootuser/LinEnum",
            "usage": "./LinEnum.sh",
            "category": "privesc"
        },
        "linux-exploit-suggester": {
            "desc": "Find Linux exploits",
            "install": "git clone https://github.com/mzet-/linux-exploit-suggester",
            "usage": "./linux-exploit-suggester.pl",
            "category": "privesc"
        },
        "winpeas": {
            "desc": "Windows privilege escalation",
            "install": "Download from github.com/carlospolop/PEASS-ng",
            "usage": "winpeas.exe",
            "category": "privesc"
        },
        "powerup": {
            "desc": "Windows privilege escalation",
            "install": "git clone https://github.com/PowerShellMafia/PowerSploit",
            "usage": "powershell -ExecutionPolicy Bypass -File powerup.ps1",
            "category": "privesc"
        },
    },
    "Post Exploitation": {
        "mimikatz": {
            "desc": "Windows credential extractor",
            "install": "Download from github.com/gentilkiwi/mimikatz",
            "usage": "mimikatz.exe",
            "category": "postex"
        },
        "laZagne": {
            "desc": "Password recovery tool",
            "install": "pip install laZagne",
            "usage": "laZagne.py all",
            "category": "postex"
        },
        "pwdump": {
            "desc": "Windows password dumper",
            "install": "Download from foo.com/pwdump",
            "usage": "pwdump.exe",
            "category": "postex"
        },
        "fgdump": {
            "desc": "Password cache dumper",
            "install": "apt install fgdump",
            "usage": "fgdump.exe",
            "category": "postex"
        },
    },
    "DNS Tools": {
        "dnsenum": {
            "desc": "DNS enumeration",
            "install": "apt install dnsenum",
            "usage": "dnsenum target.com",
            "category": "dns"
        },
        "dnsmap": {
            "desc": "DNS mapping",
            "install": "apt install dnsmap",
            "usage": "dnsmap target.com",
            "category": "dns"
        },
        "fierce": {
            "desc": "DNS scanner",
            "install": "pip install fierce",
            "usage": "fierce --domain target.com",
            "category": "dns"
        },
        "dnschef": {
            "desc": "DNS proxy",
            "install": "pip install dnschef",
            "usage": "dnschef.py",
            "category": "dns"
        },
        "dnstwist": {
            "desc": "Domain permutation",
            "install": "pip install dnstwist",
            "usage": "dnstwist example.com",
            "category": "dns"
        },
    },
    "SSL/TLS Analysis": {
        "sslscan": {
            "desc": "SSL/TLS scanner",
            "install": "apt install sslscan / brew install sslscan",
            "usage": "sslscan target.com",
            "category": "ssl"
        },
        "testssl": {
            "desc": "TLS testing tool",
            "install": "git clone https://github.com/drwetter/testssl.sh",
            "usage": "./testssl.sh target.com",
            "category": "ssl"
        },
        "sslsplit": {
            "desc": "SSL/TLS splitting proxy",
            "install": "apt install sslsplit",
            "usage": "sslsplit -D -k key.pem -c cert.pem",
            "category": "ssl"
        },
        "openssl": {
            "desc": "SSL/TLS toolkit",
            "install": "apt install openssl",
            "usage": "openssl s_client -connect target.com:443",
            "category": "ssl"
        },
    },
}


class SecurityToolsResearcher:
    """Cross-platform security tools research module"""
    
    def __init__(self):
        DATA_DIR.mkdir(exist_ok=True)
        self.tools = self._load_database()
    
    def _load_database(self):
        """Load tools database"""
        if TOOLS_DB.exists():
            with open(TOOLS_DB, 'r') as f:
                return json.load(f)
        return {"tools": SECURITY_TOOLS, "last_updated": None}
    
    def _save_database(self):
        """Save tools database"""
        self._save({"tools": SECURITY_TOOLS, "last_updated": datetime.now().isoformat()})
    
    def _save(self, data):
        """Save to JSON file"""
        with open(TOOLS_DB, 'w') as f:
            json.dump(data, f, indent=2)
    
    def check_tool(self, tool_name):
        """Check if a tool is installed (cross-platform)"""
        # Try 'which' on Unix, 'where' on Windows
        try:
            result = subprocess.run(
                ["which", tool_name] if os.name != 'nt' else ["where", tool_name],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except:
            return False
    
    def scan(self):
        """Scan for available tools"""
        available = []
        unavailable = []
        
        for category, tools in SECURITY_TOOLS.items():
            for name, info in tools.items():
                status = self.check_tool(name)
                entry = {"name": name, "desc": info["desc"], "category": category, "installed": status}
                if status:
                    available.append(entry)
                else:
                    unavailable.append(entry)
        
        return {
            "available": available,
            "unavailable": unavailable,
            "total_available": len(available),
            "total_tools": sum(len(tools) for tools in SECURITY_TOOLS.values())
        }
    
    def list_tools(self, category=None, available_only=False):
        """List tools, optionally filtered by category"""
        results = []
        
        for cat, tools in SECURITY_TOOLS.items():
            if category and cat.lower() != category.lower():
                continue
            
            for name, info in tools.items():
                is_installed = self.check_tool(name)
                
                if available_only and not is_installed:
                    continue
                
                results.append({
                    "name": name,
                    "category": cat,
                    "desc": info["desc"],
                    "install": info["install"],
                    "usage": info["usage"],
                    "installed": is_installed
                })
        
        return results
    
    def get_tool_info(self, tool_name):
        """Get info about a specific tool"""
        for category, tools in SECURITY_TOOLS.items():
            if tool_name in tools:
                info = tools[tool_name]
                info["category"] = category
                info["installed"] = self.check_tool(tool_name)
                return info
        return None
    
    def run_research(self):
        """Run research cycle"""
        print("=== Cerberus Security Tools Research ===")
        print(f"Time: {datetime.now().isoformat()}\n")
        
        scan_results = self.scan()
        
        print(f"Tools Database: {scan_results['total_tools']} tools")
        print(f"Installed: {scan_results['total_available']} / {scan_results['total_tools']}")
        
        # Save results
        self._save({
            "tools": SECURITY_TOOLS,
            "last_updated": datetime.now().isoformat(),
            "scan_results": scan_results
        })
        
        print("\n=== Installed Tools ===")
        for tool in scan_results["available"]:
            print(f"  ✓ {tool['name']} ({tool['category']})")
        
        print("\n=== Research Complete ===")
        return scan_results


def main():
    """CLI Entry Point"""
    parser = argparse.ArgumentParser(description="Cerberus Security Tools Research")
    parser.add_argument("--scan", action="store_true", help="Scan for installed tools")
    parser.add_argument("--list", action="store_true", help="List all tools")
    parser.add_argument("--category", type=str, help="Filter by category")
    parser.add_argument("--installed", action="store_true", help="Show only installed tools")
    parser.add_argument("--info", type=str, help="Get info on specific tool")
    parser.add_argument("--update", action="store_true", help="Update tools database")
    
    args = parser.parse_args()
    
    researcher = SecurityToolsResearcher()
    
    if args.scan:
        researcher.run_research()
    elif args.list:
        tools = researcher.list_tools(category=args.category, available_only=args.installed)
        for tool in tools:
            status = "✓" if tool["installed"] else "✗"
            print(f"[{status}] {tool['name']} - {tool['desc']} ({tool['category']})")
    elif args.info:
        info = researcher.get_tool_info(args.info)
        if info:
            print(f"\n=== {args.info} ===")
            print(f"Description: {info['desc']}")
            print(f"Category: {info['category']}")
            print(f"Installed: {'Yes' if info['installed'] else 'No'}")
            print(f"Install: {info['install']}")
            print(f"Usage: {info['usage']}")
        else:
            print(f"Tool '{args.info}' not found in database")
    elif args.update:
        researcher._save_database()
        print("Tools database updated!")
    else:
        # Default: show summary
        researcher.run_research()


if __name__ == "__main__":
    main()
