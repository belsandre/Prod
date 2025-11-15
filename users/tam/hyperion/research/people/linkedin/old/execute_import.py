#!/usr/bin/env python3
"""
Execute the import by outputting MCP-compatible JSON for each batch.
"""

import json
import sys

def main():
    spreadsheet_id = "1h7T4Z_VbzkrZFF9c5vGrJnuC6DHaRUvJAsnWlh5wUEM"
    sheet_name = "Sheet1"

    # Load all batches and create a single combined import using batch_update
    all_ranges = {}

    for batch_num in range(1, 12):
        batch_file = f'/tmp/import_batch_{batch_num}.json'
        try:
            with open(batch_file, 'r') as f:
                batch_info = json.load(f)

            range_key = batch_info['range']
            data = batch_info['data']

            all_ranges[range_key] = data

            print(f"✓ Loaded batch {batch_num}: {range_key} ({len(data)} records)", file=sys.stderr)
        except Exception as e:
            print(f"✗ Error loading batch {batch_num}: {e}", file=sys.stderr)
            continue

    print(f"\n✓ Total batches: {len(all_ranges)}", file=sys.stderr)
    print(f"✓ Total ranges: {list(all_ranges.keys())[:3]}... (showing first 3)", file=sys.stderr)

    # Output the complete batch_update parameters
    params = {
        "spreadsheet_id": spreadsheet_id,
        "sheet": sheet_name,
        "ranges": all_ranges
    }

    # Save to file for reference
    with open('/tmp/full_import_params.json', 'w') as f:
        json.dump(params, f, ensure_ascii=False, indent=2)

    print(f"\n✓ Full import parameters saved to /tmp/full_import_params.json", file=sys.stderr)
    print(f"✓ Ready to import {sum(len(v) for v in all_ranges.values())} total records", file=sys.stderr)

    # Also output as compact JSON for direct use
    print("\n" + json.dumps(params, ensure_ascii=False))

if __name__ == '__main__':
    main()
