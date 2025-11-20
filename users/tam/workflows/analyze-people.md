# People Analysis Workflow

## Purpose

Validate GP-related marketing claims against independent evidence to assess: (1) Are the claimed accomplishments real? (2) Are there material omissions in how GPs present themselves? This workflow cross-references dataroom narratives with research evidence to identify credibility gaps, attribution issues, and structural concerns.

## Inputs

- **Claims files**: `claims-analysis.md` and/or `_data/claims.json` (GP-related claims only)
- **Dataroom folder**: GP bios, pitch decks, reference letters, case studies
- **Research/people folders**: LinkedIn profiles, network CSVs, independent sources
- **Research/network folders**: Connection analysis by category (if available)

## Outputs

Create `marketing-to-reality/people/gp-analysis.md` with:
- **Header**: Sources consulted, validation process, analysis goal
- **Per-GP analysis**: Credentials, network, **personal attribution** (not portfolio performance), role clarity
- **Team dynamics**: Economics, redundancy, structural risks
- **Critical gaps**: Material **people-specific** omissions vs normal VC marketing
- **Recommendations**: Required validations before investment

**Note:** This workflow focuses on **GP-level concerns only**. Portfolio-level issues (company valuations, TVPI calculations, performance verification) belong in separate portfolio analysis workflows.

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
   - Network CSVs (actual connections by category: industry, school, investor)
   - Independent sources (news articles, court filings, SEC documents)
   - Affiliated sources (founder references, co-investor testimonials)
   - Dataroom sources (pitch decks, bios, letters)

4. **Categorize evidence** by objectivity tier:
   - **Tier 3** (Independent): News, public records, third-party research
   - **Tier 2** (Affiliated): Portfolio founders, co-investors, former colleagues
   - **Tier 1** (Dataroom): Self-reported materials, GP-controlled narratives

### Phase 3: Validate Claims

For each GP-related claim:

5. **Credential verification**:
   - Education: Confirm degree, graduation date, thesis/specialization (LinkedIn, university records)
   - Professional experience: Verify employers, titles, dates, deal involvement (LinkedIn, press, SEC filings)
   - Flag timing issues: Did credentials exist before claimed accomplishments?

6. **Network validation**:
   - Cross-reference claimed relationships with network CSV data
   - Count actual connections vs claimed access (e.g., "deep Harvard network" → harvard.csv connection count)
   - Assess depth vs breadth: Advisors/board seats vs passive connections
   - Identify gaps: Claimed "close relationships" with zero/minimal connections

7. **Track record attribution**:
   - Individual vs institutional contribution: Was GP at the firm during the deal?
   - Role clarity: Sourced, led, supported, board seat, passive?
   - **Personal contribution attribution**: Which deals did each GP actually work on? What was their specific role?
   - Time at firm: Junior analyst or decision-maker during claimed wins?
   - **Note:** Focus on GP's role/attribution, NOT portfolio company performance (that's portfolio analysis)

8. **Portfolio involvement**:
   - Coverage metrics: How many portfolio companies does each GP support?
   - Tier breakdown: Which companies get attention vs neglect?
   - Board seats: Actual governance role vs claimed strategic support?
   - Single point of failure: What happens if primary GP is unavailable?

### Phase 4: Identify Material Omissions (People-Specific Only)

9. **Critical people gaps** (structural concerns requiring validation):
   - **Co-GP underrepresentation**: Significant economic stake but minimal dataroom presence
   - **Attribution ambiguity**: Team vs individual contribution unclear (focus on GP's personal role, not deal outcomes)
   - **Role inflation**: Analyst-level experience presented as decision-maker track record
   - **Timing contradictions**: Retroactive narrative construction (claimed expertise before evidence exists)
   - **Relationship exaggeration**: "Close collaborator" with zero mutual connections
   - **Single points of failure**: One GP handles all critical functions (sourcing, diligence, portfolio support)
   - **Capacity misalignment**: GP count vs portfolio size creates impossible coverage
   - **Experience gaps**: Critical skills missing from team (e.g., non-technical partners in deeptech fund)

10. **Normal gaps** (expected in VC marketing, not inherently concerning):
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

11. **Per-GP assessment**:
    - Background summary (verified credentials)
    - Network quality (connection count/depth vs claims)
    - Track record (attributed deals with evidence tier)
    - Portfolio coverage (involvement metrics)
    - Strengths (verified claims with Tier 2+ evidence)
    - Concerns (unverified claims, contradictions, material omissions)
    - Rating: Conditional on verification (e.g., "Strong if Harvard network verified")

12. **Team dynamics**:
    - GP economics vs contribution: Do carry allocations align with involvement?
    - Redundancy: What happens if one GP leaves?
    - Structural risks: Over-reliance on single individual?
    - Co-GP concerns: Underrepresented partners, passive vs active roles

13. **Recommendations**:
    - Required validations: Specific follow-up investigations before investment
    - Priority: High (structural concerns), Medium (attribution clarity), Low (nice-to-have)
    - Method: Network calls, reference checks, portfolio deep dives, independent research

---

## Output Format

### Header (gp-analysis.md)

```markdown
# GP People Analysis: [Fund Name]

**Entity:** [Entity Name]
**General Partners:** [Names and titles]
**Analysis Date:** [Date]

**Analysis Goal:** Validate GP credentials, networks, personal attribution, and team structure against independent evidence.

**Sources:** Dataroom (X files), research/people folders (LinkedIn, network CSVs, independent verification), claims files

**Process:** Extracted GP claims → mapped evidence by tier (independent/affiliated/dataroom) → validated credentials/networks/attribution → identified people-specific gaps → synthesized team assessment

**Note:** People-level analysis only. Portfolio performance verification in separate workflows.

---
```

### Main Sections

1. **Executive Summary** (2-3 sentences, overall rating)

2. **GP #1: [Name]**
   - Background & Credentials (verified education/experience)
   - Network Analysis (claimed vs actual connections)
   - Track Record Attribution (deals with evidence tier)
   - Portfolio Involvement (coverage metrics)
   - Strengths (verified claims)
   - Concerns (gaps, contradictions, omissions)
   - Individual Rating (conditional on follow-up)

3. **GP #2: [Name]** (same structure)

4. **Team Dynamics**
   - GP economics alignment
   - Redundancy and structural risks
   - Co-GP representation concerns
   - Overall team assessment

5. **Critical Gaps vs Normal Gaps**
   - **Critical**: Material omissions requiring validation (bulleted list)
   - **Normal**: Expected VC marketing practices (bulleted list)

6. **Recommendations**
   - High Priority (structural concerns, must validate before investment)
   - Medium Priority (attribution clarity, role verification)
   - Low Priority (nice-to-have confirmations)

---

## Key Principles

- **Evidence-based**: Only confirm claims with Tier 2+ evidence (affiliated or independent)
- **Attribution clarity**: Distinguish individual vs institutional contribution
- **Timing verification**: Flag retroactive narrative construction
- **Materiality focus**: Separate concerning gaps from normal VC marketing
- **Conditional ratings**: "Strong if verified" vs "Weak if unverified" scenarios
- **Generalizability**: Workflow applies to any GP/fund, not entity-specific

---

## Common Validation Questions

- **Credentials**: Can we confirm education, employment, deal experience via independent sources?
- **Network**: Do actual connections (LinkedIn CSVs) support claimed access?
- **Track Record**: Was the GP at the firm during claimed deals? What was their role?
- **Attribution**: Individual contribution vs team effort? How do we know?
- **Coverage**: Does each GP support their share of portfolio companies?
- **Omissions**: Why is a co-GP absent from dataroom materials despite significant economics?
- **Timing**: Did claimed expertise exist before or after the accomplishment?
- **Structural**: What happens if the primary GP is unavailable? Single point of failure?

---

## Generalization Notes

This workflow is designed to be reusable across different funds and GPs:

- **Adaptable inputs**: Works with whatever evidence is available (CSVs, LinkedIn, public records)
- **Graceful degradation**: If network CSVs don't exist, use LinkedIn profiles or public sources
- **Clear gap taxonomy**: Distinguishes "can't verify" from "contradicts claims"
- **Scalable**: Works for solo GPs, small teams, or large partnerships
- **Prioritization framework**: Helps focus limited diligence time on material concerns

The output should be concise (3-5 pages), evidence-focused, and actionable for investment decision-making.
