# Portfolio Analysis Workflow

**Purpose**: Analyze portfolio health, defensibility of marks, and identify fund drivers vs emerging companies.

**Output**: Portfolio assessment with health evaluation, structured data in JSON, and markdown presentation.

---

## Overview

This workflow analyzes an existing portfolio by loading research data, evaluating company performance and defensibility, and assessing overall portfolio health. Focus on concentration risk, valuation methodologies, and competitive positioning.

**Key Features**:
- ✅ **Resumability**: Track progress, pause and continue anytime
- ✅ **Structured Data**: Export to `portfolio.json` for reusability
- ✅ **Evidence-Based**: 3-tier source quality validation (Independent/Affiliated/Dataroom)
- ✅ **Value-Focused**: Winners (major fund drivers) vs Emerging vs Other

---

## When to Use

- Evaluating VC fund portfolio quality and defensibility of marks
- Assessing concentration risk and portfolio health
- Analyzing whether valuations are backed by performance
- Companies already researched (run `vc-research.md` first if needed)

---

## Prerequisites

**Required Materials**:
- `{fund-name}/research/companies/` with `research-summary.md` files
- `{fund-name}/dataroom/` with portfolio valuation data (.xlsx)

**Skills**: WebSearch, WebFetch (for validation)

---

## Output Structure

```
{fund-name}/
├── research/
│   └── companies/
│       ├── portfolio-list.md            # Company inventory + Progress tracker (COMBINED)
│       ├── {company-1}/
│       │   └── independent-research.md
│       └── {company-2}/
│           └── independent-research.md
└── marketing-to-reality/
    ├── _data/
    │   └── portfolio.json               # Structured data
    └── portfolio-analysis.md            # Final assessment
```

---

## Phase 0: Load Portfolio

**Purpose**: Create inventory, load valuations, initialize tracking.

### Step 0.1: Create Portfolio List (with Progress Tracker)

**Action**: Find all companies with research

```bash
find {fund-name}/research/companies -name "independent-research.md"
```

**Location**: `{fund-name}/research/companies/portfolio-list.md`

**Template**:
```markdown
# Portfolio Analysis - {Fund Name}

**Date**: YYYY-MM-DD
**Source**: Dataroom + Research

---

## Progress Tracker

- [x] Phase 0: Load Portfolio
- [ ] Phase 1: Company Assessment (Progress: 0/X)
- [ ] Phase 2: Portfolio Analysis
- [ ] Phase 3: Output

**Output**: `marketing-to-reality/_data/portfolio.json` → `marketing-to-reality/portfolio-analysis.md`

---

## Portfolio Overview

**Total Companies**: {X} (dataroom)
**With Research**: {Y} companies
**Without Research**: {Z} companies → categorize as "Other"

---

## Company List & Valuations

| # | Company | Entry Val | Current Val | MOIC | Research | Status |
|---|---------|-----------|-------------|------|----------|--------|
| 1 | {Company} | ${X}M | ${Y}M | {Z}x | ✅ | Pending |
```

### Step 0.2: Load Dataroom Valuations & Research Data

**For each company**:
1. Parse dataroom .xlsx for entry/current valuations
2. Read `independent-research.md` for:
   - Current valuation (prefer research over outdated dataroom)
   - Performance metrics (revenue, traction, milestones)
   - Lead investors
   - Source quality (Independent/Affiliated/Dataroom)
3. Calculate MOIC: Current ÷ Entry valuation
4. Update `research/companies/portfolio-list.md` table and Status column

**CRITICAL**: Use research valuations when more current than dataroom.

**Example**:
- Dataroom: Figure AI $420M (Apr 2023)
- Research: Figure AI $39.5B (Sept 2025)
- **Use**: $39.5B

---

## Phase 1: Company Assessment

**Purpose**: Assess performance, moat, categorization, risks for each company.

**Recommended**: Batch process 5-7 companies, then update progress.

### Step 1.1: Assess Performance & Moat

**For each company**, extract from `research-summary.md`:

**Performance Signals**:
- Valuation growth (MOIC)
- Revenue & growth rate
- Customer traction (pilot vs production, Fortune 500 logos)
- Key milestones (product launches, technical achievements)
- Tier-1 investor validation

**Moat Assessment** (choose primary):
- **Technical**: Deep tech, patents, proprietary algorithms (requires external validation)
- **Network Effects**: Value increases with scale
- **Brand/Market Leadership**: Category leader, first-mover
- **Regulatory**: Licenses, certifications, compliance advantages
- **Data**: Improves with proprietary data accumulation

**Grade**: Strong / Moderate / Weak / Unproven

**Competitive Threats**: Note major competitors and risks

### Step 1.2: Categorize & Validate Sources

**Categorization**:

**WINNERS**: Drive majority of portfolio value
- Current valuation represents significant portion of total portfolio
- Strong MOIC (typically >10x) OR absolute scale with market leadership
- Tier-1 co-investor validation at scale
- Revenue traction or clear path to major returns

**EMERGING**: Featured companies, solid fundamentals
- Strong traction but not yet massive scale
- MOIC 2-8x with growth potential
- Quality signals, execution TBD

**OTHER**: Stable performers or too early to assess
- Modest performance (1-3x) OR very early stage
- Limited public information OR insufficient timeline

**RED FLAGS**: Warning signs
- Valuation ahead of traction
- False/misleading dataroom claims
- Nonstandard valuation methods
- Intense competitive threats

---

**Source Quality Validation** (3-tier system):

**INDEPENDENT** (highest quality):
- Third-party media, independent analysts, public filings, academic publications
- High confidence, externally verified

**AFFILIATED** (medium quality):
- Company website, press releases, founder interviews, company-controlled sources
- Credible but potentially optimistic, requires corroboration for high-value claims

**DATAROOM** (lowest quality):
- Dataroom testimonials, fundraising materials, GP-provided case studies
- Unverified, requires independent validation

**Flag for verification**: Customer claims, financial metrics, technical achievements, partnership claims, GP value-add claims

**Document**:
```markdown
**{Company}**
- Category: Winner / Emerging / Other / Red Flag
- Moat: {Type} ({Strength})
- Source Quality: Independent / Affiliated / Dataroom
- Red Flags: {Any false/unverifiable claims}
```

### Step 1.3: Flag Risks & Update JSON

**Risk Categories**:

**Valuation Risk**: Is valuation justified?
- Red flags: Minimal revenue + multi-billion valuation, nonstandard methodology
- Assessment: High / Moderate / Low

**Competitive Risk**: Intensity of competition
- Red flags: Well-funded competitors, commoditizing tech, losing market share
- Assessment: High / Moderate / Low

**Market Risk**: Is market ready and growing?
- Red flags: Overly optimistic TAM, slow adoption, regulatory headwinds
- Assessment: High / Moderate / Low

---

**Create/Update portfolio.json**: `{fund-name}/marketing-to-reality/_data/portfolio.json`

```json
{
  "fund_name": "{Fund Name}",
  "analysis_date": "YYYY-MM-DD",
  "total_companies": X,
  "companies": [
    {
      "name": "{Company}",
      "category": "winner",
      "entry_valuation": "{$XM}",
      "current_valuation": "{$XB}",
      "moic": X.Xx,
      "revenue_status": "Pre-revenue" | "Commercial",
      "primary_moat": "Technical" | "Network Effects" | "Brand" | "Regulatory" | "Data",
      "moat_strength": "Strong" | "Moderate" | "Weak",
      "source_quality": "independent" | "affiliated" | "dataroom",
      "risks": {
        "valuation": "High" | "Moderate" | "Low",
        "competitive": "High" | "Moderate" | "Low",
        "market": "High" | "Moderate" | "Low"
      },
      "red_flags": ["Flag 1", "Flag 2"]
    }
  ]
}
```

**Update progress**: After each batch, update Status column in `research/companies/portfolio-list.md` (Pending → Complete) and update Phase 1 progress count

---

## Phase 2: Portfolio Analysis

**Purpose**: Synthesize company data into portfolio-level insights.

### Step 2.1: Portfolio Composition

**Action**: Create composition tables (use portfolio.json data)

**By Category**:
| Category | Count | Examples |
|----------|-------|----------|
| Winners | {X} | {Company 1, Company 2} |
| Emerging | {X} | {Company 3, Company 4} |
| Other | {X} | {Company 5, Company 6} |
| Red Flags | {X} | {Company 7} |

**By Sector**:
| Sector | Count | Notable Companies |
|--------|-------|-------------------|
| {Sector} | {X} | {Companies} |

**By Stage at Entry**:
| Stage | Count |
|-------|-------|
| Pre-Seed/Seed | {X} |
| Series A | {X} |
| Series B+ | {X} |

**By Current Stage**:
| Stage | Count |
|-------|-------|
| Seed/Series A | {X} |
| Series B/C | {X} |
| Late Stage | {X} |

**Analysis**: Note concentration (sector, stage, single holdings)

### Step 2.2: Defensibility Analysis

**Moat Distribution**:
| Moat Type | Count | Assessment |
|-----------|-------|------------|
| Technical | {X} | Strong / Moderate / Weak |
| Network Effects | {X} | Strong / Moderate / Weak |
| Brand/Leadership | {X} | Strong / Moderate / Weak |
| Regulatory | {X} | Strong / Moderate / Weak |
| Data | {X} | Strong / Moderate / Weak |

**Investment Thesis Inference**: Based on patterns, what does this fund bet on? (Sector focus, stage, founder profiles, moat types)

### Step 2.3: Risk Assessment

**Concentration Risk**:
- Top holding: {Company} represents {X}% of value
- Top 3: {Y}% of value
- Assessment: ✅ Healthy (<20% top holding) / ⚠️ Moderate (20-40%) / 🚨 High (>40%)
- Implication: Binary outcome vs diversified?

**Valuation Methodology Risk**:
- Basis: Latest-round pricing / External appraisal / Subjective marks
- Unrealized gains: {X}% of portfolio value
- Bull market impact: Marks set during 2024-2025 AI bubble?
- Red flags: >$1B valuation + <$10M revenue, nonstandard methods, 10+ years to liquidity
- Assessment: Low / Moderate / High
- Implication: Will realized returns match paper returns?

**Portfolio Transparency**:
- Companies researched: {X} of {Y total} ({Z}%)
- Failed investments: Disclosed? Named? Analyzed?
- Red flags: <80% documented, selective disclosure
- Assessment: Good / Moderate / Poor

**Evidence Quality**:
- Independent sources: {X} companies ({Y}%)
- Affiliated: {X} companies
- Dataroom-only: {X} companies
- Red flags found: {List companies with false/unverifiable claims}
- Pattern: {Z}% of companies have credibility issues
- Implication: If Z% have false claims, how many other claims are questionable?

### Step 2.4: Portfolio Health Evaluation

**Healthy Indicators**:
- Multiple winners (2-3+) driving value
- Valuations backed by performance (revenue, customers, milestones)
- Category leadership (not fast followers)
- Market tailwinds (structural trends)
- Tier-1 co-investor validation
- Independent source evidence
- Balanced risk profile

**Risky Indicators**:
- Single leader concentration (>40% of value)
- No clear leaders
- Valuation ahead of traction
- Nonstandard valuation methods
- Weak moats, intense competition
- Red flags in emerging companies
- Poor transparency, selective disclosure
- Dataroom-only evidence

**Write narrative assessment** (2-3 paragraphs):
1. **Winners**: How many? What % of value? Backed by performance? Defensible? What if they compress?
2. **Pipeline**: Quality of emerging companies? Up-and-comers? Red flags? Failure risk?
3. **Overall**: Balanced or binary? Concentration? Evidence quality? Market timing? Transparency?

---

## Phase 3: Output

**Purpose**: Create final portfolio assessment.

### Step 3.1: Create Portfolio Assessment

**Location**: `{fund-name}/marketing-to-reality/portfolio-analysis.md`

**Template** (references portfolio.json, doesn't repeat data):

```markdown
# Portfolio Assessment - {Fund Name}

**Date**: {Date}
**Companies Analyzed**: {X} of {Y}
**Overall Health**: **{Rating}** ({Descriptor})

---

## Executive Summary

{2-3 paragraphs: Overall health, major winners, key strengths, key risks}

**Investment Thesis**: {Brief description}
**Stage Focus**: {Entry stage}
**Check Size**: {Average}

---

## Portfolio Composition

_See [portfolio.json](/_data/portfolio.json) for complete data_

### By Category
{table from Step 2.1}

### By Sector
{table from Step 2.1}

### Stage Evolution

**At Entry**:
{table from Step 2.1}

**Current Stage**:
{table from Step 2.1}

**Thesis Coherence**: ✅ Strong / ⚠️ Moderate / ❌ Weak
{Brief analysis}

---

## Performance Analysis

### Winners (Major Fund Drivers)

{For each winner from portfolio.json}:
#### {Company} ⭐
- Entry: {Val} → Current: {Val} (**{X}x MOIC**)
- Portfolio Contribution: Drives {majority/significant} portion of value
- Status: {Revenue status, key traction}
- Strength: {What's working}
- Risk: {Primary concern}

### Emerging (Featured Portfolio)

{For each emerging from portfolio.json}:
#### {Company} 🌱
- Entry: {Val} → Current: {Val} ({X}x MOIC)
- Status: {Brief summary}
- Opportunity: {Growth potential}
- Risk: {Concern}

### Other (Stable/Early)

{Brief summary of companies in "other" category}

### Red Flags

{For each red flag company}:
#### {Company} ❌
- Concern: {Issue}
- Evidence: {Data}
- Pattern: {If multiple, note commonality}

---

## Key Strengths

{3-5 strengths with specific evidence}:

### {Strength Title} ✅
{Description}

**Evidence**: {Specific examples}
**Implication**: {Why it matters}

---

## Key Risks & Concerns

{3-4 major risks - use data from Step 2.3}:

### {Risk Title} ⚠️ {CRITICAL/HIGH/MODERATE}

**Problem**: {Description}
**Evidence**: {Data}
**Impact**: {Scenarios: best/base/bear case}
**Recommendation**: {Action}

---

## Defensibility Assessment

**Primary Moat Types**:
{Table from Step 2.2}

**Analysis**: {What moat types does fund bet on? Why? Strength assessment}

---

## Portfolio Health

**Overall Health**: **{Rating}**

{Narrative from Step 2.4 - 2-3 paragraphs}

**Key Metrics**:
- Winners: {X} companies
- Concentration: Top holding {X}%, top 3 {Y}%
- Evidence Quality: {X}% independent sources
- Transparency: {X} of {Y} companies documented

---

## Key Findings

{7-10 bullet points}:
1. **{Finding}**: {Evidence} → {Implication}
2. **{Finding}**: {Evidence} → {Implication}

---

## Recommendations

### Critical Actions
1. **{Action}**: {Why critical}
2. **{Action}**: {Why critical}

### Further Investigation
1. **{Area}**: {Why} | Questions: {List}
2. **{Area}**: {Why} | Questions: {List}

---

**Data**: [portfolio.json](/_data/portfolio.json)
**Version**: 1.0 | **Updated**: {Date}
```

### Step 3.2: Quality Check

**Checklist**:
- [ ] All companies analyzed and categorized
- [ ] Claims supported by specific data
- [ ] Source quality documented (Independent/Affiliated/Dataroom)
- [ ] No redundancy (info presented once, not repeated)
- [ ] Balanced (strengths + risks)
- [ ] Actionable recommendations
- [ ] portfolio.json valid and complete

### Step 3.3: Mark Complete

Update `research/companies/portfolio-list.md` Progress Tracker:
```markdown
- [x] Phase 0: Load Portfolio
- [x] Phase 1: Company Assessment (Complete: X/X)
- [x] Phase 2: Portfolio Analysis
- [x] Phase 3: Output

**Output**: marketing-to-reality/portfolio-analysis.md
**Data**: marketing-to-reality/_data/portfolio.json
```

---

## Resumability

**Pause points**:
- After Phase 0 (portfolio loaded)
- After batch of companies (Phase 1)
- After Phase 2 (analysis complete)

**Resume**: Read `research/companies/portfolio-list.md` Progress Tracker → skip to next incomplete step

**Best practice**: Update progress after each batch (5-7 companies)

---

## Troubleshooting

**Dataroom valuations outdated**: Use research valuations (more current)

**Missing research**: If <80% have research, run `vc-research.md` first; otherwise categorize as "Other"

**Can't calculate portfolio value %**: Use qualitative assessment ("drives majority of value" vs precise %)

**Conflicting data**: Document all sources/dates; use most recent independent source; note discrepancies

**No clear winners**: Valid finding; assess if portfolio is too early OR concerning lack of breakouts

---

## Version History

- **v2.0** (2025-01-20): Streamlined workflow
  - Removed time estimates
  - Added portfolio.json structured output
  - Renamed source tiers: Independent/Affiliated/Dataroom
  - Merged categories: "Other" combines stable + too early
  - Fixed winner definition: drives majority of value (not rigid >$5B)
  - Split stage tables: entry vs current
  - Removed execution risk section
  - Reduced length 46% while maintaining quality
