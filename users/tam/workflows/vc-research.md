# VC Portfolio Research Workflow

**Purpose**: Deep research on VC portfolio companies and general partners (GPs) to assess portfolio quality, track record, investment thesis, and GP-company relationships.

**Output**: Comprehensive research on priority companies, GP profiles, relationship evidence, and portfolio quality assessment.

**Timeline**: 8-12 hours total (down from 15-20 hours via parallelization and smart streamlining)

**Version**: 2.0 (Streamlined) | **Maintainer**: Tam | **Last Updated**: 2025-01-11

---

## Overview

This workflow takes the output from `deal-prioritization.md` (`research/priority-deals.md`) and conducts deep research on:
1. **General Partners** (GPs) - Dynamically identified from dataroom, researched for background and track record
2. **Portfolio Companies** (Tier 1 & 2) - Business fundamentals, performance, competitive positioning
3. **GP-Company Relationships** - Evidence of GP involvement and value-add
4. **Portfolio Quality** - Overall track record, investment thesis, patterns

**Key Features**:
- ✅ **Resumability**: Track progress across sessions, pause and continue anytime
- ✅ **Parallel Execution**: GP and company research happen concurrently
- ✅ **Dynamic GP Extraction**: No hardcoded names, works with any dataroom
- ✅ **Smart Quality Thresholds**: Quality over quantity, prevents over-research

---

## When to Use This Workflow

- After completing `deal-prioritization.md` and generating `research/priority-deals.md`
- When evaluating a VC's portfolio quality and track record
- When assessing GP capabilities and relationship strength with portfolio companies
- When building portfolio-level insights for investment decisions

---

## Prerequisites

### Required Materials
- ✅ `research/priority-deals.md` (output from deal-prioritization workflow)
- ✅ Dataroom with GP information (e.g., `GP Bio.md`, `Fund I.md`, or case studies)

### Skills Used
- `company-research` - For deep research on both GPs and companies
- WebSearch - For GP mentions and relationship evidence
- WebFetch - For extracting full article content

### Expected Timeline
- **Phase 0**: Setup & Planning (~15 minutes)
- **Phase 1**: Parallel Research (~6-8 hours)
  - GP Research: ~30-45 min per GP (concurrent)
  - Company Research: ~30-50 min per company (can batch)
- **Phase 2**: Analysis & Synthesis (~2-3 hours)
- **Total**: 8-12 hours (can be split across multiple sessions)

---

## Output Structure

```
research/
├── research-progress.md           # Progress tracker (resumability)
├── gp-list.md                     # Dynamically extracted GP names
├── company-clusters.md            # Company groupings by sector
├── priority-deals.md              # Input (from deal-prioritization)
├── people/
│   ├── {gp-name-1}/
│   │   ├── research-summary.md
│   │   └── sources/
│   │       ├── linkedin.md
│   │       └── ...
│   └── {gp-name-2}/
│       └── ...
├── deals/
│   ├── tier-1/
│   │   ├── {company-name}/
│   │   │   ├── research-summary.md    # Includes GP mentions section
│   │   │   └── sources/
│   │   │       ├── website.md
│   │   │       └── ...
│   │   └── ...
│   └── tier-2/
│       └── ...
├── analysis/
│   ├── gp-relationships.md           # Matrix of GP-company relationships
│   └── portfolio-assessment.md       # Portfolio quality & track record
└── outputs/
    └── executive-summary.md          # Final deliverable
```

---

## Phase 0: Initialize, Extract GPs & Plan

**Duration**: ~15 minutes
**Purpose**: Set up tracking, identify GPs dynamically, cluster companies for efficient research.

### Step 0.1: Create or Resume Progress Tracker

**Action**: Check if `research/research-progress.md` exists

**If NOT EXISTS**: Create the file with this template:

```markdown
# VC Research Progress Tracker

**Fund/VC**: [Extract from priority-deals.md]
**Started**: [Date]
**Last Updated**: [Date]
**Status**: In Progress

---

## Phase 1A: GP Research

**GPs Identified**: [Will populate in Step 0.2]

- [ ] [GP Name 1]
- [ ] [GP Name 2]

**Progress**: 0/[total] complete

---

## Phase 1B: Company Research

### Tier 1 Companies
[Will populate in Step 0.3]

**Progress**: 0/[total] complete

### Tier 2 Companies
[Will populate in Step 0.3]

**Progress**: 0/[total] complete

---

## Phase 2: Analysis & Synthesis

- [ ] GP-Company Relationships Matrix
- [ ] Portfolio Quality Assessment
- [ ] Executive Summary

---

## Notes & Issues
[Document blockers, items needing follow-up]
```

**If EXISTS**: Read the file to identify completed work and resume from checkpoint.

---

### Step 0.2: Extract GP Names Dynamically

**Purpose**: Automatically identify GPs from dataroom (no hardcoding!)

**Action**: Search for GP names in dataroom files (priority order):

#### Source 1: GP Bio.md (Most Reliable)
**Search patterns**:
- "General Partner" or "Managing Partner" + proper nouns within 2 sentences
- Names followed by biographical info ("B.S. in", "MBA from", "Previously")
- Section headers with names ("Dillon Dunteman", "Professional Experience")

**Example extraction logic**:
```
1. Read dataroom/GP Bio.md
2. Look for patterns:
   - "[Name], General Partner"
   - Professional experience sections with person names
   - Educational backgrounds (usually follows name introduction)
3. Extract all unique proper nouns matching GP context
```

#### Source 2: Fund Deck or Fund I.md
**Search for**:
- "Team" or "Investment Team" section
- Partner bios with titles
- "Led by [Name]" or "Founders: [Name]"

#### Source 3: Case Studies
**Search for**:
- Quoted individuals (e.g., "Dillon Dunteman says...")
- "Partner [Name]" mentions

**Action**: Create `research/gp-list.md`:

```markdown
# GP Research List

**Extraction Date**: [Date]
**Sources Used**: GP Bio.md, Fund I.md, Case Studies

---

## Identified GPs

1. **[GP Name 1]**
   - Source: GP Bio.md (line 52, 60)
   - Title: General Partner
   - Context: [Brief snippet from bio]

2. **[GP Name 2]**
   - Source: Fund I.md (page 3)
   - Title: Managing Partner
   - Context: [Brief snippet]

[Continue for all GPs found...]

---

## Research Status

- [ ] [GP Name 1]
- [ ] [GP Name 2]

---

## Extraction Notes

[Document any ambiguities or assumptions made during extraction]
```

**⚠️ FALLBACK**: If automatic extraction fails or uncertain:
```
Unable to automatically identify GPs from dataroom.

Please provide GP names manually:
1. Check GP Bio.md, Fund I.md, or pitch deck
2. Add names to research/gp-list.md
3. Continue with Phase 1A
```

**Action**: Update `research-progress.md` Phase 1A section with GP names extracted.

---

### Step 0.3: Load and Parse Priority Deals

**Action**: Read `research/priority-deals.md` and extract:

1. **Tier 1 Companies**: Company names from "Tier 1 (Priority Research)" section
2. **Tier 2 Companies**: Company names from "Tier 2 (Up-and-Comers)" section

**Action**: Update `research-progress.md` with checkbox lists for all companies.

---

### Step 0.4: Cluster Companies by Sector

**Purpose**: Enable research reuse across similar companies (20% analysis time savings)

**Action**: Group companies by sector/industry and create `research/company-clusters.md`:

```markdown
# Company Clusters

**Purpose**: Group companies by sector to reuse market analysis and enable competitive comparisons

---

## Quantum Computing
- Company A (Tier 1)
- Company B (Tier 2)

## Robotics & Automation
- Company C (Tier 1)
- Company D (Tier 2)
- Company E (Tier 2)

## Energy & Cleantech
- Company F (Tier 1)
- Company G (Tier 2)

## [Other Sectors...]

---

## Research Strategy

**For clustered companies**:
1. Research first company in cluster deeply (market analysis, competitive landscape)
2. For subsequent companies in same cluster:
   - Reference first company's market analysis
   - Focus on competitive positioning differences
   - Update market trends only if significantly different
3. Minimum sources still required per company (quality threshold)
```

**Benefit**: Reduces redundant market research, saves ~10 min per company.

---

### Step 0.5: Check Existing Work (Resumability)

**Action**: Scan file system to identify completed research:

**Check**:
- `research/people/` - Which GPs have folders? Mark as complete
- `research/deals/tier-1/` - Which companies researched? Mark as complete
- `research/deals/tier-2/` - Which companies researched? Mark as complete
- `research/analysis/` - Which analysis docs exist?

**Action**: Update `research-progress.md` to reflect actual completion status (file system is source of truth).

---

### Step 0.6: Display Progress Summary

**Action**: Show current status:

```
VC RESEARCH PROGRESS SUMMARY
============================
GPs Identified: [X] GPs
  ⬜ [GP Name 1]
  ⬜ [GP Name 2]

Company Clusters: [Y] sectors identified
  - Quantum Computing (2 companies)
  - Robotics (3 companies)
  - Energy (2 companies)

Tier 1 Companies: 0/[X] complete
Tier 2 Companies: 0/[Y] complete

Research Mode: PARALLEL (GP + Company research concurrent)
Estimated Time: 8-12 hours

Ready to begin Phase 1 (Parallel Research)
```

---

## Phase 1: Parallel Research (GP + Companies)

**Duration**: 6-8 hours
**Purpose**: Research GPs and companies concurrently, then cross-reference for relationships.

**⚠️ KEY INSIGHT**: GP research and company research are independent. You can:
- Work on GPs and companies in parallel
- Complete all companies before GPs (or vice versa)
- Batch companies (research 3, break, research 3 more)
- GP mentions are searched AFTER both tracks complete (Phase 1C)

---

## Phase 1A: GP Research (Parallel Track)

**Duration**: ~30-45 minutes per GP
**Checkpoint**: Before starting each GP, check if `research/people/{gp-name}/` exists. If yes, skip.

### For Each GP in gp-list.md:

#### Step 1A.1: Invoke Company-Research Skill

**Prompt**:
```
Use the company-research skill to research [GP NAME] as a person/investor. Focus on:

1. **Professional Background**
   - Career history (pre-VC and VC roles)
   - Educational credentials
   - Areas of expertise (technical, domain, functional)
   - Notable achievements

2. **Investment Experience**
   - Years in venture capital
   - Previous firms, funds, roles
   - Notable investments (public successes and lessons learned)
   - Investment focus (sectors, stages, geographies)
   - Portfolio company involvement patterns

3. **Public Profile & Thought Leadership**
   - Social media presence (Twitter/X, LinkedIn activity)
   - Speaking engagements, podcasts, interviews
   - Published content (articles, blog posts)
   - Board positions and advisory roles
   - Industry recognition, awards, rankings

4. **Reputation & Network**
   - What founders say (testimonials, references)
   - Co-investor relationships
   - Industry reputation and credibility
   - Media mentions and visibility

5. **Investment Philosophy & Approach**
   - Stated investment criteria and thesis
   - Decision-making style and process
   - Value-add methodology
   - Differentiation as an investor

Save to: research/people/{gp-name}/

Create sources/ subfolder with each significant source as separate markdown file using the company-research skill's source template format:
- **URL**: [Full URL]
- **Date**: [Publication/Last Updated Date in YYYY-MM-DD format]
- **Source Type**: [LinkedIn Profile / News Article / Interview / etc.]
- **Objectivity Level**: [High / Medium / Low]
- **Reliability Assessment**: [Brief assessment]
- **Key Information**: [Bullet points]
- **Critical Assessment**: [Strengths, limitations, biases, verification status]
- **Raw Content**: [Full extracted content]
```

**Expected Output**:
- `research/people/{gp-name}/research-summary.md`
- `research/people/{gp-name}/sources/*.md`

#### Step 1A.2: Batch Update Progress

**Action**: After completing **all GPs** (not after each), update `research-progress.md`:
- Mark all completed GPs with checkboxes: `[x] [GP Name] (completed: YYYY-MM-DD)`
- Update progress counter
- Update "Last Updated" timestamp

**Why batch?**: Reduces interruptions, maintains flow. File system is source of truth for individual GP status.

---

## Phase 1B: Company Research (Parallel Track)

**Duration**: Tier 1: ~45-60 min per company | Tier 2: ~30-40 min per company
**Order**: Process Tier 1 first, then Tier 2 (but can batch within each tier)

**Checkpoint**: Before each company, check if `research/deals/tier-[1|2]/{company-name}/` exists. If yes, skip.

### For Each Company (Tier 1 then Tier 2):

#### Step 1B.1: Extract Company Details

**Action**: From `research/priority-deals.md`, extract:
- Company name, website URL
- Founder name(s)
- Latest valuation & funding round
- Investment details (entry date, check size, MOIC if available)
- Company description
- Why priority (criteria met)

#### Step 1B.2: Check Company Cluster

**Action**: Refer to `research/company-clusters.md`:
- Is this the first company in its sector cluster?
  - **If YES**: Do full market analysis
  - **If NO**: Reference prior company's market analysis, focus on competitive differentiation

#### Step 1B.3: Invoke Company-Research Skill

**Prompt**:
```
Use the company-research skill to research [COMPANY NAME]. This is a [Tier 1/Tier 2] portfolio company.

[IF FIRST IN CLUSTER: Include comprehensive market analysis]
[IF NOT FIRST: Reference {previous company in cluster} market analysis, focus on competitive positioning]

Focus on:

1. **Company Overview**
   - Business model and value proposition
   - Product/service description
   - Target customers and market
   - Revenue model and go-to-market
   - Company stage and maturity

2. **Traction & Performance Indicators**
   - Growth metrics (revenue, users, ARR, etc.)
   - Market position and share
   - Recent milestones and achievements
   - Financial performance signals (if public)
   - Customer traction and retention

3. **Founder & Team Assessment**
   - Founder background, expertise, track record
   - Team composition and key hires
   - Organizational maturity
   - Leadership strengths/weaknesses

4. **Market & Competitive Landscape**
   [IF FIRST IN CLUSTER]
   - Market size and growth (TAM/SAM/SOM)
   - Market dynamics and trends
   - Competitive landscape overview

   [IF NOT FIRST]
   - Competitive positioning vs [previous companies in cluster]
   - Differentiation and unique positioning
   - Market share and competitive advantages

5. **Funding & Investors**
   - Complete funding history
   - All investors (lead and syndicate)
   - Current valuation and terms (if available)
   - Board composition
   - Notable co-investors

6. **Risks & Red Flags**
   - Execution risks
   - Competitive threats
   - Market risks
   - Team or product concerns
   - Any negative signals

**IMPORTANT**: Save research to research/deals/tier-[1 or 2]/{company-name}/

Create research-summary.md with a section for "Investor Relationship & GP Involvement" (will populate in Phase 1C).

Include template:
## Investor Relationship & GP Involvement

**Lead Investor**: [If known]
**Board Members**: [If known]

**GP Mentions**: [To be researched in Phase 1C]

Create sources/ subfolder with each source as separate markdown file using the company-research skill's source template format:
- **URL**: [Full URL]
- **Date**: [Publication/Last Updated Date in YYYY-MM-DD format]
- **Source Type**: [Company Website / News Article / Press Release / etc.]
- **Objectivity Level**: [High / Medium / Low]
- **Reliability Assessment**: [Brief assessment]
- **Key Information**: [Bullet points including funding details, customer info]
- **Critical Assessment**: [Strengths, limitations, biases, verification status, inconsistencies]
- **Raw Content**: [Full extracted content]
```

**Quality Thresholds** (Smart, not arbitrary):

**Tier 1 Minimum**:
- ✅ 1 comprehensive company website source
- ✅ 1 funding announcement or press release
- ✅ 1 third-party article (TechCrunch, Bloomberg, etc.)
- ✅ 2+ additional high-quality sources
- **OR** 5+ sources if company has rich public information

**Tier 2 Minimum**:
- ✅ 1 company website source
- ✅ 1 funding announcement or press release
- ✅ 1 third-party source
- **OR** 3+ sources if readily available

**Quality > Quantity**: Better 3 excellent sources than 6 mediocre ones. Focus on:
- Primary sources (company, official announcements)
- Recent information (within 12-18 months)
- Substantive content (not just mentions)
- Credible outlets

**Expected Output**:
- `research/deals/tier-[1|2]/{company-name}/research-summary.md`
- `research/deals/tier-[1|2]/{company-name}/sources/*.md`

#### Step 1B.4: Batch Progress Updates

**Action**: Update `research-progress.md` after completing **batches** (not every company):
- After every 3-4 companies
- After completing all Tier 1
- After completing all Tier 2
- Before ending any session

**Format**:
- Mark completed companies: `[x] Company Name (completed: YYYY-MM-DD)`
- Update progress counters

**Why batch?**: Reduces context switching, maintains momentum. File system shows real-time status anyway.

#### Step 1B.5: Quality Check (Every 3 Companies)

**Action**: After every 3 companies, pause 5 minutes to review:
- Do research-summary.md files have substantive content?
- Are source files properly formatted and saved?
- Did we meet quality thresholds?
- Any issues to document in progress tracker?

---

## Phase 1C: GP-Company Cross-Reference (After 1A + 1B Complete)

**Duration**: ~15-20 minutes per company
**Purpose**: Now that GP and company research is complete, search for GP mentions in relation to each company.

**⚠️ Prerequisites**:
- Phase 1A complete (all GPs researched)
- Phase 1B complete (all companies researched)

### For Each Company (Tier 1 and Tier 2):

#### Step 1C.1: Consolidated GP Mention Search

**Strategy**: Single efficient search instead of 6 separate searches (saves ~15 min per company).

**Search Query** (adapt GP names from gp-list.md):
```
"[COMPANY NAME]" ("[GP1 NAME]" OR "[GP2 NAME]" OR "[GP3 NAME]") (funding OR investment OR quote OR announcement OR partner)
```

**Example**:
```
"Acme Robotics" ("Dillon Dunteman" OR "Harry Bellew") (funding OR quote OR announcement)
```

**If no results**: Escalate to targeted searches:
```
site:techcrunch.com "[COMPANY NAME]" [FUND NAME]
site:linkedin.com/pulse "[COMPANY NAME]" "[GP NAME]"
site:bloomberg.com "[COMPANY NAME]" funding "[GP NAME]"
```

#### Step 1C.2: Analyze and Categorize Mentions

**For each mention found**:

**Signal Strength Categories**:
- **Strong**: GP quoted in article about company, GP on company board, GP featured in company press release, GP wrote public analysis of company
- **Medium**: GP mentioned in investor list, GP retweeted/shared company content, GP attended company event
- **Weak**: Generic mention, no specific interaction, passing reference

**Action**: Extract key information:
- Article title and URL
- Publication date
- Exact quote or mention (copy verbatim)
- Context (funding announcement, interview, thought leadership, etc.)
- Signal strength assessment

#### Step 1C.3: Update Company Research Summary

**Action**: Open `research/deals/tier-[1|2]/{company-name}/research-summary.md`

**Locate section**: "## Investor Relationship & GP Involvement"

**Update with**:
```markdown
## Investor Relationship & GP Involvement

**Lead Investor**: [Name from funding history]
**Board Members**: [If known]

### GP Relationship Evidence

**Overall Relationship Strength**: Strong / Medium / Weak / None Found

---

#### [GP Name 1]

**Mentions Found**: [X] ([Signal Strength])

**Key Evidence**:
- **Source**: [Article Title](URL) | Date: [YYYY-MM-DD]
- **Context**: [Funding announcement / Interview / Thought leadership / etc.]
- **Quote/Mention**:
  > [Exact verbatim text with GP name and company reference]
- **Signal Strength**: Strong / Medium / Weak
- **Analysis**: [What this reveals about GP involvement and value-add]

[Repeat for additional mentions]

**Summary**: [Brief assessment of GP1's relationship with company]

---

#### [GP Name 2]

[Same structure as above]

---

### Relationship Insights

[Comparative analysis: Which GPs more involved? Value-add demonstrated? Public vs private relationship?]
```

**If No Mentions Found**:
```markdown
### GP Relationship Evidence

**Mentions Found**: 0 mentions across comprehensive search

**Search Strategy Used**:
- Primary query: "[COMPANY]" ("[GP1]" OR "[GP2]") (funding OR quote)
- Escalation searches: TechCrunch, LinkedIn, Bloomberg
- Date range: [Specify]

**Analysis**: Absence of public GP mentions suggests:
- Limited public involvement (not unusual for early-stage)
- OR relationship is more private/behind-the-scenes
- OR company operates with limited PR/media presence

**Relationship Strength**: Unable to assess from public sources
```

#### Step 1C.4: Save High-Quality GP Mention Sources

**Action**: For strong signal mentions, save source as separate file:

**Location**: `research/deals/tier-[1|2]/{company-name}/sources/gp-mention-[descriptor].md`

**Format**:
```markdown
# GP Mention: [Brief Descriptor]

**Source**: [Article Title]
**URL**: [Full URL]
**Date**: [Publication Date]
**GP Featured**: [GP Name]
**Signal Strength**: Strong / Medium / Weak

---

## Full Context

[Full article text or relevant excerpt - use WebFetch if high value]

---

## Key Excerpt

> [Exact text with GP mention and company reference, with enough surrounding context]

---

## Analysis

**What This Reveals**:
- GP involvement level
- Type of value-add demonstrated
- Nature of relationship (board, advisor, hands-on, etc.)

**Relevance**: [Why this matters for portfolio assessment]
```

#### Step 1C.5: Batch Update Progress

**Action**: After completing GP mentions for all companies (or major batch), update `research-progress.md`:
- Add note: "Phase 1C complete: GP-company cross-references completed (Date)"

---

## Phase 2: Analysis & Synthesis

**Duration**: 2-3 hours
**Purpose**: Synthesize all research into portfolio-level insights and actionable deliverables.

---

### Step 2.1: Create GP-Company Relationships Matrix

**Action**: Create `research/analysis/gp-relationships.md`

**Prompt**:
```
Review all company research-summary.md files (Tier 1 and Tier 2) and compile GP relationship evidence into a comprehensive matrix.

Analyze the "Investor Relationship & GP Involvement" sections from all companies.

Create the following analysis:

# GP-Company Relationships Analysis

**Analysis Date**: [Date]
**Companies Analyzed**: [X Tier 1, Y Tier 2]
**GPs Evaluated**: [List from gp-list.md]

---

## Executive Summary

[3-4 sentences: Overall pattern of GP involvement across portfolio, key insights, notable findings]

---

## GP Involvement Overview

**Total Companies with GP Mentions**: [X out of Y companies]

By GP:
- **[GP1 Name]**: [X] companies, [Y] strong signals, [Z] medium signals
- **[GP2 Name]**: [X] companies, [Y] strong signals, [Z] medium signals
- [Continue for all GPs]

**Companies with Multiple GP Mentions**: [List companies where 2+ GPs mentioned]
**Companies with No GP Mentions**: [List and note patterns]

---

## Relationship Strength Matrix

| Company | Tier | [GP1] | [GP2] | [GP3] | Strongest Evidence |
|---------|------|-------|-------|-------|-------------------|
| Company A | 1  | Strong | Weak  | -     | [GP1] quoted in Series B announcement |
| Company B | 1  | -      | Strong| -     | [GP2] featured in company case study |
| Company C | 1  | Medium | Medium| -     | Both mentioned in investor list |
| Company D | 2  | Weak   | -     | -     | Generic mention only |
| [...]     |    |        |       |       |                   |

**Legend**:
- **Strong**: Quoted, featured, board role, deep public involvement
- **Medium**: Mentioned in materials, social engagement, event attendance
- **Weak**: Generic mentions, passing references
- **-**: No mentions found

---

## Value-Add Patterns

Based on relationship evidence, what value-add do GPs demonstrate?

### [GP1 Name]
**Value-Add Style**: [Technical advisor / Strategic partner / Network connector / Board governance / etc.]

**Evidence**:
- [Example 1: Company X - GP quoted on technical strategy]
- [Example 2: Company Y - GP made introduction to customer]
- [Pattern across portfolio...]

**Sectors of Focus**: [Which sectors show stronger GP involvement?]

### [GP2 Name]
[Same structure]

---

## Involvement Patterns by Sector

Are GPs more publicly involved in certain sectors?

**High Involvement Sectors**:
- [Sector 1]: [X] strong mentions across [Y] companies
- [Reasoning: Why might this be?]

**Low Involvement Sectors**:
- [Sector 2]: Limited mentions despite [X] companies
- [Potential reasons...]

---

## Involvement Patterns by Stage

- **Seed/Early Stage**: [Pattern observed]
- **Series A/B**: [Pattern observed]
- **Later Stage**: [Pattern observed]

**Insight**: [Do GPs stay involved as companies mature? Evidence?]

---

## Red Flags & Notable Absences

**Companies with Unexpectedly Low GP Involvement**:
- [Company X]: High priority (Tier 1) but no GP mentions
  - Possible reasons: [Stealth mode / Limited PR / Behind-scenes involvement]

**Inconsistencies**:
- [If portfolio materials claim close involvement but public evidence lacking]

---

## GP Profile Insights

Based on mention patterns, what do we learn about each GP?

### [GP1 Name]
**Involvement Style**: [Hands-on / Strategic / Behind-scenes]
**Public Visibility**: [High / Medium / Low]
**Value-Add Focus**: [What types of value-add appear most?]
**Portfolio Focus**: [Which companies get most attention?]

### [GP2 Name]
[Same structure]

---

## Key Findings

1. [Finding 1 with evidence]
2. [Finding 2 with evidence]
3. [Finding 3 with evidence]
[5-7 total findings]

---

## Implications for Portfolio Assessment

[How do GP relationships inform portfolio quality evaluation?]
```

**Output**: Save to `research/analysis/gp-relationships.md`

**Action**: Mark complete in `research-progress.md`

---

### Step 2.2: Create Portfolio Quality Assessment

**Action**: Create `research/analysis/portfolio-assessment.md`

**Prompt**:
```
Review ALL research-summary.md files from Tier 1 and Tier 2 companies, PLUS GP research from research/people/, PLUS company-clusters.md.

Create a comprehensive portfolio quality assessment:

# Portfolio Quality Assessment

**Assessment Date**: [Date]
**Portfolio Scope**: [X Tier 1 companies, Y Tier 2 companies]
**GPs Assessed**: [List]

---

## Executive Summary

[3-4 paragraphs]
- Overall portfolio quality assessment
- Key strengths and differentiation
- Notable weaknesses or concerns
- High-level track record indicators

---

## Portfolio Composition

### Sector Distribution

| Sector | Count | Tier 1 | Tier 2 | % of Portfolio |
|--------|-------|--------|--------|---------------|
| Quantum Computing | 2 | 1 | 1 | X% |
| Robotics | 3 | 2 | 1 | Y% |
| [...]  | ... | ... | ... | ... |

**Analysis**: [Concentration, diversification, sector bet sizing]

### Stage Distribution

| Stage | Count | Notes |
|-------|-------|-------|
| Seed | X | [Observations] |
| Series A | X | [Observations] |
| Series B+ | X | [Observations] |

**Analysis**: [Stage focus, portfolio maturity]

### Geographic Distribution

[If applicable - where are companies based?]

### Vintage Distribution

[When were investments made? Cohort analysis]

---

## Performance Assessment

### Winners (Strong Performers)

**Companies showing strong performance indicators**:

#### [Company Name] (Tier 1)
- **Performance Signals**: [Revenue growth / Market leadership / Recent milestone]
- **Evidence**: [Specific metrics or achievements from research]
- **Estimated MOIC Potential**: [Conservative estimate if data available]
- **Why Winning**: [Key success factors]

[Repeat for all strong performers]

**Summary**: [X] out of [Y] companies showing strong performance ([Z]%)

### Steady Performers

**Companies showing moderate/stable performance**:

[Same structure as above]

**Summary**: Solid portfolio core, risk/opportunity balanced

### Strugglers / Red Flags

**Companies showing concerning signals**:

#### [Company Name]
- **Concerning Signals**: [Slow growth / Increased competition / Team turnover / etc.]
- **Evidence**: [From research]
- **Risk Assessment**: [Potential write-down? Pivot needed?]
- **Mitigation Factors**: [Any positive signals?]

[Repeat for concerning companies]

**Summary**: [X] companies warrant closer monitoring

### Companies Lacking Performance Data

[List companies where public info insufficient to assess performance]
**Implication**: [Early stage? Stealth? Requires direct inquiry?]

---

## Investment Thesis Inference

Based on portfolio patterns, what does this VC look for?

### Sector Preferences (Evidence-Based)

1. **[Sector 1]**: [X] companies, [evidence of why this sector]
   - Pattern observed: [Type of companies, stage, business model]

2. **[Sector 2]**: [Y] companies, [thesis inference]
   - Pattern observed: [...]

### Stage Preference

**Observed Pattern**: [Primary entry point? Follow-on strategy?]
**Evidence**: [Funding rounds, check sizes if available]

### Founder Profile Patterns

Based on founder backgrounds across portfolio:
- **Common traits**: [Technical founders? Serial entrepreneurs? Domain experts?]
- **Diversity**: [Varied or consistent founder types?]
- **Evidence**: [Examples from research]

### Business Model Preferences

- **B2B vs B2C**: [Observed split]
- **SaaS, marketplace, infrastructure, etc.**: [Pattern]
- **Revenue models**: [Subscription, transaction, enterprise, etc.]

### Go-to-Market Patterns

[Any patterns in how portfolio companies go to market?]

### Differentiation / Moat Types

What types of competitive advantages does this VC bet on?
- Technical moat (deep tech, patents)
- Network effects
- Brand/market leadership
- Regulatory barriers
- [Evidence from portfolio]

---

## Competitive Positioning Analysis

### Within-Portfolio Comparisons

For companies in same sectors (use company-clusters.md):

#### Quantum Computing Cluster
- **[Company A]**: [Market position, strengths]
- **[Company B]**: [Market position, strengths]
- **Comparison**: [How do they stack up? Portfolio conflict or complementary?]

[Repeat for each sector cluster]

### Cross-Portfolio Insights

- **Portfolio Synergies**: [Any complementary companies? Cross-selling opportunities?]
- **Portfolio Conflicts**: [Direct competition within portfolio?]
- **Gaps**: [Any notable gaps in sectors/capabilities?]

---

## GP Value-Add Assessment

Based on GP relationship evidence (from gp-relationships.md):

### Involvement Level: [High / Medium / Low]
**Evidence**: [X]% of companies have GP mentions, [Y] strong signals found

### Value-Add Demonstrated:
- **[Value type 1]**: [Evidence across portfolio]
- **[Value type 2]**: [Evidence]
- [Technical guidance / Customer intros / Follow-on fundraising / Team building / etc.]

### Differentiation vs Other VCs:
[Based on GP research, how do these GPs differentiate?]

### Areas for Improvement:
[Based on gaps in involvement or value-add evidence]

---

## Risk Assessment

### Portfolio-Level Risks

1. **Concentration Risk**
   - [Sector, stage, or other concentration concerns]
   - Impact: [What if sector faces headwinds?]

2. **Market Risk**
   - [Market dynamics affecting multiple portfolio companies]
   - Examples: [Specific risks identified in research]

3. **Competitive Risk**
   - [Threats across portfolio]
   - Evidence: [From company research]

4. **Execution Risk**
   - [Common execution challenges observed]
   - Patterns: [Early-stage, scaling, etc.]

5. **Vintage Risk**
   - [Are investments from challenging vintage years?]

### Company-Specific High Risks

[List top 3-5 companies with elevated risk profiles and why]

---

## Portfolio Quality Scoring

Create scoring framework (1-10 scale, 10 = exceptional):

### 1. Company Quality Score: [X]/10
**Components**:
- Team quality: [Score] (founder backgrounds, key hires)
- Product/Technology: [Score] (innovation, defensibility)
- Traction: [Score] (growth metrics, customer adoption)

**Justification**: [Evidence from research]

### 2. Market Positioning Score: [X]/10
**Components**:
- Market opportunity: [Score] (TAM, growth rates)
- Competitive position: [Score] (vs competitors, market share)
- Timing: [Score] (market readiness, trends)

**Justification**: [Evidence]

### 3. Performance Trajectory Score: [X]/10
**Components**:
- Growth momentum: [Score]
- Operational execution: [Score]
- Capital efficiency: [Score] (if data available)

**Justification**: [Evidence]

### 4. GP Value-Add Score: [X]/10
**Components**:
- Relationship strength: [Score] (from GP mentions)
- Demonstrated support: [Score] (evidence of value-add)
- Strategic guidance: [Score] (based on GP capabilities)

**Justification**: [From gp-relationships.md]

### 5. Risk-Adjusted Potential Score: [X]/10
**Components**:
- Upside potential: [Score]
- Risk factors: [Score] (inverse - lower risk = higher score)
- Portfolio balance: [Score]

**Justification**: [From risk assessment]

---

## Overall Portfolio Quality Score: [X]/10

**Overall Assessment**: Strong / Above Average / Average / Below Average / Weak

**Detailed Justification**:
[2-3 paragraphs explaining the score, weighing factors, comparing to typical VC portfolios]

---

## Key Findings Summary

1. **[Finding 1]**: [High-level insight]
   - Evidence: [Supporting data from research]
   - Implication: [What this means]

2. **[Finding 2]**: [...]

[Continue for 7-10 key findings]

---

## Opportunities

**High-Priority Opportunities**:
1. [Opportunity 1 - company or portfolio-level]
2. [Opportunity 2]
3. [...]

**Rationale**: [Why these are opportunities]

---

## Areas for Further Investigation

**Requires Deeper Diligence**:
1. [Area 1 - specific company or theme]
   - Reason: [Why needs more research]
   - Questions: [Specific questions to answer]

2. [Area 2]

[Continue...]

---

## Recommendations

Based on this assessment, recommend:

1. **Priority Companies for Detailed Investment Memos**:
   - [Company A]: [Brief rationale]
   - [Company B]: [Brief rationale]

2. **Companies Requiring Monitoring**:
   - [Company X]: [Concern to track]

3. **Portfolio-Level Actions**:
   - [Strategic recommendation 1]
   - [Strategic recommendation 2]

4. **Further Research Needed**:
   - [Area requiring additional investigation]
```

**Output**: Save to `research/analysis/portfolio-assessment.md`

**Action**: Mark complete in `research-progress.md`

---

### Step 2.3: Create Executive Summary

**Action**: Create `research/outputs/executive-summary.md`

**Prompt**:
```
Synthesize all research into a concise 2-3 page executive summary. Readers should understand the portfolio quality, GP capabilities, and key insights without reading the full research.

# VC Portfolio Research: Executive Summary

**Fund/VC**: [Name]
**Research Period**: [Start Date] - [End Date]
**Companies Researched**: [X Tier 1, Y Tier 2 = Z total]
**GPs Evaluated**: [Names from gp-list.md]

---

## Key Findings

**TL;DR**: [2-3 sentence summary of overall assessment]

### Top 5 Insights

1. **[Insight 1]**: [One sentence with evidence]

2. **[Insight 2]**: [One sentence with evidence]

3. **[Insight 3]**: [One sentence with evidence]

4. **[Insight 4]**: [One sentence with evidence]

5. **[Insight 5]**: [One sentence with evidence]

---

## Portfolio Overview

**Composition**: [Brief description of sector mix, stage, geography]

**Performance Snapshot**:
- **Strong Performers**: [X] companies showing clear positive signals
- **Steady Performers**: [Y] companies with stable/moderate growth
- **Concerns**: [Z] companies with red flags or challenges
- **Insufficient Data**: [W] companies (early-stage or stealth)

**Notable Companies**: [List 3-4 standout companies from research]

---

## Investment Thesis

Based on portfolio analysis, this VC's investment focus:

**Sectors**: [Primary sectors with evidence]

**Stage**: [Typical entry point and follow-on strategy]

**Founder Profile**: [Common founder characteristics observed]

**Business Models**: [Preferred models - SaaS, marketplace, etc.]

**Differentiation**: [What makes this VC's portfolio unique?]

**Thesis Coherence**: [Strong / Moderate / Unclear - is there a clear pattern?]

---

## GP Assessment

### [GP1 Name]
**Background**: [1 sentence: key experience]
**Involvement**: [High / Medium / Low across portfolio]
**Value-Add**: [Primary value demonstrated]
**Strengths**: [Key strengths from research]

### [GP2 Name]
[Same structure]

**GP Team Assessment**: [How do GPs complement each other? Coverage gaps?]

---

## Portfolio Quality Assessment

### Overall Score: [X]/10

**Rating**: Strong / Above Average / Average / Below Average / Weak

**Justification** (3-4 paragraphs):
- Company quality and team strength
- Market positioning and opportunity size
- Performance trajectory and traction
- GP value-add and relationship strength
- Risk factors and concerns

**Comparison**: [How does this compare to typical VC portfolios?]

---

## Strengths

1. **[Strength 1]**: [Evidence]
2. **[Strength 2]**: [Evidence]
3. **[Strength 3]**: [Evidence]
[Continue for 4-6 strengths]

---

## Concerns & Risks

1. **[Risk 1]**: [Description and evidence]
2. **[Risk 2]**: [Description and evidence]
3. **[Risk 3]**: [Description and evidence]
[Continue for 4-5 key risks]

---

## Priority Companies

### Recommended for Detailed Investment Memos

1. **[Company A]**: [Why priority - strong performer? Strategic fit? Unique opportunity?]

2. **[Company B]**: [Why priority]

3. **[Company C]**: [Why priority]

[Continue for 3-5 priority companies]

---

## Companies Requiring Monitoring

1. **[Company X]**: [Concern to track, why needs attention]
2. **[Company Y]**: [Concern]

---

## Next Steps & Recommendations

### Immediate Actions
1. [Specific recommendation 1]
2. [Specific recommendation 2]
3. [Specific recommendation 3]

### Further Research Required
- [Area 1 needing deeper investigation]
- [Area 2 requiring follow-up]
- [Questions remaining unanswered]

### Strategic Considerations
- [Portfolio-level insight or decision point]
- [Strategic opportunity or concern]

---

## Research Methodology & Limitations

**Sources Used**: [Brief description]
- Company-research skill for systematic research
- [X] companies across Tier 1 and Tier 2
- [Y] GPs researched with biographical and track record analysis
- [Z] high-quality sources documented (average per company)

**Limitations**:
- Public information only (no proprietary portfolio data)
- Performance metrics limited for early-stage/stealth companies
- GP involvement may be more extensive than public evidence suggests
- Point-in-time assessment ([Date])

**Confidence Level**: [High / Medium / Low for overall assessment]

---

## Appendix: Research Artifacts

**Full Research Available**:
- Individual company research: `research/deals/tier-[1|2]/{company}/`
- GP profiles: `research/people/{gp-name}/`
- Relationship analysis: `research/analysis/gp-relationships.md`
- Portfolio assessment: `research/analysis/portfolio-assessment.md`

**Total Research Hours**: [Approximate time invested]
**Sources Documented**: [Total count]
```

**Output**: Save to `research/outputs/executive-summary.md`

**Action**: Mark complete in `research-progress.md`

---

### Step 2.4: Final Progress Update

**Action**: Update `research-progress.md`:

1. Mark all Phase 2 items complete
2. Update status to "Complete"
3. Add completion summary:

```markdown
## Completion Summary

**Status**: Complete
**Completion Date**: [Date]
**Total Time Invested**: [Estimate]

**Outputs Created**:
- [X] GPs researched → research/people/
- [Y] Tier 1 companies researched → research/deals/tier-1/
- [Z] Tier 2 companies researched → research/deals/tier-2/
- GP-Company Relationships Matrix → research/analysis/gp-relationships.md
- Portfolio Quality Assessment → research/analysis/portfolio-assessment.md
- Executive Summary → research/outputs/executive-summary.md

**Key Deliverable**: research/outputs/executive-summary.md

**Next Steps**: [What should happen with this research? Investment decisions? Deeper diligence? Memos?]
```

---

## Quality Checklist

Before marking workflow complete, verify:

### Completeness ✅
- [ ] All GPs from gp-list.md researched (folders in research/people/)
- [ ] All Tier 1 companies researched (folders in research/deals/tier-1/)
- [ ] All Tier 2 companies researched (folders in research/deals/tier-2/)
- [ ] GP mentions searched for all companies (integrated in research-summary.md)
- [ ] GP-relationships matrix created
- [ ] Portfolio assessment created
- [ ] Executive summary created

### Quality Standards ✅
- [ ] Each company meets source quality thresholds (not just counts)
- [ ] Research-summary.md files are comprehensive (not superficial)
- [ ] GP mentions section populated (even if "none found")
- [ ] Analysis documents cite specific evidence
- [ ] Portfolio assessment includes scoring framework
- [ ] Executive summary is concise (2-3 pages) and actionable

### Source Documentation ✅
- [ ] Every claim has source attribution
- [ ] Source files properly formatted as .md
- [ ] All source files include URL field (full URL, not just domain)
- [ ] All source files include Date field in YYYY-MM-DD format
- [ ] Source URLs working (spot check sample)
- [ ] Each source includes Objectivity Level assessment
- [ ] High-value sources saved as separate files

### Progress Tracking ✅
- [ ] research-progress.md fully updated
- [ ] Completion dates filled in
- [ ] Final status = "Complete"
- [ ] Completion summary added

---

## Resuming After Interruption

This workflow is designed for resumability. Here's how to continue after any interruption:

### Step 1: Open Progress Tracker
Read `research/research-progress.md`:
- What phase were you in?
- What's marked complete?
- Any notes about blockers or in-progress items?

### Step 2: Verify File System
Scan actual folders (file system = source of truth):
- `research/people/` - Which GPs complete?
- `research/deals/tier-1/` - Which Tier 1 companies complete?
- `research/deals/tier-2/` - Which Tier 2 companies complete?
- `research/analysis/` - Which analysis docs exist?

### Step 3: Reconcile Discrepancies
If progress tracker doesn't match file system:
- Trust the file system
- Update progress tracker to reflect reality
- Note discrepancy in "Notes & Issues"

### Step 4: Identify Next Task
From progress tracker, find first unchecked item:
- **Phase 1A**: Continue with next uncompleted GP
- **Phase 1B**: Continue with next uncompleted company (Tier 1 first, then Tier 2)
- **Phase 1C**: Check which companies lack GP mention updates in their research-summary.md
- **Phase 2**: Complete remaining analysis documents

### Step 5: Resume from Checkpoint
- Jump directly to the relevant step in this workflow
- All phases designed to check for existing work before starting
- No risk of duplication

### Example Resume Scenario:
```
Progress tracker shows:
✅ Phase 1A: 2/2 GPs complete
✅ Phase 1B: 4/6 Tier 1 complete, 0/10 Tier 2 complete
⬜ Phase 1C: Not started

File system shows:
✅ research/people/gp1/ exists
✅ research/people/gp2/ exists
✅ research/deals/tier-1/company-a/ exists
✅ research/deals/tier-1/company-b/ exists
✅ research/deals/tier-1/company-c/ exists
✅ research/deals/tier-1/company-d/ exists

ACTION: Resume Phase 1B, continue with Tier 1 Company E (5th of 6)
THEN: Complete Tier 1 Company F
THEN: Move to Tier 2 companies
THEN: Start Phase 1C (GP mentions cross-reference)
```

---

## Common Issues & Troubleshooting

### Issue: GP Extraction Fails
**Symptoms**: Can't find GP names in dataroom automatically

**Solution**:
1. Manually check these files (in order):
   - GP Bio.md
   - Fund I.md or pitch deck
   - Case studies (look for quoted individuals)
2. Extract names manually
3. Create research/gp-list.md manually
4. Continue with Phase 1A

**Prevention**: Document extraction notes for future reference

---

### Issue: Company-Research Skill Returns Limited Results
**Symptoms**: Sparse research for certain companies

**Solution**:
1. Check if company is very early-stage or stealth (expected)
2. Manually supplement with targeted WebSearch:
   - Company website
   - LinkedIn company page
   - Founder LinkedIn profiles
   - Crunchbase/PitchBook if available
3. Document data limitations in research-summary.md
4. Note in progress tracker: "Limited public info available"

**Quality Check**: Still require minimum sources (company website + 1-2 others)

---

### Issue: No GP Mentions Found for Multiple Companies
**Symptoms**: Many companies show "no mentions found"

**Solution**:
1. **This is valid data** - absence of evidence is informative
2. Document search strategy used in research-summary.md
3. Note patterns in gp-relationships.md:
   - Are certain sectors lacking mentions?
   - Stage-dependent pattern?
   - Stealth portfolio?
4. Consider: GP involvement may be private (common in early-stage)

**Not a failure**: Report finding accurately in analysis

---

### Issue: Progress Tracker Out of Sync
**Symptoms**: Progress tracker doesn't match actual work completed

**Solution**:
1. Scan file system comprehensively
2. Update progress tracker to match reality
3. Add note explaining sync issue
4. Continue from actual state (file system = truth)

**Prevention**: Update progress at batch boundaries as instructed

---

### Issue: Research Taking Longer Than Expected
**Symptoms**: Exceeding 8-12 hour estimate significantly

**Solution**:
1. **Check if over-researching**: Are you exceeding quality thresholds significantly?
2. **Focus on priorities**:
   - Complete all Tier 1 first
   - Tier 2 can be lighter depth
   - Phase 2 analysis is most valuable output
3. **Time-box per company**:
   - Tier 1: Hard stop at 60 minutes
   - Tier 2: Hard stop at 40 minutes
4. **Batch and break**: Research 3 companies, take break, review efficiency

**Reminder**: Quality > Quantity. Better to complete workflow with smart thresholds than abandon mid-way.

---

## Workflow Completion

When all phases complete:

### Step 1: Final Quality Review
Run through quality checklist above - all items checked?

### Step 2: Update Progress Tracker
- Status: "Complete"
- Add completion summary (see Step 2.4)
- Document total time invested

### Step 3: Organize Outputs
Ensure these files are ready for review:
- **Primary Deliverable**: `research/outputs/executive-summary.md` (read this first)
- **Deep Dive**: `research/analysis/portfolio-assessment.md` (full assessment)
- **Relationships**: `research/analysis/gp-relationships.md` (GP involvement)
- **Individual Research**: `research/deals/` and `research/people/` (detailed sources)

### Step 4: Share & Next Steps
- Share executive summary with stakeholders
- Based on findings, decide:
  - Which companies need detailed investment memos? (separate workflow)
  - Any immediate concerns requiring follow-up?
  - Strategic decisions informed by this research?

---

## Follow-Up Workflows

After completing vc-research:

### Investment Memo Creation (Separate Workflow)
**When**: After identifying priority companies in executive summary

**Process**:
- Input: Company research from this workflow
- Output: Detailed investment memo for decision-making
- Duration: ~2-3 hours per memo
- Format: Formal investment committee document

### Competitive Deep Dive
**When**: Need detailed competitive analysis for specific sector

**Process**:
- Input: Company cluster from this research
- Output: Competitive landscape map, positioning analysis
- Leverage: Reuse market analysis from multiple companies

### Founder Reference Checks
**When**: Moving to deeper diligence on specific companies

**Process**:
- Input: Founder info from company research
- Output: Reference call summaries, background verification

---

## Workflow Metrics & Optimization

Track these metrics for continuous improvement:

### Efficiency Metrics
- Total hours invested: [Target: 8-12 hours]
- Average time per company: [Tier 1: 45-60 min, Tier 2: 30-40 min]
- Average sources per company: [Tier 1: 5+, Tier 2: 3+]
- GP mention hit rate: [% of companies with mentions found]

### Quality Metrics
- Executive summary clarity: [Actionable insights?]
- Portfolio assessment depth: [Sufficient evidence for scoring?]
- Research resumability: [Was progress tracker effective?]

### Areas for Optimization
[After completing workflow, note what could be improved for next time]

---

## Related Workflows

- **Prerequisite**: `deal-prioritization.md` (creates research/priority-deals.md input)
- **Complementary**: `market-assessment` skill (for competitive deep dives)
- **Follow-up**: Investment memo creation workflow (for priority companies)
- **Complementary**: Founder research workflow (for deeper due diligence)

---

## Adaptations & Variations

### Variation 1: Single Company Deep Dive
If researching only one portfolio company:
- Skip: Phase 1A (GP research) OR research only relevant GP
- Skip: Other companies in Phase 1B
- Skip: Phase 2.1 (GP relationships matrix)
- Focus: Phase 1B for target company + Phase 2.2-2.3 (company assessment)

### Variation 2: GP-Only Research
If only evaluating GP team:
- Complete: Phase 1A (all GPs)
- Skip: Phase 1B and 1C (companies)
- Focus: GP profiles, backgrounds, track records
- Output: GP assessment document

### Variation 3: Quick Portfolio Scan
If need rapid high-level view (not deep research):
- Use existing public data (Crunchbase, PitchBook, LinkedIn)
- Skip company-research skill invocation (too deep)
- Manual scan of company websites + funding announcements
- Focus on Phase 2 analysis with lighter evidence
- Timeline: 2-4 hours vs 8-12 hours

### Variation 4: Sector-Specific Research
If focusing on one sector only:
- Filter companies in Phase 0.3 by target sector
- Deep dive only relevant companies (ignore other tiers)
- Add competitive landscape analysis
- Market sizing and trends as additional output

---

## Appendix: GP Extraction Examples

### Example 1: GP Bio.md Pattern
```markdown
Line 52: "Mr. Dunteman brings over 15 years of experience..."
Line 60: "Dillon Dunteman holds a B.S. in Electrical Engineering from Stanford..."

EXTRACTION:
- GP Name: Dillon Dunteman
- Source: GP Bio.md (lines 52, 60)
- Context: Professional bio section
```

### Example 2: Fund Deck Pattern
```markdown
Slide 3: "Investment Team"
- Dillon Dunteman, General Partner
- Harry Bellew, General Partner

EXTRACTION:
- GP Name 1: Dillon Dunteman (Title: General Partner)
- GP Name 2: Harry Bellew (Title: General Partner)
- Source: Fund I.md (page 3)
```

### Example 3: Case Study Pattern
```markdown
"Our partnership with Hyperion, particularly Dillon's technical guidance,
was instrumental in..." - CEO, Acme Robotics

EXTRACTION:
- GP Name: Dillon (likely Dillon Dunteman based on context)
- Source: Case Study - Acme Robotics
- Confidence: Medium (first name only, need to cross-reference)
- Action: Validate with other sources
```

---

## Version History

- **v2.0** (2025-01-11): Streamlined version
  - Added dynamic GP extraction (Phase 0.2)
  - Parallelized research (Phases 1A + 1B concurrent)
  - Consolidated GP mention searches (Phase 1C)
  - Integrated GP mentions into research-summary.md (eliminated separate files)
  - Unified Tier 1/2 process
  - Removed investment memos from core workflow (now separate)
  - Batch progress updates (reduced overhead)
  - Smart source quality thresholds
  - Added company clustering for research reuse
  - **Time reduction**: 15-20 hours → 8-12 hours (40-50% faster)

- **v1.0** (2025-01-11): Initial version
  - Sequential workflow
  - Hardcoded GP names
  - Separate gp-mentions.md files
  - Investment memos included

---

## Questions or Issues?

Document in `research/progress-notes.md` or `research/research-progress.md` Notes & Issues section.
