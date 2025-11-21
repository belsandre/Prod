# Analyze Network Workflow

## Purpose

Systematically assess the quality and relevance of a GP's professional network by analyzing LinkedIn connection data, validating claimed relationships, and identifying gaps between marketing narratives and actual network evidence.

**Key Questions:**
- How broad is the network across relevant categories?
- How deep are claimed strategic relationships?
- Does network composition align with fund thesis?
- What critical connections or ecosystems are missing?
- Which claimed relationships require verification?

## Inputs

**Required:**
- `research/people/[name]/network/*.csv` - LinkedIn connection exports by category
- `marketing-to-reality/_data/claims.json` - Network-related claims to validate
- `marketing-to-reality/claims-analysis.md` - Context on which claims matter

**Optional:**
- Deal flow documentation (to verify introduction sources)
- Portfolio documentation (to verify co-investor relationships)

## Outputs

### 1. JSON Data File: `marketing-to-reality/_data/network.json`

```json
{
  "metadata": {
    "analysis_date": "YYYY-MM-DD",
    "data_sources": ["harvard.csv", "vcpe.csv", "deeptech.csv"],
    "methodology_note": "Analysis based on partial LinkedIn connection captures - not complete network representation"
  },
  "overall_statistics": {
    "total_connections_analyzed": 0,
    "categories": {
      "harvard": 0,
      "vcpe": 0,
      "deeptech": 0
    }
  },
  "network_composition": {
    "by_firm_type": [
      {
        "type": "tier1_vc|early_stage|growth_equity|pe|corporate_vc|lp|other",
        "count": 0,
        "percentage": "0%",
        "top_firms": ["Firm Name (X connections)", "..."]
      }
    ],
    "by_seniority": [
      {
        "level": "partner|principal|vp|associate|founder|operator",
        "count": 0,
        "percentage": "0%"
      }
    ],
    "by_ecosystem": [
      {
        "ecosystem": "AI|quantum|fusion|biotech|robotics|infrastructure|other",
        "count": 0,
        "percentage": "0%",
        "relevance_to_thesis": "High|Medium|Low"
      }
    ]
  },
  "top_firms": [
    {
      "firm": "Firm Name",
      "connections": 0,
      "firm_type": "tier1_vc|early_stage|growth_equity|pe",
      "key_contacts": ["Name (Title)", "..."],
      "significance": "Description of why this firm matters",
      "claim_references": ["CLAIM_ID_1", "CLAIM_ID_2"]
    }
  ],
  "strategic_relationships": {
    "central_hub_partners": [
      {
        "entity": "Firm/Person Name",
        "claimed_relationship": "Quote from claims",
        "claim_id": "CLAIM_ID",
        "connection_count": 0,
        "connection_details": ["Name (Title)", "..."],
        "assessment": "Strong|Moderate|Weak|Unverified",
        "verification_status": "verified|partial|unverified|conflicting",
        "notes": "Context and significance"
      }
    ],
    "deal_sources": [],
    "co_investors": [],
    "mentors": [],
    "high_value_connections": []
  },
  "network_quality_assessment": {
    "strengths": [
      {
        "dimension": "breadth|depth|relevance|prestige",
        "description": "Specific strength observed",
        "evidence": "Supporting data",
        "significance": "Why this matters"
      }
    ],
    "gaps": [
      {
        "gap_type": "shallow_key_relationship|network_mismatch|missing_ecosystem|lp_network_underdeveloped|founder_network_unverifiable",
        "description": "Specific gap identified",
        "claim_reference": "CLAIM_ID or null",
        "evidence": "What the data shows",
        "significance": "Impact on fund strategy/credibility",
        "risk_severity": "red_flag|yellow_flag|minor"
      }
    ]
  },
  "verification_priorities": [
    {
      "entity": "Firm/Person Name",
      "relationship_claimed": "Description",
      "claim_id": "CLAIM_ID",
      "current_evidence": "X connections in category Y",
      "priority": "critical|high|medium|low",
      "verification_approach": "Suggested next steps",
      "rationale": "Why this verification matters"
    }
  ]
}
```

### 2. Markdown Template: `marketing-to-reality/network-analysis.md`

Pure Nunjucks/Liquid template that renders `network.json` data. No substantive content in markdown.

## Methodology

### Phase 1: CSV Enrichment & Preparation

**For each network CSV file:**

1. **Load and inspect** the CSV structure (columns vary by file)
2. **Add characterization columns** to enable analysis:
   - `Firm_Type`: Categorize as tier1_vc, early_stage, growth_equity, pe, corporate_vc, lp, operator, academic, other
   - `Seniority`: Extract from title (partner, principal, vp, associate, founder, ceo, etc)
   - `Ecosystem`: Identify technical domain (AI, quantum, fusion, biotech, robotics, infrastructure, generalist, other)
   - `Relevance`: Rate relevance to fund thesis (high, medium, low) based on firm type + ecosystem + seniority

3. **Firm extraction**: If no explicit Firm column, extract from Title field (e.g., "Partner at Sequoia" → "Sequoia")

4. **Save enriched CSVs** for further analysis (optional, for reference)

**Key Principles for Enrichment:**
- Use Title and LinkedIn profile context to infer missing data
- Be conservative with categorization (use "other" when uncertain)
- Focus on VC/PE relevant categorizations
- Flag ambiguous cases in notes

### Phase 2: Quantitative Network Analysis

**Aggregate statistics:**

1. **Overall counts**: Total connections per category (harvard, vcpe, deeptech, etc)
2. **Firm aggregation**: Group by firm, count connections per firm, rank by connection count
3. **Composition analysis**:
   - Distribution by firm_type (how many tier1_vc vs growth_equity vs PE?)
   - Distribution by seniority (partner-level vs associate-level network?)
   - Distribution by ecosystem (AI-heavy vs quantum vs fusion vs generalist?)

4. **Top firms analysis**: Identify top 20-30 firms by connection count, assess relevance to fund thesis

**Output**: Populate `overall_statistics`, `network_composition`, `top_firms` in JSON

### Phase 3: Strategic Relationship Validation

**Map claims to connection evidence:**

1. **Extract network claims** from `claims.json`:
   - Central hub partners (claimed filtering/referral relationships)
   - Deal sources (claimed introductions to portfolio companies)
   - Co-investors (claimed co-investment relationships)
   - Mentors (claimed guidance relationships)
   - High-value connections (unicorn founders, notable investors)

2. **For each claimed relationship:**
   - Search network CSVs for connections at that firm/person
   - Count total connections (e.g., "8 connections at Sequoia")
   - Identify key contacts (partners vs associates)
   - Assess claim strength: Does "close relationship with Sequoia" align with 1 associate connection? Or 5 partner connections?

3. **Categorize verification status:**
   - ✅ **Verified**: Multiple senior connections support claimed relationship depth
   - ⚠️ **Partial**: Some connections exist but fewer/more junior than claim suggests
   - ❓ **Unverified**: No connections found (doesn't prove no relationship - partial capture limitation)
   - ❌ **Conflicting**: Connection evidence contradicts claim (e.g., "close" but 0 connections)

**Output**: Populate `strategic_relationships` in JSON

### Phase 4: Network Quality Assessment & Gap Identification

**Assess network across key dimensions:**

1. **Breadth**: Overall network size and category diversity
2. **Depth**: Quality of key relationships (partner-level vs junior connections)
3. **Relevance**: Alignment between network composition and fund thesis
4. **Recency**: When did key relationships form? (if data available)

**Identify critical gaps:**

1. **Shallow key relationships**: Claimed "close relationship" with 0-2 connections
2. **Network mismatch**: Network composition doesn't match fund positioning (e.g., growth equity network for early-stage deeptech fund)
3. **Missing ecosystems**: Fund focuses on quantum but 0 quantum scientist connections
4. **LP network underdeveloped**: Few connections at LP firms despite fundraising claims
5. **Founder network unverifiable**: Claimed founder referral network lacks connection evidence

**Risk severity classification:**
- 🚩 **Red Flag**: Material gap that undermines core fund strategy (e.g., no deeptech network for deeptech fund)
- 🟡 **Yellow Flag**: Moderate concern that may indicate overstated claims (e.g., "close" relationship with 1 junior connection)
- **Minor**: Expected gap or limited significance

**Identify verification priorities:**
- Which claimed relationships are most critical to validate?
- What verification approach would be most productive? (reference checks, portfolio company interviews, etc)

**Output**: Populate `network_quality_assessment` and `verification_priorities` in JSON

## Key Principles

1. **Evidence-Based Assessment**: Connection count is ONE signal, not definitive proof. No connection ≠ no relationship (LinkedIn usage varies). Focus on patterns, not individual data points.

2. **Methodology Transparency**: State clearly this is "partial connection capture" - not complete network inventory. Frame as "evidence of relationships" not "complete relationship census."

3. **Claim-Agnostic Design**: Reference claim IDs from claims.json, not hardcoded claims. Workflow works for any GP/fund.

4. **Graceful Degradation**: If certain network CSVs don't exist, analyze what's available. If claim validation data is incomplete, note limitations.

5. **Privacy-Conscious**: Aggregate patterns, don't expose individual connection names in final report (except key contacts at top firms). Focus on firm-level insights.

6. **Context-Aware Interpretation**:
   - Institutional relationships (ex-colleagues) vs personal (alumni, co-investors)
   - Timing matters: When formed vs when used
   - Direction matters: Who introduced whom?

7. **Integration with Other Workflows**: Network analysis complements claims-analysis and people-analysis. Cross-reference claim IDs. Don't duplicate credential verification (that's in analyze-people).

## Quality Checklist

**Before completing analysis:**

- [ ] All network CSV files processed and enriched with characterization columns
- [ ] Overall statistics calculated (total connections, category breakdown)
- [ ] Top 20-30 firms identified and assessed for relevance
- [ ] Network composition analyzed (firm_type, seniority, ecosystem distributions)
- [ ] All network claims from claims.json mapped to connection evidence
- [ ] Strategic relationships categorized by verification status
- [ ] Network quality assessed across breadth, depth, relevance dimensions
- [ ] Critical gaps identified with risk severity classification
- [ ] Verification priorities established with clear rationale
- [ ] Methodology limitations clearly stated (partial capture, LinkedIn-only)
- [ ] JSON validates and markdown template renders correctly
- [ ] Specific people mentioned in claims-analysis.md searched in network data

## Example Use Case: Hyperion Fund (Dillon Chen)

**Inputs:**
- `research/people/dillon-chen/network/harvard.csv` (604 connections)
- `research/people/dillon-chen/network/vcpe.csv` (638 connections)
- `research/people/dillon-chen/network/deeptech.csv` (if exists)
- `marketing-to-reality/_data/claims.json` (network claims)

**Key Questions to Answer:**
1. **Deeptech network depth**: How many connections in quantum/fusion/advanced computing? What seniority? Any scientists/technical founders?
2. **Harvard network strength**: 604 connections - but what's the composition? Investors, operators, academics? How many in relevant sectors?
3. **VCPE network quality**: 638 connections - but tier1_vc vs growth equity vs PE? Partner-level vs associate-level?
4. **Claimed relationships**: Search for specific people mentioned in claims-analysis.md (e.g., Mike Annunziata @ Also Capital, Tamarack team, Founders Fund contacts, Coatue partners)

**Process:**
1. Enrich CSVs with Firm_Type, Seniority, Ecosystem, Relevance columns
2. Aggregate: "X deeptech founders, Y tier1_vc partners, Z quantum specialists"
3. Validate claimed relationships: "Mike Annunziata (Also Capital)" - how many Also Capital connections? What titles?
4. Identify gaps: "Claims 'deep quantum network' but 0 quantum physicist connections" (red flag)
5. Output to `marketing-to-reality/_data/network.json` + template

**Expected Insights:**
- Network composition match/mismatch with "early-stage deeptech" positioning
- Depth of claimed strategic relationships (Sequoia, Coatue, Founders Fund, etc)
- Harvard network relevance (investors vs operators vs academics)
- Critical missing ecosystems (quantum, fusion specialists if fund claims focus)
- Verification priorities (which relationships most critical to confirm)
