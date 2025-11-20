# Google Sheet Importer Workflow

**Purpose**: Import structured markdown data to Google Sheets with faithful data preservation
**Input**: Markdown file with `**Field**: Value` format + Google Sheets URL
**Output**: Data appended to specified Google Sheet
**Version**: 1.0
**Maintainer**: tam

---

## Overview

This workflow enables automated import of structured markdown data into Google Sheets using the Google Sheets MCP. It parses markdown files containing structured field-value pairs and appends them to an existing Google Sheet, preserving data integrity and maintaining existing sheet data.

**Key Features**:
- Parses `**Field**: Value` structured markdown format
- Automatically maps markdown fields to sheet columns
- Appends data without overwriting existing records
- Handles multi-record markdown files
- Preserves exact data from source (no transformations)

---

## When to Use

Use this workflow when you need to:
- Import LinkedIn connection data from markdown to Google Sheets
- Transfer structured research data from markdown files to spreadsheets
- Bulk upload field-based records to Google Sheets
- Sync markdown-based data sources with collaborative spreadsheets

**Prerequisites**:
- Markdown file with structured `**Field**: Value` format
- Google Sheets URL with edit permissions
- Google Sheets MCP enabled (`/mcp` to enable if needed)
- Target sheet must have column headers matching markdown field names

---

## Input Format

### Expected Markdown Structure

The input markdown file should contain records with structured fields in this format:

```markdown
# Record Title (Optional - used for grouping)

**Field Name 1**: Value 1
**Field Name 2**: Value 2
**Field Name 3**: Value 3

---

**Field Name 1**: Another Value 1
**Field Name 2**: Another Value 2
**Field Name 3**: Another Value 3
```

### Example: LinkedIn Connections

```markdown
# LinkedIn Connections

**Name**: John Doe
**Company**: Acme Corp
**Position**: CEO
**Connected On**: 2025-01-15
**Email**: john@acme.com
**LinkedIn URL**: https://linkedin.com/in/johndoe

---

**Name**: Jane Smith
**Company**: Tech Startup Inc
**Position**: CTO
**Connected On**: 2025-02-20
**Email**: jane@techstartup.com
**LinkedIn URL**: https://linkedin.com/in/janesmith
```

**Record Separators**: Use `---` (horizontal rule) or blank lines + headers to separate records

---

## Workflow Steps

### Phase 1: Preparation

#### Step 1.1: Verify Inputs

**Prompt to Claude**:
```
I need to import data from a markdown file to Google Sheets.

Input file: [PASTE FILE PATH]
Google Sheets URL: [PASTE URL]

Please:
1. Read the markdown file
2. Extract the spreadsheet ID from the URL
3. Confirm the file format matches the expected structure
4. Show me a preview of the first 2-3 records found
```

**Expected Output**:
- Confirmation of file read
- Spreadsheet ID extracted (e.g., `1h7T4Z_VbzkrZFF9c5vGrJnuC6DHaRUvJAsnWlh5wUEM`)
- Preview of parsed records
- Field names identified

---

### Phase 2: Sheet Setup

#### Step 2.1: Inspect Target Sheet

**Prompt to Claude**:
```
Now inspect the Google Sheet to understand its structure:

1. List all sheets in the spreadsheet
2. Get the current data from the target sheet (or specify sheet name if not default)
3. Identify existing column headers
4. Show me how many rows currently exist
```

**Expected Output**:
- List of sheet tabs
- Current headers in target sheet
- Row count (to determine where to append)

#### Step 2.2: Map Fields to Columns

**Prompt to Claude**:
```
Map the markdown fields to the Google Sheet columns:

Markdown fields: [List from Step 1.1]
Sheet columns: [List from Step 2.1]

Please:
1. Create a mapping between markdown field names and sheet column headers
2. Identify any markdown fields that don't have matching columns
3. Identify any sheet columns that won't be populated
4. Show me the mapping table
```

**Expected Output**:
```
Field Mapping:
- **Name** → Column A (Name)
- **Company** → Column B (Company)
- **Position** → Column C (Title)
- **Connected On** → Column D (Date)
- **Email** → Column E (Email)
- **LinkedIn URL** → Column F (Profile URL)

Unmapped markdown fields: None
Unpopulated sheet columns: Column G (Notes)
```

---

### Phase 3: Data Import

#### Step 3.1: Parse and Structure Data

**Prompt to Claude**:
```
Parse all records from the markdown file and structure them for import:

1. Extract all records from the markdown file
2. For each record, extract field-value pairs
3. Build a 2D array where each row represents one record
4. Order columns according to the sheet's column sequence
5. Handle missing fields by using empty strings
6. Show me the first 3 rows of the structured data array
```

**Expected Output**:
```python
[
    ["John Doe", "Acme Corp", "CEO", "2025-01-15", "john@acme.com", "https://linkedin.com/in/johndoe", ""],
    ["Jane Smith", "Tech Startup Inc", "CTO", "2025-02-20", "jane@techstartup.com", "https://linkedin.com/in/janesmith", ""],
    ...
]
```

#### Step 3.2: Execute Import

**Prompt to Claude**:
```
Now append the data to the Google Sheet:

1. Determine the starting row (current row count + 1)
2. Determine the range for the import (e.g., A{start_row}:G{end_row})
3. Use mcp__google-sheets__update_cells to append all rows in one operation
4. Verify the import was successful
5. Report the final row count and number of records added
```

**Implementation Note**: Use the `update_cells` tool with the calculated range:

```python
# Example:
# If sheet has 5 rows (including header) and we're adding 10 records:
# Starting row: 6
# Range: "A6:G15" (assuming 7 columns)
# Data: 2D array with 10 rows × 7 columns
```

---

### Phase 4: Verification

#### Step 4.1: Confirm Import

**Prompt to Claude**:
```
Verify the import was successful:

1. Read the last 5 rows from the Google Sheet
2. Compare them against the last 5 records from the markdown file
3. Confirm all fields were copied faithfully
4. Report any discrepancies
```

**Expected Output**:
```
✓ Import successful
✓ Added 47 records
✓ Final row count: 52 (including header)
✓ Spot check: Last 5 records match source data
✓ No discrepancies found
```

---

## Advanced Usage

### Handling Multiple Files

If you need to import multiple markdown files:

**Prompt to Claude**:
```
I have multiple markdown files to import:
- [FILE_PATH_1]
- [FILE_PATH_2]
- [FILE_PATH_3]

Please process each file sequentially:
1. Parse file 1 and append to sheet
2. Parse file 2 and append to sheet
3. Parse file 3 and append to sheet
4. Report total records added from all files
```

### Custom Field Mapping

If field names don't exactly match:

**Prompt to Claude**:
```
Use this custom field mapping:
- Markdown "Full Name" → Sheet column "Name"
- Markdown "Job Title" → Sheet column "Position"
- Markdown "Connection Date" → Sheet column "Connected On"

Apply this mapping when importing the data.
```

### Updating Specific Sheet Tab

If the spreadsheet has multiple tabs:

**Prompt to Claude**:
```
Import the data to the sheet tab named "Q1 2025 Connections" (not the default first sheet).
```

---

## Troubleshooting

### Issue: "Field names don't match column headers"

**Solution**: Either:
1. Modify the markdown file field names to match sheet columns exactly
2. Use custom field mapping (see Advanced Usage)
3. Manually add columns to the Google Sheet to match markdown fields

### Issue: "Data appears in wrong columns"

**Cause**: Column order mismatch between mapping and actual import

**Solution**:
1. Re-run Step 2.2 to verify the mapping
2. Ensure the 2D array in Step 3.1 matches the sheet's column order (A, B, C...)
3. Check that the range in Step 3.2 starts from column A

### Issue: "Some records are missing fields"

**Expected Behavior**: Missing fields should be represented as empty strings in the import

**Verification**:
```
Check the parsed data array in Step 3.1 - each row should have the same number of elements (matching column count), with "" for missing values.
```

### Issue: "Import fails with permission error"

**Solution**:
1. Verify you have edit access to the Google Sheet
2. Check that the spreadsheet ID is correct
3. Ensure Google Sheets MCP is properly authenticated
4. Try accessing the sheet URL directly in a browser

### Issue: "Special characters are corrupted"

**Note**: The MCP should handle UTF-8 properly. If you see corruption:
1. Check the source markdown file encoding (should be UTF-8)
2. Verify special characters display correctly when reading the file
3. Test with a small sample first

---

## Example Complete Session

```
USER: I need to import data from users/tam/hyperion/people/linkedin/connections.md
to https://docs.google.com/spreadsheets/d/1h7T4Z_VbzkrZFF9c5vGrJnuC6DHaRUvJAsnWlh5wUEM/edit#gid=0

CLAUDE: I'll help you import this data. Let me start by reading the markdown file
and extracting the spreadsheet ID...

[Executes Phase 1, Step 1.1]

I've found 47 connection records with these fields:
- Name
- Company
- Position
- Connected On
- Email
- LinkedIn URL

Spreadsheet ID: 1h7T4Z_VbzkrZFF9c5vGrJnuC6DHaRUvJAsnWlh5wUEM

[Executes Phase 2, Steps 2.1-2.2]

The sheet "Sheet1" has 6 columns that perfectly match the markdown fields.
Currently 5 rows (1 header + 4 data rows).

[Executes Phase 3, Steps 3.1-3.2]

Parsed 47 records. Appending to rows 6-52 (range A6:F52)...

[Executes import via MCP]

✓ Successfully imported 47 records
✓ Final row count: 52
✓ All data faithfully copied from source

[Executes Phase 4, Step 4.1]

Verification complete. Last 5 records match source exactly.
Import completed successfully!
```

---

## Quality Standards

To ensure faithful data import:

1. **No Transformations**: Import data exactly as written in markdown
2. **Preserve Empty Fields**: Missing fields → empty cells (not "N/A" or placeholders)
3. **Maintain Order**: Import records in the same order as the markdown file
4. **Exact Text Match**: No trimming, case changes, or formatting modifications
5. **Complete Import**: All records from markdown must appear in sheet

**Validation Checklist**:
- [ ] Record count in sheet matches markdown record count
- [ ] All field names correctly mapped to columns
- [ ] Spot check: First, middle, and last records match source
- [ ] Special characters preserved correctly
- [ ] No duplicate records created
- [ ] Existing sheet data remains unchanged

---

## Technical Notes

### MCP Tools Used

1. **mcp__google-sheets__get_sheet_data**: Read current sheet structure and data
2. **mcp__google-sheets__list_sheets**: Identify available sheet tabs
3. **mcp__google-sheets__update_cells**: Append new data rows
4. **mcp__google-sheets__batch_update_cells**: Alternative for very large imports

### Range Notation

Google Sheets uses A1 notation:
- `A1:F1` = First row, columns A through F (header row)
- `A2:F100` = Rows 2-100, columns A through F (99 data rows)
- `Sheet1!A1:F100` = Specific sheet tab with range

### Parsing Strategy

For `**Field**: Value` format:
1. Use regex: `\*\*([^*]+)\*\*:\s*(.+?)(?=\n|$)`
2. Group records by separators (`---` or blank lines + headers)
3. Build dictionary per record: `{field_name: value}`
4. Convert to array: `[record[col1], record[col2], ...]`

### Performance

- Small imports (<100 records): Single `update_cells` call
- Large imports (100-1000 records): Single `update_cells` call (still fast)
- Very large imports (>1000 records): Consider `batch_update_cells` with chunking

---

## Version History

**v1.0** (2025-11-14)
- Initial release
- Support for `**Field**: Value` markdown format
- Append-only import mode
- Automatic field-to-column mapping
- Multi-record file support

---

## Related Workflows

- **vc-research.md**: Generates structured research data that can be imported
- **validator.md**: Can validate markdown files before import
- **conflict-resolver.md**: Resolves data conflicts before import
