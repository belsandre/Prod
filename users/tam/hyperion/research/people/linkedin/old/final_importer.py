#!/usr/bin/env python3
"""
Final importer - outputs instructions for manual MCP calls or automation.
Since we cannot programmatically call MCP tools from Python, this script
prepares the data and provides instructions.
"""

import json

SPREADSHEET_ID = "1h7T4Z_VbzkrZFF9c5vGrJnuC6DHaRUvJAsnWlh5wUEM"
SHEET_NAME = "Sheet1"

def main():
    print("=" * 70)
    print("LINKEDIN CONNECTIONS IMPORT - FINAL EXECUTION PLAN")
    print("=" * 70)
    print()

    # Load and prepare each batch
    for batch_num in range(1, 6):
        batch_file = f'/tmp/med_batch_{batch_num}.json'

        with open(batch_file, 'r') as f:
            batch = json.load(f)

        print(f"\n{'─' * 70}")
        print(f"BATCH {batch_num}/5")
        print(f"{'─' * 70}")
        print(f"Range: {batch['range']}")
        print(f"Records: {batch['count']}")
        print(f"First record: {batch['data'][0][0]}")
        print(f"Last record: {batch['data'][-1][0]}")
        print()

        # Create compact JSON for the data parameter
        data_json = json.dumps(batch['data'], ensure_ascii=False, separators=(',', ':'))

        # Save to individual file
        output_file = f'/tmp/batch_{batch_num}_data.json'
        with open(output_file, 'w') as f:
            f.write(data_json)

        print(f"✓ Data saved to: {output_file}")
        print(f"✓ Size: {len(data_json) / 1024:.1f} KB")
        print()
        print("MCP Call Parameters:")
        print(f"  spreadsheet_id: {SPREADSHEET_ID}")
        print(f"  sheet: {SHEET_NAME}")
        print(f"  range: {batch['range']}")
        print(f"  data: <load from {output_file}>")

    print()
    print("=" * 70)
    print("NEXT STEPS:")
    print("=" * 70)
    print("1. For each batch (1-5), make an mcp__google-sheets__update_cells call")
    print("2. Use the parameters shown above")
    print("3. Load the data array from the corresponding batch_X_data.json file")
    print()
    print("After all 5 batches are imported successfully:")
    print("- Total rows in sheet: 1040 (1 header + 1039 data)")
    print("- Verify by checking the last few rows match the source")
    print("=" * 70)

if __name__ == '__main__':
    main()
