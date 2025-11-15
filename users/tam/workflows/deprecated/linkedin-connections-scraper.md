# LinkedIn Connections Scraper

**Purpose**: Extract LinkedIn connection data from a profile's connections search page and save as structured markdown.

---

## Input

1. LinkedIn connections search URL:
   ```
   https://www.linkedin.com/search/results/people/?origin=MEMBER_PROFILE_CANNED_SEARCH&network=%5B%22F%22%2C%22S%22%5D&connectionOf=%5B%22ACoAAB...%22%5D
   ```
2. **Page range** (optional): e.g., `1-5` or single page `3`
   - Default: page 1 only

## Output

Markdown file at: `users/tam/hyperion/research/people/linkedin/[name].md`

---

## Tool Usage Guidelines

**Use these tools in this order for each page:**

1. **Playwright** (`mcp__playwright__browser_navigate`, `mcp__playwright__browser_snapshot`): Navigate to LinkedIn page and capture connections
2. **Direct Formatting**: Format connections as markdown directly using the pattern below (no Bash/Python needed)
3. **Read**: Check if file exists and get last ~100 lines to find current footer and last connection number
4. **Edit**: Replace old footer with new connections + updated footer

**IMPORTANT**: Do NOT use Bash to run Python scripts. Format markdown directly in Claude.

---

## Simplified Workflow

**The entire process in 3 steps:**

1. **Extract**: Navigate to LinkedIn page → Capture snapshot → Parse connection data
2. **Format**: Create markdown text directly (no scripts needed) using the pattern below
3. **Save**: Use Edit tool to append formatted markdown and update footer

**No Bash commands needed. No Python scripts needed. Just extract, format, and save.**

---

## Execution

### Phase 0: Setup

1. Parse page range (e.g., `2-5` → pages 2, 3, 4, 5)
2. For page N, construct URL: `{base_url}&page=N`
3. Get starting connection number:
   - Use **Read** tool to check if file exists at `users/tam/hyperion/research/people/linkedin/connections.md`
   - If file exists, scan for patterns like `## 123. Name` to find the highest number
   - Starting number = highest found number + 1 (or 1 if file doesn't exist)

### Phase 1: Navigate and Extract (per page)

1. **Navigate**: Use `mcp__playwright__browser_navigate` to LinkedIn URL
2. **Wait**: Pause 1-2 seconds (prevents rate limiting)
3. **Capture**: Use `mcp__playwright__browser_snapshot` (do NOT click links)
   - If snapshot fails due to token limit, use `browser_evaluate` with JavaScript to extract data directly
4. **Parse** YAML snapshot to extract for each connection:
   - Name
   - Title/position
   - Location
   - Mutual connections (total count + named connections)
   - Profile URL

### Phase 2: Format and Append (per page)

**Step 1: Format connections directly**

For each connection extracted from the snapshot, format as markdown using this exact pattern:

```markdown
## N. [Name]

- **Title**: [Title]
- **Location**: [Location]
- **Mutual Connections**: [Count] ([Person 1], [Person 2], and [X] others)
- **Profile**: [URL]
```

Example:
```markdown
## 901. Jane Smith

- **Title**: VP of Engineering at TechCorp
- **Location**: San Francisco Bay Area
- **Mutual Connections**: 12 (Alice Johnson, Bob Chen, and 10 others)
- **Profile**: https://www.linkedin.com/in/janesmith
```

Note: Skip any field that's not available (e.g., if no location is shown, omit that line)

**Step 2: Read current file footer**

Use Read tool to get last ~100 lines:
```
Read tool: file_path='users/tam/hyperion/.../connections.md', offset=-100
```
Identify the current footer (lines starting with `---` and `**Pages extracted**:`)

**Step 3: Append using Edit tool**

Use Edit to replace old footer with new content:
```
old_string: "---\n\n**Pages extracted**: 81-90"
new_string: "{new_connections}\n\n---\n\n**Pages extracted**: 81-91"
```

**Step 4: Validate**
- Verify Edit succeeded
- Count connections added (should match page count, typically 10)
- Update `start_num` for next page

**Step 5: On final page, update with full range**
```
old_string: "---\n\n**Pages extracted**: 81-99"
new_string: "{new_connections}\n\n---\n\n**Pages extracted**: 81-100"
```

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

```markdown
# LinkedIn Connections for [Name]

Extracted from: [URL]
Date: YYYY-MM-DD

---

## 1. [Connection Name]

- **Title**: [Position]
- **Location**: [City, State/Country]
- **Mutual Connections**: [Number] ([Named Person 1], [Named Person 2], and [X] others)
- **Profile**: [LinkedIn URL]

## 2. [Next Connection]
...

---

**Pages extracted**: 1-3
```

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
- ✅ Profile URLs are complete and clickable
- ✅ Mutual connection counts include total + named connections
- ✅ No data fabricated or inferred beyond what's visible
- ✅ 1-2 second delays between pages (rate limiting)
- ✅ Validation after each page append
- ✅ Recovery possible from any interruption point

---

**Version**: 3.0 (2025-11-14) - Eliminated all Bash/Python calls, direct markdown formatting, simplified workflow
