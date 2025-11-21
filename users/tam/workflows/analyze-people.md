# People Analysis Workflow

## Purpose

Validate GP-related marketing claims against independent evidence to assess: (1) Are the claimed accomplishments real? (2) Are there material omissions in how GPs present themselves? This workflow cross-references dataroom narratives with research evidence to identify credibility gaps, attribution issues, and structural concerns.

## Inputs

- **Claims files**: `claims-analysis.md` and/or `_data/claims.json` (GP-related claims only)
- **Dataroom folder**: GP bios, pitch decks, reference letters, case studies
- **Research/people folders**: LinkedIn profiles, network CSVs (subset of connections), independent sources
- **Research/network folders**: Partial connection data by category (methodology limitations mean not all connections captured)

## Outputs

### marketing-to-reality/_data/people.json

Structured data containing all GP analysis findings:

```json
{
  "entity_name": "string",
  "fund_name": "string",
  "analysis_date": "YYYY-MM-DD",
  "general_partners": [
    {
      "name": "string",
      "role": "string",
      "verified_credentials": {...},
      "key_attribution_claims": [
        {
          "claim_id": "VISTA_DEPLOYMENT|FIRMAMENT_EXITS|etc",
          "claim": "string",
          "verification_status": "verified|role_unclear|timing_issue|etc",
          "verification_tier": "independent|affiliated|dataroom_only",
          "concern": "string (if applicable)"
        }
      ],
      "material_concerns": [...]
    }
  ],
  "critical_people_gaps": [
    {
      "gap_type": "vista_role_ambiguity|co_gp_underrepresentation|etc",
      "person": "string",
      "description": "string",
      "why_it_matters": "string",
      "what_to_ask": "string",
      "risk_severity": "red_flag|yellow_flag",
      "priority": "critical|important"
    }
  ],
  "team_structure_assessment": {...},
  "risk_synthesis": {...},
  "executive_summary": {...}
}
```

### marketing-to-reality/people-analysis.md

Template file that renders data from people.json using Nunjucks template syntax:

**Data Separation Principle** (following claims-analysis.md pattern):

- **people.json = ALL CONTENT**: Complete structured data with ALL substantive content including credentials, claims, evidence tiers, concerns, validations, analysis. Contains narrative text in fields like "description", "why_it_matters", "what_to_ask".
- **people-analysis.md = PURE TEMPLATE**: Nunjucks template with NO substantive content. Only contains:
  - Template variables: `{{ hyperionPeople.field }}`
  - Loops: `{% for gp in hyperionPeople.general_partners %}...{% endfor %}`
  - Conditionals: `{% if gp.thought_leadership %}...{% endif %}`
  - Document structure (headings, sections)

**Key Principle**: If you delete all JSON data, the markdown should be just empty template structure with no substance.

**Markdown Template Example**:
```markdown
## GP Profiles

{% for gp in hyperionPeople.general_partners %}
### {{ gp.name }} ({{ gp.role }})

**Key Claims vs Evidence:**

| Claim | Evidence Source | Status |
|-------|----------------|--------|
{% for claim in gp.key_attribution_claims %}
| {{ claim.claim }} | {{ claim.verification_tier }} | {{ claim.verification_status }} |
{% endfor %}
{% endfor %}
```

**Writing Approach**:
- ALL substantive content (facts, analysis, paragraphs) goes in people.json
- Markdown is ONLY template logic + structure
- Use Nunjucks syntax for all data display
- Updates modify JSON, not markdown

---

## Methodology

### Phase 1: Extract GP-Related Claims

1. **Filter claims** from claims.json/claims-analysis.md where category involves people:
   - Technical expertise (education, professional background)
   - Network access (relationships, sourcing channels)
   - Track record (prior investments, performance attribution)
   - Value-add (board seats, strategic support, portfolio involvement)

2. **Identify claim structure** for each:
   - Main claim (headline narrative)
   - Sub-claims (specific evidence points)
   - Source classification (dataroom/affiliated/independent)
   - Current verification status

### Phase 2: Map Available Evidence

3. **Inventory research sources** by GP:
   - LinkedIn profiles (education, employment history)
   - Network data (partial connection captures—methodology limitations mean incomplete data; do not claim captured connections = total network size)
   - Independent sources (news articles, court filings, SEC documents)
   - Affiliated sources (founder references, co-investor testimonials)
   - Dataroom sources (pitch decks, bios, letters)

4. **Categorize evidence** by source type:
   - **Independent**: News, public records, third-party research
   - **Affiliated**: Portfolio founders, co-investors, former colleagues
   - **Dataroom**: Self-reported materials, GP-controlled narratives

### Phase 3: Validate Claims

For each GP-related claim:

5. **Credential verification**:
   - Education: Confirm degree, graduation date, thesis/specialization (LinkedIn, university records)
   - Professional experience: Verify employers, titles, dates, deal involvement (LinkedIn, press, SEC filings)
   - Thought leadership: Assess substance (frequency, consistency, engagement) not just existence—sporadic posting ≠ credible expertise
   - Flag timing issues: Did credentials exist before claimed accomplishments?

6. **Track record attribution**:
   - Individual vs institutional contribution: Was GP at the firm during the deal?
   - Role clarity: Sourced, led, supported, board seat, passive?
   - **Personal contribution attribution**: Which deals did each GP actually work on? What was their specific role?
   - Time at firm: Junior analyst or decision-maker during claimed wins?
   - **Note:** Focus on GP's role/attribution, NOT portfolio company performance (that's portfolio analysis)

### Phase 4: Identify Material Omissions (People-Specific Only)

7. **Critical people gaps** (structural concerns requiring validation):
   - **Co-GP underrepresentation**: Significant economic stake but minimal dataroom presence
   - **Attribution ambiguity**: Team vs individual contribution unclear (focus on GP's personal role, not deal outcomes)
   - **Role inflation**: Analyst-level experience presented as decision-maker track record
   - **Timing contradictions**: Retroactive narrative construction (claimed expertise before evidence exists)
   - **Relationship exaggeration**: "Close collaborator" with zero mutual connections
   - **Single points of failure**: One GP handles all critical functions (sourcing, diligence, portfolio support)
   - **Capacity misalignment**: GP count vs portfolio size creates impossible coverage
   - **Experience gaps**: Critical skills missing from team (e.g., non-technical partners in deeptech fund)

8. **Normal gaps** (expected in VC marketing, not inherently concerning):
    - Selective disclosure of wins vs losses (this is portfolio-level, not people-level)
    - Limited independent sources: Most references from affiliated parties
    - Founder testimonials: Self-selected positive feedback
    - Aspirational framing: "Building networks" vs "established networks"
    - Unverifiable personal track records: Angel returns are always private

**IMPORTANT:** Exclude portfolio-level gaps from this analysis:
- ❌ Portfolio valuation methodology (e.g., secondary vs institutional marks)
- ❌ Stale portfolio data or performance updates
- ❌ TVPI/IRR calculation methods
- ❌ Specific company valuation verification
These belong in portfolio analysis workflows, NOT people analysis.

### Phase 5: Synthesize Findings

9. **Per-GP assessment**:
    - Background summary (verified credentials, networks, track record)
    - Key claims vs evidence (table showing claim → evidence source → status)
    - Material concerns (unverified claims, contradictions, omissions)
    - Rating: Conditional on verification (e.g., "Strong if Vista role verified")

10. **Team dynamics**:
    - GP economics vs contribution: Do carry allocations align with involvement?
    - Redundancy: What happens if one GP leaves?
    - Structural risks: Over-reliance on single individual?
    - Co-GP concerns: Underrepresented partners, passive vs active roles

11. **Recommendations**:
    - Required validations: Specific follow-up investigations before investment
    - Priority: High (structural concerns), Medium (attribution clarity), Low (nice-to-have)
    - Method: Network calls, reference checks, portfolio deep dives, independent research

---

## Key Principles

- **Evidence-based**: Only confirm claims with affiliated or independent sources (not just dataroom)
- **Attribution clarity**: Distinguish individual vs institutional contribution
- **Timing verification**: Flag retroactive narrative construction
- **Materiality focus**: Separate concerning gaps from normal VC marketing
- **Conditional ratings**: "Strong if verified" vs "Weak if unverified" scenarios
- **Conciseness**: Eliminate redundancy—state insights once, clearly
- **Generalizability**: Workflow applies to any GP/fund, not entity-specific

---

## Common Validation Questions

- **Credentials**: Can we confirm education, employment, deal experience via independent sources?
- **Track Record**: Was the GP at the firm during claimed deals? What was their specific role?
- **Attribution**: Individual contribution vs team effort? How do we know?
- **Omissions**: Why is a co-GP absent from dataroom materials despite significant economics?
- **Timing**: Did claimed expertise exist before or after the accomplishment?
- **Structural**: What happens if the primary GP is unavailable? Single point of failure?
- **Capacity**: Can the GP team realistically support the target portfolio size?

---

## Generalization Notes

This workflow is designed to be reusable across different funds and GPs:

- **Adaptable inputs**: Works with whatever evidence is available (network data, LinkedIn, public records)
- **Graceful degradation**: If certain data sources don't exist, use available alternatives
- **Clear gap taxonomy**: Distinguishes "can't verify" from "contradicts claims"
- **Scalable**: Works for solo GPs, small teams, or large partnerships
- **Prioritization framework**: Helps focus limited diligence time on material concerns

The output should be **concise and non-redundant** (aim for 200-400 lines), evidence-focused, and actionable for investment decision-making. Avoid repeating the same insight in multiple sections.
