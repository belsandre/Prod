# LinkedIn Connections Scraper To CSV

**Purpose**: Extract LinkedIn connection data from a profile's connections search page and save as structured CSV.

---

## Input

1. LinkedIn connections search URL:
   ```
   https://www.linkedin.com/search/results/people/?origin=MEMBER_PROFILE_CANNED_SEARCH&network=%5B%22F%22%2C%22S%22%5D&connectionOf=%5B%22ACoAAB...%22%5D
   ```
2. **Page range** (optional): e.g., `1-5` or single page `3`
   - Default: page 1 only

## Output

CSV file at: `users/tam/hyperion/research/people/linkedin/[name].csv`

**Columns**: Name, Degree Connection, Title, Location, Mutual Connections Count, Mutual Connections Names, Profile

---

## Tool Usage Guidelines

**Use these tools in this order for each page:**

1. **Playwright** (`mcp__playwright__browser_navigate`, `mcp__playwright__browser_snapshot`): Navigate to LinkedIn page and capture connections
2. **Direct Formatting**: Format connections as CSV rows directly (no Bash/Python needed)
3. **Read**: Check if file exists to determine if CSV header is needed and count existing rows
4. **Edit** or **Write**: Append new CSV rows to existing file (or create with header if new)

**IMPORTANT**: Do NOT use Bash to run Python scripts. Format CSV rows directly in Claude.

---

## Simplified Workflow

**The entire process in 3 steps:**

1. **Extract**: Navigate to LinkedIn page → Capture snapshot → Parse connection data (including connection degree badge)
2. **Format**: Create CSV rows directly (no scripts needed) with proper escaping
3. **Save**: Use Edit tool to append CSV rows (or Write tool to create new file with header)

**No Bash commands needed. No Python scripts needed. Just extract, format, and save.**

---

## Execution

### Phase 0: Setup

1. Parse page range (e.g., `2-5` → pages 2, 3, 4, 5)
2. For page N, construct URL: `{base_url}&page=N`
3. Check if CSV file exists:
   - Use **Read** tool to check if file exists at `users/tam/hyperion/research/people/linkedin/connections.csv`
   - If file doesn't exist, will need to create with header row: `Name,Degree Connection,Title,Location,Mutual Connections Count,Mutual Connections Names`
   - Count existing data rows (excluding header) to track progress

### Phase 1: Navigate and Extract (per page)

1. **Navigate**: Use `mcp__playwright__browser_navigate` to LinkedIn URL
2. **Wait**: Pause 1-2 seconds (prevents rate limiting)
3. **Capture**: Use `mcp__playwright__browser_snapshot` (do NOT click links)
   - If snapshot fails due to token limit, use `browser_evaluate` with JavaScript to extract data directly
4. **Parse** YAML snapshot to extract for each connection:
   - Name
   - Degree Connection (extract "1st" or "2nd" from badge next to name - look for text like "• 1st" or "• 2nd")
   - Title/position
   - Location
   - Mutual connections count (numeric value)
   - Mutual connections names (list of named people, e.g., "Alice Johnson, Bob Chen, and 10 others")
   - Profile URL

### Phase 2: Format and Append (per page)

**Step 1: Format connections as CSV rows**

For each connection extracted from the snapshot, format as a CSV row with these 7 columns:
1. Name
2. Degree Connection ("1st" or "2nd")
3. Title
4. Location
5. Mutual Connections Count
6. Mutual Connections Names
7. Profile (LinkedIn profile URL)

**CSV Escaping Rules**:
- Wrap fields in double quotes if they contain commas, quotes, or newlines
- Escape internal double quotes by doubling them (`""`)
- Use empty quotes `""` for missing/unavailable fields

Example CSV row:
```csv
"Jane Smith","1st","VP of Engineering at TechCorp","San Francisco Bay Area","12","Alice Johnson, Bob Chen, and 10 others","https://www.linkedin.com/in/janesmith"
```

**Step 2: Check if file exists and read header**

Use Read tool to check file:
```
Read tool: file_path='users/tam/hyperion/research/people/linkedin/connections.csv'
```

If file doesn't exist, you'll need to create it with header row first.

**Step 3: Append CSV rows**

**For new file** (doesn't exist):
Use Write tool to create file with header + data rows:
```
Name,Degree Connection,Title,Location,Mutual Connections Count,Mutual Connections Names,Profile
"Jane Smith","1st","VP of Engineering at TechCorp","San Francisco Bay Area","12","Alice Johnson, Bob Chen, and 10 others","https://www.linkedin.com/in/janesmith"
...
```

**For existing file** (append mode):
Use Edit tool to append new rows at the end:
```
old_string: "{last_existing_row}"
new_string: "{last_existing_row}\n{new_csv_rows}"
```

**Step 4: Validate**
- Verify file operation succeeded
- Count rows added (should match page count, typically 10)
- Ensure all rows have 7 comma-separated fields

---

## Error Handling & Validation

### Rate Limiting
- **Wait 1-2 seconds between page navigations** (prevents LinkedIn blocking)
- Use `mcp__playwright__browser_wait_for` with `time: 1.5` parameter

### Page Load Failures
If page fails to load or snapshot times out:
1. Retry once after 3-second wait
2. If second attempt fails, skip page and log warning
3. Continue with next page (don't abort entire process)

### Snapshot Too Large
If `browser_snapshot` exceeds token limit:
- Use `browser_evaluate` to extract connection data directly via JavaScript
- Example: `await page.evaluate(() => Array.from(document.querySelectorAll('[data-test-search-result]'))...)`

### Validation After Each Page
After appending each page:
1. ✅ Verify connection count (typically 10 per page, may be fewer on last page)
2. ✅ Check that all profile URLs start with `https://www.linkedin.com/in/`
3. ✅ Confirm Edit operation succeeded (no errors)
4. ✅ Update running total for final footer

### Recovery from Interruptions
- Progress is saved after each page (incremental Edit operations)
- If process interrupted, resume from last completed page
- Use `extract_last_connection_number()` to find restart point

---

## Output Format

CSV file with header row and one row per connection:

```csv
Name,Degree Connection,Title,Location,Mutual Connections Count,Mutual Connections Names,Profile
"Jane Smith","1st","VP of Engineering at TechCorp","San Francisco Bay Area","12","Alice Johnson, Bob Chen, and 10 others","https://www.linkedin.com/in/janesmith"
"John Doe","2nd","Senior Product Manager at StartupXYZ","New York, NY","5","Sarah Williams, and 4 others","https://www.linkedin.com/in/johndoe"
"Alice Johnson","1st","Data Scientist at AI Labs","Boston, MA","8","Jane Smith, Mike Brown, and 6 others","https://www.linkedin.com/in/alicejohnson"
```

**Field descriptions**:
- **Name**: Full name of the connection
- **Degree Connection**: "1st" or "2nd" degree connection (extracted from badge)
- **Title**: Current job title and company
- **Location**: Geographic location
- **Mutual Connections Count**: Numeric count of mutual connections
- **Mutual Connections Names**: Names of mutual connections (format: "Person 1, Person 2, and X others")
- **Profile**: LinkedIn profile URL (e.g., "https://www.linkedin.com/in/username")

**Note**: Fields are quoted to handle commas in values. Empty fields use `""`.

---

## Helper Script Reference (OPTIONAL - DO NOT EXECUTE)

**Location**: `users/tam/workflows/linkedin_scraper.py`

**IMPORTANT**: This Python script is provided for reference only. DO NOT execute it via Bash. Instead:
- Format markdown directly in Claude using the pattern shown above
- Use the Read tool to find the last connection number
- Use the Edit tool for all file operations

**Reference Functions** (for understanding the logic, not for execution):
- `extract_last_connection_number()` - Shows how to find the last number (use Read tool instead)
- `format_connection_markdown()` - Shows the markdown format (format directly instead)
- `parse_connection_from_yaml()` - Shows YAML parsing patterns (parse directly from snapshot)

**Why We Don't Use This Script**:
- Running Python via Bash requires user approval for each command
- Claude can format markdown directly without external scripts
- Direct formatting is more efficient and transparent
- No dependencies on external files or imports

---

## Quality Standards

- ✅ All visible connections extracted (no skips)
- ✅ Connection degree ("1st" or "2nd") accurately extracted from badge
- ✅ Profile URLs are complete and clickable
- ✅ Mutual connection counts split into numeric count and names
- ✅ CSV properly formatted with 7 columns per row
- ✅ CSV fields properly escaped (quotes around fields with commas)
- ✅ No data fabricated or inferred beyond what's visible
- ✅ 1-2 second delays between pages (rate limiting)
- ✅ Validation after each page append
- ✅ Recovery possible from any interruption point

---

**Version**: 4.1 (2025-11-14) - Added Profile URL column to CSV output (7 columns total)
