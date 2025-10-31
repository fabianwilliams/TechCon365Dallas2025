#!/usr/bin/env python3
"""
Security verification script for TechCon365Dallas2025 repository.
Checks for any remaining secrets or sensitive information before public release.
"""

import os
import re
import sys
from pathlib import Path

# Patterns that should NOT be in the public repository
SENSITIVE_PATTERNS = [
    r'CLIENT_SECRET.*["\']([^"\']+)["\']',  # CLIENT_SECRET values
    r'[a-zA-Z0-9]{32,}',  # Long random strings (potential secrets)
    r'fabian@adotob\.com',  # Personal email (should be template)
    r'adotob\.com',  # Personal domain (should be generic)
    r'/Users/fabswill/',  # Personal file paths
    r'password.*[=:].*["\']([^"\']+)["\']',  # Password assignments
    r'secret.*[=:].*["\']([^"\']+)["\']',  # Secret assignments
    r'api_key.*[=:].*["\']([^"\']+)["\']',  # API key assignments
]

# Files to exclude from scanning
EXCLUDE_FILES = {
    '.git',
    '__pycache__',
    'node_modules',
    '.env',
    'sessions.db',  # Binary database file
    'Sessions-TechCon365Dallas2025.pdf',  # PDF document
    'lmstudio-mcp-config.json',  # Local config (should be git-ignored)
    '.claude',  # Local Claude settings
    '.msgraph-mcp',  # Token cache directory
}

# Files that are expected to contain references (documentation about security)
EXPECTED_REFERENCES = {
    'SECURITY.md',  # This file documents what was removed
    'security_check.py',  # This file (self-reference)
    'sanitize_repo.sh',  # The sanitization script itself
}

def scan_file(file_path: Path) -> list:
    """Scan a file for sensitive patterns."""
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        for line_num, line in enumerate(content.split('\n'), 1):
            for pattern in SENSITIVE_PATTERNS:
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    # Skip if this is in an expected reference file 
                    if file_path.name in EXPECTED_REFERENCES:
                        continue
                    # Skip if this is documentation about what was removed/sanitized
                    if ('removed' in line.lower() or 'sanitized' in line.lower() or 
                        '→' in line or 'Template values' in line or 
                        'not-needed-for-device-flow' in line):
                        continue
                    # Skip CLIENT_SECRET references in code that are just reading env vars
                    if 'os.getenv("CLIENT_SECRET")' in line:
                        continue
                        
                    issues.append({
                        'file': str(file_path),
                        'line': line_num,
                        'pattern': pattern,
                        'match': match.group(0),
                        'context': line.strip()
                    })
                    
    except Exception as e:
        print(f"Warning: Could not scan {file_path}: {e}")
        
    return issues

def main():
    """Main security scan function."""
    print("🔒 TechCon365Dallas2025 Security Scan")
    print("="*50)
    
    repo_root = Path(__file__).parent
    all_issues = []
    files_scanned = 0
    
    # Scan all files in the repository
    for root, dirs, files in os.walk(repo_root):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_FILES]
        
        for file in files:
            if file in EXCLUDE_FILES:
                continue
                
            file_path = Path(root) / file
            
            # Skip binary files and certain extensions
            if file_path.suffix in {'.db', '.pdf', '.pyc', '.so', '.dylib'}:
                continue
                
            files_scanned += 1
            issues = scan_file(file_path)
            all_issues.extend(issues)
    
    # Report results
    print(f"📊 Scanned {files_scanned} files")
    
    if all_issues:
        print(f"\n❌ FOUND {len(all_issues)} SECURITY ISSUES:")
        print("="*50)
        
        for issue in all_issues:
            print(f"\n🚨 {issue['file']}:{issue['line']}")
            print(f"   Pattern: {issue['pattern']}")
            print(f"   Match: {issue['match']}")
            print(f"   Context: {issue['context'][:100]}...")
            
        print("\n⚠️  REPOSITORY NOT READY FOR PUBLIC RELEASE")
        print("   Please fix the issues above before making public.")
        return 1
        
    else:
        print("\n✅ NO SECURITY ISSUES FOUND!")
        print("="*30)
        print("🎉 Repository appears safe for public release")
        print("\n✅ Verified:")
        print("   - No CLIENT_SECRET values")
        print("   - No personal email addresses")
        print("   - No hardcoded credentials")
        print("   - No local file paths")
        print("   - No API keys or tokens")
        
        print("\n📋 Final Checklist:")
        print("   [ ] Review .gitignore coverage")
        print("   [ ] Test template files work")
        print("   [ ] Verify setup instructions")
        print("   [ ] Check presentation for personal info")
        
        return 0

if __name__ == "__main__":
    sys.exit(main())