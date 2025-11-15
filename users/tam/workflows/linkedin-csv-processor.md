# LinkedIn CSV Processor - Firm and Role Extraction

## Overview
This workflow processes LinkedIn connections CSV files to automatically extract and add **Firm** and **Role** columns by intelligently parsing the Title field. The processor uses pattern matching and keyword recognition to identify company names and job titles while maintaining a conservative approach—only filling in data when clearly apparent from the title.

## Purpose
- Parse LinkedIn connection exports to structure unstructured title data
- Extract firm names (companies, VC firms, PE firms, etc.)
- Extract role/position information
- Maintain data quality by avoiding guesses when information is ambiguous

## Input Requirements
- A CSV file containing LinkedIn connections data
- Must have at minimum a "Title" column
- Typical LinkedIn export format with columns: Name, Degree Connection, Title, Location, etc.

## Output
- The same CSV file with two additional columns appended:
  - **Firm**: The company/organization name
  - **Role**: The job title/position
- Both columns will be blank if the information cannot be clearly determined from the Title field

## Processing Instructions

When the user provides a LinkedIn connections CSV file, follow these steps:

### 1. Locate or Create the Parser Script

First, check if the parser script exists. If not, create it:

**File location**: `users/tam/workflows/parse_titles.py`

**Script functionality**:
- Parses title strings using multiple pattern-matching strategies
- Uses word boundary regex matching to distinguish similar keywords (e.g., "investor" vs "investors")
- Recognizes common patterns:
  - "Role at Firm" or "Role @ Firm"
  - "Role | Firm" (pipe separator)
  - "Role of Firm"
  - "Role, Firm" (comma separator)
  - Standalone firm names (with keywords like Capital, Ventures, Partners, Investors, etc.)
- Employs role keywords (partner, GP, associate, principal, investor, VP, director, founder, CEO, etc.)
- Employs firm keywords (capital, ventures, partners, equity, fund, management, etc.)
- Excludes non-firm patterns (Forbes 30 under 30, taglines, etc.)

**Usage**:
```bash
python3 users/tam/workflows/parse_titles.py <input_csv> <output_csv>
```

### 2. Verify CSV Structure

Read the first few rows of the CSV to confirm:
- File format is valid CSV
- "Title" column exists
- Understand the data structure

### 3. Run the Parser

Execute the Python script to process the CSV:
```bash
python3 users/tam/workflows/parse_titles.py <input_csv> <output_csv>
```

The script should:
- Read the input CSV file
- Parse each Title field
- Add Firm and Role columns
- Save the updated CSV (either overwriting or creating a new file)
- Report statistics (total rows, firms extracted, roles extracted, coverage %)

### 4. Handle Duplicates (if any)

If the script accidentally creates duplicate columns, run a deduplication fix to ensure clean output with unique column headers:

```bash
python3 users/tam/workflows/fix_duplicates.py <input_csv> <output_csv>
```

### 5. Validate Results

Sample the output to verify:
- Firm column correctly identifies company names
- Role column correctly identifies job titles
- Ambiguous titles are left blank (not guessed)
- Common edge cases are handled properly:
  - Standalone firm names (e.g., "8VC", "ArchPoint Investors")
  - Pipe separators (e.g., "Associate | Apollo Global Management")
  - Comma separators (e.g., "Senior Managing Director, Industry Ventures")
  - Multiple roles (e.g., "GP @ Cyrus Ventures, Principal at JDY Capital" - extracts first one)

### 6. Report Results

Provide the user with:
- Total number of rows processed
- Number and percentage of firms successfully extracted
- Number and percentage of roles successfully extracted
- Sample of results showing before/after for a few representative entries
- Any notable patterns or edge cases encountered

## Quality Standards

**Conservative Parsing**: Only fill in Firm/Role when clearly identifiable. Blank is better than a guess.

**Pattern Recognition**: The script should recognize:
- Common VC/PE firm naming patterns
- Standard job title formats
- LinkedIn-specific formatting (@ symbols, pipe separators)

**Edge Case Handling**:
- Multi-word firm names (e.g., "Bain Capital Ventures")
- Hyphenated roles (e.g., "Co-founder")
- Abbreviations (e.g., "VP", "GP", "CEO")
- Combined titles (e.g., "Partner, Research at Lux Capital")

## Expected Coverage

A well-tuned parser should achieve:
- **70-85% firm extraction rate** (firms clearly identifiable)
- **65-75% role extraction rate** (roles clearly identifiable)
- **0% false positive rate** (no guesses/hallucinations)

Lower coverage is acceptable and expected for:
- Vague titles (e.g., "Forbes 30 under 30")
- Taglines (e.g., "Building the Future")
- Incomplete information
- Non-standard formats

## Example Transformations

| Title | Firm | Role |
|-------|------|------|
| Partner at 8VC | 8VC | Partner |
| GP @ Cyrus Ventures | Cyrus Ventures | GP |
| ArchPoint Investors | ArchPoint Investors | _(blank)_ |
| Private Equity Associate \| Apollo Global Management | Apollo Global Management | Private Equity Associate |
| Senior Managing Director, Industry Ventures | Industry Ventures | Senior Managing Director |
| Forbes 30 under 30 | _(blank)_ | _(blank)_ |
| Venture Capitalist \| Building the Future, One Investment at a Time | _(blank)_ | _(blank)_ |

## Usage Examples

### Example 1: Basic Processing
```
User: "Process this LinkedIn CSV file and add Firm and Role columns"
Assistant:
1. Reads the CSV file
2. Deploys the parser script
3. Processes all rows
4. Adds Firm and Role columns
5. Reports: "Processed 176 rows. Extracted 135 firms (76.7%) and 124 roles (70.5%)"
```

### Example 2: Custom Input Location
```
User: "Here's my LinkedIn connections export at ~/Downloads/connections.csv - extract firms and roles"
Assistant:
1. Locates the file at ~/Downloads/connections.csv
2. Copies or adapts the parser script to work with this location
3. Processes the file
4. Saves updated CSV
5. Shows sample results
```

## Troubleshooting

**Issue**: Script fails to find Title column
- **Solution**: Verify CSV has correct headers, check for encoding issues

**Issue**: Too many blank entries
- **Solution**: Review title patterns in the CSV, consider adjusting keywords/patterns

**Issue**: Duplicate columns created
- **Solution**: Run deduplication script to remove duplicate Firm/Role headers

**Issue**: Incorrect parsing
- **Solution**: Examine specific cases, adjust regex patterns or keywords as needed

## Extensibility

This workflow can be extended to:
- Extract additional fields (location, industry, seniority level)
- Standardize firm names (e.g., "8VC" vs "Eight VC")
- Categorize roles (Investor, Operator, Advisor, etc.)
- Export to different formats (Excel, JSON, database)
- Integrate with CRM or research tools

## Files Referenced

- **Parser Script**: `users/tam/workflows/parse_titles.py`
- **Deduplication Script**: `users/tam/workflows/fix_duplicates.py` (if needed)
- **Input**: Any LinkedIn connections CSV export
- **Output**: Same CSV with Firm and Role columns added

## Success Criteria

- ✅ CSV file successfully processed without errors
- ✅ Firm and Role columns added to CSV
- ✅ Coverage rate >70% for both Firm and Role (or reasonable for the dataset)
- ✅ No false positives (no guessing or hallucinated data)
- ✅ Blank entries for ambiguous titles
- ✅ Clean, well-formatted output CSV
- ✅ Processing statistics reported to user

---

**Last Updated**: 2025-11-14
**Version**: 1.0
**Tested With**: LinkedIn connections CSV exports (standard format)
**Python Version**: 3.x (requires csv, re, typing modules)
