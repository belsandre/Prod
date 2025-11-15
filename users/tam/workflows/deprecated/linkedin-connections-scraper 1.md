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

## Execution

### Phase 0: Setup (if page range specified)

1. Parse page range (e.g., `2-5` → pages 2, 3, 4, 5)
2. For page N, append `&page=N` to base URL
3. Track starting connection number for continuation across pages

### Phase 1: Navigate and Extract (per page)

1. Use Playwright MCP to navigate to the LinkedIn URL (with `&page=N` if applicable)
2. Capture page snapshot (do NOT click any links)
3. Extract for each connection:
   - Name
   - Title/position
   - Location
   - Total mutual connections (including named connections)
   - Profile URL

### Phase 2: Save Data

**First page:**
1. Create directory: `users/tam/hyperion/research/people/linkedin/`
2. Create new file: `[name].md` with full header

**Subsequent pages (if range specified):**
1. Read existing file
2. Append new connections with continued numbering
3. Update page note at bottom

Format:
- Header with source URL and date (page 1 only)
- Numbered list of connections (continuous across pages)
- Each connection as H2 with fields as bullet points

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
**Total connections**: 30
```

---

## Pagination

At end of file, add:
```markdown
---

**Pages extracted**: [X-Y] (or "Page [X]" for single page)
**Total connections**: [N]
```

LinkedIn page URLs: append `&page=N` to base URL (e.g., `&page=2`, `&page=3`)

---

## Quality Standards

- ✅ All visible connections extracted
- ✅ Profile URLs are complete and clickable
- ✅ Mutual connection counts include total (named + "X others")
- ✅ No data fabricated or inferred
- ✅ Source URL and extraction date documented

---

**Version**: 1.1 (2025-11-14) - Added page range support
