#!/usr/bin/env python3
"""
Parse LinkedIn connections markdown file into structured data for Google Sheets import.
"""

import re
import json

def parse_connections(md_file_path):
    """
    Parse LinkedIn connections from markdown file.

    Expected format:
    ## Number. Name
    - **Title**: Value
    - **Location**: Value
    - **Mutual Connections**: Value
    - **Profile**: URL
    """
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by connection entries (## Number. Name pattern)
    entries = re.split(r'\n## \d+\.\s+', content)

    records = []

    for entry in entries[1:]:  # Skip first split (header section)
        lines = entry.strip().split('\n')
        if not lines:
            continue

        # First line is the name
        name = lines[0].strip()

        # Initialize record with name
        record = {
            'Name': name,
            'Title': '',
            'Location': '',
            'Mutual Connections': '',
            'Profile': ''
        }

        # Parse bullet points for fields
        for line in lines[1:]:
            line = line.strip()

            # Match - **FieldName**: Value pattern
            match = re.match(r'-\s*\*\*(.+?)\*\*:\s*(.+)', line)
            if match:
                field_name = match.group(1).strip()
                field_value = match.group(2).strip()

                # Map to our record fields
                if field_name in record:
                    record[field_name] = field_value

        # Convert to array in correct column order
        row = [
            record['Name'],
            record['Title'],
            record['Location'],
            record['Mutual Connections'],
            record['Profile']
        ]

        records.append(row)

    return records

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python parse_connections.py <md_file_path>")
        sys.exit(1)

    md_file = sys.argv[1]
    records = parse_connections(md_file)

    # Output as JSON for easy consumption
    print(json.dumps(records, indent=2, ensure_ascii=False))
    print(f"\n# Total records parsed: {len(records)}", file=sys.stderr)
