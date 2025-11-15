#!/usr/bin/env python3
"""
LinkedIn Connections Scraper - REFERENCE ONLY

⚠️ IMPORTANT: DO NOT EXECUTE THIS SCRIPT VIA BASH IN CLAUDE CODE
This script is provided as a reference implementation only.
Claude should format markdown directly without calling external Python scripts.

Why this is reference only:
- Running Python via Bash requires user approval for each command
- Claude can format markdown directly without external scripts
- Direct formatting is more efficient and doesn't require file imports

Instead of using this script:
1. Use the Read tool to find the last connection number
2. Format markdown directly using the pattern shown in the workflow
3. Use the Edit tool for all file operations

Original purpose (for reference):
A generalizable script to extract LinkedIn connection data from Playwright page snapshots
and append to markdown files with proper formatting and numbering.
"""

import argparse
import re
import sys
from pathlib import Path
from datetime import datetime


def parse_page_range(page_range_str):
    """Parse page range string like '61-70' or '5' into list of page numbers."""
    if '-' in page_range_str:
        start, end = page_range_str.split('-')
        return list(range(int(start), int(end) + 1))
    else:
        return [int(page_range_str)]


def extract_last_connection_number(file_path):
    """Extract the last connection number from existing markdown file."""
    if not Path(file_path).exists():
        return 0

    with open(file_path, 'r') as f:
        content = f.read()

    # Find all connection numbers (## 123. Name)
    matches = re.findall(r'^## (\d+)\.\s', content, re.MULTILINE)
    if matches:
        return int(matches[-1])
    return 0


def parse_connection_from_yaml(yaml_text, profile_url):
    """
    Extract connection details from YAML snapshot text.

    Returns dict with: name, title, location, mutual_connections, profile
    """
    connection = {
        'name': '',
        'title': '',
        'location': '',
        'mutual_connections': '',
        'profile': profile_url
    }

    # Extract name from link text or paragraph
    name_match = re.search(r'link "([^"]+)".*\n.*\/url: ' + re.escape(profile_url), yaml_text)
    if name_match:
        connection['name'] = name_match.group(1)

    # Try alternative name pattern
    if not connection['name']:
        alt_name_match = re.search(r'figure "([^"]+)"', yaml_text)
        if alt_name_match:
            connection['name'] = alt_name_match.group(1)

    # Extract title (usually appears in paragraph after name)
    title_match = re.search(r'paragraph.*?: (.+?)(?:\n|$)', yaml_text)
    if title_match:
        title_text = title_match.group(1).strip()
        # Filter out location-like text and connection degree indicators
        if not any(x in title_text.lower() for x in ['united states', 'area', '• 1st', '• 2nd', 'followers']):
            connection['title'] = title_text

    # Extract location (contains geographic terms)
    location_patterns = [
        r'paragraph.*?: (.+?(?:United States|United Kingdom|Area|Metropolitan|California|New York|Texas|Florida|Germany|International)[^\n]*)',
        r'paragraph.*?: ([^:]+, [A-Z][a-z]+(?:, [A-Z][a-z]+)?)'
    ]
    for pattern in location_patterns:
        location_match = re.search(pattern, yaml_text)
        if location_match:
            loc = location_match.group(1).strip()
            if '•' not in loc and 'Profile' not in loc:
                connection['location'] = loc
                break

    # Extract mutual connections
    mutual_patterns = [
        r'strong.*?: (.+?)\n.*text: ","\n.*link "(.+?)".*\n.*strong.*?: (.+?)\n.*text: "and"\n.*link "(\d+) (?:other )?mutual connections?"',
        r'link "(.+?)".*strong.*?: \1.*text: "and".*link "(.+?)".*text: "(?:are|is) mutual connections?"',
        r'(\d+) followers',
    ]

    for pattern in mutual_patterns:
        mutual_match = re.search(pattern, yaml_text, re.DOTALL)
        if mutual_match:
            if 'followers' in pattern:
                # This is follower count, not mutual connections
                continue
            groups = mutual_match.groups()
            if len(groups) >= 4:
                connection['mutual_connections'] = f"{groups[3]} ({groups[0]}, {groups[2]}, and {groups[3]} others)"
            elif len(groups) >= 2:
                connection['mutual_connections'] = f"2 ({groups[0]} and {groups[1]} are mutual connections)"
            break

    return connection


def format_connection_markdown(number, connection):
    """Format a connection dict as markdown."""
    md = f"\n## {number}. {connection['name']}\n\n"
    if connection['title']:
        md += f"- **Title**: {connection['title']}\n"
    if connection['location']:
        md += f"- **Location**: {connection['location']}\n"
    if connection['mutual_connections']:
        md += f"- **Mutual Connections**: {connection['mutual_connections']}\n"
    md += f"- **Profile**: {connection['profile']}\n"
    return md


def append_to_file(file_path, content, update_footer=True, total_pages=None):
    """Append content to file, optionally updating footer."""
    # Read existing content
    if Path(file_path).exists():
        with open(file_path, 'r') as f:
            existing = f.read()

        # Remove old footer if it exists
        if '**Pages extracted**:' in existing:
            existing = re.sub(r'\n---\n\n\*\*Pages extracted\*\*:.*$', '', existing, flags=re.DOTALL)
    else:
        existing = ""

    # Append new content
    with open(file_path, 'w') as f:
        f.write(existing)
        f.write(content)

        if update_footer and total_pages:
            f.write(f"\n\n---\n\n**Pages extracted**: {total_pages}\n")


def main():
    parser = argparse.ArgumentParser(
        description='Extract LinkedIn connections from Playwright snapshots',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--url', required=True, help='Base LinkedIn search URL')
    parser.add_argument('--pages', required=True, help='Page range (e.g., "61-70" or "5")')
    parser.add_argument('--output', required=True, help='Output markdown file path')
    parser.add_argument('--start-num', type=int, help='Starting connection number')
    parser.add_argument('--auto', action='store_true', help='Auto-detect starting number from file')
    parser.add_argument('--playwright-snapshots', nargs='+', help='Playwright YAML snapshot files or text')

    args = parser.parse_args()

    # Determine starting connection number
    if args.auto:
        start_num = extract_last_connection_number(args.output) + 1
        print(f"Auto-detected starting number: {start_num}")
    elif args.start_num:
        start_num = args.start_num
    else:
        start_num = 1

    # Parse page range
    pages = parse_page_range(args.pages)
    print(f"Processing pages: {pages}")

    # Extract connections
    # Note: This script is designed to work with manual snapshot input
    # In production, integrate with Playwright MCP directly

    print(f"\nScript ready to process {len(pages)} pages starting at connection #{start_num}")
    print(f"Output file: {args.output}")
    print("\nTo use this script with Claude Code:")
    print("1. Navigate to each page with Playwright browser_navigate")
    print("2. Capture snapshot with browser_snapshot")
    print("3. Parse the YAML snapshot to extract connection data")
    print("4. Use this script's functions to format and append to file")

    return 0


if __name__ == '__main__':
    sys.exit(main())
