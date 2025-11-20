#!/usr/bin/env python3
"""
Parse LinkedIn connection titles to extract Firm and Role information.
Only fills in data when it's clearly apparent from the title.
"""

import csv
import re
from typing import Tuple, Optional


def parse_title(title: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Parse a LinkedIn title to extract Firm and Role.
    Returns (firm, role) tuple. Returns None for either if not clearly apparent.
    """
    if not title or title.strip() == '':
        return None, None

    title = title.strip()
    firm = None
    role = None

    # Common role keywords to identify job titles (using word boundaries)
    role_keywords = [
        r'\bpartner\b', r'\bgp\b', r'\blp\b', r'\bassociate\b', r'\bprincipal\b',
        r'\bvice president\b', r'\bvp\b', r'\bdirector\b', r'\bmanager\b',
        r'\bfounder\b', r'\bco-founder\b', r'\bchief\b', r'\bhead\b',
        r'\bportfolio manager\b', r'\banalyst\b', r'\binvesting\b',
        r'\bvc\b', r'\bpe\b', r'\bventure capitalist\b',
        r'\bpresident\b', r'\bmanaging director\b', r'\bsenior managing director\b',
        r'\bcfo\b', r'\bceo\b', r'\bcoo\b', r'\bcto\b', r'\bofficer\b', r'\bmember\b'
    ]

    # Special role keyword for "investor" (singular, not "investors")
    role_keywords.append(r'\binvestor\b(?!s)')

    # Common firm-indicating keywords (using word boundaries)
    firm_keywords = [
        r'\bcapital\b', r'\bventures\b', r'\bpartners\b', r'\bventure\b',
        r'\bequity\b', r'\binvestments\b', r'\bmanagement\b', r'\bfund\b',
        r'\bgroup\b', r'\bholdings\b', r'\binvestors\b', r'\badvisors\b',
        r'\badvisers\b', r'\blabs\b', r'\bstudio\b', r'\bstudios\b',
        r'\bcollective\b'
    ]

    # Exclude patterns that are definitely not firms
    exclude_patterns = ['forbes', '30 under 30', 'building the future', 'one investment at a time',
                       'strategic', 'mba', 'phd']

    # Helper function to check if text matches any regex pattern
    def matches_any_pattern(text: str, patterns: list) -> bool:
        text_lower = text.lower()
        return any(re.search(pattern, text_lower, re.IGNORECASE) for pattern in patterns)

    # Pattern 1: "Role at Firm" or "Role @ Firm"
    # Examples: "Partner at 8VC", "GP @ Cyrus Ventures", "Investor at USV"
    pattern_at = r'^(.+?)\s+(?:at|@)\s+(.+?)(?:,|$)'
    match = re.match(pattern_at, title, re.IGNORECASE)
    if match:
        potential_role = match.group(1).strip()
        potential_firm = match.group(2).strip()

        # Only accept if the role looks like a job title
        if matches_any_pattern(potential_role, role_keywords):
            role = potential_role
            firm = potential_firm
            return firm, role

    # Pattern 2: "Role | Firm" (pipe separator, common in LinkedIn)
    # Example: "Private Equity Associate | Apollo Global Management"
    if '|' in title:
        parts = title.split('|')
        if len(parts) == 2:
            potential_role = parts[0].strip()
            potential_firm = parts[1].strip()

            # Check if first part is a role and second part might be a firm
            if matches_any_pattern(potential_role, role_keywords):
                # Don't accept if the "firm" looks like a tagline
                if not any(excl in potential_firm.lower() for excl in exclude_patterns):
                    role = potential_role
                    firm = potential_firm
                    return firm, role

    # Pattern 3: "Role of Firm"
    # Examples: "Founder and Managing Director of Linse Capital"
    pattern_of = r'^(.+?)\s+of\s+(.+?)$'
    match = re.match(pattern_of, title, re.IGNORECASE)
    if match:
        potential_role = match.group(1).strip()
        potential_firm = match.group(2).strip()

        if matches_any_pattern(potential_role, role_keywords):
            role = potential_role
            firm = potential_firm
            return firm, role

    # Pattern 4: "Role, Firm" (comma separator where firm comes after)
    # Examples: "Senior Managing Director, Industry Ventures"
    if ',' in title:
        parts = title.split(',', 1)  # Split on first comma only
        if len(parts) == 2:
            potential_role = parts[0].strip()
            potential_firm = parts[1].strip()

            # Check if first part is a role
            if matches_any_pattern(potential_role, role_keywords):
                # Check if second part might be a firm (has firm keywords or is short enough)
                firm_like = matches_any_pattern(potential_firm, firm_keywords)
                short_enough = len(potential_firm.split()) <= 5
                no_excludes = not any(excl in potential_firm.lower() for excl in exclude_patterns)

                if (firm_like or short_enough) and no_excludes:
                    role = potential_role
                    firm = potential_firm
                    return firm, role

    # Pattern 5: Just a firm name (no role indicators)
    # Examples: "8VC", "BCV", "ArchPoint Investors"
    no_excludes = not any(excl in title.lower() for excl in exclude_patterns)
    has_firm_keyword = matches_any_pattern(title, firm_keywords)
    no_role_keyword = not matches_any_pattern(title, role_keywords)

    if no_excludes and no_role_keyword and len(title.split()) <= 5:
        # Has firm-indicating keyword
        if has_firm_keyword:
            firm = title
            role = None
            return firm, role

        # Common VC/PE firm patterns (e.g., "8VC", "a16z", "USV", "BCV")
        if re.match(r'^[A-Z0-9]{2,6}$', title) or re.match(r'^\d+\w+$', title):
            firm = title
            role = None
            return firm, role

    # If we can't clearly determine, return None for both
    return None, None


def process_csv(input_file: str, output_file: str):
    """
    Read CSV, parse titles, add Firm and Role columns, and save.
    """
    rows_processed = 0
    firms_found = 0
    roles_found = 0

    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)

        # Add new columns to fieldnames (filter out None values if any)
        original_fieldnames = [f for f in reader.fieldnames if f is not None]
        fieldnames = original_fieldnames + ['Firm', 'Role']

        rows = []
        for row in reader:
            title = row.get('Title', '')
            firm, role = parse_title(title)

            # Create a new row with only the valid fieldnames
            new_row = {k: v for k, v in row.items() if k in original_fieldnames}
            new_row['Firm'] = firm if firm else ''
            new_row['Role'] = role if role else ''

            rows.append(new_row)
            rows_processed += 1

            if firm:
                firms_found += 1
            if role:
                roles_found += 1

    # Write to output file
    with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Processing complete!")
    print(f"Total rows processed: {rows_processed}")
    print(f"Firms extracted: {firms_found} ({firms_found/rows_processed*100:.1f}%)")
    print(f"Roles extracted: {roles_found} ({roles_found/rows_processed*100:.1f}%)")
    print(f"Output saved to: {output_file}")


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 3:
        print("Usage: python3 parse_titles.py <input_csv> <output_csv>")
        print("\nExample:")
        print("  python3 parse_titles.py connections.csv connections_with_roles.csv")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    process_csv(input_file, output_file)
