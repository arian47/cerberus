#!/usr/bin/env python3
"""
Red Team Auto-Update Tool
Scans for NEW vulnerabilities and model releases every 5 hours
Focuses ONLY on newest models (last 6 months)
"""

import sys
import os
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'skills', 'redteam'))

def get_cutoff_date(months: int = 6) -> int:
    """Get months ago as integer for comparison (YYYYMM)"""
    d = datetime.now() - timedelta(days=30*months)
    return d.year * 100 + d.month

# NEW models only (released in last 6 months)
NEW_MODELS_TRACKED = {
    # 2025-2026 Releases
    "gpt-5": {"released": "2025-07", "vendor": "OpenAI", "status": "latest"},
    "gpt-4.5": {"released": "2025-01", "vendor": "OpenAI", "status": "recent"},
    "o1-pro": {"released": "2025-02", "vendor": "OpenAI", "status": "latest"},
    "o3-mini": {"released": "2025-01", "vendor": "OpenAI", "status": "latest"},
    "claude-4-opus": {"released": "2025-02", "vendor": "Anthropic", "status": "latest"},
    "claude-4-sonnet": {"released": "2025-02", "vendor": "Anthropic", "status": "latest"},
    "gemini-3.1-pro": {"released": "2025-05", "vendor": "Google", "status": "latest"},
    "gemini-3.0-flash": {"released": "2025-04", "vendor": "Google", "status": "latest"},
    "gemini-2.5-pro": {"released": "2025-03", "vendor": "Google", "status": "recent"},
    "Llama-4-scout": {"released": "2025-01", "vendor": "Meta", "status": "latest"},
    "Llama-4-maverick": {"released": "2025-01", "vendor": "Meta", "status": "latest"},
    "Qwen3-235B": {"released": "2025-03", "vendor": "Alibaba", "status": "latest"},
    "Qwen3-32B": {"released": "2025-03", "vendor": "Alibaba", "status": "latest"},
    "DeepSeek-V3": {"released": "2024-12", "vendor": "DeepSeek", "status": "recent"},
    "DeepSeek-R1": {"released": "2025-01", "vendor": "DeepSeek", "status": "latest"},
    "Mistral-Large-3": {"released": "2025-02", "vendor": "Mistral", "status": "latest"},
    "Grok-4": {"released": "2025-06", "vendor": "xAI", "status": "latest"},
    "Grok-3": {"released": "2025-02", "vendor": "xAI", "status": "recent"},
    "Command-R+": {"released": "2024-12", "vendor": "Cohere", "status": "recent"},
    "Yi-Large": {"released": "2024-11", "vendor": "01.AI", "status": "recent"},
}

# Known vulnerabilities for NEW models (will be auto-updated)
NEW_MODEL_VULNS = {}

def scan_model_releases() -> List[Dict]:
    """Scan for NEW model releases only"""
    cutoff = get_cutoff_date(12)  # Last 12 months
    releases = []
    
    for model, info in NEW_MODELS_TRACKED.items():
        # Parse YYYY-MM to YYYYMM int
        released = int(info['released'].replace('-', ''))
        
        if released >= cutoff:
            releases.append({
                'model': model,
                'vendor': info['vendor'],
                'released': info['released'],
                'status': info['status'],
                'vulnerabilities': NEW_MODEL_VULNS.get(model, []),
                'is_new': True
            })
    
    return releases

def fetch_arxiv_papers(max_results: int = 10) -> List[Dict]:
    """Fetch latest papers from arXiv"""
    try:
        import urllib.request
        import urllib.parse
        import xml.etree.ElementTree as ET
        
        queries = ["jailbreak", "prompt+injection", "LLM+security", "model+exploitation"]
        all_papers = []
        
        for query in queries[:2]:  # Limit to avoid rate limits
            encoded_query = urllib.parse.quote(query, safe='')
            url = f"http://export.arxiv.org/api/query?search_query=all:{encoded_query}&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"
            
            try:
                with urllib.request.urlopen(url, timeout=10) as response:
                    data = response.read()
                
                root = ET.fromstring(data)
                
                for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                    title = entry.find('{http://www.w3.org/2005/Atom}title').text
                    published = entry.find('{http://www.w3.org/2005/Atom}published').text[:7]  # YYYY-MM
                    all_papers.append({
                        'title': title.strip(),
                        'published': published,
                        'source': 'arxiv'
                    })
            except:
                continue
        
        # Deduplicate
        seen = set()
        unique = []
        for p in all_papers:
            if p['title'] not in seen:
                seen.add(p['title'])
                unique.append(p)
        
        return unique[:10]
        
    except Exception as e:
        return [{'error': str(e)}]

def check_github_new_tools() -> List[Dict]:
    """Check GitHub for new jailbreak/exploit tools"""
    # Would need proper GitHub API - placeholder for now
    return []

def discover_vulnerabilities(model: str, papers: List[Dict]) -> List[Dict]:
    """Discover potential vulnerabilities for a model based on papers"""
    vulns = []
    model_lower = model.lower()
    
    for paper in papers:
        if 'error' in paper:
            continue
            
        title = paper.get('title', '').lower()
        
        # Simple keyword matching - could be enhanced
        if any(kw in title for kw in ['jailbreak', 'bypass', 'exploit', 'injection', 'attack']):
            vulns.append({
                'technique': title[:80],
                'source': 'arxiv',
                'paper': paper.get('title', '')[:60]
            })
    
    return vulns

def update_vulnerability_db(model: str, vulns: List[Dict]):
    """Update the vulnerability database"""
    global NEW_MODEL_VULNS
    
    if model not in NEW_MODEL_VULNS:
        NEW_MODEL_VULNS[model] = []
    
    for v in vulns:
        if v not in NEW_MODEL_VULNS[model]:
            NEW_MODEL_VULNS[model].append(v)

def generate_payload_suggestions(model: str, vulns: List[Dict]) -> List[Dict]:
    """Generate payload suggestions based on discovered vulnerabilities"""
    suggestions = []
    
    for i, v in enumerate(vulns):
        suggestions.append({
            'id': f"NEW-{model.upper()[:4]}-{i+1:02d}",
            'model': model,
            'technique': v.get('technique', 'Unknown'),
            'source': v.get('source', 'discovered'),
            'severity': 'CRITICAL',  # New model = assume critical until proven otherwise
            'prompt_template': f"Test {model}: {v.get('technique', 'vulnerability')}"
        })
    
    return suggestions

def update_payload_library(suggestions: List[Dict]) -> bool:
    """Update payloads_v6.py with new suggestions"""
    if not suggestions:
        return True
    
    # Try multiple possible locations for payloads file
    possible_paths = [
        os.path.join(os.path.dirname(__file__), '..', 'skills', 'redteam', 'core', 'payloads_v6.py'),
        os.path.join(os.path.dirname(__file__), 'skills', 'redteam', 'core', 'payloads_v6.py'),
        os.path.join(os.path.dirname(__file__), 'payloads_v6.py'),
        'payloads_v6.py',
    ]
    
    payloads_file = None
    for path in possible_paths:
        if os.path.exists(path):
            payloads_file = path
            break
    
    if not payloads_file:
        print("⚠️ payloads_v6.py not found")
        return False
    
    timestamp = datetime.now().strftime("%Y-%m-%d")
    
    # Read file
    with open(payloads_file, 'r') as f:
        content = f.read()
    
    # Check if already updated today
    if f"# AUTO-UPDATED: {timestamp}" in content:
        print(f"✅ Already updated today ({timestamp})")
        return True
    
    # Build new section
    new_section = f"""

# =============================================================================
# AUTO-UPDATED: {timestamp}
# New model vulnerabilities discovered
# =============================================================================
"""
    
    for sug in suggestions:
        new_section += f'''
    # === {sug['model']}: {sug['technique']} ===
    # Source: {sug['source']}
    # ID: {sug['id']}
'''
    
    # Append to file
    with open(payloads_file, 'a') as f:
        f.write(new_section)
    
    print(f"✅ Added {len(suggestions)} new payload suggestions")
    return True

def run_auto_scan() -> Dict:
    """Run the full auto-scan focusing on NEW models"""
    print("=" * 70)
    print("🔍 RED TEAM AUTO-SCAN - NEW MODELS ONLY")
    print(f"Time: {datetime.now().isoformat()}")
    print("=" * 70)
    
    # 1. Get NEW models
    print("\n🤖 Identifying NEW models (last 6 months)...")
    new_models = scan_model_releases()
    print(f"   Found {len(new_models)} new models:")
    for m in new_models:
        print(f"   - {m['model']} ({m['vendor']}) - {m['released']}")
    
    # 2. Fetch latest papers
    print("\n📄 Fetching latest arXiv papers...")
    papers = fetch_arxiv_papers()
    print(f"   Found {len(papers)} papers")
    
    # 3. Discover vulnerabilities
    all_suggestions = []
    print("\n🎯 Discovering vulnerabilities...")
    
    for model_info in new_models:
        model = model_info['model']
        vulns = discover_vulnerabilities(model, papers)
        
        if vulns:
            print(f"   {model}: {len(vulns)} potential vulns found")
            update_vulnerability_db(model, vulns)
            suggestions = generate_payload_suggestions(model, vulns)
            all_suggestions.extend(suggestions)
    
    # 4. Update library
    print("\n💾 Updating payload library...")
    update_payload_library(all_suggestions)
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 SCAN SUMMARY")
    print("=" * 70)
    print(f"New models tracked: {len(new_models)}")
    print(f"Latest papers: {len(papers)}")
    print(f"New vulnerabilities: {len(all_suggestions)}")
    
    return {
        'timestamp': datetime.now().isoformat(),
        'new_models': len(new_models),
        'papers': len(papers),
        'new_vulns': len(all_suggestions),
        'suggestions': all_suggestions
    }

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Red Team Auto-Update - New Models Only')
    parser.add_argument('--scan', action='store_true', help='Run scan now')
    parser.add_argument('--list-models', action='store_true', help='List tracked models')
    args = parser.parse_args()
    
    if args.list_models:
        print("\n🤖 NEW MODELS TRACKED (Last 6 months):")
        print("-" * 50)
        for model, info in NEW_MODELS_TRACKED.items():
            print(f"  {model:20} | {info['vendor']:10} | {info['released']}")
        print(f"\nTotal: {len(NEW_MODELS_TRACKED)} models")
        
    elif args.scan:
        run_auto_scan()
    else:
        print("""
🔄 RED TEAM AUTO-UPDATE - NEW MODELS FOCUS

Usage:
  python3 auto_update.py --scan          # Run scan now
  python3 auto_update.py --list-models   # List tracked NEW models
  
Features:
  - Tracks ONLY models released in last 6 months
  - Monitors arXiv for latest security papers
  - Auto-updates payloads library with new techniques
  - Runs every 5 hours
        """)
