#!/usr/bin/env python3
"""
Fix duplicate Firm and Role columns in the CSV file.
"""

import csv
import sys

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 fix_duplicates.py <input_csv> <output_csv>")
        print("\nExample:")
        print("  python3 fix_duplicates.py connections.csv connections_fixed.csv")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    rows = []
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)

        # Get unique fieldnames (removing duplicates while preserving order)
        seen = set()
        unique_fieldnames = []
        for field in reader.fieldnames:
            if field not in seen:
                seen.add(field)
                unique_fieldnames.append(field)

        for row in reader:
            # Create new row with unique fields only (take first occurrence)
            new_row = {}
            for field in unique_fieldnames:
                if field in row:
                    new_row[field] = row[field]
            rows.append(new_row)

    # Write back
    with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=unique_fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✓ Fixed duplicate columns")
    print(f"✓ New header: {', '.join(unique_fieldnames)}")
    print(f"✓ Total rows: {len(rows)}")
    print(f"✓ Output saved to: {output_file}")
