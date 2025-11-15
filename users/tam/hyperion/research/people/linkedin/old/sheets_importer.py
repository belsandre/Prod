#!/usr/bin/env python3
"""
Import LinkedIn connections to Google Sheets.
Uses the batch_update_cells MCP to import all data at once.
"""

import json

def main():
    # Load all data
    with open('/tmp/parsed_clean.json', 'r') as f:
        all_data = json.load(f)

    spreadsheet_id = "1h7T4Z_VbzkrZFF9c5vGrJnuC6DHaRUvJAsnWlh5wUEM"
    sheet_name = "Sheet1"

    # For batch_update_cells, we need ranges as a dictionary
    # Format: { "A2:E1040": [[data], [data], ...] }

    ranges_dict = {
        f"A2:E{len(all_data) + 1}": all_data
    }

    print(f"Spreadsheet ID: {spreadsheet_id}")
    print(f"Sheet: {sheet_name}")
    print(f"Total records: {len(all_data)}")
    print(f"Range: A2:E{len(all_data) + 1}")
    print(f"\nFirst 3 records:")
    for i, record in enumerate(all_data[:3]):
        print(f"  {i+1}. {record[0]} - {record[1]}")

    # Save the ranges dict for the MCP call
    output = {
        "spreadsheet_id": spreadsheet_id,
        "sheet": sheet_name,
        "ranges": ranges_dict
    }

    with open('/tmp/batch_import_params.json', 'w') as f:
        json.dump(output, f, ensure_ascii=False)

    print(f"\n✓ Parameters saved to /tmp/batch_import_params.json")
    print(f"✓ Ready to import {len(all_data)} records")

if __name__ == '__main__':
    main()
