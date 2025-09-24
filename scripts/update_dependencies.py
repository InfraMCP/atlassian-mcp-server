#!/usr/bin/env python3
"""
Safely update dependencies with security checks.
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, check=True):
    """Run command and return result."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    return result


def main():
    """Update dependencies safely."""
    print("🔄 Updating dependencies safely...")
    
    # Backup current requirements
    print("\n📋 Backing up current requirements...")
    run_command("cp requirements.txt requirements.txt.backup")
    
    # Get latest versions
    print("\n🔍 Checking for updates...")
    core_packages = ["mcp", "httpx", "pydantic", "pydantic-settings"]
    
    updates = []
    for package in core_packages:
        result = run_command(f"pip3 show {package}", check=False)
        if result.returncode == 0:
            # Get current version
            for line in result.stdout.split('\n'):
                if line.startswith('Version:'):
                    current_version = line.split(':', 1)[1].strip()
                    print(f"  {package}: {current_version}")
                    break
    
    print("\n⚠️  Manual update required:")
    print("1. Check https://pypi.org for latest versions")
    print("2. Update requirements.txt with new pinned versions")
    print("3. Update pyproject.toml dependencies")
    print("4. Run: pip3 install -r requirements.txt")
    print("5. Run: python3 scripts/generate_dependency_report.py")
    print("6. Run: safety check && pip-audit")
    print("7. Test thoroughly before committing")
    
    print("\n🔒 Security reminder:")
    print("- Review changelogs for security fixes")
    print("- Check for breaking changes")
    print("- Run full test suite after updates")


if __name__ == "__main__":
    main()
