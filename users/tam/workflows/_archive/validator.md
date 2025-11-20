# Workflow Validator

A generalizable validator that auto-detects requirements from workflows/skills and validates their outputs against quality standards.

## Purpose

Ensure workflow/skill outputs meet documented standards, particularly around source documentation, file structure, completeness, and attribution requirements.

## Inputs

User provides:
1. **Workflow/Skill File Path**: Path to the workflow or skill definition (markdown file)
2. **Output Location**: Path to the output directory to validate

Example:
```
Workflow File: users/tam/workflows/vc-research.md
Output Location: users/tam/hyperion/research/
```

## Validation Process

### Phase 1: Requirement Extraction

Read the target workflow/skill file and extract:

1. **File Structure Requirements**
   - Search for directory structures, file paths mentioned in the workflow
   - Look for "Output Structure", "File Organization", "Directory Layout" sections
   - Extract required files/folders from code blocks and examples

2. **Source Documentation Requirements**
   - Identify mentions of "source files", "attribution", "citations"
   - Extract required metadata fields (URL, Date, Source Type, etc.)
   - Find quality checklist sections mentioning source standards

3. **Content Requirements**
   - Look for "required sections", "must include", "minimum" thresholds
   - Extract tier-specific requirements (Tier 1/2/3 standards)
   - Identify completion criteria and progress tracking requirements

4. **Attribution Requirements**
   - Find statements about "source attribution", "cite sources", "reference"
   - Extract rules about facts vs projections, inferred data
   - Identify verification requirements

5. **Quality Standards**
   - Locate quality checklists, pre-submission checklists
   - Extract minimum source counts, diversity requirements
   - Find objectivity and reliability assessment requirements

6. **Universal Patterns** (apply if not explicitly mentioned)
   - Source files always need: URL, Date, Raw Content
   - Progress trackers should reflect actual completion
   - No orphaned files or broken cross-references

### Phase 2: Filesystem Validation

Scan the output location and compare against extracted requirements:

#### A. File Structure Validation

**Check:**
- ✅ All required directories exist
- ✅ All required files present
- ✅ Naming conventions followed (lowercase, hyphens, no spaces)
- ✅ No orphaned files outside expected structure
- ✅ File extensions appropriate (.md for docs, appropriate for data)

**Example from vc-research.md:**
```
Required Structure:
research/
├── research-progress.md
├── gp-list.md
├── company-clusters.md
├── people/{gp-name}/
│   ├── research-summary.md
│   └── sources/
├── deals/tier-1/{company-name}/
│   ├── research-summary.md
│   └── sources/
└── outputs/executive-summary.md
```

**Validation:**
- Check each required directory exists
- Verify each company in tier-1 has both research-summary.md and sources/ folder
- Confirm all GPs from gp-list.md have folders in people/

#### B. Source Documentation Validation

**For each source file in sources/ directories:**

**Required Fields (Universal):**
- ✅ **URL**: Full URL present (not just domain, not "N/A")
- ✅ **Date**: Publication/Last Updated Date in YYYY-MM-DD format
- ✅ **Source Type**: Categorized (LinkedIn Profile, News Article, Company Website, etc.)
- ✅ **Objectivity Level**: High / Medium / Low specified
- ✅ **Reliability Assessment**: Brief assessment present
- ✅ **Key Information**: Bullet points or summary present
- ✅ **Critical Assessment**: Includes Strengths, Limitations, Biases, Verification Status
- ✅ **Raw Content**: Full extracted content preserved

**Validation Logic:**
```
For each .md file in */sources/ directories:
  - Parse file, extract field headers
  - Check each required field present
  - Validate Date format matches YYYY-MM-DD
  - Ensure URL is complete (starts with http/https)
  - Confirm Raw Content section has substantial text (>100 chars)
  - Verify Critical Assessment has subsections
```

**Report Format:**
```
❌ FAIL: sources/linkedin.md
   - Missing: Date field
   - Invalid: URL (contains "N/A")
   - Missing: Raw Content section

✅ PASS: sources/company-website-overview.md
   - All required fields present and valid
```

#### C. Content Completeness Validation

**Check against workflow-specific requirements:**

**For vc-research.md:**
- ✅ All GPs from gp-list.md have folders in people/
- ✅ All Tier 1 companies from input have folders in deals/tier-1/
- ✅ All Tier 2 companies from input have folders in deals/tier-2/
- ✅ Each company research-summary.md has required sections:
  - Company Overview
  - Traction & Performance
  - Founder & Team Assessment
  - Market & Competitive Landscape
  - Funding & Investors
  - Risks & Red Flags
  - GP Mentions (even if "none found")
- ✅ Analysis documents exist (gp-relationships.md, portfolio-assessment.md)
- ✅ Executive summary exists and is 2-3 pages

**For deal-prioritization.md:**
- ✅ Tiered structure with clear criteria
- ✅ No company in multiple tiers
- ✅ All Tier 1/2 companies mentioned in narrative materials
- ✅ Every metric has source attribution

**Validation Logic:**
```
1. Read gp-list.md, extract GP names
2. List directories in people/, compare
3. Report missing GPs

4. Read input priority-deals.md or equivalent, extract company names by tier
5. List directories in deals/tier-1/, deals/tier-2/
6. Report missing companies

7. For each research-summary.md:
   - Parse markdown headers
   - Check required sections present
   - Flag sections that are empty or placeholder text
   - Verify GP Mentions section exists
```

**Report Format:**
```
❌ FAIL: Completeness Check
   - Missing: 2/5 GPs not researched (Alice Chen, Bob Smith)
   - Missing: 1/8 Tier 1 companies not researched (Normal Computing)
   - Missing: gp-relationships.md not found

✅ PASS: All companies researched
✅ PASS: Executive summary exists (2.1 pages)
```

#### D. Attribution Standards Validation

**Check for source citations in analysis documents:**

**Rules:**
- Every factual claim must have source attribution
- Distinguish facts from projections ("expected", "projected", "forecasted")
- No inferred information without explicit "inferred from X"
- Valuation discrepancies noted and reconciled

**Validation Logic:**
```
For analysis documents (research-summary.md, portfolio-assessment.md, etc.):
  - Scan for factual claims (metrics, dates, names, amounts)
  - Check if followed by citation pattern:
    - "(Source: ...)"
    - "[source-file-name]"
    - "According to [source]"
  - Flag uncited claims for review
  - Check for projection keywords without "projected" qualifier
  - Look for "inferred" statements without explanation
```

**Report Format:**
```
⚠️ WARNING: Attribution Issues
   - deals/tier-1/company-x/research-summary.md:15
     "Revenue grew 300% in 2024" - no source citation
   - analysis/portfolio-assessment.md:42
     "Valued at $50M" - no source attribution

✅ PASS: All claims in executive summary properly cited
```

#### E. Consistency Validation

**Cross-document checks:**

**For vc-research.md:**
- ✅ research-progress.md completion counts match actual file counts
- ✅ company-clusters.md companies match researched companies
- ✅ gp-relationships.md references only researched GPs and companies
- ✅ No mutual exclusivity violations

**For deal-prioritization.md:**
- ✅ No company in multiple tiers
- ✅ Excel data matches narrative documents
- ✅ Failed investments explicitly excluded

**Validation Logic:**
```
1. Parse research-progress.md for completion counts
2. Count actual folders/files in filesystem
3. Compare and report discrepancies

4. Extract company names from all tier directories
5. Check for duplicates across tiers
6. Report violations

7. Parse cross-references in analysis documents
8. Verify referenced files/entities exist
9. Flag broken references
```

**Report Format:**
```
❌ FAIL: Consistency Check
   - research-progress.md claims 5/5 GPs complete, but only 3 folders exist
   - Company "Acme Corp" appears in both Tier 1 and Tier 2

✅ PASS: All cross-references valid
✅ PASS: No duplicate companies across tiers
```

#### F. Quality Standards Validation

**Tier-specific source thresholds (for vc-research.md):**

**Tier 1 Minimum:**
- 5+ total sources (or 1 company website + 1 funding announcement + 1 third-party article + 2+ additional)
- Must include diverse source types (not all news articles)
- At least 1 high objectivity source

**Tier 2 Minimum:**
- 3+ total sources (or 1 company website + 1 funding announcement + 1 third-party source)

**Tier 3/4:**
- 1-2 sources acceptable (limited public information expected)

**Validation Logic:**
```
For each company in tier-1/:
  - Count source files in sources/ directory
  - Parse each source for Source Type
  - Categorize sources (company website, news, funding announcement, etc.)
  - Check diversity (not all same type)
  - Parse Objectivity Level from sources
  - Compare against tier-specific threshold
  - Flag if below minimum

Apply same logic for tier-2/, tier-3/, tier-4/ with adjusted thresholds
```

**Report Format:**
```
❌ FAIL: Quality Standards
   - Tier 1: Company X has only 3 sources (minimum 5)
   - Tier 1: Company Y has 6 sources but all are news articles (need diversity)
   - Tier 1: Company Z has no high-objectivity sources

✅ PASS: Tier 2 companies meet 3+ source threshold
⚠️ WARNING: Tier 1: Company A has exactly 5 sources (consider more for confidence)
```

### Phase 3: Generate Validation Report

Compile all checks into structured pass/fail summary using this template:

```markdown
# Validation Report

**Workflow**: [workflow file path]
**Output Location**: [output directory path]
**Validation Date**: [YYYY-MM-DD]

## Summary

**Overall Status**: [PASSED / FAILED / WARNINGS] ([X] critical issues, [Y] warnings)

[Category breakdown table with Status and Issues columns]

## Critical Issues (Must Fix)

[List with file paths + fix instructions for each critical failure]

## Warnings (Should Address)

[List with recommendations for quality improvements]

## Passed Checks ✅

[Brief summary of what's working well]

## Recommended Actions

[Prioritized action plan: Priority 1 (Critical), Priority 2 (Quality), Priority 3 (Enhancement)]
```

For complete validation report format examples, see `users/tam/workflows/templates/quality-checklist.md`.

## Workflow Adaptability

The validator auto-detects requirements from different workflow types:

### For vc-research.md:
- Detects tier structure, applies tier-specific thresholds
- Validates source documentation standards
- Checks progress tracking against filesystem
- Ensures GP research and relationship mapping

### For deal-prioritization.md:
- Validates no companies in multiple tiers
- Checks every metric has source attribution
- Ensures facts vs projections distinguished
- Verifies Excel vs narrative consistency

### For custom workflows:
- Extracts requirements from "Quality Checklist" sections
- Identifies required files from "Output Structure" sections
- Detects minimum thresholds from "must have X sources" statements
- Applies universal source documentation standards

### For skills (company-research, etc.):
- Reads skill SKILL.md or README for output requirements
- Validates against skill-specific quality standards
- Checks for high-quality source preservation
- Ensures critical assessment sections present

## Universal Source Standards

For complete source documentation standards, see `users/tam/workflows/templates/source-documentation.md`. The validator always checks (unless workflow explicitly exempts):
- URL field present and valid (full URL, not "N/A")
- Date field in YYYY-MM-DD format
- Raw Content preserved (not just summaries)
- Source Type categorized
- No unsourced factual claims in analysis

## When to Use Validator

**Required**:
- Before submitting research to stakeholders
- When resuming interrupted workflows (verify consistency)

**Optional**:
- Mid-workflow quality spot-check (after completing a phase)
- When experimenting with workflow modifications

## After Validation Report

1. **Address ALL critical issues** (blocking - must fix before proceeding)
2. **Review warnings** with stakeholder (decide priority)
3. **Re-run validator** after fixes to confirm compliance
4. **Proceed only when** report shows PASSED overall or stakeholder accepts remaining warnings

## Output Specification

Generate a markdown validation report in the format shown in Phase 3, including:
1. **Summary table** with pass/fail by category
2. **Critical Issues section** with specific file paths and fix instructions
3. **Warnings section** with recommended improvements
4. **Passed Checks section** listing what's working well
5. **Recommended Actions** prioritized by severity

Save report to: `{output_location}/VALIDATION-REPORT.md`

Also provide a brief summary in the job output for quick review.

## Notes

- **Auto-detection may not catch everything**: If workflow has unique requirements not in common patterns, validator may miss them. Always review workflow manually for edge cases.
- **Thresholds are minimums**: Meeting minimum doesn't guarantee quality. Use judgment.
- **Context matters**: Some warnings may be acceptable (e.g., Tier 3 companies naturally have fewer sources).
- **Extensible design**: As new workflows emerge, validator learns patterns and adapts.

## Example Usage

**Input:**
```
Workflow File: users/tam/workflows/vc-research.md
Output Location: users/tam/hyperion/research/
```

**Validator Actions:**
1. Reads vc-research.md, extracts file structure, source requirements, tier thresholds
2. Scans users/tam/hyperion/research/, validates against requirements
3. Generates VALIDATION-REPORT.md with specific issues and fixes
4. Returns summary: "❌ FAILED - 3 critical issues in source documentation, 1 consistency issue, 5 warnings"

**Input:**
```
Workflow File: users/tam/workflows/deal-prioritization.md
Output Location: users/tam/outputs/priority-deals.md
```

**Validator Actions:**
1. Reads deal-prioritization.md, extracts tiering rules, attribution requirements
2. Parses priority-deals.md file (single-file output, not directory)
3. Checks no duplicates across tiers, all metrics cited, facts vs projections clear
4. Generates VALIDATION-REPORT.md
5. Returns summary: "✅ PASSED - All checks passed, high-quality output"

## Validation Checklist Meta-Validation

**Validator validates itself against these principles:**
- ✅ Works with file paths as inputs
- ✅ Auto-detects requirements from workflow structure
- ✅ Provides pass/fail summary (not verbose analysis)
- ✅ Generalizable across multiple workflow types
- ✅ Actionable feedback with specific file paths and fixes
- ✅ Succinct design (~300 lines, not sprawling)
- ✅ Supports both directory-based and file-based outputs

---

**End of Workflow**
