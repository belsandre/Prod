# Deal Prioritization Workflow

**Purpose:** Systematically analyze fund datarooms to identify and prioritize portfolio companies for research

**Output:** Tiered research list (`research/deals/research-list.md`) with comprehensive company profiles

**Applicable To:** Any fund's portfolio analysis (VC, PE, angel portfolios)

---

## Overview

This workflow transforms raw dataroom materials (pitch decks, case studies, portfolio spreadsheets) into a prioritized research list. The process identifies "winners" (companies the fund brags about), "up-and-comers" (featured but not yet winners), "red flags" (top positions not featured in materials), and remaining active portfolio, then organizes them into a 4-tier framework by strategic importance with comprehensive data capture.

---

## Prerequisites

### Required Materials
- **Narrative documents** (markdown, PDFs converted to markdown):
  - Fund pitch decks
  - Case studies (outperforming/recent investments)
  - GP bios
  - Letters to LPs
  - Sourcing differentiation docs
  - Founder references
- **Portfolio data** (Excel/CSV files):
  - Portfolio summary spreadsheets
  - Investment tracking sheets
  - Performance reports

### Tools & Usage
- **Document skills (xlsx):** Open portfolio spreadsheets, extract investment data, read multiple sheets (Holdings, Performance, Pipeline)
- **Task/Explore agents:** Large dataroom searches ("Find all case studies", "Identify companies valued at $1B+", "Find all founder testimonials")
- **Grep tool:** Targeted searches for specific companies/keywords (`grep "CompanyName" dataroom-md/`, `grep -i "valuation.*billion"`)
- **Read tool:** Full document reads, specific sections with offset/limit, cross-referencing between documents

---

## PHASE 1: Analyze Narrative Documents

### Step 1.1: Map the Dataroom

```bash
# List all markdown files
find dataroom-md/ -name "*.md"

# Identify key document types
# - Case Studies (Outperforming, Recent, etc.)
# - GP Bio
# - Fund deck
# - Sourcing/Network documents
# - Founder references
```

### Step 1.2: Identify "Winners"

**Definition:** Companies explicitly featured in case studies, highlighted as success stories, or repeatedly bragged about

**Where to Look:**
- Documents titled "Outperforming Investments" / "Success Stories" / "Track Record"
- Case study sections in fund decks
- Featured prominently in GP bios (top 3-5 investments)
- Mentioned in letters to LPs as formative investments

**For Each Winner, Extract:** Founder info, company website/description, how mentioned, investment thesis, sourcing story, value-add delivered, founder reference, key milestones, current status, why featured. Source all data points (e.g., "Source: Case Studies - Outperforming Investments.md, page 2").

### Step 1.3: Identify "Up-and-Comers"

**Definition:** Companies mentioned/featured but not in case studies - recent investments, pipeline opportunities, or portfolio positions showing momentum

**Where to Look:**
- "Recent Opportunities" / "Recent Investments" sections
- Sourcing differentiation documents (network maps)
- Portfolio lists in fund decks
- Pipeline/deployment opportunity sections
- Founder reference sections (companies mentioned but not case studied)

**For Each Up-and-Comer, Extract:**
- Same checklist as winners, but note they're "featured as recent opportunity" or "mentioned in sourcing docs"
- Pay attention to: fundraising status, expected next round, momentum indicators

### Step 1.4: Create Initial Company List

Organize findings:
- **Category 1: Winners** (companies with dedicated case studies)
- **Category 2: Up-and-Comers** (featured/mentioned but not case studied)
- **Category 3: Other Mentions** (brief mentions, network context, sourcing examples)

---

## PHASE 2: Analyze Excel Portfolio Data

### Step 2.1: Load Portfolio Spreadsheet(s)

```markdown
Use document-skills:xlsx to open portfolio files
Look for sheets named: Portfolio Summary, Investments, Performance, Holdings
```

### Step 2.2: Identify Fund Drivers by Performance

**Key Metrics to Extract:**
- MOIC (Multiple on Invested Capital)
- IRR (Internal Rate of Return)
- Entry valuation
- Current/latest valuation
- Capital invested
- Current value

**Prioritization Criteria:**
- Top 10 by MOIC
- Top 10 by absolute value created
- Unicorns ($1B+ valuation)
- Companies with >3x MOIC
- Largest capital deployments

**Flag:** Any top performers NOT mentioned in narrative documents (these are fund drivers absent from fundraising materials)

### Step 2.3: Extract Comprehensive Investment Details

**For Each Company in Excel, Capture:**
- **Entry:** Date, valuation, check size, round, co-investors
- **Current:** Latest valuation/date, follow-on checks, last round details, total raised
- **Performance:** MOIC, IRR, mark type
- **Notes:** Excel status updates, distinguish projections vs. actuals, note multiple tranches

**Important:** Distinguish facts from projections (see Quality Standards section for examples)

### Step 2.4: Cross-Reference with Phase 1

**For companies in BOTH narrative docs AND Excel:**
- Merge data into single comprehensive profile
- Reconcile any discrepancies (often Excel has older data than pitch decks)
- Note valuation updates: "Excel shows $2.6B (Dec-24), pitch deck shows $39.5B (April 2025)"

**For companies ONLY in Excel (not in narrative docs):**
- Add to research list if they meet fund driver criteria
- Flag as "Fund driver not featured in fundraising materials"
- Include note: "Not mentioned in pitch deck/case studies despite X.Xx MOIC"

---

## PHASE 3: Prioritization Framework

**Tiers Are Naturally Mutually Exclusive**

Each company belongs to exactly ONE tier. The tiers are non-overlapping by definition:

- **Tier 1 & 2:** Companies the GP IS showcasing in fundraising materials (case studies, testimonials, sourcing maps, recent opportunities, GP bio, pitch deck)
- **Tier 3:** Companies with significant capital deployed that are conspicuously ABSENT from all fundraising materials
- **Tier 4:** Everything else (performing adequately but not meeting Tier 1-3 criteria)

A company cannot simultaneously be "featured in materials" and "conspicuously absent" - therefore no overlap is possible.

**The Tier 3 Question:** Where did the GP put their biggest checks but somehow aren't talking about it in fundraising materials? This capital allocation vs. narrative misalignment is the critical red flag.

---

### Tier 1: PRIORITY RESEARCH (Top Fund Drivers)

**Inclusion Criteria (must meet 2+ of these):**
- [ ] Featured in case study as winner
- [ ] Top 5 by MOIC
- [ ] Top 5 by absolute value created
- [ ] Unicorn valuation ($1B+)
- [ ] Mentioned 3+ times across different documents
- [ ] First/formative investment for the fund
- [ ] Strong founder testimonial provided
- [ ] Significant capital deployed (top 5 positions)
- [ ] Network hub (source of multiple referrals)

**By definition:** All Tier 1 companies must be mentioned in narrative materials (case studies, testimonials, sourcing docs, GP bio, or pitch deck).

**Target Size:** <6 companies

**Profile Depth:** Full comprehensive profiles with all data points

---

### Tier 2: UP-AND-COMERS (Watch List)

**Inclusion Criteria (must meet 1+ of these):**
- [ ] Featured in "Recent Opportunities" or similar section
- [ ] MOIC >3x or IRR >50%
- [ ] Upcoming catalysts (Series A/B imminent, product launch, etc.)
- [ ] Strong momentum indicators (customer traction, fundraising interest)
- [ ] Mentioned in multiple contexts (sourcing + references, etc.)
- [ ] Recent investment (<12 months) with early positive signals

**By definition:** All Tier 2 companies must be mentioned in narrative materials. Companies not meeting Tier 1's higher bar (2+ criteria) but still showcased positively.

**Target Size:** <10 companies

**Profile Depth:** Comprehensive but slightly lighter than Tier 1

---

### Tier 3: TOP POSITIONS NOT FEATURED (Red Flags)

**Inclusion Criteria (ALL must be true):**
- [ ] **Significant capital deployed:** Top 10 positions by dollars invested
- [ ] **AND:** Not mentioned in ANY narrative documents (case studies, pitch deck, GP bio, sourcing docs, founder references)

**Supporting Evidence (strengthens red flag):**
- High MOIC (>3x) or strong absolute value created despite absence
- Multiple rounds/follow-ons (shows continued capital commitment)

**Why This Matters:**

The core question: **Where did the GP put their biggest checks but aren't talking about it?**

This capital allocation vs. narrative misalignment may signal:
- Weak founder relationship (no testimonial, no value-add story)
- Underperforming expectations (good entry, but momentum lost)
- Strategic narrative choice (doesn't fit fund thesis)
- Recent performance issues (was good, now problematic)
- Low GP engagement (hands-off investment)

**By definition:** Tier 3 companies cannot appear in Tier 1 or 2 because they are not mentioned in narrative materials.

**Target Size:** 2-5 companies

**Profile Depth:** Brief summaries with emphasis on:
- Financial metrics (MOIC, IRR, entry/current valuation, total capital deployed)
- Excel status notes (critical for understanding circumstances)
- Why not featured (red flag analysis: which documents checked, what's missing)
- Brief company description
- Investment thesis gap (if inferable from absence)

---

### Tier 4: REMAINING ACTIVE PORTFOLIO (Brief Summary)

**Inclusion Criteria:**
- All other companies in portfolio
- Companies performing adequately but not meeting Tier 1-3 criteria
- Smaller positions or earlier-stage with insufficient data
- Mentioned occasionally but not prominently featured

**Presentation:**
- Organize by category (Quantum, Robotics, Energy, Cyber, etc.)
- 1-2 sentences per company OR aggregated summary
- List key metrics only (valuation, MOIC if strong)
- No failed investments (exclude write-offs/shutdowns)
- Emphasize active status (still in portfolio, monitoring)

**Target Size:** Brief summary covering remaining active companies

---

## PHASE 5: Compile Research List

### Document Structure

**Required Sections:**
1. Header (fund name, source attribution, analysis date)
2. Tier 1 (Priority Research) - Full profiles
3. Tier 2 (Up-and-Comers) - Comprehensive profiles
4. Tier 3 (Red Flags) - Brief profiles with performance analysis
5. Tier 4 (Remaining Portfolio) - Category summaries
6. Portfolio Performance Summary
7. Research Prioritization Guide

### Company Profile Elements

**For Tier 1 & 2 (Comprehensive):**
- Founder(s), website
- Latest valuation (date, round, source) + Excel valuation if different
- Investment details: entry date, valuation, check size, MOIC, IRR (sourced from Excel)
- Description (sourced from narrative docs)
- Why priority/watch (criteria met, with sources)
- How mentioned (specific documents)
- Value-add delivered (if available)
- Founder reference (if available)
- Key milestones (if available)
- Excel notes/updates
- Research focus
- Key investors

**For Tier 3 (Red Flag Analysis):**
- Financial performance: entry date/valuation, invested, MOIC, IRR, current valuation (sourced from Excel)
- Excel status/notes (exact quotes)
- Brief description (if available)
- Red flag analysis: why absent despite performance (list documents checked: pitch deck, case studies, GP bio, references)
- Circumstances: fundraising status, business momentum, relationship indicators
- Research priority level

**For Tier 4 (Brief Summaries):**
- Organize by category (Quantum, Robotics, Energy, Cyber, etc.)
- 1-2 sentences per company OR category aggregation
- Key metrics only (MOIC if >3x, notable valuations)

---

## Quality Standards & Validation

### Source Attribution

**Every data point must cite its source.** For complete source documentation standards, see `users/tam/workflows/templates/source-documentation.md`.

✅ **Good:** "Entry valuation: $420M post-money (Source: Excel, entry date April 2023)"
❌ **Bad:** "Valuation: $5B" (no source, no date)

### Facts vs. Projections

**Always distinguish:**
- ✅ "Current valuation: $258M (Source: Excel, Series A actual, Aug 2025)"
- ✅ "Projected valuation: $40M (Source: Excel Dec-24 projections)"
- ❌ Don't present projections as current facts

### No Inference Rule

**ONLY use what's explicitly stated in source documents.** State limitations for missing data: "Description: (not provided in documents)"

### Flag Fund Drivers Not Featured

> **⚠️ Example:** Pierisca shows 4.0x MOIC (3rd best performer) but is not mentioned in any fundraising documents or case studies.

**Why:** Indicates potential relationship issues, recent additions, or strategic narrative choices

### Exclude Failed Investments

**Do NOT include:** Write-offs, shut down companies, fire-sale exits
**Exception:** Can mention in summary: "4 write-offs totaling $110K (excluded from research list)"

### Omit Individual Investor Allocations

**Omit:** Roger/Kurt/Rich breakdowns unless strategically relevant
**Focus on:** Total capital deployed, fund-level ownership, follow-on decisions

### Pre-Submission Checklist

For complete quality checklist, see `users/tam/workflows/templates/quality-checklist.md`. Workflow-specific items to verify:

- [ ] **No company appears in multiple tiers**
- [ ] **All Tier 1/2 companies are mentioned in narrative materials**
- [ ] **All Tier 3 companies are NOT mentioned anywhere despite significant capital**
- [ ] Every Tier 1/2 company has comprehensive data
- [ ] All metrics have source attribution
- [ ] Facts distinguished from projections
- [ ] No inferred information
- [ ] Failed investments excluded
- [ ] Valuation discrepancies noted and explained
- [ ] "Why Priority" / "Why Watch" sections completed

### Validation Questions

**Completeness:** Captured all case study companies? Cross-referenced Excel vs. narrative docs? Top capital deployments identified?

**Accuracy:** Valuations match between sources? Dates accurate? Projections vs. actuals distinguished?

**Prioritization:** Tier 1 truly drives fund narrative? Companies mentioned 3+ times captured?

**Tier 3 Red Flags:** Identified companies with significant capital deployed (top 10 positions by $) but conspicuously missing from all fundraising materials? Checked all documents (case studies, GP bio, pitch deck, sourcing docs, founder references)?

**Mutual Exclusivity:** No company appears in multiple tiers? All Tier 1/2 companies mentioned somewhere? All Tier 3 companies absent everywhere?

### Success Criteria

**Workflow complete when:** <16 priority companies (Tiers 1-2) with full profiles; Tier 3 red flags identified; all data sourced; facts vs. projections distinguished; no inference; failed investments excluded; research priorities clear and actionable.

**Output enables:** Immediate action (top 3-5 companies to deep dive), informed conversations, pattern recognition (fund thesis/value-add), due diligence baseline, and portfolio benchmarking.

---

## Adaptations for Different Fund Types

**Early-Stage VC:** Emphasize sourcing stories, founder relationships, conviction signals (follow-ons, advisory roles), network effects/referral patterns, and Series A/B milestones.

**Growth/Late-Stage:** Focus on commercial traction, revenue metrics, entry multiples, post-investment value creation, exit potential, strategic positioning, and operational value-add.

**Angel/Rolling:** Track personal vs. syndicate capital, founder relationship depth, high-conviction concentrated bets, and asymmetric return potential.

**Multi-Stage:** Segment by stage (early vs. growth), track graduation success (seed → Series A → B), note reserve deployment/ownership management, and highlight platform/portfolio synergies.

---

## Output Location & Naming

### Standard Path
```
[user]/[fund-name]/research/deals/research-list.md
```

### Alternative Paths (if applicable)
```
[user]/[fund-name]/outputs/deal-prioritization-[date].md
shared/research/[fund-name]-deal-research.md
```

---

## Version Control & Updates

**When to Re-Run This Workflow:**
- New dataroom materials received
- Portfolio performance updated (quarterly/annually)
- Significant valuation changes (new funding rounds)
- Exit events (acquisitions, IPOs)
- Adding new companies to research scope

**Versioning Recommendation:**
- Include analysis date in document header
- Note when source materials are from (Excel date, pitch deck date)
- Archive previous versions before major updates
- Track material changes (new Tier 1 company, removed company, etc.)

---

## Related Workflows

- **Company Deep Dive Workflow** (next step after prioritization)
- **Competitive Analysis Workflow** (for researching specific companies)
- **Fund Thesis Extraction Workflow** (synthesizing investment strategy)
- **Value-Add Assessment Workflow** (analyzing GP value creation)

---

**Workflow Version:** 1.0
**Last Updated:** November 2025
**Maintained By:** Shared Workflows
**Feedback:** Refine based on usage across different fund analyses
