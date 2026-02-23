#!/usr/bin/env python3
"""
Cerberus Web Fuzzer Module
Directory, subdomain, and web vulnerability fuzzing
"""

import subprocess
import argparse
import requests
import concurrent.futures
from pathlib import Path
from urllib.parse import urljoin, urlparse


class WebFuzzer:
    """Web fuzzing and enumeration"""
    
    def __init__(self):
        self.results = []
        self.session = requests.Session()
    
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
    
    def dir_scan(self, target, wordlist=None, extensions=None):
        """Directory scanning using gobuster/dirb"""
        results = {"target": target, "found": []}
        
        # Check for gobuster
        if self.check_tool("gobuster"):
            cmd = ["gobuster", "dir", "-u", target]
            if wordlist:
                cmd.extend(["-w", wordlist])
            if extensions:
                cmd.extend(["-x", extensions])
            cmd.extend(["-q", "--no-error"])
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                for line in result.stdout.split("\n"):
                    if "200" in line or "301" in line or "302" in line:
                        results["found"].append(line.strip())
            except:
                pass
        
        # Fallback to dirb
        elif self.check_tool("dirb"):
            cmd = ["dirb", target]
            if wordlist:
                cmd.append(wordlist)
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                for line in result.stdout.split("\n"):
                    if "+ " in line:
                        results["found"].append(line.strip())
            except:
                pass
        
        # Pure Python fallback
        else:
            return self._python_dir_scan(target, extensions)
        
        return results
    
    def _python_dir_scan(self, target, extensions=None, wordlist=None):
        """Pure Python directory scanner"""
        results = {"target": target, "found": [], "errors": []}
        
        # Default wordlist
        if wordlist is None:
            dirs = ["admin", "api", "backup", "cgi-bin", "config", "dashboard",
                   "data", "db", "files", "ftp", "images", "include", "login",
                   "logs", "phpmyadmin", "test", "uploads", "wp-admin"]
        else:
            with open(wordlist) as f:
                dirs = [line.strip() for line in f]
        
        if extensions is None:
            extensions = ["", ".php", ".html", ".txt", ".asp", ".aspx", ".jsp"]
        
        def check_path(path):
            try:
                r = self.session.get(path, timeout=5)
                if r.status_code < 400:
                    return {"path": path, "status": r.status_code}
            except:
                pass
            return None
        
        base_url = target if target.startswith("http") else f"http://{target}"
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            paths = []
            for d in dirs[:50]:  # Limit for speed
                for ext in extensions[:5]:
                    paths.append(f"{base_url}/{d}{ext}")
            
            for result in executor.map(check_path, paths):
                if result:
                    results["found"].append(f"{result['path']} ({result['status']})")
        
        return results
    
    def subdomain_enum(self, domain, wordlist=None):
        """Subdomain enumeration"""
        results = {"domain": domain, "found": []}
        
        # Check for tools
        if self.check_tool("gobuster"):
            cmd = ["gobuster", "dns", "-d", domain, "-q"]
            if wordlist:
                cmd.extend(["-w", wordlist])
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                for line in result.stdout.split("\n"):
                    if domain in line:
                        results["found"].append(line.strip())
            except:
                pass
        
        # Pure Python DNS brute force
        else:
            return self._python_subdomain_enum(domain)
        
        return results
    
    def _python_subdomain_enum(self, domain):
        """Pure Python subdomain enumeration"""
        results = {"domain": domain, "found": []}
        
        subdomains = ["www", "mail", "ftp", "localhost", "webmail", "smtp",
                     "pop", "ns1", "webdisk", "ns2", "cpanel", "whm",
                     "autodiscover", "autoconfig", "m", "imap", "test",
                     "ns", "blog", "pop3", "dev", "www2", "admin",
                     "forum", "news", "vpn", "ns3", "mail2", "new",
                     "mysql", "old", "lists", "support", "mobile", "mx",
                     "static", "docs", "beta", "shop", "sql", "secure"]
        
        def check_subdomain(sub):
            try:
                host = f"{sub}.{domain}"
                ip = __import__('socket').gethostbyname(host)
                return {"subdomain": host, "ip": ip}
            except:
                return None
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            for result in executor.map(check_subdomain, subdomains):
                if result:
                    results["found"].append(result)
        
        return results
    
    def parameter_discovery(self, target):
        """Discover web parameters"""
        results = {"target": target, "parameters": []}
        
        # Common parameters
        params = ["id", "q", "search", "query", "s", "page", "lang",
                 "file", "dir", "action", "debug", "test", "id", "uid",
                 "user", "name", "pass", "email", "login", "admin"]
        
        def check_param(param):
            try:
                r = self.session.get(f"{target}?{param}=test", timeout=5)
                # Check for parameter-based vulnerabilities
                if r.status_code == 200 and "error" not in r.text.lower():
                    return param
            except:
                pass
            return None
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            found = executor.map(check_param, params)
            results["parameters"] = [p for p in found if p]
        
        return results
    
    def cms_detect(self, target):
        """Detect CMS"""
        results = {"target": target, "cms": None, "version": None}
        
        try:
            r = self.session.get(target, timeout=10)
            content = r.text.lower()
            
            # WordPress
            if "wp-content" in content or "wordpress" in content:
                results["cms"] = "WordPress"
            
            # Joomla
            elif "joomla" in content or "/administrator/" in content:
                results["cms"] = "Joomla"
            
            # Drupal
            elif "drupal" in content or "sites/default" in content:
                results["cms"] = "Drupal"
            
            # Magento
            elif "magento" in content or "mage-" in content:
                results["cms"] = "Magento"
            
            # Check generator meta
            if "generator" in content:
                import re
                gen = re.search(r'generator[^>]*>([^<]+)', content, re.I)
                if gen:
                    results["version"] = gen.group(1).strip()
        
        except Exception as e:
            results["error"] = str(e)
        
        return results
    
    def tech_detect(self, target):
        """Detect technologies"""
        results = {"target": target, "tech": []}
        
        try:
            r = self.session.get(target, timeout=10)
            headers = r.headers
            
            # Server
            if "Server" in headers:
                results["tech"].append(f"Server: {headers['Server']}")
            
            # X-Powered-By
            if "X-Powered-By" in headers:
                results["tech"].append(f"Powered-By: {headers['X-Powered-By']}")
            
            # Content-Type
            if "Content-Type" in headers:
                results["tech"].append(f"Content-Type: {headers['Content-Type']}")
            
            # Check cookies for tech
            if "JSESSIONID" in r.text:
                results["tech"].append("Java/JSP")
            if "PHPSESSID" in r.text:
                results["tech"].append("PHP")
            if "ASP.NET" in r.text or "ASPX" in r.text:
                results["tech"].append("ASP.NET")
        
        except Exception as e:
            results["error"] = str(e)
        
        return results


def main():
    """CLI Entry Point"""
    parser = argparse.ArgumentParser(description="Cerberus Web Fuzzer")
    parser.add_argument("target", help="Target URL or domain")
    parser.add_argument("--scan", choices=["dir", "subdomain", "param", "cms", "tech", "full"],
                       default="dir", help="Scan type")
    parser.add_argument("--wordlist", type=str, help="Custom wordlist")
    parser.add_argument("--extensions", type=str, help="File extensions (e.g., php,html)")
    
    args = parser.parse_args()
    
    fuzzer = WebFuzzer()
    
    print(f"=== Cerberus Web Fuzzer ===")
    print(f"Target: {args.target}\n")
    
    if args.scan == "dir":
        result = fuzzer.dir_scan(args.target, args.wordlist, args.extensions)
        print(f"Found {len(result['found'])} paths:")
        for p in result["found"][:20]:
            print(f"  ✓ {p}")
    
    elif args.scan == "subdomain":
        result = fuzzer.subdomain_enum(args.target, args.wordlist)
        print(f"Found {len(result['found'])} subdomains:")
        for s in result["found"][:20]:
            print(f"  ✓ {s}")
    
    elif args.scan == "param":
        result = fuzzer.parameter_discovery(args.target)
        print(f"Found {len(result['parameters'])} parameters:")
        for p in result["parameters"]:
            print(f"  ✓ {p}")
    
    elif args.scan == "cms":
        result = fuzzer.cms_detect(args.target)
        print(f"CMS: {result['cms']}")
        print(f"Version: {result.get('version', 'Unknown')}")
    
    elif args.scan == "tech":
        result = fuzzer.tech_detect(args.target)
        print("Technologies detected:")
        for t in result["tech"]:
            print(f"  • {t}")
    
    elif args.scan == "full":
        print("--- CMS Detection ---")
        print(f"CMS: {fuzzer.cms_detect(args.target)['cms']}")
        
        print("\n--- Technology Detection ---")
        for t in fuzzer.tech_detect(args.target)["tech"]:
            print(f"  • {t}")
        
        print("\n--- Parameter Discovery ---")
        params = fuzzer.parameter_discovery(args.target)
        print(f"Found {len(params['parameters'])} parameters")


if __name__ == "__main__":
    main()
