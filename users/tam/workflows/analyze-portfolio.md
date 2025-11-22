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

**For ALL companies from xlsx**, extract:
- Entry check size, current value, MOIC
- Entry stage (Seed/A/B/C) and current stage
- Sector/category (infer from company description if not explicit)

This enables full-portfolio Stage Evolution and By Sector tables (not just researched companies).

**Then for researched companies**, read `independent-research.md` for:
- More recent valuation (if research shows higher than dataroom's valuation date)
- Performance metrics (revenue, traction, milestones)
- Lead investors
- Source quality (Independent/Affiliated/Dataroom)

**Value Presentation**: Use dataroom values as baseline. If research shows newer valuation:
- "Dataroom: ${check} at ${dataroom MOIC}x (based on ${old val}); research shows ${new val} - current value likely higher"
- Do NOT calculate your own MOIC from valuations - use dataroom MOIC or note it cannot be calculated

**Source Citation**: Cite specific documents with links (not generic "research"):
- Dataroom: `[Source: Portfolio Summary ({date})]` (xlsx not linkable on static site)
- Research: `[Source: [{company}](../../research/companies/{company}/independent-research/)]`
- Specific source: `[Source: [{doc-name}](../../research/companies/{company}/sources/{doc}/)]`
- Independent: `[Source: {Publication Name}, {URL}]`

Note: Use clean URLs (no .md extension, trailing slash) since Eleventy converts markdown to HTML.

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

**Categorization** (EXCLUSIVE - each company appears in only one category):

**WINNERS**: Drive majority of portfolio value
- Current valuation represents significant portion of total portfolio
- Strong MOIC (typically >10x) OR absolute scale with market leadership
- Tier-1 co-investor validation at scale
- Revenue traction or clear path to major returns

**EMERGING**: Featured companies, solid fundamentals
- Strong traction but not yet massive scale
- MOIC 2-8x with growth potential
- Quality signals, execution TBD

**RED FLAGS**: Warning signs (requires concrete evidence of misrepresentation) - TAKES PRIORITY
- Valuation ahead of traction (with weak moat/competition)
- False/misleading dataroom claims (material discrepancies: failed major deals, cancelled partnerships)
- Nonstandard valuation methods
- Intense competitive threats (existential, not normal competition)
- **NOT red flags**: Timeline discrepancies from normal fundraising delays (companies often announce rounds late, sometimes don't announce, sometimes lump rounds together)
- **If red flag identified**: Remove from Winners/Emerging/Other and place exclusively in Red Flags

**OTHER**: Stable performers or too early to assess
- Modest performance (1-3x) OR very early stage
- Limited public information OR insufficient timeline

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

**Timeline guidance**: Investment dates preceding public announcements are common (companies announce late, batch announcements, or skip them). Only flag with concrete evidence of misrepresentation vs. plausible normal explanation.

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
  "dataroom_source": "{xlsx filename}",
  "overall_health": "STRONG" | "MODERATE" | "WEAK",
  "health_descriptor": "{brief descriptor}",

  "portfolio_overview": {
    "total_companies": 34,
    "researched": 13,
    "research_coverage": "38%",
    "writedowns": 4,
    "by_category": { "winners": 2, "emerging": 5, "red_flags": 2, "other": 3, "unresearched": 21 }
  },

  "executive_summary": {
    "strength": "{key strength with evidence}",
    "primary_risk": "{primary risk}",
    "thesis": "{investment thesis}"
  },

  "by_sector": [
    { "sector": "{Sector}", "count": X, "notable": ["{Company} ⭐", "{Company} 🌱"] }
  ],

  "stage_evolution": {
    "at_entry": { "pre_seed_seed": X, "series_a": X, "series_bc": X, "late_stage": X },
    "current": { "pre_seed_seed": X, "series_a": X, "series_bc": X, "late_stage": X },
    "analysis": "{brief analysis}"
  },

  "defensibility": {
    "by_moat": [
      { "type": "Technical", "count": X, "assessment": "Strong|Moderate|Weak", "notes": "{notes}" }
    ],
    "analysis": "{moat analysis}"
  },

  "companies": {
    "winners": [{
      "name": "{Company}",
      "icon": "⭐",
      "sector": "{Sector}",
      "dataroom": { "check": "${X}K", "moic": X.XX, "valuation_basis": "${X}B" },
      "research": { "current_valuation": "${X}B", "valuation_note": "{if newer than dataroom}" },
      "portfolio_contribution": "{majority/significant}",
      "revenue_status": "Pre-revenue" | "Commercial",
      "status": "{current state}",
      "strength": "{key strengths}",
      "risk": { "level": "HIGH|MODERATE|LOW", "description": "{risk description}" },
      "primary_moat": "Technical",
      "moat_strength": "Strong",
      "source_quality": "independent|affiliated|dataroom",
      "sources": [{ "name": "{doc}", "path": "{relative path}", "type": "dataroom|research" }]
    }],
    "emerging": [{ "...similar structure, with opportunity instead of strength..." }],
    "red_flags": [{ "...similar, with concern/evidence/pattern fields..." }],
    "other": [{ "name": "{Company}", "sector": "{Sector}", "dataroom": {...}, "status": "{notes}" }],
    "unresearched": [{ "name": "{Company}", "entry": "${X}M", "current": "${X}M", "moic": X.X, "note": "{optional}" }]
  },

  "key_risk": {
    "title": "{Risk Title}",
    "level": "HIGH|MODERATE|LOW",
    "problem": "{1-2 sentences}",
    "evidence": ["{evidence point 1}", "{evidence point 2}"],
    "recommendation": "{action}"
  },

  "recommendations": {
    "critical": [{ "action": "{action}", "details": "{details}" }],
    "further_investigation": [{ "area": "{area}", "why": "{why}", "questions": ["{q1}", "{q2}"] }]
  },

  "source_tier_summary": { "independent": X, "affiliated": X, "dataroom": X },
  "version": "2.0",
  "last_updated": "YYYY-MM-DD"
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

**Stage Evolution**:
| Stage | Count at Entry | Count Today |
|-------|----------------|-------------|
| Pre-Seed/Seed | {X} | {X} |
| Series A | {X} | {X} |
| Series B/C | {X} | {X} |
| Late Stage (Series C+) | {X} | {X} |

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

**Portfolio Concentration** (VC Power Law):
- Top holding: {Company} represents {X}% of value
- Top 3: {Y}% of value
- Note: Concentration is normal for VC portfolios due to power law returns. Focus on whether top holdings have defensible valuations and execution capability, not concentration percentage itself
- Assessment: Are top holdings' valuations justified by performance and defensibility?

**Valuation Methodology Risk**:
- Basis: Latest-round pricing / External appraisal / Subjective marks
- Unrealized gains: {X}% of portfolio value
- Bull market impact: Marks set during 2024-2025 AI bubble?
- Red flags: >$1B valuation + <$10M revenue, nonstandard methods, 10+ years to liquidity
- Assessment: Low / Moderate / High
- Implication: Will realized returns match paper returns?

**Portfolio Coverage**:
- Companies researched: {X} of {Y total} ({Z}%)
- Focus: Winners and emerging companies are most important to analyze
- Note: Analyzing winners + emerging = effective full portfolio analysis
- Failed investments: Disclosed? Named? Analyzed?

**Evidence Quality** (Flag only if suggests overvaluation risk):
- Independent sources: {X} companies ({Y}%)
- Affiliated: {X} companies
- Dataroom-only: {X} companies
- **Critical assessment**: Flag only when weak evidence + reason to believe overvaluation
  - Lower risk: Companies marked at 1x with weak evidence (limited downside)
  - Higher risk: Companies marked significantly above entry with weak evidence + no clear traction
- Red flags found: {List companies with concrete evidence of false/misleading claims}
- Focus on: Material discrepancies between dataroom claims and reality (failed major deals, timeline mismatches with concrete evidence)

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
- Valuation ahead of traction **in winners** (more concerning than in emerging)
- Nonstandard valuation methods **in winners**
- Weak moats, intense competition **in winners** (more concerning than in emerging)
- Red flags in any category (but assess severity by stage: winners with red flags = critical, emerging with red flags = concerning)
- Limited commercial traction **in winners** (expected in emerging, but problematic in companies driving majority of value)
- Poor transparency, selective disclosure
- Dataroom-only evidence for high-value holdings

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

{2-3 paragraphs covering: Overall health assessment, major winners with brief validation, primary risk (typically execution in top holdings), thesis coherence. This IS the synthesis - do not repeat elsewhere.}

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

{Table from xlsx - ALL companies, not just researched}

**Thesis Coherence**: ✅ Strong / ⚠️ Moderate / ❌ Weak
{Brief analysis}

---

## Defensibility Assessment

**Primary Moat Types**:
{Table from Step 2.2 - researched companies only}

**Analysis**: {What moat types does fund bet on? Why? Strength assessment}

---

## Performance Analysis

### Winners (Major Fund Drivers)

{For each winner from portfolio.json}:
#### {Company} ⭐
- **Dataroom**: ${check} at {X}x MOIC (based on ${dataroom val}); {if research shows newer: "research shows ${new val} - current value likely higher"}
- **Portfolio Contribution**: Drives {majority/significant} portion of value
- **Status**: {Revenue status, key traction}
- **Strength**: {What's working}
- **Risk**: {Primary concern} [Source: [{doc}](../research/companies/{company}/sources/{doc}.md)]

### Emerging (Featured Portfolio)

{For each emerging from portfolio.json}:
#### {Company} 🌱
- **Dataroom**: ${check} at {X}x MOIC → ${current val}
- **Status**: {Brief summary}
- **Opportunity**: {Growth potential}
- **Risk**: {Concern} [Source: [{doc}](../research/companies/{company}/independent-research.md)]

### Red Flags

{For each red flag company}:
#### {Company} ❌
- **Dataroom**: ${check} at {X}x MOIC → ${current val}
- **Status**: {Current state, revenue/pre-revenue}
- **Opportunity**: {What could work if issues resolve}
- **Concern**: {Issue} [Source: [{doc}](../research/companies/{company}/sources/{doc}.md)]
- **Evidence**: {Data}
- **Pattern**: {If multiple, note commonality}

### Other (Stable/Early)

{Brief summary of companies in "other" category}

---

## Key Risk

{Single consolidated risk if material - typically valuation/execution for top holdings}:

### {Risk Title} ⚠️

**Problem**: {1-2 sentences}
**Evidence**: {Key data points}
**Recommendation**: {Action}

Note: Do NOT include separate "impact" or "scenarios" subsections - implications are self-evident. Do NOT flag "evidence quality concerns" - limited evidence is expected for early-stage companies in power-law portfolios. Do NOT flag "portfolio transparency" - research coverage reflects analyst process, not fund characteristics.

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
- [ ] **No redundancy** - each insight appears ONCE (Executive Summary synthesizes, sections provide detail, never repeat)
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
