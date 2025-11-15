#!/usr/bin/env python3
"""
Direct import to Google Sheets using update_cells.
This script will load each batch and print the parameters needed for MCP calls.
"""

import json
import sys

SPREADSHEET_ID = "1h7T4Z_VbzkrZFF9c5vGrJnuC6DHaRUvJAsnWlh5wUEM"
SHEET_NAME = "Sheet1"

def main():
    # Load all 6 batches and prepare them
    for batch_num in range(1, 7):
        batch_data_file = f'/tmp/batch_{batch_num}.json'
        batch_info_file = f'/tmp/batch_{batch_num}_info.json'

        with open(batch_data_file, 'r') as f:
            data = json.load(f)

        with open(batch_info_file, 'r') as f:
            info = json.load(f)

        print(f"\n{'='*60}")
        print(f"BATCH {batch_num}/{info['total_batches']}")
        print(f"Range: {info['range']}")
        print(f"Records: {info['record_count']}")
        print(f"{'='*60}")

        # Output the MCP command parameters as JSON
        mcp_params = {
            "spreadsheet_id": SPREADSHEET_ID,
            "sheet": SHEET_NAME,
            "range": info['range'],
            "data": data
        }

        # Print in a format that can be easily used
        print("\nMCP Parameters:")
        print(json.dumps(mcp_params, ensure_ascii=False, indent=2))

        # Save to individual file for easier loading
        with open(f'/tmp/mcp_params_batch_{batch_num}.json', 'w') as f:
            json.dump(mcp_params, f, ensure_ascii=False)

        print(f"\nSaved to: /tmp/mcp_params_batch_{batch_num}.json")

    print(f"\n{'='*60}")
    print("All batch parameters prepared!")
    print("='*60}\n")

if __name__ == '__main__':
    main()
