#!/usr/bin/env python3
"""
Convert parsed LinkedIn connections to CSV format.
"""

import json
import csv

def main():
    # Load parsed data
    with open('/tmp/parsed_clean.json', 'r') as f:
        data = json.load(f)

    # Define CSV output file
    output_file = '/Users/changxu/Agents/Prod/users/tam/hyperion/research/people/linkedin/connections.csv'

    # Column headers (matching Google Sheet structure)
    headers = ['Name', 'Title', 'Location', 'Mutual Connections', 'Profile']

    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Write header row
        writer.writerow(headers)

        # Write all data rows
        writer.writerows(data)

    print(f"✓ CSV file created: {output_file}")
    print(f"✓ Total records: {len(data)}")
    print(f"✓ Columns: {', '.join(headers)}")
    print(f"\nYou can now:")
    print(f"1. Open Google Sheets")
    print(f"2. Go to File > Import")
    print(f"3. Upload this CSV file")
    print(f"4. Choose 'Append to current sheet' to add to existing data")
    print(f"   OR 'Replace current sheet' to overwrite")

if __name__ == '__main__':
    main()
