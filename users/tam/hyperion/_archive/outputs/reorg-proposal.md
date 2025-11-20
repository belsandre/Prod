# Hyperion Folder Reorganization Proposal

**Date**: 2025-11-17
**Version**: 3.0 (Output-Focused, Iterative Analysis)
**Purpose**: Reorganize users/tam/hyperion/ around how outputs are viewed and used, supporting iterative analysis as diligence evolves

---

## Table of Contents

1. [Current Structure Issues](#current-structure-issues)
2. [Design Principles](#design-principles)
3. [Proposed New Structure](#proposed-new-structure)
4. [Executive Summary Template](#executive-summary-template)
5. [Structured Data Opportunities](#structured-data-opportunities)
6. [Navigation & Linking](#navigation-linking)
7. [Iterative Analysis Support](#iterative-analysis-support)
8. [Incremental Migration Path](#incremental-migration-path)
9. [Benefits Summary](#benefits-summary)
10. [Open Questions](#open-questions)
11. [Next Steps](#next-steps)

---

## Current Structure Issues

### Problem 1: Workflow-Focused, Not Output-Focused
- Structure reflects processing steps (dataroom → portfolio → network → synthesis)
- Should reflect **how you view results**: executive summary → findings → supporting evidence
- Current: "Where did this come from?" New: "What do I need to know?"

### Problem 2: No Executive Summary Entry Point
- No single starting point that shows:
  - What data sources we have
  - What analysis we've completed
  - What's still left to do
  - What the main findings and recommendations are
- User must read multiple files to understand status

### Problem 3: Hard to Navigate from Findings to Evidence
- Findings scattered across multiple analysis files
- No easy way to click through from a recommendation to the supporting analysis and sources
- Can't easily answer "Why is this a critical action?"

### Problem 4: Linear Structure for Iterative Process
- Current structure assumes linear workflow (phase 1 → 2 → 3 → 4)
- Reality: Getting new information (meeting notes, new data sources) requires revisiting earlier analyses
- No clear way to track:
  - What analyses need to be revisited when new data arrives
  - How new information changed previous findings
  - What's the delta between analysis v1 and v2

### Problem 5: Too Much New Terminology
- Introduced terms need explanation (Tier 1/2/3, Phase 1/2/3/4)
- Glossaries are poor UX
- Better to use existing, intuitive terms (dataroom, research, findings, recommendations)

### Problem 6: Data Mixed with Presentation
- Analyses mix structured data with narrative
- Hard to reuse data for comparisons or charts
- No programmatic access to findings

---

## Design Principles

### 1. Output-Focused Structure

**Organize by how you consume information, not how it was created**

Users start with:
- **Executive Summary**: What do I need to know right now?
- **Findings**: What did we learn?
- **Recommendations**: What should I do next?

Then drill down to:
- **Supporting Analysis**: How did we reach these findings?
- **Source Evidence**: What's the proof?

Not organized by processing workflow (dataroom → portfolio → network → synthesis).

---

### 2. Support Iterative Analysis

**Diligence is not linear - design for iteration**

When new information arrives (meeting notes, Crunchbase data, reference checks):
- Identify which analyses need revisiting
- Re-run those analyses
- Track what changed (delta from previous version)
- Update findings and recommendations accordingly

Support versioning:
- `portfolio-assessment.md` (current)
- `portfolio-assessment-2025-11-15.md` (snapshot after Crunchbase data added)
- `_process/change-log.md` (what changed and why)

---

### 3. Use Intuitive Terms, Not New Jargon

**No glossaries needed**

Avoid introducing terms that need explanation:
- ❌ Tier 1/2/3 evidence (requires glossary)
- ❌ Phase 1/2/3/4 (requires workflow diagram)
- ✅ Dataroom materials (private info provided by target)
- ✅ Independent sources (journalism, verified databases - objective)
- ✅ Target sources (publicly accessible but target-controlled/influenced)

**Source Type Hierarchy** (from most to least reliable):
1. **Independent sources**: TechCrunch, Bloomberg, Crunchbase, verified journalism (objective, third-party)
2. **Target sources**: GP's LinkedIn, Substack, social media; company websites, press releases (externally acquired, target-influenced)
3. **Dataroom materials**: GP-provided private documents, confidential materials (private, target-provided)

**Key Distinction**:
- **Dataroom materials**: Private information provided BY the target
- **Target sources**: Public information controlled/influenced BY the target (but externally acquired)
- **Independent sources**: Information created by third parties, not controlled by target

Use terminology the industry already knows:
- Dataroom, due diligence, reference checks, portfolio companies, co-investors, target sources

---

### 4. Separate Data from Presentation

**Structured data (JSON) + Human narrative (Markdown)**

Mature, stable outputs should be JSON:
- Portfolio company list with valuations, funding rounds, co-investors
- Network statistics (connections by category, relationship strength)
- Timeline of key events

Benefits:
- Programmatic comparison between funds
- Charts and visualizations
- Automated validation
- Easy updates when new data arrives

Narrative analyses remain Markdown:
- Executive summary
- Investment recommendation
- Qualitative assessments

---

### 5. Full Traceability

**Every finding links back to supporting evidence**

Executive Summary → Findings → Analysis → Sources

Example navigation path:
```
Executive Summary: "Critical: Verify GP relationships"
  ↓ Click for details
Recommendation: "100% of value-add claims unverified"
  ↓ Click for analysis
Finding: "No portfolio founders mention GP help in public sources"
  ↓ Click for sources
Evidence: [Links to 14 company research files, each with sources]
  ↓ Click for raw data
Sources: TechCrunch articles, LinkedIn profiles, Crunchbase
```

No dead ends. Always able to drill down or trace back.

---

### 6. Clear Status Visibility

**Always show: What we have, what we've done, what's left**

Executive summary shows:
- **Data Sources**: Dataroom (✓), Crunchbase (⏳ pending), Reference checks (⏳ pending)
- **Analysis Completed**: Portfolio (14/24 companies), Network (✓), Timeline (✓), Claims validation (✓)
- **Gaps**: 10 companies not researched, GP value-add claims unverified, Henry Bellew analysis incomplete

---

## Proposed New Structure

**Key Changes from Current**:
- **START** with executive summary (not buried 3 levels deep)
- Organize by **output type** (findings, recommendations, evidence) not workflow steps
- **No phase terminology** - use intuitive folder names
- **Separate JSON data** from markdown narratives
- **Iteration support** with versioning and change tracking

```
users/tam/hyperion/
│
├── index.md                            # 🚀 EXECUTIVE SUMMARY (start here)
│   │                                   # - Current status (data sources, analysis done, gaps)
│   │                                   # - Key findings (portfolio quality, network strength, red flags)
│   │                                   # - Critical recommendations (what to do next)
│   │                                   # - Links to drill down into details
│
├── research/                           # 📚 RAW EVIDENCE (what we gathered)
│   ├── dataroom/                       # Private materials provided by target
│   │   ├── GP Bio.md
│   │   ├── Fund I.md
│   │   ├── Sourcing Differentiation.md
│   │   ├── Portfolio Company Profiles.md
│   │   └── [all dataroom files...]
│   │
│   ├── companies/                      # Per-company research
│   │   ├── figure/
│   │   │   ├── independent-research.md # Independent sources (TechCrunch, Bloomberg, etc.)
│   │   │   ├── target-sources.md       # Company website, press releases, pitch deck
│   │   │   └── funding-history.md      # Verified funding rounds from Crunchbase
│   │   ├── quantinuum/
│   │   ├── normal-computing/
│   │   └── [24 total companies...]
│   │
│   └── people/                         # GP and network raw data
│       ├── dillon-dunteman/
│       │   ├── independent-research.md # Third-party sources (Vista alumni, news)
│       │   ├── target-sources/         # Target-controlled public info
│       │   │   ├── linkedin-profile.md # GP's LinkedIn
│       │   │   ├── linkedin-export/    # LinkedIn connection data (CSV)
│       │   │   │   ├── connections_1k.csv
│       │   │   │   ├── connections_harvard.csv
│       │   │   │   └── connections_deeptech.csv
│       │   │   └── substack-archive/   # GP's Substack posts
│       │   └── background-sources.md   # Vista, Firmament research
│       │
│       └── henry-bellew/
│           └── research-notes.md       # What we found (or didn't find)
│
├── findings/                           # 📊 ANALYSIS (how we interpreted the evidence)
│   ├── portfolio-assessment.md         # ANALYSIS: Portfolio quality, winners, concerns
│   ├── network-analysis.md             # ANALYSIS: GP network depth and relationship validation
│   ├── claims-analysis.md            # ANALYSIS: Which GP claims verified/unverified
│   ├── timeline.md                     # ANALYSIS: Chronological fund narrative with interpretation
│   ├── gp-analysis.md                  # ANALYSIS: Dillon background, Henry absence
│   │
│   ├── _data/                          # 📊 STRUCTURED DATA (supports findings above)
│   │   ├── portfolio.json              # Companies, valuations, funding rounds, co-investors
│   │   ├── network.json                # GP connections, relationship strength, dimensions
│   │   ├── timeline.json               # Key events with dates and sources
│   │   ├── claims.json                 # GP claims + validation status + evidence links
│   │   └── gp-profiles.json            # Dillon, Henry backgrounds and involvement
│   │
│   ├── _process/                       # 🔧 ANALYSIS METHODOLOGY (how we did the work)
│   │   ├── methodology.md              # How to interpret evidence quality
│   │   ├── analysis-log.md             # Chronological work done
│   │   ├── data-updates.md             # When new data added, what changed
│   │   ├── workflows-used.md           # Which workflows generated what
│   │   └── change-log.md               # Version history of analyses
│   │
│   └── _archive/                       # Previous versions when analyses updated
│       ├── portfolio-assessment-2025-11-15.md
│       └── network-analysis-2025-11-10.md
│
└── recommendations/                    # 🎯 ACTIONABLE NEXT STEPS (what to do)
    ├── critical/
    │   ├── verify-gp-relationships.md  # Founder reference checks
    │   └── validate-figure-execution.md # Verify customer deployment claims
    ├── high-priority/
    │   ├── investigate-henry-bellew.md  # Understand co-GP absence
    │   └── validate-customer-claims.md  # Cross-check deployment stories
    └── medium-priority/
        ├── benchmark-portfolio.md       # Compare to similar funds
        └── deep-dive-quantinuum.md      # Second-largest holding validation
```

**Navigation Flow - Full Traceability**:
```
START: index.md (executive summary)
  ↓
Critical Recommendation: "Verify GP relationships"
  ↓
Click → recommendations/critical/verify-gp-relationships.md
  ↓ "Why this matters"
Links to → findings/claims-analysis.md (ANALYSIS: "100% of value-add claims unverified")
  ↓ "Evidence reviewed"
Links to → research/companies/figure/independent-research.md (RAW: TechCrunch, Bloomberg - no GP mention)
  AND → research/companies/figure/target-sources.md (RAW: Company website, press releases - no GP mention)
  AND → research/dataroom/GP Bio.md (RAW: GP claims of value-add)
  ↓ "Structured data"
Can also view → findings/_data/claims.json (programmatic access to all claims + validation status)
```

**Key Insight**: The three-layer structure provides complete traceability:
1. **research/** = Raw evidence (what sources say, verbatim or summarized)
2. **findings/** = Analysis layer (how we interpreted the evidence, what patterns we see, what conclusions we draw)
3. **recommendations/** = Action layer (what to do based on findings)

Each layer links bi-directionally to the layers above and below.

---

## Executive Summary Template

The `index.md` file is the starting point for all users. It should answer three questions:

1. **Where are we?** (Status/progress)
2. **What did we learn?** (Key findings)
3. **What should we do?** (Recommendations)

### Template Structure

```markdown
# Hyperion Ventures Fund I: Due Diligence Assessment

**Last Updated**: 2025-11-17
**Overall Assessment**: 7.5/10 (Above Average/Strong)

---

## Current Status

### Data Sources Available
- ✅ **Dataroom**: GP Bio, Fund I details, Portfolio profiles, Sourcing deck
- ✅ **Public Research**: 14 companies researched via TechCrunch, LinkedIn, Crunchbase
- ✅ **Network Data**: 1000+ LinkedIn connections analyzed
- ⏳ **Pending**: Crunchbase export, Reference checks, Meeting notes

### Analysis Completed
- ✅ **Portfolio Assessment**: 14/24 companies researched ([view →](findings/portfolio-assessment.md))
- ✅ **Network Analysis**: Dillon's connections quantified ([view →](findings/network-analysis.md))
- ✅ **Claims Validation**: GP claims verified against independent sources ([view →](findings/claims-analysis.md))
- ✅ **Timeline**: Objective chronology of fund events ([view →](findings/timeline.md))
- ⏳ **Incomplete**: 10 companies not yet researched, Henry Bellew analysis partial

### What's Left to Do
- **Research**: 10 remaining portfolio companies
- **Validation**: Verify GP value-add claims via reference checks
- **Investigation**: Understand Henry Bellew's role and absence from public data
- **Benchmarking**: Compare portfolio metrics to similar funds

---

## Key Findings

### Portfolio Quality: Strong Winners, Limited Visibility on Rest
- **Standout**: Figure AI ($39.5B, 94x MOIC), Quantinuum ($5B, 119x)
- **Concern**: 10 companies not researched, 3 unnamed underperformers
- **Co-investors**: Tier-1 syndicate (BMW i Ventures, BlackRock, Intel Capital)
- [View full portfolio assessment →](findings/portfolio-assessment.md)

### Network Strength: Deep Connections, Unproven Conversion
- **Harvard Network**: 150 alumni connections, 603 total from graduation years
- **Deeptech Focus**: 33% of connections in deeptech industries
- **VC/PE Relationships**: 80+ investors (Vista, Tamarack, Coatue ties)
- **Unverified**: No proof network converts to referrals or deal flow
- [View full network analysis →](findings/network-analysis.md)

### Claims Validation: Independent Sources Contradict GP Spin
- **100% of GP value-add claims unverified** (hiring help, VC intros, advisory)
- **Missing data**: 18/24 investment dates, amounts, or details not provided
- **Red flag**: Henry Bellew (co-GP) has zero documented portfolio involvement
- [View full claims validation →](findings/claims-analysis.md)

### GP Background: Dillon Strong, Henry Absent
- **Dillon Dunteman**: Harvard MBA, 5 years at Vista Equity, Firmament Capital experience
- **Thought Leadership**: Active Substack on deeptech trends (credibility signal)
- **Henry Bellew**: Co-GP with no visible network, portfolio involvement, or public presence
- [View full GP analysis →](findings/gp-analysis.md)

---

## Critical Recommendations

### 🔴 **CRITICAL**: Verify GP Relationships
**Why**: 100% of value-add claims rely on dataroom (GP-controlled) sources only

**What to do**:
1. Reference checks with 6 claimed founder relationships
2. Verify hiring referrals with Figure AI, Quantinuum
3. Confirm VC introduction claims with co-investors

[View full recommendation →](recommendations/critical/verify-gp-relationships.md)

---

### 🔴 **CRITICAL**: Validate Figure AI Execution
**Why**: 50%+ of portfolio value concentrated in Figure AI - deployment claims unverified

**What to do**:
1. Confirm BMW deployment status (GP claims "first humanoid in F500")
2. Verify customer pipeline claims
3. Cross-check Series C valuation sources

[View full recommendation →](recommendations/critical/validate-figure-execution.md)

---

### 🟠 **HIGH**: Investigate Henry Bellew Role
**Why**: Co-GP with zero portfolio involvement is a red flag for fund governance

**What to do**:
1. Understand Henry's actual role (capital only? silent partner?)
2. Clarify decision-making authority
3. Assess risk if Dillon becomes unavailable

[View full recommendation →](recommendations/high-priority/investigate-henry-bellew.md)

---

### 🟡 **MEDIUM**: Complete Portfolio Research
**Why**: Only 14/24 companies researched - missing view of underperformers

**What to do**:
1. Research remaining 10 companies
2. Identify the 3 unnamed underperformers
3. Calculate full portfolio MOIC distribution

---

## Analysis Details

All findings and supporting evidence are available:

- **Findings**: [portfolio-assessment.md](findings/portfolio-assessment.md), [network-analysis.md](findings/network-analysis.md), [claims-analysis.md](findings/claims-analysis.md)
- **Recommendations**: [critical/](recommendations/critical/), [high-priority/](recommendations/high-priority/), [medium-priority/](recommendations/medium-priority/)
- **Company Research**: [research/companies/](research/companies/)
- **GP Research**: [research/people/](research/people/)
- **Structured Data**: [findings/_data/portfolio.json](findings/_data/portfolio.json), [findings/_data/network.json](findings/_data/network.json)

---

## Methodology

### Data Sources Used
- **Independent sources**: TechCrunch, Bloomberg, Crunchbase, verified journalism (objective, third-party - most reliable)
- **Target sources**: GP's LinkedIn/Substack/social media, company websites, press releases (externally acquired, target-influenced)
- **Dataroom materials**: GP-provided private documents, confidential materials (private, target-provided - requires verification)

### Evidence Quality
- ✅ **Verified**: Claim supported by independent sources (high confidence)
- ⚠️ **Partial**: Claim partially supported or only from target sources (medium confidence)
- ❓ **Unverified**: Claim from dataroom only, no external confirmation (requires validation)
- ❌ **Contradicted**: Independent sources contradict dataroom/target source claims (red flag)

### How This Was Generated
- **Workflows**: [vc-research.md](findings/_process/workflows-used.md), deal-prioritization.md, validator.md
- **Analysis Log**: [findings/_process/analysis-log.md](findings/_process/analysis-log.md)
- **Last Updated**: 2025-11-17

[View full methodology →](findings/_process/methodology.md)

---

**Questions?** See [Open Questions](#open-questions) or contact the research team.
```

---

## Structured Data Opportunities

### 1. portfolio.json

**Why**: Most mature, stable data - perfect for JSON conversion

**What to include**:
- Company names, sectors, investment dates
- Valuations, funding rounds, MOICs
- Co-investors
- Source citations (with URLs)

**Example**:
```json
{
  "fund_name": "Hyperion Ventures Fund I",
  "overall_rating": 7.5,
  "companies": [
    {
      "id": "figure-ai",
      "name": "Figure AI",
      "sector": "Robotics",
      "description": "Humanoid robots for manufacturing",
      "investment": {
        "date": "2023-04-01",
        "stage": "Pre-Seed",
        "amount_usd": 500000,
        "valuation_at_entry_usd": 42000000
      },
      "current_valuation": {
        "amount_usd": 39500000000,
        "date": "2024-09-15",
        "source": "https://techcrunch.com/2024/09/15/figure-ai-series-c"
      },
      "moic": 94,
      "co_investors": ["BMW i Ventures", "BlackRock", "Intel Capital", "Nvidia"],
      "gp_relationship": {
        "sourcing_claim": "Sourced via Tamarack Global relationship",
        "value_add_claims": ["Hiring referrals", "Customer introductions"],
        "verification_status": "partial"
      },
      "sources": [
        {
          "type": "independent",
          "url": "https://techcrunch.com/2024/09/15/figure-ai-series-c",
          "title": "Figure AI raises Series C at $39.5B valuation",
          "date": "2024-09-15"
        },
        {
          "type": "independent",
          "url": "https://www.bloomberg.com/news/bmw-deploys-figure-humanoids",
          "title": "BMW Deploys Humanoid Robots in South Carolina Plant",
          "date": "2024-08-20"
        }
      ]
    }
  ]
}
```

**Benefits**:
- Can programmatically query: "Show all companies with >50x MOIC"
- Easy to generate charts (MOIC distribution, sector breakdown)
- Simple to compare to other funds
- Automated validation (e.g., check all companies have independent sources)

---

### 2. network.json

**Why**: Network statistics are quantitative and stable

**What to include**:
- Total connections count
- Breakdown by category (Harvard, deeptech, VC/PE)
- Claimed relationships and verification status

**Example**:
```json
{
  "gp_id": "dillon-dunteman",
  "network_summary": {
    "total_connections": 1000,
    "harvard_alumni": 150,
    "deeptech_pct": 33,
    "vcpe_investors": 80
  },
  "claimed_relationships": [
    {
      "founder": "Brett Adcock",
      "company": "Figure AI",
      "relationship_type": "sourcing",
      "claim": "Sourced via Tamarack Global relationship",
      "verification_status": "partial",
      "source": "dataroom/Sourcing Differentiation.md"
    },
    {
      "founder": "Ilyas Khan",
      "company": "Quantinuum",
      "relationship_type": "sourcing",
      "claim": "Direct founder relationship",
      "verification_status": "unverified",
      "source": "dataroom/GP Bio.md"
    }
  ]
}
```

---

### 3. timeline.json

**Why**: Timeline is a sequence of events - perfect for structured data

**What to include**:
- Date, event description, source
- Event type (investment, exit, milestone)

**Example**:
```json
{
  "timeline": [
    {
      "date": "2023-04-01",
      "event": "Hyperion invests $500K in Figure AI pre-seed",
      "event_type": "investment",
      "source": "dataroom/Fund I.md",
      "source_quality": "dataroom"
    },
    {
      "date": "2024-02-26",
      "event": "Figure AI raises $675M Series B at $2.6B valuation (OpenAI, Nvidia, Bezos)",
      "event_type": "funding_round",
      "source": "https://techcrunch.com/2024/02/26/figure-ai-series-b",
      "source_quality": "independent"
    }
  ]
}
```

---

### 4. claims.json

**Why**: Claims validation is core to analysis - needs structure for tracking

**What to include**:
- Claim ID, text, source
- Validation status, evidence
- Recommendations generated

**Example**:
```json
{
  "claims": [
    {
      "id": "gp-value-add-1",
      "category": "value_add",
      "text": "Dillon provides hiring referrals to portfolio companies",
      "source": {
        "file": "research/dataroom/GP Bio.md",
        "page": 2,
        "source_quality": "dataroom"
      },
      "validation": {
        "status": "unverified",
        "evidence": [
          {
            "type": "portfolio_research",
            "finding": "No portfolio founders mention hiring help in public sources",
            "source": "findings/portfolio-assessment.md"
          }
        ],
        "recommendation_id": "verify-gp-relationships"
      }
    }
  ]
}
```

---

### 5. gp-profiles.json

**Why**: GP background data is factual and stable

**What to include**:
- Name, background, experience
- Network stats, involvement metrics

**Example**:
```json
{
  "gps": [
    {
      "id": "dillon-dunteman",
      "name": "Dillon Dunteman",
      "background": {
        "education": "Harvard Business School MBA",
        "prior_experience": [
          {"company": "Vista Equity Partners", "role": "Investor", "years": 5},
          {"company": "Firmament Capital", "role": "Associate", "years": 2}
        ]
      },
      "portfolio_involvement": {
        "companies_documented": 14,
        "sourcing_claims": 6,
        "value_add_documented": 0
      },
      "thought_leadership": {
        "substack": "https://substack.com/@dillondunteman",
        "posts_count": 45,
        "topics": ["deeptech", "AI", "robotics"]
      }
    },
    {
      "id": "henry-bellew",
      "name": "Henry Bellew",
      "background": {
        "education": "Unknown",
        "prior_experience": []
      },
      "portfolio_involvement": {
        "companies_documented": 0,
        "red_flags": ["No public network", "Zero portfolio involvement"]
      }
    }
  ]
}
```

---

## Navigation & Linking

### Bi-Directional Links

Every finding should link to:
- **Supporting evidence** (drill down)
- **Recommendations** (what to do)
- **Related findings** (cross-reference)

Every recommendation should link to:
- **Driving findings** (why this matters)
- **Evidence** (proof)
- **Related recommendations** (dependencies)

### Example: Recommendation File

```markdown
---
id: verify-gp-relationships
priority: critical
status: pending
---

# Recommendation: Verify GP Relationships Through Independent Founder Interviews

## Why This Matters (CRITICAL Risk Level)

100% of Dillon's value-add evidence comes from dataroom sources only. No independent validation exists for:
- Hiring referrals
- VC introductions
- Advisory support

**Finding**: [Claims Validation Analysis →](../../findings/claims-analysis.md#gp-value-add)

**Evidence**:
- [Figure AI Independent Research →](../../research/companies/figure/independent-research.md) - No mention of Dillon in TechCrunch, Bloomberg
- [Figure AI Target Sources →](../../research/companies/figure/target-sources.md) - Company website, press releases - no GP mention
- [Portfolio Assessment →](../../findings/portfolio-assessment.md#gp-relationships) - 14 companies researched, zero value-add documented

**Data**: [claims.json](../../findings/_data/claims.json) (see claim IDs: gp-value-add-1, gp-value-add-2, gp-value-add-3)

---

## Recommended Action

### 1. Founder Reference Checks

Contact 6 founders Dillon claims relationships with:
- Brett Adcock (Figure AI)
- Ilyas Khan (Quantinuum)
- [4 more from dataroom...]

**Questions to ask**:
- How did Hyperion source your deal?
- What value-add has Dillon provided post-investment?
- Can you provide specific examples of hiring help or introductions?

### 2. Co-Investor Validation

Reach out to tier-1 co-investors:
- BMW i Ventures
- BlackRock
- Intel Capital

**Questions**:
- Did Dillon bring this deal or did you co-invest separately?
- What's your assessment of Dillon's network and capabilities?

---

## Expected Timeline

2-3 weeks (founder outreach, scheduling, calls)

---

## Related Recommendations

- [Validate Figure AI Execution →](validate-figure-execution.md) (customer claims verification)
- [Investigate Henry Bellew →](../high-priority/investigate-henry-bellew.md) (understand co-GP role)

---

## If This Recommendation Not Completed

**Mitigation**: Discount GP value-add claims entirely, assess fund on portfolio quality alone

**Impact on Rating**: Could drop from 7.5/10 to 6.5/10 (network differentiation unproven)
```

---

## Iterative Analysis Support

### The Problem

Diligence is iterative. New information arrives that requires revisiting previous analyses:

**Example scenarios**:
1. **Crunchbase data arrives** → Need to update funding rounds, valuations
2. **Reference check completed** → Update claims validation, GP assessment
3. **New meeting notes** → May contradict earlier findings
4. **Portfolio company exit** → Update valuations, MOIC

Current structure doesn't support this well.

---

### The Solution

**1. Version Snapshots**

When updating an analysis, save previous version:
```
findings/
├── portfolio-assessment.md           (current version)
└── _archive/
    ├── portfolio-assessment-2025-11-15.md (before Crunchbase data)
    └── portfolio-assessment-2025-11-10.md (before reference checks)
```

**2. Change Log**

Track what changed and why in `findings/_process/change-log.md`:

```markdown
# Analysis Change Log

## 2025-11-17: Crunchbase Data Integration

**Data Source Added**: Crunchbase export (24 companies)

**Analyses Updated**:
- `findings/portfolio-assessment.md` - Added 6 missing investment dates
- `findings/_data/portfolio.json` - Updated funding rounds for 10 companies
- `findings/claims-analysis.md` - Verified 2 additional GP claims

**Key Changes**:
- Figure AI investment date corrected: 2023-04-01 (was estimated as Q2 2023)
- Quantinuum Series B confirmed: $300M at $5B valuation
- 3 companies had valuation discrepancies (GP claimed higher than Crunchbase)

**Findings Impact**:
- Portfolio rating: No change (7.5/10)
- Critical recommendations: No change
- New concern: Valuation discrepancies require investigation

**Recommendation Updates**:
- Added: `recommendations/medium-priority/investigate-valuation-gaps.md`

**Archived Versions**:
- `findings/_archive/portfolio-assessment-2025-11-15.md`
- `findings/_data/_archive/portfolio-2025-11-15.json`

---

## 2025-11-15: Reference Check - Figure AI

**Data Source Added**: Phone call with Brett Adcock (Figure AI founder)

**Analyses Updated**:
- `findings/claims-analysis.md` - Updated GP value-add claims
- `recommendations/critical/verify-gp-relationships.md` - Marked as in-progress

**Key Changes**:
- **CONTRADICTED**: Brett confirmed Dillon did NOT source the deal (Tamarack introduced directly)
- **VERIFIED**: Dillon provided 2 engineering hiring referrals (both hired)
- **UNVERIFIED**: Customer introduction claims (Brett wouldn't comment)

**Findings Impact**:
- Sourcing claim downgraded from "unverified" to "contradicted"
- Value-add partially verified (hiring help confirmed)
- Portfolio rating: No change (7.5/10)

**Recommendation Updates**:
- `verify-gp-relationships.md` updated: 5 remaining founders to check

**Archived Versions**:
- `findings/_archive/claims-analysis-2025-11-14.md`
```

**3. Data Update Tracking**

Track when new data sources arrive in `findings/_process/data-updates.md`:

```markdown
# Data Source Updates

| Date | Source | Files Added | Analyses Affected |
|------|--------|-------------|-------------------|
| 2025-11-17 | Crunchbase export | `research/dataroom/crunchbase-export.csv` | portfolio-assessment, claims-analysis |
| 2025-11-15 | Reference check (Brett Adcock) | `research/companies/figure/reference-check-founder.md` | claims-analysis |
| 2025-11-10 | Meeting notes (Dillon) | `research/people/dillon-dunteman/meeting-notes-2025-11-10.md` | gp-analysis |
```

**4. Impact Assessment**

When new data arrives, identify which analyses need updating:

**Crunchbase data** affects:
- ✅ `findings/portfolio-assessment.md` (funding rounds, valuations)
- ✅ `findings/_data/portfolio.json` (structured company data)
- ✅ `findings/timeline.md` (investment dates)
- ❌ `findings/network-analysis.md` (not affected)

**Reference check** affects:
- ✅ `findings/claims-analysis.md` (GP claims)
- ✅ `findings/portfolio-assessment.md` (GP relationship quality)
- ✅ `recommendations/critical/verify-gp-relationships.md` (progress update)
- ❌ `findings/network-analysis.md` (not affected)

---

## Incremental Migration Path

**Goal**: Migrate objective content first, preserve old files for reference, validate differences

**Philosophy**: Start with what's certain (folder structure, raw research), then tackle interpretive work (findings, recommendations) while keeping the old version available for comparison.

---

### PHASE 1: OBJECTIVE MIGRATION (Safe, No Deletion)

---

#### Step 1: Create New Folder Structure

**Time**: 5 minutes

**What to do**:
```bash
cd users/tam/hyperion/
mkdir -p research/{dataroom,companies,people}
mkdir -p findings/{_data,_process,_archive}
mkdir -p recommendations/{critical,high-priority,medium-priority}
```

**Result**: Empty folders created, zero risk

**Test**: `ls -la` to verify folders exist

---

#### Step 2: Migrate Dataroom (Objective Content)

**Time**: 10 minutes

**What to do**:
```bash
# Copy dataroom files to new location
cp -r dataroom/* research/dataroom/
```

**Result**: Dataroom files in new location, originals untouched

**Why objective**: These are GP-provided files, no interpretation required, safe to move

**Test**: Verify file count matches: `ls dataroom/ | wc -l` vs `ls research/dataroom/ | wc -l`

---

#### Step 3: Migrate Company Research (Objective Content)

**Time**: 30 minutes

**What to do**:
```bash
# Move all company research to new location, removing tier terminology
cp -r research/deals/tier-1/* research/companies/
cp -r research/deals/tier-2/* research/companies/

# Rename files within each company folder to match new structure
# Example: figure/research-notes.md → figure/independent-research.md
#          figure/pitch-deck-notes.md → figure/target-sources.md
```

**Result**: All company research in `research/companies/`, originals preserved in `research/deals/`

**Why objective**: These are research notes, not analysis - factual content only

**Test**: Verify all 24 companies present in `research/companies/`

---

#### Step 4: Migrate GP/People Research (Objective Content)

**Time**: 15 minutes

**What to do**:
```bash
# People research is already in research/people/, just reorganize
# Move raw data files (LinkedIn exports, etc.) to proper locations
```

**Result**: GP research organized, raw data clearly separated

**Why objective**: LinkedIn CSVs, background research notes are factual

**Test**: Verify CSV files and research notes present

---

### PHASE 2: STRUCTURED DATA CONVERSION (Objective Extraction)

---

#### Step 5: Extract Structured Data to JSON

**Time**: 3-4 hours

**What to do**:
- Create `findings/_data/portfolio.json` by extracting data from current outputs
- Create `findings/_data/network.json` (LinkedIn stats, connection counts)
- Create `findings/_data/timeline.json` (chronological events)
- Create `findings/_data/claims.json` (GP claims + validation status)
- Create `findings/_data/gp-profiles.json` (background data)

Use JSON schemas from "Structured Data Opportunities" section.

**Result**: All structured data in `findings/_data/`, source files untouched

**Why objective**: Extracting factual data (dates, numbers, names) into structured format

**Test**: Validate JSON schemas, verify data completeness

---

### PHASE 3: SUBJECTIVE CONTENT (Preserve Old for Reference)

---

#### Step 6: Preserve Old Findings for Reference

**Time**: 2 minutes

**What to do**:
```bash
# Create migration reference folder
mkdir -p migration-reference

# Copy ALL old findings/outputs for comparison
cp -r outputs/* migration-reference/
cp -r research/deals/ migration-reference/old-company-structure/
```

**Result**: Complete snapshot of old analysis preserved

**Why critical**: Old findings contain your interpretations - need to reference during rewrite

**Test**: Verify `migration-reference/` contains all old files

---

#### Step 7: Create New index.md (Executive Summary)

**Time**: 2-3 hours

**What to do**:
- Create `index.md` using template from this proposal
- Reference old files in `migration-reference/` as you write
- Include status, findings, recommendations
- Link to research files in new locations

**Result**: New executive summary exists

**Why subjective**: This is synthesis and interpretation

**Test**: Open `index.md`, verify all links work

---

#### Step 8: Create New Findings (Rewrite from Old)

**Time**: 4-6 hours

**What to do**:
For each old output file, create new finding:
- `migration-reference/vc-research-summary.md` → `findings/portfolio-assessment.md`
- `migration-reference/claims-analysis.md` → `findings/claims-analysis.md`
- `migration-reference/network-analysis.md` → `findings/network-analysis.md`
- Etc.

**Keep old files available**: Reference `migration-reference/` as you write

**Result**: New findings in `findings/`, old versions preserved

**Why subjective**: Analysis and interpretation may evolve during rewrite

**Test**: Compare new vs old side-by-side, note differences

---

#### Step 9: Create Recommendations (New Content)

**Time**: 3-4 hours

**What to do**:
- Create all recommendation files in `recommendations/`
- Use template from "Navigation & Linking" section
- Ensure full traceability (links to findings and research)
- Organize by priority

**Reference old files**: Check `migration-reference/` for recommendations scattered in old outputs

**Result**: All recommendations surfaced and prioritized

**Why subjective**: Recommendations require judgment

**Test**: Navigate from index.md → recommendation → finding → evidence

---

#### Step 10: Create Process Documentation

**Time**: 1-2 hours

**What to do**:
- Create `findings/_process/methodology.md`
- Create `findings/_process/analysis-log.md`
- Create `findings/_process/workflows-used.md`
- Create `findings/_process/change-log.md` (initial entry documenting migration)

**Result**: Process documentation complete

**Test**: Review for completeness

---

### PHASE 4: VALIDATION & CLEANUP

---

#### Step 11: Validate Migration Differences

**Time**: 2-3 hours

**What to do**:
Create `migration-validation.md` that documents:

**What Changed**:
- Portfolio assessment: [List specific changes from old to new]
- Claims validation: [List differences]
- Network analysis: [List differences]
- Recommendations: [What's new, what's different]

**What Stayed the Same**:
- Core findings
- Evidence base
- Overall rating

**Structural Changes**:
- Folder organization
- File naming
- Navigation flow

**Result**: Clear documentation of migration impact

**Why critical**: You need to know if rewrite changed substance or just structure

**Test**: Review validation doc, confirm no critical findings lost

---

#### Step 12: Update Eleventy Config

**Time**: 1 hour

**What to do**:
- Update `sites/tam/.eleventy.js` to recognize new structure
- Ensure `/hyperion/` routes to `index.md`
- Test JSON file passthrough (`findings/_data/*.json`)
- Verify `migration-reference/` folder is included (for your reference)

**Result**: Site builds with new structure + reference folder

**Test**: `npm run build:tam` succeeds, review site locally

---

#### Step 13: Review & Decision Point

**Time**: 1-2 hours

**What to do**:
- Review new structure end-to-end
- Compare new findings to `migration-reference/` originals
- Verify no critical content lost
- Check navigation flow works
- Read `migration-validation.md`

**Decision**: Are you comfortable deleting old structure?

**If NO**: Keep both structures, iterate on new version
**If YES**: Proceed to Step 14

---

#### Step 14: Delete Old Structure (Optional)

**Time**: 5 minutes

**Only do this after you've validated the migration**

**What to do**:
```bash
# Delete old folders (migration-reference remains for your reference)
rm -rf outputs/
rm -rf research/deals/
rm -rf dataroom/

# Keep migration-reference folder indefinitely for comparison
```

**Result**: Clean new structure, reference folder preserved

**Test**: Verify site still builds, no broken links

---

#### Step 15: Deploy

**Time**: 30 minutes

**What to do**:
- Commit changes: `git add . && git commit -m "Reorganize hyperion to output-focused structure (objective-first migration)"`
- Push to GitHub: `git push -u origin claude/review-reorg-proposal-01WCf9Y8ssCGRbMptPbyybif`
- Monitor GitHub Actions build
- Verify deployment to Cloudflare Pages

**Result**: New structure live

**Test**: Visit site, verify everything works

---

### Migration Timeline Summary

| Phase | Steps | Description | Time |
|-------|-------|-------------|------|
| **1: Objective** | 1-4 | Create folders, migrate research (dataroom, companies, people) | 1 hour |
| **2: Structured Data** | 5 | Convert markdown to JSON for findings/_data/ | 3-4 hours |
| **3: Subjective** | 6-10 | Preserve old, create new findings/recommendations/process docs | 12-16 hours |
| **4: Validation** | 11-15 | Validate differences, update Eleventy, delete old (optional) | 5-7 hours |
| **TOTAL** | | | **21-28 hours** |

**Key Differences from Previous Approach**:
- ✅ Migrate objective content first (research, dataroom)
- ✅ Preserve old files in `migration-reference/` folder (never delete until validated)
- ✅ Create validation document to track differences
- ✅ Decision point before deleting old structure
- ✅ Keep `migration-reference/` indefinitely for comparison

**Recommended Pace**:
- **Week 1**: Phase 1-2 (4-5 hours) - Objective migration + JSON conversion
- **Week 2**: Phase 3 (12-16 hours) - Subjective content rewrite
- **Week 3**: Phase 4 (5-7 hours) - Validation + deployment

---

## Benefits Summary

### For Viewing Outputs

**Before**:
- Start in `users/tam/hyperion/outputs/` (3 levels deep)
- Read `claims-analysis.md`, `portfolio-assessment.md`, `network-analysis.md` separately
- Manually synthesize findings
- Hunt for recommendations scattered across files

**After**:
- Start at `users/tam/hyperion/index.md` (executive summary)
- See status, findings, and recommendations immediately
- Click through to details only if needed
- Clear navigation: summary → finding → evidence → sources

---

### For Iterative Analysis

**Before**:
- New data arrives (e.g., Crunchbase export)
- Unclear which files to update
- No tracking of what changed
- Risk of inconsistencies between files

**After**:
- New data arrives → logged in `_process/data-updates.md`
- Identify affected analyses (documented process)
- Update analyses → archive old versions
- Track changes in `_process/change-log.md`
- Structured data (JSON) easier to update programmatically

---

### For Stakeholder Communication

**Before**:
- Share 5+ markdown files
- Stakeholder reads linearly
- Must read everything to understand recommendations
- Follow-up questions: "What should I do with this?"

**After**:
- Share single link: `https://tam.pages.dev/hyperion/`
- Executive summary answers: Where are we? What did we learn? What should we do?
- Stakeholder can drill down into details only if interested
- Recommendations clearly prioritized (critical, high, medium)

---

### For Data Reuse

**Before**:
- Data mixed with narrative in markdown
- Hard to extract for comparisons (e.g., compare Hyperion to Craft Ventures)
- Can't generate charts or visualizations
- No programmatic access

**After**:
- Structured data in JSON files
- Easy to query: "Show all companies with >50x MOIC"
- Can generate charts (MOIC distribution, sector breakdown, co-investor overlap)
- Can compare funds programmatically
- Automated validation (check all companies have independent sources)

---

## Open Questions

1. **Terminology** ✅ **RESOLVED**: Using three-tier source hierarchy without glossary needed:
   - **Independent sources**: Third-party journalism, verified databases (objective)
   - **Target sources**: Externally acquired but target-controlled/influenced (GP's LinkedIn/Substack, company websites, press releases)
   - **Dataroom materials**: Private information provided by target (confidential documents)

2. **Iteration Workflow**: When new data arrives, should there be a checklist of "analyses to review"? Or is the change log sufficient?

3. **Archiving**: How many versions should we keep in `findings/_archive/`? (e.g., last 3 versions only?)

4. **JSON Schema Validation**: Should we create formal JSON schemas and validate in CI/CD?

5. **Benchmarking Data**: For fund comparisons, do you have access to similar funds' data in JSON format? (e.g., Craft Ventures, Basis Set)

6. **Eleventy Integration**: Should JSON files in `findings/_data/` auto-render as HTML tables? Or just provide download link?

7. **Process Documentation**: Should `findings/_process/methodology.md` include the old "tier" framework for reference? Or completely remove that terminology?

8. **Migration Reference Folder**: Should `migration-reference/` be published to the site or kept gitignored (for your eyes only)?

---

## Next Steps

### Recommended Immediate Actions

**If you approve this approach**:

1. **Review this proposal** - Does the output-focused structure make sense? Any changes needed?

2. **Start incremental migration** - Follow Step 1 (create folders) and Step 2 (executive summary)

3. **Test navigation** - Verify the executive summary → finding → evidence flow works

4. **Decide on JSON priority** - Which structured data file is most valuable? Start there

5. **Set timeline** - Commit to migration pace (e.g., 10 hours/week = 3 weeks)

---

**If you want to see a proof of concept first**:

1. I can implement Steps 1-6 (create structure, executive summary, one recommendation, one finding, one company)

2. You review the working prototype

3. We iterate on the approach

4. Then proceed with full migration

---

**Questions or feedback?** Let me know what adjustments you'd like to see.

---

**Version History**:
- **v3.0** (2025-11-17): Complete rewrite to output-focused structure, removed phase/tier terminology, added iterative analysis support
- **v2.0** (2025-11-16): Phase-based analytical workflow (deprecated)
- **v1.0** (2025-11-15): Initial proposal (deprecated)
