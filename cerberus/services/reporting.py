#!/usr/bin/env python3
"""
Cerberus Report Generator Module
Generate security assessment reports
"""

import json
import argparse
from datetime import datetime
from pathlib import Path
from enum import Enum


class ReportFormat(Enum):
    """Report output formats"""
    MARKDOWN = "md"
    HTML = "html"
    JSON = "json"
    TEXT = "txt"


class ReportGenerator:
    """Generate security assessment reports"""
    
    def __init__(self):
        self.data = {}
        self.sections = []
    
    def add_section(self, title, content, level=2):
        """Add a section to the report"""
        self.sections.append({
            "title": title,
            "content": content,
            "level": level
        })
    
    def add_finding(self, severity, title, description, evidence=None, recommendation=None):
        """Add a security finding"""
        finding = {
            "severity": severity,
            "title": title,
            "description": description,
            "evidence": evidence or [],
            "recommendation": recommendation or []
        }
        
        if "findings" not in self.data:
            self.data["findings"] = []
        self.data["findings"].append(finding)
    
    def set_metadata(self, **kwargs):
        """Set report metadata"""
        self.data["metadata"] = kwargs
    
    def generate_markdown(self):
        """Generate Markdown report"""
        lines = []
        
        # Title
        title = self.data.get("metadata", {}).get("title", "Security Assessment Report")
        lines.append(f"# {title}\n")
        
        # Metadata
        if "metadata" in self.data:
            lines.append("## Metadata\n")
            for k, v in self.data["metadata"].items():
                lines.append(f"- **{k}:** {v}")
            lines.append("")
        
        # Findings summary
        if "findings" in self.data:
            severities = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
            for f in self.data["findings"]:
                sev = f.get("severity", "info").lower()
                severities[sev] = severities.get(sev, 0) + 1
            
            lines.append("## Findings Summary\n")
            lines.append("| Severity | Count |")
            lines.append("|----------|-------|")
            for sev, count in severities.items():
                if count > 0:
                    lines.append(f"| {sev.title()} | {count} |")
            lines.append("")
        
        # Findings details
        if "findings" in self.data:
            lines.append("## Detailed Findings\n")
            
            # Sort by severity
            severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
            sorted_findings = sorted(
                self.data["findings"],
                key=lambda x: severity_order.get(x.get("severity", "info"), 4)
            )
            
            for i, finding in enumerate(sorted_findings, 1):
                sev = finding.get("severity", "info").upper()
                lines.append(f"### {i}. [{sev}] {finding.get('title', 'Untitled')}\n")
                lines.append(f"{finding.get('description', '')}\n")
                
                if finding.get("evidence"):
                    lines.append("**Evidence:**")
                    for e in finding["evidence"]:
                        lines.append(f"- {e}")
                    lines.append("")
                
                if finding.get("recommendation"):
                    lines.append("**Recommendation:**")
                    for r in finding["recommendation"]:
                        lines.append(f"- {r}")
                    lines.append("")
        
        # Custom sections
        for section in self.sections:
            level = "#" * section["level"]
            lines.append(f"\n{level} {section['title']}\n")
            lines.append(f"{section['content']}\n")
        
        return "\n".join(lines)
    
    def generate_html(self):
        """Generate HTML report"""
        md = self.generate_markdown()
        
        # Simple HTML template
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{self.data.get('metadata', {}).get('title', 'Security Report')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
        h1 {{ color: #333; border-bottom: 2px solid #333; }}
        h2 {{ color: #555; }}
        h3 {{ color: #777; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .critical {{ color: #d9534f; font-weight: bold; }}
        .high {{ color: #f0ad4e; font-weight: bold; }}
        .medium {{ color: #5bc0de; font-weight: bold; }}
        .low {{ color: #5cb85c; }}
        code {{ background: #f4f4f4; padding: 2px 6px; }}
    </style>
</head>
<body>
{self._md_to_html(md)}
</body>
</html>"""
        
        return html
    
    def _md_to_html(self, md):
        """Simple Markdown to HTML conversion"""
        import re
        
        # Headers
        md = re.sub(r'^### (.+)$', r'<h3>\1</h3>', md, flags=re.MULTILINE)
        md = re.sub(r'^## (.+)$', r'<h2>\1</h2>', md, flags=re.MULTILINE)
        md = re.sub(r'^# (.+)$', r'<h1>\1</h1>', md, flags=re.MULTILINE)
        
        # Bold
        md = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', md)
        
        # Lists
        md = re.sub(r'^- (.+)$', r'<li>\1</li>', md, flags=re.MULTILINE)
        md = re.sub(r'<li>(.+)</li>', r'<ul>\g<0></ul>', md)
        
        # Paragraphs
        md = re.sub(r'\n\n', r'</p><p>', md)
        
        # Tables (basic)
        md = re.sub(r'\|(.+)\|', r'<td>\1</td>', md)
        md = re.sub(r'<td>(.+)</td><td>(.+)</td>', r'<tr><td>\1</td><td>\2</td></tr>', md)
        
        return f"<p>{md}</p>"
    
    def generate_json(self):
        """Generate JSON report"""
        return json.dumps(self.data, indent=2)
    
    def generate_text(self):
        """Generate plain text report"""
        md = self.generate_markdown()
        
        # Remove markdown syntax
        import re
        text = re.sub(r'#+ ', '', md)
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        text = re.sub(r'\|', '|', text)
        text = re.sub(r'-+', '-', text)
        
        return text
    
    def save(self, filepath, format="md"):
        """Save report to file"""
        if format == "md" or format == "markdown":
            content = self.generate_markdown()
        elif format == "html":
            content = self.generate_html()
        elif format == "json":
            content = self.generate_json()
        else:
            content = self.generate_text()
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        return {"saved": filepath, "size": len(content)}


def create_sample_report():
    """Create a sample security report"""
    report = ReportGenerator()
    
    # Metadata
    report.set_metadata(
        title="Sample Security Assessment",
        target="example.com",
        date=datetime.now().isoformat(),
        assessor="Cerberus"
    )
    
    # Add findings
    report.add_finding(
        severity="high",
        title="SQL Injection Vulnerability",
        description="The login form is vulnerable to SQL injection.",
        evidence=["' OR '1'='1 bypasses authentication"],
        recommendation=["Use parameterized queries", "Implement input validation"]
    )
    
    report.add_finding(
        severity="medium",
        title="Missing Security Headers",
        description="Missing X-Content-Type-Options header.",
        evidence=["Headers checked with curl -I"],
        recommendation=["Add 'X-Content-Type-Options: nosniff'"]
    )
    
    # Generate
    return report


def main():
    """CLI Entry Point"""
    parser = argparse.ArgumentParser(description="Cerberus Report Generator")
    parser.add_argument("--output", "-o", help="Output file")
    parser.add_argument("--format", "-f", choices=["md", "html", "json", "txt"],
                       default="md", help="Output format")
    parser.add_argument("--sample", action="store_true", help="Generate sample report")
    
    args = parser.parse_args()
    
    if args.sample:
        report = create_sample_report()
    else:
        report = create_sample_report()
    
    if args.output:
        report.save(args.output, args.format)
        print(f"Report saved to {args.output}")
    else:
        print(report.generate_markdown())


if __name__ == "__main__":
    main()
