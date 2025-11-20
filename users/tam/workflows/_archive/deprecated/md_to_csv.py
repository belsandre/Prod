#!/usr/bin/env python3
"""
Markdown to CSV Converter
==========================

A robust, general-purpose tool for converting structured markdown data to CSV format.

Supported markdown formats:
1. Numbered headers with bullet fields:
   ## 1. Record Name
   - **Field**: Value

2. Field-value pairs:
   **Field**: Value
   **Another Field**: Another Value

3. Markdown tables:
   | Column1 | Column2 |
   |---------|---------|
   | Data    | Data    |

Usage:
    python md_to_csv.py input.md output.csv [--format FORMAT] [--fields FIELDS]

Arguments:
    input.md         Input markdown file path
    output.csv       Output CSV file path
    --format         Input format: 'numbered_bullets', 'field_pairs', 'table' (auto-detect if not specified)
    --fields         Comma-separated list of field names to extract (for field_pairs format)
    --skip-header    Skip writing CSV header row
    --validate       Validate all records have same fields before writing
    --encoding       Input file encoding (default: utf-8)
    --delimiter      CSV delimiter (default: comma)
    --quiet          Suppress output except errors

Examples:
    # Auto-detect format and convert
    python md_to_csv.py connections.md connections.csv

    # Specify format explicitly
    python md_to_csv.py data.md data.csv --format numbered_bullets

    # Extract specific fields only
    python md_to_csv.py data.md data.csv --fields "Name,Title,Location,Profile"

    # Validate data consistency
    python md_to_csv.py data.md data.csv --validate

Output:
    - Creates CSV file with extracted data
    - Prints summary statistics
    - Returns exit code 0 on success, 1 on error
"""

import re
import csv
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from collections import Counter


class MarkdownParser:
    """Parse structured markdown into records."""

    @staticmethod
    def detect_format(content: str) -> str:
        """Auto-detect markdown format."""
        # Check for markdown table
        if re.search(r'\|.+\|.+\|', content) and re.search(r'\|[-:| ]+\|', content):
            return 'table'

        # Check for numbered headers with bullets
        if re.search(r'^##\s+\d+\.\s+.+', content, re.MULTILINE):
            return 'numbered_bullets'

        # Check for field-value pairs
        if re.search(r'\*\*[^*]+\*\*:\s*.+', content):
            return 'field_pairs'

        return 'unknown'

    @staticmethod
    def parse_numbered_bullets(content: str) -> Tuple[List[str], List[List[str]]]:
        """
        Parse format:
        ## 1. Name
        - **Field**: Value
        - **Field2**: Value2
        """
        # Split by numbered headers
        entries = re.split(r'\n##\s+\d+\.\s+', content)

        if not entries:
            return [], []

        # First split is metadata before first entry, skip it
        entries = entries[1:] if len(entries) > 1 else entries

        records = []
        all_fields = set()

        for entry in entries:
            lines = entry.strip().split('\n')
            if not lines:
                continue

            # First line is the name/title
            name = lines[0].strip()

            record = {'_name': name}

            # Parse bullet points for fields
            for line in lines[1:]:
                match = re.match(r'-\s*\*\*(.+?)\*\*:\s*(.+)', line.strip())
                if match:
                    field_name = match.group(1).strip()
                    field_value = match.group(2).strip()
                    record[field_name] = field_value
                    all_fields.add(field_name)

            records.append(record)

        # Determine column order: name first, then alphabetically sorted fields
        sorted_fields = ['_name'] + sorted([f for f in all_fields])

        # Convert to rows
        rows = []
        for record in records:
            row = [record.get(field, '') for field in sorted_fields]
            rows.append(row)

        # Create headers (use "Name" instead of "_name")
        headers = ['Name' if f == '_name' else f for f in sorted_fields]

        return headers, rows

    @staticmethod
    def parse_field_pairs(content: str, field_names: Optional[List[str]] = None) -> Tuple[List[str], List[List[str]]]:
        """
        Parse format:
        **Field1**: Value1
        **Field2**: Value2
        ---
        **Field1**: Value3
        **Field2**: Value4
        """
        # Split by separator (--- or double newlines)
        entries = re.split(r'\n---\n|\n\n##|\n\n\n', content)

        # Auto-detect fields if not provided
        if not field_names:
            detected_fields = set()
            for entry in entries:
                matches = re.findall(r'\*\*([^*]+)\*\*:', entry)
                detected_fields.update(matches)
            field_names = sorted(detected_fields)

        records = []

        for entry in entries:
            record = {}

            # Extract all field-value pairs
            matches = re.findall(r'\*\*([^*]+)\*\*:\s*(.+?)(?=\n|$)', entry)
            for field_name, field_value in matches:
                field_name = field_name.strip()
                field_value = field_value.strip()
                if field_name in field_names:
                    record[field_name] = field_value

            # Only add if we found at least one field
            if record:
                records.append(record)

        # Convert to rows
        rows = []
        for record in records:
            row = [record.get(field, '') for field in field_names]
            rows.append(row)

        return field_names, rows

    @staticmethod
    def parse_table(content: str) -> Tuple[List[str], List[List[str]]]:
        """
        Parse markdown table format:
        | Column1 | Column2 |
        |---------|---------|
        | Data1   | Data2   |
        """
        lines = content.split('\n')

        # Find table start
        table_lines = []
        in_table = False

        for line in lines:
            if '|' in line:
                in_table = True
                table_lines.append(line)
            elif in_table and line.strip() == '':
                break

        if len(table_lines) < 3:  # Need header, separator, and at least one data row
            return [], []

        # Parse header
        headers = [col.strip() for col in table_lines[0].split('|') if col.strip()]

        # Parse data rows (skip separator row at index 1)
        rows = []
        for line in table_lines[2:]:
            if '|' in line:
                row = [col.strip() for col in line.split('|') if col.strip()]
                if len(row) == len(headers):
                    rows.append(row)

        return headers, rows


class CSVConverter:
    """Convert markdown to CSV with validation and error handling."""

    def __init__(self, input_path: str, output_path: str, **options):
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        self.options = options
        self.parser = MarkdownParser()

    def convert(self) -> bool:
        """Execute the conversion. Returns True on success."""
        try:
            # Read input file
            encoding = self.options.get('encoding', 'utf-8')
            with open(self.input_path, 'r', encoding=encoding) as f:
                content = f.read()

            if not self.options.get('quiet'):
                print(f"✓ Read {len(content)} characters from {self.input_path}")

            # Detect or use specified format
            fmt = self.options.get('format')
            if not fmt or fmt == 'auto':
                fmt = self.parser.detect_format(content)
                if not self.options.get('quiet'):
                    print(f"✓ Detected format: {fmt}")

            # Parse based on format
            if fmt == 'numbered_bullets':
                headers, rows = self.parser.parse_numbered_bullets(content)
            elif fmt == 'field_pairs':
                field_names = self.options.get('fields')
                if field_names:
                    field_names = [f.strip() for f in field_names.split(',')]
                headers, rows = self.parser.parse_field_pairs(content, field_names)
            elif fmt == 'table':
                headers, rows = self.parser.parse_table(content)
            else:
                print(f"✗ Error: Unknown or unsupported format: {fmt}", file=sys.stderr)
                return False

            if not rows:
                print(f"✗ Error: No data extracted from markdown", file=sys.stderr)
                return False

            if not self.options.get('quiet'):
                print(f"✓ Extracted {len(rows)} records with {len(headers)} fields")

            # Validate if requested
            if self.options.get('validate'):
                if not self._validate_records(headers, rows):
                    return False

            # Write CSV
            delimiter = self.options.get('delimiter', ',')
            with open(self.output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f, delimiter=delimiter)

                # Write header unless skipped
                if not self.options.get('skip_header'):
                    writer.writerow(headers)

                # Write data rows
                writer.writerows(rows)

            if not self.options.get('quiet'):
                print(f"✓ Wrote CSV to {self.output_path}")
                print(f"\nSummary:")
                print(f"  Records: {len(rows)}")
                print(f"  Fields: {', '.join(headers)}")
                print(f"  File size: {self.output_path.stat().st_size / 1024:.1f} KB")

            return True

        except Exception as e:
            print(f"✗ Error: {e}", file=sys.stderr)
            import traceback
            if not self.options.get('quiet'):
                traceback.print_exc()
            return False

    def _validate_records(self, headers: List[str], rows: List[List[str]]) -> bool:
        """Validate record consistency."""
        # Check all rows have same number of fields
        expected_fields = len(headers)

        for i, row in enumerate(rows):
            if len(row) != expected_fields:
                print(f"✗ Validation error: Row {i+1} has {len(row)} fields, expected {expected_fields}", file=sys.stderr)
                return False

        # Check for empty required fields
        empty_counts = Counter()
        for row in rows:
            for i, value in enumerate(row):
                if not value or value.strip() == '':
                    empty_counts[headers[i]] += 1

        if empty_counts and not self.options.get('quiet'):
            print(f"\n⚠ Warning: Found empty fields:")
            for field, count in empty_counts.most_common():
                print(f"  {field}: {count} empty values")

        print(f"✓ Validation passed")
        return True


def main():
    parser = argparse.ArgumentParser(
        description='Convert structured markdown to CSV',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument('input', help='Input markdown file')
    parser.add_argument('output', help='Output CSV file')
    parser.add_argument('--format', choices=['auto', 'numbered_bullets', 'field_pairs', 'table'],
                        default='auto', help='Input format (default: auto-detect)')
    parser.add_argument('--fields', help='Comma-separated field names to extract')
    parser.add_argument('--skip-header', action='store_true', help='Skip CSV header row')
    parser.add_argument('--validate', action='store_true', help='Validate data consistency')
    parser.add_argument('--encoding', default='utf-8', help='Input file encoding')
    parser.add_argument('--delimiter', default=',', help='CSV delimiter character')
    parser.add_argument('--quiet', action='store_true', help='Suppress non-error output')

    args = parser.parse_args()

    # Convert to options dict
    options = {
        'format': args.format,
        'fields': args.fields,
        'skip_header': args.skip_header,
        'validate': args.validate,
        'encoding': args.encoding,
        'delimiter': args.delimiter,
        'quiet': args.quiet
    }

    # Execute conversion
    converter = CSVConverter(args.input, args.output, **options)
    success = converter.convert()

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
