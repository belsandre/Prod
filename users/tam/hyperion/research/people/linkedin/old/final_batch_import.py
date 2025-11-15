#!/usr/bin/env python3
"""
Final batch import script - generates importable data for each batch.
Outputs compact JSON that can be used in MCP tool calls.
"""

import json
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python final_batch_import.py <batch_num>")
        print("  batch_num: 1-5")
        sys.exit(1)

    batch_num = int(sys.argv[1])

    if batch_num < 1 or batch_num > 5:
        print(f"Error: batch_num must be between 1 and 5, got {batch_num}")
        sys.exit(1)

    # Load the specified batch
    batch_file = f'/tmp/med_batch_{batch_num}.json'

    try:
        with open(batch_file, 'r') as f:
            batch = json.load(f)
    except FileNotFoundError:
        print(f"Error: Batch file not found: {batch_file}")
        sys.exit(1)

    # Output batch info to stderr
    print(f"Batch {batch_num}/5", file=sys.stderr)
    print(f"Range: {batch['range']}", file=sys.stderr)
    print(f"Records: {batch['count']}", file=sys.stderr)
    print(f"First: {batch['data'][0][0]}", file=sys.stderr)
    print(f"Last: {batch['data'][-1][0]}", file=sys.stderr)
    print(f"", file=sys.stderr)

    # Output the data array as compact JSON to stdout
    # This can be directly used in MCP tool calls
    print(json.dumps(batch['data'], ensure_ascii=False, separators=(',', ':')))

if __name__ == '__main__':
    main()
