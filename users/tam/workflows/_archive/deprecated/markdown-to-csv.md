# Markdown to CSV Converter Workflow

**Purpose**: Convert structured markdown data to CSV format for spreadsheet import or data analysis
**Input**: Markdown file with structured format (numbered lists, field-value pairs, or tables)
**Output**: Clean CSV file with validated data
**Version**: 2.0
**Maintainer**: tam

---

## Overview

This workflow converts structured markdown data into CSV format using a robust Python converter (`md_to_csv.py`). The resulting CSV can be imported into Google Sheets, Excel, or any spreadsheet application, or used for data analysis.

**Key Features**:
- **Auto-format detection** - works with 3 common markdown structures
- **Data validation** - ensures consistency before output
- **Faithful extraction** - preserves all data exactly as written
- **Flexible output** - customizable fields, delimiters, encodings
- **Error handling** - clear messages for troubleshooting

**Supported Formats**:
1. **Numbered bullets** - `## 1. Name` with `- **Field**: Value` bullets
2. **Field-value pairs** - `**Field**: Value` separated by `---`
3. **Markdown tables** - Standard `| Column | Column |` format

---

## When to Use

Use this workflow when you need to:
- Convert LinkedIn connection exports to spreadsheet format
- Extract structured research data from markdown files
- Transform markdown tables into importable CSV
- Prepare markdown data for database import
- Create spreadsheet-ready datasets from documented sources

**Prerequisites**:
- Markdown file with consistent structured format
- Python 3.7+ installed
- Access to `md_to_csv.py` script (located in `users/tam/hyperion/workflows/`)

**NOT suitable for**:
- Unstructured narrative text
- Mixed-format markdown documents
- Real-time streaming data

---

## Input Format Examples

### Format 1: Numbered Bullets (LinkedIn-style)

```markdown
# LinkedIn Connections

## 1. Jane Doe

- **Title**: CEO at Acme Corp
- **Location**: San Francisco, CA
- **Mutual Connections**: 42 (John Smith, Alice Johnson, and 40 others)
- **Profile**: https://linkedin.com/in/janedoe

## 2. Bob Smith

- **Title**: CTO at Tech Startup
- **Location**: Austin, TX
- **Mutual Connections**: 15 (Jane Doe, Charlie Brown, and 13 others)
- **Profile**: https://linkedin.com/in/bobsmith
```

**Output columns**: Name, Location, Mutual Connections, Profile, Title (auto-sorted)

### Format 2: Field-Value Pairs

```markdown
**Company**: Acme Corporation
**Sector**: Enterprise Software
**Valuation**: $500M
**Founded**: 2018

---

**Company**: Beta Industries
**Sector**: Hardware
**Valuation**: $200M
**Founded**: 2020
```

**Output columns**: Company, Founded, Sector, Valuation (auto-sorted)

### Format 3: Markdown Table

```markdown
| Company Name | Sector | Employees | Revenue |
|--------------|--------|-----------|---------|
| Acme Corp    | SaaS   | 250       | $50M    |
| Beta Inc     | Hardware | 100     | $20M    |
```

**Output columns**: Company Name, Sector, Employees, Revenue (preserves order)

---

## Workflow Steps

### Phase 1: Preparation

#### Step 1.1: Verify Input File

**Prompt to Claude**:
```
I have a markdown file with structured data that I need to convert to CSV.

File location: [PASTE FILE PATH]

Please:
1. Read the file and show me the first 3-5 records
2. Identify what format it uses (numbered bullets, field-value pairs, or table)
3. List the field names that will become CSV columns
4. Confirm the file is suitable for conversion
```

**Expected Output**:
- File preview
- Detected format
- List of field names
- Record count estimate

**Example**:
```
✓ Format detected: numbered_bullets
✓ Fields found: Name, Title, Location, Mutual Connections, Profile
✓ Estimated records: ~1,039
✓ File is suitable for conversion
```

---

### Phase 2: Conversion

#### Step 2.1: Run the Converter Script

**Prompt to Claude**:
```
Please convert this markdown file to CSV using the md_to_csv.py script:

Input file: [FILE PATH]
Output file: [DESIRED OUTPUT PATH].csv

Options:
- Enable validation (--validate flag)
- Use auto-format detection

Command to run:
python users/tam/hyperion/workflows/md_to_csv.py [INPUT] [OUTPUT] --validate
```

**Expected Output**:
```
✓ Read 275,955 characters from connections.md
✓ Detected format: numbered_bullets
✓ Extracted 1,039 records with 5 fields

⚠ Warning: Found empty fields:
  Title: 1 empty values

✓ Validation passed
✓ Wrote CSV to connections.csv

Summary:
  Records: 1,039
  Fields: Name, Title, Location, Mutual Connections, Profile
  File size: 193.4 KB
```

#### Step 2.2: Verify Output Quality

**Prompt to Claude**:
```
Please verify the CSV output:

1. Show me the first 5 rows
2. Show me the last 3 rows
3. Confirm the record count matches the source
4. Check for any obvious data quality issues
```

**Expected Output**:
- Header row with correct field names
- Sample data rows properly formatted
- Confirmation that counts match
- Any warnings about empty fields or formatting issues

---

### Phase 3: Import to Spreadsheet (Manual)

#### Step 3.1: Google Sheets Import

**Steps**:
1. Open Google Sheets: https://sheets.google.com
2. Create new sheet or open existing
3. **File** → **Import**
4. **Upload** tab
5. Select your CSV file
6. **Import location**:
   - "Create new spreadsheet" - fresh import
   - "Insert new sheet" - add to existing workbook
   - "Append to current sheet" - add rows to existing data
   - "Replace current sheet" - overwrite existing
7. **Separator type**: Comma
8. **Convert text to numbers**: Recommended to UNCHECK (preserves leading zeros, etc.)
9. Click **Import data**

**Result**: Data appears in spreadsheet with proper column headers

#### Step 3.2: Post-Import Cleanup (Optional)

Common cleanup tasks:
- Freeze header row (View → Freeze → 1 row)
- Adjust column widths (double-click column borders)
- Apply filters (Data → Create a filter)
- Format URLs as hyperlinks (if not auto-detected)
- Sort by specific columns
- Remove duplicates if needed

---

## Advanced Usage

### Custom Field Selection

If you only want specific fields from field-value pairs format:

**Prompt to Claude**:
```
Please convert this markdown to CSV, extracting ONLY these fields:
- Name
- Title
- Profile

Use the --fields flag:
python md_to_csv.py input.md output.csv --fields "Name,Title,Profile"
```

### TSV Output (Tab-Separated)

For Excel compatibility or when data contains many commas:

**Prompt to Claude**:
```
Please create a TSV file instead of CSV using the --delimiter flag:

python md_to_csv.py input.md output.tsv --delimiter $'\t'
```

### Skip Header Row

If appending to existing CSV with headers:

**Prompt to Claude**:
```
Please convert without writing a header row:

python md_to_csv.py input.md output.csv --skip-header
```

### Batch Conversion

For multiple markdown files:

**Prompt to Claude**:
```
Please convert all markdown files in this directory to CSV:

Directory: [PATH]
Pattern: *.md

For each file, create a corresponding .csv file with the same name.
```

---

## Troubleshooting

### Issue: "No data extracted from markdown"

**Symptoms**: Script runs but says 0 records found

**Causes**:
- Markdown format doesn't match any supported pattern
- Inconsistent formatting (mixed bullet styles, irregular spacing)
- Missing required patterns (no `##` headers, no `**Field**:` markers)

**Solutions**:
1. Verify format manually - check first few records
2. Look for format consistency issues
3. Try specifying format explicitly: `--format numbered_bullets`
4. Check for unusual characters or encoding issues

### Issue: "Validation error: Row X has Y fields, expected Z"

**Symptoms**: Some records have different number of fields

**Causes**:
- Inconsistent field names across records
- Some records missing fields
- Extra fields in some records

**Solutions**:
1. Run without `--validate` to see the raw output
2. Review source markdown for inconsistencies
3. Standardize field names (check for typos, extra spaces)
4. Add missing fields to incomplete records
5. If acceptable, proceed without validation and handle in spreadsheet

### Issue: "Data contains commas - columns misaligned"

**Symptoms**: CSV columns don't line up in spreadsheet

**Causes**:
- Commas in data values confusing CSV parser
- Script should auto-quote these, but import tool might not handle correctly

**Solutions**:
1. Verify CSV uses proper quoting (open in text editor)
2. Try TSV format instead: `--delimiter $'\t'`
3. When importing to Google Sheets, ensure "Comma" is selected as separator
4. Try different spreadsheet import tool

### Issue: "Special characters display incorrectly"

**Symptoms**: Emojis, accents, or symbols show as garbled text

**Causes**:
- Encoding mismatch between CSV and spreadsheet
- CSV created with non-UTF-8 encoding

**Solutions**:
1. Ensure script uses UTF-8: `--encoding utf-8` (default)
2. When importing to Google Sheets, select "UTF-8" encoding
3. Save source markdown as UTF-8 before conversion
4. For Excel: Use "Get Data" → "From Text/CSV" and select UTF-8

### Issue: "Empty fields in output"

**Symptoms**: Warning about empty fields, or blanks in CSV

**Expected Behavior**: If source markdown doesn't have a field for every record, that's normal

**Solutions**:
1. Review source data - add missing fields if needed
2. If acceptable, proceed (spreadsheet can handle empty cells)
3. Use validation warnings to identify which fields are commonly empty
4. Consider removing rarely-used fields: `--fields "Field1,Field2"`

---

## Script Reference

### Location
```
users/tam/hyperion/workflows/md_to_csv.py
```

### Full Usage
```bash
python md_to_csv.py INPUT OUTPUT [OPTIONS]

Required:
  INPUT                 Path to input markdown file
  OUTPUT                Path to output CSV file

Options:
  --format FORMAT       Force format: auto, numbered_bullets, field_pairs, table
                        (default: auto)

  --fields FIELDS       Comma-separated list of fields to extract
                        Example: "Name,Title,Email"

  --validate            Validate all records have same field count
                        Warns about empty fields

  --skip-header         Don't write CSV header row
                        Useful when appending to existing CSV

  --encoding ENCODING   Input file encoding (default: utf-8)
                        Common: utf-8, latin-1, cp1252

  --delimiter CHAR      CSV delimiter character (default: comma)
                        For TSV use: --delimiter $'\t'

  --quiet               Suppress output except errors
                        Useful in scripts/automation
```

### Examples

**Basic conversion with validation**:
```bash
python users/tam/hyperion/workflows/md_to_csv.py \
  users/tam/hyperion/research/people/linkedin/connections.md \
  users/tam/hyperion/research/people/linkedin/connections.csv \
  --validate
```

**Extract specific fields only**:
```bash
python users/tam/hyperion/workflows/md_to_csv.py \
  input.md output.csv \
  --fields "Name,Company,Email,Phone" \
  --validate
```

**Create TSV for Excel**:
```bash
python users/tam/hyperion/workflows/md_to_csv.py \
  input.md output.tsv \
  --delimiter $'\t'
```

**Force specific format**:
```bash
python users/tam/hyperion/workflows/md_to_csv.py \
  input.md output.csv \
  --format field_pairs
```

**Quiet mode for automation**:
```bash
python users/tam/hyperion/workflows/md_to_csv.py \
  input.md output.csv \
  --quiet

if [ $? -eq 0 ]; then
  echo "Conversion successful"
else
  echo "Conversion failed"
fi
```

---

## Quality Standards

To ensure high-quality CSV output:

1. **Faithful Data Extraction**
   - [ ] All records from source markdown present in CSV
   - [ ] No data transformations or modifications
   - [ ] Special characters preserved (emojis, accents, symbols)
   - [ ] URLs intact and unmodified

2. **Format Correctness**
   - [ ] CSV header row matches extracted fields
   - [ ] All rows have same number of columns
   - [ ] Commas in data properly quoted
   - [ ] Newlines in data properly escaped

3. **Data Validation**
   - [ ] Record count matches source (±1 for header)
   - [ ] First and last records verified against source
   - [ ] Empty fields documented and acceptable
   - [ ] No truncated data

4. **Import Compatibility**
   - [ ] CSV imports cleanly to Google Sheets
   - [ ] Columns align correctly
   - [ ] No encoding issues
   - [ ] URLs clickable (if desired)

**Validation Checklist**:
```
✓ Source file readable and properly formatted
✓ Format detected correctly (or specified)
✓ All expected fields present in output
✓ Record count matches: [SOURCE COUNT] = [CSV COUNT - 1 header]
✓ Spot check first, middle, last records
✓ Empty fields reviewed and acceptable
✓ CSV opens correctly in text editor
✓ CSV imports correctly to spreadsheet
✓ Special characters display properly
✓ No data truncation or corruption
```

---

## Complete Example Session

### Scenario: Convert LinkedIn Connections Export

**User**: I have LinkedIn connections in markdown format and need them in Google Sheets.

**Claude**: Let me help you convert that. First, let me examine the file:

```
Reading: users/tam/hyperion/research/people/linkedin/connections.md

Found format: Numbered bullets (## 1. Name with - **Field**: Value)

Preview:
## 1. Jack Moshkovich
- **Title**: Partner at 8VC
- **Location**: Stanford, California, United States
- **Mutual Connections**: 110 (Arjun Chopra, Mercedes Chatfield-Taylor, and 108 others)
- **Profile**: https://www.linkedin.com/in/jack-moshkovich-b623ab149/

Fields detected: Name, Title, Location, Mutual Connections, Profile
Estimated records: 1,039

✓ File is suitable for conversion
```

Now converting to CSV with validation...

```bash
python users/tam/hyperion/workflows/md_to_csv.py \
  users/tam/hyperion/research/people/linkedin/connections.md \
  users/tam/hyperion/research/people/linkedin/connections.csv \
  --validate
```

**Output**:
```
✓ Read 275,955 characters from connections.md
✓ Detected format: numbered_bullets
✓ Extracted 1,039 records with 5 fields

⚠ Warning: Found empty fields:
  Title: 1 empty values

✓ Validation passed
✓ Wrote CSV to connections.csv

Summary:
  Records: 1,039
  Fields: Name, Location, Mutual Connections, Profile, Title
  File size: 193.4 KB
```

Verifying output quality...

```csv
Name,Location,Mutual Connections,Profile,Title
Jack Moshkovich,"Stanford, California, United States","110 (Arjun Chopra, Mercedes Chatfield-Taylor, and 108 others)",https://www.linkedin.com/in/jack-moshkovich-b623ab149/,Partner at 8VC
Jesse Beller,"Los Angeles, California, United States","11 (Mercedes Bent, Vaughn Blake, and 9 others)",https://www.linkedin.com/in/jesse-beller-69182175/,Founder & CEO @ Terrace
...
Andrew Musk,"San Francisco, California, United States","13 (Hugo Amsellem, Sam Teller, and 11 others)",https://www.linkedin.com/in/andrew-musk/,Engineering at X
```

✓ CSV created successfully
✓ 1,039 records (matches source)
✓ 5 columns with proper headers
✓ Data properly quoted and escaped
✓ Ready for import to Google Sheets

**Next steps**:
1. Open: https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit
2. File → Import → Upload
3. Select `connections.csv`
4. Choose "Append to current sheet" or "Replace current sheet"
5. Click Import

---

## Version History

**v2.0** (2025-11-14)
- Complete rewrite: removed Google Sheets MCP dependency
- Now generates CSV files for manual import
- Added robust `md_to_csv.py` Python converter
- Support for 3 markdown format types
- Auto-format detection
- Data validation and quality checks
- Comprehensive error handling and troubleshooting guide

**v1.0** (2025-11-14) [Deprecated]
- Used Google Sheets MCP for direct import
- Limited to field-value pairs format
- No validation support

---

## Related Workflows

- **vc-research.md**: Generates markdown research that can be converted to CSV
- **validator.md**: Can validate markdown files before conversion
- **conflict-resolver.md**: Resolves data conflicts in source markdown

## See Also

- Python CSV module documentation
- Google Sheets import documentation
- Markdown formatting standards
