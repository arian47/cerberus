#!/usr/bin/env python3
"""
Cerberus Forensics Module
Digital forensics and incident response tools
"""

import subprocess
import argparse
import os
import hashlib
import re
from pathlib import Path
from datetime import datetime


class ForensicsToolkit:
    """Digital forensics toolkit"""
    
    def __init__(self):
        self.findings = []
    
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
    
    def file_hash(self, filepath):
        """Calculate file hashes"""
        if not os.path.exists(filepath):
            return {"error": "File not found"}
        
        hashes = {}
        
        # MD5
        with open(filepath, "rb") as f:
            hashes["md5"] = hashlib.md5(f.read()).hexdigest()
        
        # SHA1
        with open(filepath, "rb") as f:
            hashes["sha1"] = hashlib.sha1(f.read()).hexdigest()
        
        # SHA256
        with open(filepath, "rb") as f:
            hashes["sha256"] = hashlib.sha256(f.read()).hexdigest()
        
        return {
            "file": filepath,
            "size": os.path.getsize(filepath),
            "hashes": hashes
        }
    
    def strings_extract(self, filepath, min_len=4):
        """Extract strings from binary"""
        if not os.path.exists(filepath):
            return {"error": "File not found"}
        
        strings = []
        
        try:
            result = subprocess.run(
                ["strings", "-n", str(min_len), filepath],
                capture_output=True,
                text=True,
                timeout=30
            )
            strings = result.stdout.split("\n")[:100]  # Limit to 100
        except:
            # Pure Python fallback
            with open(filepath, "rb") as f:
                content = f.read()
                # Extract printable strings
                current = ""
                for byte in content:
                    if 32 <= byte <= 126:
                        current += chr(byte)
                    else:
                        if len(current) >= min_len:
                            strings.append(current)
                        current = ""
        
        return {"file": filepath, "strings": strings}
    
    def hexdump(self, filepath, offset=0, length=256):
        """Create hexdump"""
        if not os.path.exists(filepath):
            return {"error": "File not found"}
        
        try:
            result = subprocess.run(
                ["hexdump", "-C", "-s", str(offset), "-n", str(length), filepath],
                capture_output=True,
                text=True,
                timeout=10
            )
            return {"hexdump": result.stdout}
        except:
            # Pure Python fallback
            with open(filepath, "rb") as f:
                f.seek(offset)
                data = f.read(length)
            
            lines = []
            for i in range(0, len(data), 16):
                chunk = data[i:i+16]
                hex_part = " ".join(f"{b:02x}" for b in chunk)
                ascii_part = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
                lines.append(f"{i:08x}  {hex_part:<48}  {ascii_part}")
            
            return {"hexdump": "\n".join(lines)}
    
    def metadata_extract(self, filepath):
        """Extract file metadata"""
        if not os.path.exists(filepath):
            return {"error": "File not found"}
        
        stat = os.stat(filepath)
        
        return {
            "file": filepath,
            "size": stat.st_size,
            "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "accessed": datetime.fromtimestamp(stat.st_atime).isoformat(),
            "permissions": oct(stat.st_mode)[-3:]
        }
    
    def xor_decrypt(self, data, key):
        """XOR decryption"""
        if isinstance(data, str):
            data = bytes.fromhex(data.replace(" ", ""))
        
        if isinstance(key, str):
            key = key.encode()
        
        result = bytearray()
        for i, byte in enumerate(data):
            result.append(byte ^ key[i % len(key)])
        
        return result.hex()
    
    def base64_decode(self, data):
        """Base64 decode"""
        import base64
        try:
            return {"decoded": base64.b64decode(data).decode("utf-8", errors="ignore")}
        except Exception as e:
            return {"error": str(e)}
    
    def url_decode(self, data):
        """URL decode"""
        from urllib.parse import unquote
        return {"decoded": unquote(data)}
    
    def detect_encoding(self, filepath):
        """Detect file encoding"""
        if not os.path.exists(filepath):
            return {"error": "File not found"}
        
        # Read first 10KB
        with open(filepath, "rb") as f:
            data = f.read(10000)
        
        # Check for BOM
        if data.startswith(b'\xef\xbb\xbf'):
            return {"encoding": "UTF-8 (BOM)", "confidence": "high"}
        elif data.startswith(b'\xff\xfe'):
            return {"encoding": "UTF-16 LE (BOM)", "confidence": "high"}
        elif data.startswith(b'\xfe\xff'):
            return {"encoding": "UTF-16 BE (BOM)", "confidence": "high"}
        
        # Try UTF-8
        try:
            data.decode("utf-8")
            return {"encoding": "UTF-8", "confidence": "medium"}
        except:
            pass
        
        # Check for common encodings
        for enc in ["latin-1", "cp1252", "iso-8859-1"]:
            try:
                data.decode(enc)
                return {"encoding": enc, "confidence": "low"}
            except:
                continue
        
        return {"encoding": "unknown", "confidence": "low"}
    
    def find_suspicious(self, directory):
        """Find suspicious files"""
        suspicious = []
        patterns = [
            r"\.exe$",
            r"\.dll$", 
            r"\.tmp$",
            r"\~",
            r"\.bak$",
            r"\.ps1$",
            r"\.vbs$",
            r"\.bat$",
            r"\.sh$",
            r"nc\.exe",
            r"mimikatz",
            r"password",
            r"\.log$"
        ]
        
        for root, dirs, files in os.walk(directory):
            for f in files:
                filepath = os.path.join(root, f)
                for pattern in patterns:
                    if re.search(pattern, f, re.I):
                        suspicious.append(filepath)
                        break
        
        return {"suspicious_files": suspicious, "count": len(suspicious)}
    
    def timeline_analysis(self, directory):
        """Create timeline of file changes"""
        timeline = []
        
        for root, dirs, files in os.walk(directory):
            for f in files:
                filepath = os.path.join(root, f)
                try:
                    stat = os.stat(filepath)
                    timeline.append({
                        "file": filepath,
                        "mtime": stat.st_mtime,
                        "ctime": stat.st_ctime,
                        "size": stat.st_size
                    })
                except:
                    pass
        
        # Sort by modification time
        timeline.sort(key=lambda x: x["mtime"], reverse=True)
        
        return {"timeline": timeline[:50]}  # Return 50 most recent
    
    def carve_files(self, image_file, output_dir, extension=None):
        """Carve files from disk image"""
        if not os.path.exists(image_file):
            return {"error": "Image file not found"}
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Use binwalk if available
        if self.check_tool("binwalk"):
            cmd = ["binwalk", "--extract", "--directory", output_dir, image_file]
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                return {"status": "extracted", "output": result.stdout}
            except Exception as e:
                return {"error": str(e)}
        
        return {"error": "binwalk not installed"}


def main():
    """CLI Entry Point"""
    parser = argparse.ArgumentParser(description="Cerberus Forensics")
    parser.add_argument("file", nargs="?", help="Target file or directory")
    parser.add_argument("--hash", action="store_true", help="Calculate hashes")
    parser.add_argument("--strings", action="store_true", help="Extract strings")
    parser.add_argument("--hexdump", action="store_true", help="Hexdump")
    parser.add_argument("--meta", action="store_true", help="Extract metadata")
    parser.add_argument("--encoding", action="store_true", help="Detect encoding")
    parser.add_argument("--suspicious", action="store_true", help="Find suspicious files")
    parser.add_argument("--timeline", action="store_true", help="Timeline analysis")
    
    args = parser.parse_args()
    
    forensics = ForensicsToolkit()
    
    print("=== Cerberus Forensics ===\n")
    
    if args.file:
        if args.hash:
            result = forensics.file_hash(args.file)
            if "error" in result:
                print(f"Error: {result['error']}")
            else:
                print(f"File: {result['file']}")
                print(f"Size: {result['size']} bytes")
                print(f"MD5:  {result['hashes']['md5']}")
                print(f"SHA1: {result['hashes']['sha1']}")
                print(f"SHA256: {result['hashes']['sha256']}")
        
        elif args.strings:
            result = forensics.strings_extract(args.file)
            print(f"Strings found: {len(result.get('strings', []))}")
            for s in result.get('strings', [])[:20]:
                print(f"  {s}")
        
        elif args.hexdump:
            result = forensics.hexdump(args.file)
            print(result.get("hexdump", "Error"))
        
        elif args.meta:
            result = forensics.metadata_extract(args.file)
            for k, v in result.items():
                print(f"{k}: {v}")
        
        elif args.encoding:
            result = forensics.detect_encoding(args.file)
            print(f"Encoding: {result.get('encoding', 'unknown')}")
            print(f"Confidence: {result.get('confidence', 'low')}")
        
        elif os.path.isdir(args.file):
            if args.suspicious:
                result = forensics.find_suspicious(args.file)
                print(f"Suspicious files: {result['count']}")
                for f in result.get('suspicious_files', [])[:10]:
                    print(f"  {f}")
            
            elif args.timeline:
                result = forensics.timeline_analysis(args.file)
                print("Recent file changes:")
                for item in result.get('timeline', [])[:10]:
                    print(f"  {datetime.fromtimestamp(item['mtime'])} - {item['file']}")
    else:
        print("Usage:")
        print("  --hash <file>        Calculate hashes")
        print("  --strings <file>    Extract strings")
        print("  --hexdump <file>    Hexdump")
        print("  --meta <file>       Extract metadata")
        print("  --encoding <file>   Detect encoding")
        print("  --suspicious <dir>  Find suspicious files")


if __name__ == "__main__":
    main()
