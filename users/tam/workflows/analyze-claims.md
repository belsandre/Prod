# Analyze Claims Workflow

Extract key narratives from data rooms, identify conspicuous gaps, and recommend validation approaches.

## Input

Data room materials: pitch decks, memos, marketing materials, portfolio summaries, website content, thought leadership.

## Core Questions

1. **What is the key narrative?** (sourcing differentiator, right to win competitive deals, network quality, other claims)
2. **What are conspicuous gaps?** (missing from the narrative, timeline silences, unsubstantiated claims)
3. **How to validate?** (request materials, network analysis, portfolio analysis, timing verification)

## Methodology

### Source Classification

Evaluate claim objectivity based on source type:

- **Data room**: Entity-controlled materials (pitch deck, website, marketing content) - lowest objectivity, self-reported
- **Affiliated**: Friendly sources (portfolio company quotes, co-investor testimonials, PR releases) - medium objectivity
- **Independent**: Third-party sources (news articles, SEC filings, court documents, third-party research) - highest objectivity

### Verification Statuses

- ✅ **Verified**: Independent sources confirm claim and timing
- ⚠️ **Partial**: Directionally true but timing uncertain, or only affiliated sources
- ❓ **Unverified**: Only data room sources, no external confirmation
- ❌ **Conflicting**: Independent sources contradict claim
- 🕐 **Timing Issue**: Event happened but timing contradicts narrative framing

**Important**: When calculating returns/multiples, compare entry valuation to current valuation (apples-to-apples), not check size to valuation. Example: "$500K check at $10M post-money → $100M valuation" = 10x return on entry valuation, not 200x.

### Timing Analysis for Predictive Claims

Claims about being "early" or "predictive" require timing verification:

- **Early investor claims**: >90 days before consensus = ✅ verified early; <90 days = ⚠️ partial (reactive); after consensus = ❌ conflicting
- **Predictive thought leadership**: Published >30 days before investment/action = ✅ verified; ±30 days = ⚠️ partial; published after = 🕐 timing issue (retroactive narrative)

### Context for VC Datarooms

**Expected in VC datarooms** (not critical gaps):
- Limited/zero independent sources (entity-controlled materials)
- Selective disclosure emphasizing winners (VC is power law distribution)
- Unverified superlatives and marketing language
- Founder testimonials from portfolio companies (affiliated sources)

**Critical gaps** (actually concerning):
- **Stale data presented as current**: Spreadsheets dated 2025 containing 2024 data
- **Material role ambiguity**: Claiming involvement without clarifying role (sourced vs. led vs. board seat vs. participated)
- **Co-founder/co-GP underrepresentation**: Multiple GPs but one dominates narrative with minimal mention of others
- **Material footnote disclosures**: Key caveats buried in footnotes (e.g., "excludes digital assets," "secondary transaction valuation," "SAFE/convertible note not institutional round")
- **Timeline silences with contradiction**: Multi-year gaps contradicting "continuous activity" narrative
- **Retroactive narrative construction**: Thesis documents dated after investments, thought leadership published post-investment
- **Conspicuous omissions with materiality**: Selective disclosure where missing information would materially change assessment (e.g., excluding half the portfolio)

## Process

### Step 1: Extract Claims

Read all data room materials and extract key narratives organized by type:

**Claim Categories:**
- Sourcing differentiator (proprietary deal flow, unique access, network advantages)
- Competitive positioning (right to win deals, selection criteria, decision-making edge)
- Network quality (relationships, expertise, pattern recognition)
- Track record (portfolio performance, exits, value creation)
- Other differentiators (speed, conviction, founder empathy, operational support)

**For each claim:**
- Exact quote with source reference
- Source classification (data room/affiliated/independent)
- Supporting sub-claims with specific examples
- Implied timing or chronology

**Structure:** 3-5 KEY claims, each with 2-5 supporting sub-claims

### Step 2: Identify Gaps

Focus on **critical gaps** that materially impact assessment, not normal VC dataroom practices:

**Stale Data:**
- Spreadsheets/appendices dated recently but containing old data
- Missing time periods (e.g., "as of Q4 2024" when analyzing in 2025)
- Speculative projections that should now be actuals

**Role Ambiguity:**
- Claimed involvement without clarifying specific role or contribution
- "Deployed $X" or "Involved in Y deals" without sourcing/leading/board seat clarity
- Credit-claiming that may be overstated relative to actual responsibility

**Co-GP/Team Underrepresentation:**
- Multiple GPs listed but unequal representation in materials
- Key team members mentioned without substance on their contributions

**Material Footnote Disclosures:**
- Valuation methodology caveats (secondary transactions, SAFE caps, not institutional rounds)
- Explicit exclusions ("digital assets excluded," "non-core investments omitted")
- Performance calculation disclaimers that materially affect interpretation

**Timing Contradictions:**
- Thesis timing unclear relative to investment timing
- Thought leadership archive missing when "early positioning" claimed
- "We predicted X" without dated public record

**Conspicuous Omissions with Materiality:**
- Missing portfolio data that would significantly change performance assessment
- Selective disclosure where pattern of missing info suggests adverse selection

### Step 3: Validation Roadmap

For each claim type, recommend specific validation methods:

**Validation Approaches:**

1. **Review all provided materials first:**
   - Read all spreadsheets, appendices, footnotes in dataroom
   - Check dates on files vs. data they contain
   - Analyze footnotes for material disclosures
   - Map out what's already disclosed before requesting more

2. **Characterize networks (breadth, depth, high-profile relationships):**
   - Map stated networks by category (e.g., Harvard network, deeptech network, VCPE network)
   - Identify specific high-profile individuals or companies mentioned
   - Assess depth of relationships (advisory roles, board seats, co-investments)
   - Note any conspicuous absences in expected networks

3. **Portfolio analysis:**
   - Verify valuations (Crunchbase, PitchBook, news archives)
   - Check footnotes for material caveats (secondary transactions, SAFE caps, convertible notes)
   - Compare claimed portfolio to public records

4. **Clarify role and contribution:**
   - Determine specific role: sourcing lead, deal lead, board member, observer, participant?
   - Cross-reference with LinkedIn, news, co-investor sources

5. **Timing verification:**
   - Search for public thought leadership (blog posts, articles, talks, tweets)
   - Compare thesis publication dates to investment dates
   - Verify "early" claims against market consensus timing

6. **Independent validation:**
   - Web search (news, articles, third-party mentions)
   - LinkedIn (employment history, connections)
   - PitchBook/Crunchbase (deal participation)
   - Reference checks (co-investors, former colleagues, non-portfolio founders)

**Prioritization:** Focus validation efforts on critical gaps with material impact and high feasibility.

## Outputs

### marketing-to-reality/_data/claims.json

Structured data containing all findings (only fields displayed in template):

```json
{
  "entity_name": "string",
  "entity_gp": "string",
  "analysis_date": "YYYY-MM-DD",
  "data_room_sources": ["source1", "source2"],
  "key_claims": [
    {"claim_id": "TRACK_RECORD"},
    {"claim_id": "SOURCING_EDGE"}
  ],
  "conspicuous_gaps": [
    {
      "gap_type": "stale_data|role_ambiguity|co_gp_underrepresentation|material_footnote|timing_contradiction",
      "description": "string",
      "significance": "why this matters",
      "risk_severity": "red_flag|yellow_flag",
      "risk_level": "Material concern|Moderate concern"
    }
  ],
  "source_tier_summary": {
    "data_room_sources": 12,
    "affiliated_sources": 12,
    "independent_sources": 0
  },
  "narrative_analysis": {...},
  "risk_synthesis": {...},
  "validation_tiers": [...],
  "conclusion": {...}
}
```

**Note**: JSON contains ONLY fields that are displayed in the template. Detailed sub-claims, verification status, and granular validation actions are NOT stored since they're not displayed.

### marketing-to-reality/claims-analysis.md

Template file that renders data from claims.json using Nunjucks/Liquid syntax:

**Data Separation Principle (following network-analysis.md / objective-timeline.md pattern):**

- **claims.json = ALL CONTENT**: Complete structured data with ALL substantive content including facts, analysis paragraphs, descriptions, findings, evidence, validation actions. Contains narrative text in fields like "summary", "description", "details", "significance".
- **claims-analysis.md = PURE TEMPLATE**: Nunjucks/Liquid template with NO substantive content. Only contains:
  - Template variables: `{{ hyperionClaims.field }}`
  - Loops: `{% for item in array %}...{% endfor %}`
  - Conditionals: `{% if condition %}...{% endif %}`
  - Document structure (headings, sections)
  - Brief 1-sentence section introductions

**Key Principle**: If you delete all JSON data, the markdown should be just empty template structure with no substance.

**JSON Structure** (all content stored here):
```json
{
  "key_claims": [...],
  "conspicuous_gaps": [...],
  "validation_roadmap": [...],
  "narrative_analysis": {
    "hero_journey": {
      "summary": "...",
      "phases": [...],
      "positioning": "..."
    },
    "emphasis_areas": {
      "performance_outliers": {"summary": "...", "details": [...]},
      "sourcing_differentiators": {...},
      "technical_credibility": {...},
      "market_timing": {...}
    }
  },
  "risk_synthesis": {
    "red_flags": "...",
    "yellow_flags": "...",
    "mitigating_factors": [...]
  },
  "validation_tiers": [
    {
      "tier": 1,
      "priority": "...",
      "goal": "...",
      "actions": [{"title": "...", "bullets": [...]}]
    }
  ],
  "conclusion": {
    "summary": "...",
    "critical_gaps_summary": "...",
    "recommendation": "..."
  }
}
```

**Markdown Template Structure**:
```markdown
## 1. Narrative Analysis

### The Hero's Journey Arc

{{ hyperionClaims.narrative_analysis.hero_journey.summary }}:

{% for phase in hyperionClaims.narrative_analysis.hero_journey.phases %}
{{ loop.index }}. **{{ phase.name }}** ({{ phase.years }}): {{ phase.description }}
{% endfor %}

### What's Emphasized

{% for area_key, area in hyperionClaims.narrative_analysis.emphasis_areas %}
**{{ area.summary }}**:
{% for detail in area.details %}
- {{ detail }}
{% endfor %}
{% endfor %}
```

**Writing Approach**:
- ALL substantive content (facts, analysis, paragraphs) goes in claims.json
- Markdown is ONLY template logic + structure (~100 lines of template code)
- Use Nunjucks/Liquid syntax for all data display
- Pattern matches network-analysis.md and objective-timeline.md exactly

## Quality Checklist

- [ ] 3-5 KEY claim IDs identified (simplified array with just claim_id fields)
- [ ] Critical gaps identified (distinguished from normal VC dataroom practices)
- [ ] Material footnote disclosures analyzed and flagged
- [ ] claims.json validates as proper JSON format
- [ ] claims.json contains ALL substantive content (facts, analysis paragraphs, descriptions)
- [ ] claims.json includes sections: narrative_analysis, risk_synthesis, validation_tiers, conclusion
- [ ] claims.json contains ONLY fields displayed in template (no unused fields like detailed sub_claims or validation_roadmap)
- [ ] claims-analysis.md is pure Nunjucks/Liquid template (~100 lines of template code)
- [ ] Markdown uses {% raw %}`{{ variable }}`{% endraw %} and {% raw %}`{% for %}`{% endraw %} syntax to display JSON data
- [ ] NO substantive content in markdown (only template logic + structure)
- [ ] Apples-to-apples comparisons (entry valuation to current valuation, not check size to valuation)
- [ ] Timing analysis applied to all "early" or "predictive" claims
- [ ] Pattern matches network-analysis.md and objective-timeline.md structure

## Example Use Case

**Input:** VC fund data room claiming "proprietary access to AI infrastructure deals through our network of technical founders"

**Claims extraction:**
- KEY claim: Proprietary sourcing via technical founder network
- Sub-claims: Early investor in 5 AI infrastructure companies, CTO introductions, technical thesis from 2019

**Critical gap identification** (not normal VC practices):
- Thesis document dated 2021, but claims investments from 2019 (timing contradiction = retroactive narrative)
- Portfolio spreadsheet dated 2024 but presenting as current in 2025 (stale data)
- Footnote reveals "excludes 7 non-AI investments" (material footnote disclosure)

**Validation roadmap:**
- Review provided materials: Check portfolio spreadsheet for all investments and dates
- Verify thesis timing: Web search for blog posts or public statements from 2019
- Characterize networks: Map CTO relationships by category, identify high-profile connections
- Clarify role: For "early investor" claims, determine if sourcing lead or participant

**Output:** claims.json with structured findings + claims-analysis.md interpreting critical gaps (retroactive narrative, stale data) vs. normal practices (power law selective disclosure)
