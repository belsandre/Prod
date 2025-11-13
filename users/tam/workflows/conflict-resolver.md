# Company Name Conflict Resolution Workflow

**Purpose**: Systematically resolve situations where multiple portfolio companies have identical or similar names

**When to Use**: When research discovers potential name conflicts (e.g., "Scout" and "Scout AI" both appearing in portfolio materials with inconsistent information)

---

## Phase 1: Conflict Detection

**You've identified a potential conflict when:**
- Same/similar company names appear with different founders
- Same company name has inconsistent descriptions (e.g., "robotics" vs "sales platform")
- Investment dates don't align with company founding dates
- Different logos appear for same company name in source documents

**Document the conflict:**
- Company names in question
- Conflicting information observed
- Source documents where conflicts appear

---

## Phase 2: Source Material Investigation

**For each dataroom source, systematically check:**
1. Company mentions (exact name + variants)
2. Logos (visual differentiation = strong signal different companies)
3. Founder names (same/different)
4. Descriptions (compatible vs. mutually exclusive)
5. Investment details (dates, amounts, valuations)

**Sources to check (in priority order):**
1. **Excel Portfolio Spreadsheet** (most authoritative for investment data)
2. **Founder References Document** (check testimonial logos + names)
3. **Sourcing Differentiation Document** (check network map logos + categorization)
4. **Case Studies Document** (check founder names, descriptions)
5. **Public Sources** (company websites, LinkedIn, founding dates validation)

---

## Phase 3: Decision Framework

**Classify as ONE company if:**
- Same founder(s) across all sources
- Same investment dates in Excel
- Same logo in visual materials
- Descriptions can be reconciled (e.g., product pivot, naming evolution)

**Classify as MULTIPLE companies if:**
- Different founders
- Different founding dates
- Different logos in source documents
- Mutually exclusive descriptions (can't both be true for same company)
- Different geographical locations

**Information gap if:**
- Excel unclear or conflicting
- One company has full details, other lacks investment info
- Cannot definitively determine from available sources

---

## Phase 4: Resolution Actions

### For ONE Company (Naming Inconsistency)
1. Choose canonical name (most recent/official)
2. Update priority-deals.md with canonical name, note aliases
3. Update company-clusters.md to remove duplicates
4. Update research-progress.md to clarify single company
5. Consolidate research summary with all source materials

### For MULTIPLE Companies
1. Create separate entries in priority-deals.md for each company
2. **Re-tier each company independently** using tier criteria from `deal-prioritization.md` (Tier 1: Priority Research, Tier 2: Up-and-Comers, Tier 3: Red Flags, Tier 4: Remaining Portfolio). Consider:
   - Investment performance (if data available)
   - Strategic fit with fund thesis
   - Relationship strength with GPs
   - Information completeness
3. Update company-clusters.md:
   - Assign each to appropriate sector cluster
   - Remove incorrect categorizations
4. Update research-progress.md:
   - Separate into distinct research items
   - Flag information gaps if investment details missing for any company
5. Create/update separate research summaries for each company
6. **Attribute source materials correctly**:
   - Assign each dataroom mention to correct company
   - Note which testimonials belong to which company
   - Clarify which metrics apply to which company

### For Information Gaps
1. Document gap clearly in priority-deals.md with "⚠️ INFORMATION GAP" section
2. List missing information needed: investment date, amount, valuation, founder confirmation
3. **Interim tier assignment**: Classify based on available data ONLY
   - If partial evidence suggests Tier 1/2 criteria met → assign tentatively
   - If insufficient evidence → assign Tier 4 (Remaining Portfolio)
   - Mark tier as "PROVISIONAL - pending information"
4. Note in research-progress.md that tier assessment pending information
5. Flag for follow-up with GP or deeper dataroom review

---

## Phase 5: Verification

**After resolution, verify:**
- [ ] No orphaned references in priority-deals.md
- [ ] Company-clusters.md has each company in exactly one cluster
- [ ] Research-progress.md accurately reflects status of each company
- [ ] All source material citations correctly attributed (see `templates/source-documentation.md`)
- [ ] Tier classifications justified with clear rationale
- [ ] Information gaps clearly documented with interim tier assignments

For complete quality standards, see `templates/quality-checklist.md`.

---

## Example Application (Scout vs Scout AI)

**Conflict detected:** "Scout AI" in priority-deals with Tanner Baldwin, but public research found two companies

**Investigation findings:**
- Excel: One entry (Tanner Baldwin, April 2023 & Jan 2024 investments)
- Founder references: Scout logo + Tanner Baldwin testimonial
- Sourcing differentiation: Scout AI logo + robotics description
- Public research: Tanner Baldwin's Scout (sales platform, 2023) vs Colby Adcock's Scout AI (robotics, Aug 2024)

**Decision:** TWO distinct companies

**Resolution:**
- Scout (sales) → Moved to Tier 2 (strong returns but outside deeptech thesis)
- Scout AI (robotics) → Information gap (no investment details in dataroom)
- Updated all three tracking documents
- Created clear separation with distinct entries

---

## Output Requirements

After completing this workflow, produce:
1. **Updated priority-deals.md** with clear company separation and tier assignments
2. **Updated company-clusters.md** with correct sector assignments
3. **Updated research-progress.md** with accurate status
4. **Brief resolution summary** documenting decision rationale

**Always prioritize accuracy over speed** - incorrect company attribution can misrepresent portfolio strategy.
