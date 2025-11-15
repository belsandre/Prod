#!/usr/bin/env python3
"""
Import parsed connections data to Google Sheets in batches.
Uses the Google Sheets MCP via command-line calls.
"""

import json
import sys

def load_data(json_file):
    """Load parsed data from JSON file."""
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def chunk_data(data, chunk_size=100):
    """Split data into chunks for batch processing."""
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

def format_range(start_row, end_row, end_col='E'):
    """Format A1 notation range."""
    return f"A{start_row}:{end_col}{end_row}"

if __name__ == '__main__':
    # Load the data
    data = load_data('/tmp/parsed_clean.json')
    print(f"Total records to import: {len(data)}", file=sys.stderr)

    # Split into manageable chunks
    chunks = list(chunk_data(data, chunk_size=100))
    print(f"Split into {len(chunks)} chunks of ~100 records each", file=sys.stderr)

    # Print import commands for each chunk
    current_row = 2  # Start at row 2 (after header)

    for i, chunk in enumerate(chunks):
        end_row = current_row + len(chunk) - 1
        range_notation = format_range(current_row, end_row)

        print(f"\n# Chunk {i+1}/{len(chunks)}: Rows {current_row}-{end_row}", file=sys.stderr)
        print(f"# Range: {range_notation}", file=sys.stderr)
        print(f"# Records: {len(chunk)}", file=sys.stderr)

        # Output the chunk data as JSON
        print(json.dumps({
            "chunk": i + 1,
            "total_chunks": len(chunks),
            "range": range_notation,
            "data": chunk
        }, ensure_ascii=False))

        current_row = end_row + 1

    print(f"\n# Import plan complete", file=sys.stderr)
    print(f"# Final row will be: {current_row - 1} (1 header + {len(data)} data rows)", file=sys.stderr)
