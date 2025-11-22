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
- `research/people/{gp-name}/network/*.csv` - LinkedIn connection exports by category

**Optional:**
- `marketing-to-reality/_data/claims.json` - Network-related claims to validate
- `marketing-to-reality/claims-analysis.md` - Context on which claims matter
- Deal flow documentation (to verify introduction sources)
- Portfolio documentation (to verify co-investor relationships)

**Note:** LinkedIn exports have variable column structures. Minimum required columns: `Name`, `Title`. Optional but helpful: `Firm`, `Location`, `Profile`.

## Outputs

### 1. JSON Data File: `marketing-to-reality/_data/network.json`

```json
{
  "metadata": {
    "analysis_date": "YYYY-MM-DD",
    "data_sources": ["harvard.csv", "vcpe.csv", "deeptech.csv"],
    "methodology_note": "Analysis based on partial LinkedIn connection captures - not complete network representation",
    "distill_cache_path": "research/people/{gp-name}/network/distill_profiles.json (if low-confidence workflow run)"
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
        "type": "tier1_vc|early_stage|growth_equity|pe|corporate_vc|lp|operator|academic|other",
        "count": 0,
        "percentage": "0%"
      }
    ],
    "by_seniority": [
      {
        "level": "partner|principal|vp|associate|founder|c_suite|director|other",
        "count": 0,
        "percentage": "0%"
      }
    ],
    "by_ecosystem": [
      {
        "ecosystem": "ai|quantum|fusion_energy|biotech|robotics_hardware|infrastructure|generalist|other",
        "count": 0,
        "percentage": "0%",
        "relevance_to_thesis": "high|medium|low"
      }
    ]
  },
  "top_firms": [
    {
      "firm": "Firm Name",
      "connections": 0,
      "firm_type": "tier1_vc|early_stage|growth_equity|pe|corporate|other",
      "key_contacts": ["Name (Title)", "..."]
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

Nunjucks/Liquid template that renders `network.json` data. Use `{{ network.field }}` syntax to reference JSON fields:

```liquid
Total: {{ network.overall_statistics.total_connections_analyzed }}

{% for firm in network.top_firms %}
- {{ firm.firm }}: {{ firm.connections }} connections
{% endfor %}

{% for gap in network.network_quality_assessment.gaps %}
### {{ gap.gap_type | replace("_", " ") | capitalize }}
{{ gap.description }}
{% endfor %}
```

## Prerequisites

**Python environment setup:**

```bash
cd {analysis-directory}
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install pandas
```

Alternatively, install system-wide (not recommended): `pip install pandas --user`

## Script Templates

Reusable Python scripts are available in `workflows/_py/`:

- **`network_analysis.py`** - Phase 1-2: CSV enrichment & statistical analysis
- **`network_validation.py`** - Phase 3-4: Strategic validation & gap analysis

**Usage:**
1. Copy scripts to your analysis directory
2. Update `GP_NAME` and paths in the configuration section at top of each script
3. Run `network_analysis.py` first, then `network_validation.py`

These templates handle NaN values, variable CSV structures, and optional claims.json gracefully.

## Methodology

### Phase 1-2: CSV Enrichment & Statistical Analysis (~5 minutes)

**Combined script that loads, enriches, and analyzes all CSV files.**

#### Step 1: Load CSV files

```python
import pandas as pd

harvard_df = pd.read_csv('research/people/{gp-name}/network/harvard.csv')
vcpe_df = pd.read_csv('research/people/{gp-name}/network/vcpe.csv')
deeptech_df = pd.read_csv('research/people/{gp-name}/network/deeptech.csv')
```

**Handle variable CSV structures:**
- If `Firm` column missing: Extract from `Title` using patterns like "@ Firm" or "at Firm"
- Handle NaN values gracefully: `pd.isna()`, `str()` conversion before `.lower()`

#### Step 2: Add enrichment columns

**Column labeling:** Mark original columns `[O]`, inferred columns `[I]` in output CSV header comments.

| Column | Type | Values |
|--------|------|--------|
| Firm_Type | [I] | tier1_vc, early_stage, growth_equity, pe_lmm, pe_large, hedge_fund, lp, operator, academic, other |
| Seniority | [I] | partner, founder, c_suite, principal, vp, associate, director, other |
| Ecosystem | [I] | quantum, fusion_energy, ai, biotech, robotics_hardware, infrastructure, generalist |
| Stage | [I] | **For VCPE:** seed, series_a, series_b, growth, pe_lmm, pe_large, hedge_fund. **For founders:** pre_seed, seed, series_a, series_b, growth, public, exited, unknown |
| Relevance | [I] | high, medium, low |
| Source_CSV | [I] | harvard, vcpe, deeptech |

**Stage classification for VCPE** - Use firm name + intrinsic knowledge of VC landscape:
- `seed`: First Round, Precursor, Hustle Fund, etc.
- `series_a`: a16z, Benchmark, Sequoia (early), etc.
- `growth`: Tiger, Coatue, D1, etc.
- `pe_lmm`: Vista, Thoma Bravo (lower-middle-market deals)
- `pe_large`: KKR, Blackstone, Apollo
- `hedge_fund`: Point72, Citadel, Two Sigma

**Stage classification for founders** - Infer from company context, funding news, or title signals.

**Ecosystem: Quantum validation** - Use comprehensive keyword search:
- Keywords: quantum, qubit, ion trap, superconducting, photonic, error correction, NISQ, fault-tolerant, topological
- **List all matches explicitly** in output with confidence note: "X titles reviewed, Y classified as quantum"

**Low-Confidence Categorization**: When title/company alone cannot determine ecosystem or category (e.g., "Founder at Stealth", generic titles) and accurate classification matters for claim validation:

1. **Identify candidates for Distill enrichment:**
   - Filter `combined_deduped.csv` for founders (`Is_Founder_I == 'yes'`)
   - Prioritize records with ambiguous titles: "Stealth", "Building something new", "Founder & CEO" without company
   - Extract LinkedIn Profile URLs (post-dedup to avoid duplicate API calls)

2. **Use Distill MCP to fetch profile summaries:**
   ```
   # Batch lookup (up to 10 profiles at once)
   mcp__distill__viewManyProfiles(urls=[
     "https://www.linkedin.com/in/profile1/",
     "https://www.linkedin.com/in/profile2/",
     ...
   ])

   # Single detailed profile (when more context needed)
   mcp__distill__viewProfile(url="https://www.linkedin.com/in/profile/")
   ```

3. **Save deeptech-focused classifications to `distill_profiles.json`:**
   ```json
   {
     "metadata": {
       "created_at": "YYYY-MM-DD",
       "source": "Distill MCP viewManyProfiles",
       "description": "Deeptech categorization for network connections"
     },
     "profiles": {
       "https://www.linkedin.com/in/profile1/": {
         "name": "Person Name",
         "ecosystem": "quantum|fusion_energy|nuclear|ai|biotech|robotics_hardware|semiconductors|space|climate_tech|defense|generalist_vc|not_deeptech",
         "deeptech_relevance": "high|medium|low|none",
         "sector_specifics": "ion-trap computing|ML infrastructure|solid-state batteries|etc.",
         "role_type": "founder|investor|operator|academic",
         "deeptech_companies": ["Company1", "Company2"],
         "investor_focus": ["quantum", "ai"]
       }
     }
   }
   ```

   **Field definitions:**
   - `ecosystem`: Primary deeptech sector classification
   - `deeptech_relevance`: How central is deeptech to their work (high=core focus, low=tangential, none=not deeptech)
   - `sector_specifics`: Granular sub-classification (e.g., "superconducting qubits", "nuclear fusion", "LLM infrastructure")
   - `role_type`: founder/investor/operator/academic
   - `deeptech_companies`: List of relevant deeptech companies they're associated with
   - `investor_focus`: For VCs—which deeptech sectors they invest in (null for non-investors)

4. **Add `_D` columns to `combined_deduped.csv`:**
   - `Ecosystem_D`: Primary deeptech sector from Distill analysis
   - `Relevance_D`: Deeptech relevance level (high/medium/low/none)
   - `Sector_D`: Specific sub-sector classification
   - `Role_D`: Role type (founder/investor/operator/academic)

   Use `workflows/_py/add_distill_columns.py` to programmatically merge profiles:
   ```bash
   python add_distill_columns.py /path/to/network
   ```

5. **Re-categorize based on enriched data:**
   - Update `Ecosystem_I` if `Ecosystem_D` provides better classification
   - Flag discrepancies between `_I` and `_D` columns for review

**Distill MCP Best Practices:**
- Use `viewManyProfiles` for batches (max 10 URLs per call) - more efficient
- Use `viewProfile` with `performResearch=true` for deep dives (takes ~60 seconds)
- Cache all responses to `distill_profiles.json` to avoid duplicate API calls
- Match profiles by LinkedIn URL (normalize with/without trailing slash)

Flag categories with >20% unclassifiable records as "low confidence" in output.

#### Step 3: Calculate statistics

Aggregate:
- Total connections per category
- Distribution by firm_type, seniority, ecosystem (counts + percentages)
- Top 20-30 firms by connection count (dedupe `key_contacts`—no name should appear twice per firm)
- Group by firm, rank by relevance

#### Step 4: Deduplicate and save enriched data

```python
# Combine all dataframes with source tracking
harvard_df['Source_CSV'] = 'harvard'
vcpe_df['Source_CSV'] = 'vcpe'
deeptech_df['Source_CSV'] = 'deeptech'
all_df = pd.concat([harvard_df, vcpe_df, deeptech_df], ignore_index=True)

# Deduplicate by Profile URL (keep first occurrence, preserve Source_CSV)
deduped_df = all_df.drop_duplicates(subset=['Profile'], keep='first')

# Save deduplicated CSV (primary analysis file)
deduped_df.to_csv('research/people/{gp-name}/network/combined_deduped.csv', index=False)
```

**Output files:**
- `combined_deduped.csv` = primary analysis file (deduplicated, includes distill enrichment `_D` columns if low-confidence workflow run)
- `distill_profiles.json` = full distill responses cached by LinkedIn URL (if low-confidence workflow run)

**Quality check (Items 1-4):**
- [ ] All CSV files loaded and enriched with characterization columns
- [ ] Overall statistics calculated (total connections, category breakdown)
- [ ] Top 20-30 firms identified by connection count
- [ ] Network composition analyzed (firm_type, seniority, ecosystem distributions)

---

### Phase 3: Strategic Relationship Validation (~5-10 minutes)

**Map claims to connection evidence (optional if no claims.json).**

**Scope requirement:** Comprehensively validate ALL entities where a relationship is explicitly claimed in the dataroom/claims.json. Do not cherry-pick examples—include every firm, person, or organization mentioned as a relationship.

**Section boundary:** `strategic_relationships` is for claim validation only. `top_firms` shows raw connection data ranked by count. If a firm appears in both, `top_firms` shows quantitative data (count, firm type, contacts); `strategic_relationships` assesses whether claimed relationship depth is supported by evidence. Avoid duplicating the same names/details across sections.

#### Approach A: With claims.json

1. **Extract ALL network claims** from `claims.json` and dataroom materials:
   - Central hub partners (claimed VC partnerships, referral relationships)
   - Deal sources (claimed introductions to portfolio companies)
   - Co-investors, mentors, high-value connections
   - Any other explicitly claimed relationships

2. **For each claimed relationship:**
   - Search enriched CSV for connections at that firm/person
   - Count total connections (e.g., "8 connections at Sequoia")
   - Identify key contacts—apply firm-type-aware seniority (see Principle 6)
   - Assess claim strength vs evidence

3. **Categorize verification status:**
   - ✅ **Verified**: Multiple senior connections support claimed depth
   - ⚠️ **Partial**: Some connections but fewer/junior than claimed
   - ❓ **Unverified**: No connections (doesn't prove no relationship)
   - ❌ **Conflicting**: Evidence contradicts claim

4. **Deduplicate:** Ensure no name appears twice within `connection_details` or `key_contacts` arrays.

#### Approach B: Without claims.json

1. List key firms/relationships mentioned in marketing materials
2. For each: count connections, assess seniority (firm-type-aware), note verification needs
3. Skip claim_id references, focus on top firm analysis

**Output:** Populate `strategic_relationships` in JSON

**Quality check (Items 5-6):**
- [ ] Network claims mapped to connection evidence (if claims.json exists)
- [ ] Strategic relationships categorized by verification status

---

### Phase 4: Network Quality Assessment & Gap Identification (~10-15 minutes)

**Assess network and identify critical gaps.**

#### Step 1: Assess across dimensions

1. **Breadth**: Network size and category diversity
2. **Depth**: Quality of key relationships (partner-level vs junior)
3. **Relevance**: Alignment between network composition and fund thesis
4. **Recency**: When relationships formed (if data available)

#### Step 2: Identify gaps

Common gap types:
- **Shallow key relationships**: Claimed "close" with 0-2 connections
- **Network mismatch**: Composition doesn't match positioning (e.g., generalist network for deeptech fund)
- **Missing ecosystems**: Fund focuses on X but 0 connections in X
- **LP network underdeveloped**: Few LP connections despite fundraising
- **Founder network unverifiable**: Claimed referral network lacks evidence

#### Step 3: Risk severity classification

- 🚩 **Red Flag**: Material gap undermining core strategy
- 🟡 **Yellow Flag**: Moderate concern, possible overstated claims
- **Minor**: Expected gap or limited significance

#### Step 4: Verification priorities

Rank relationships by:
- **Critical**: Core to fund thesis, material if disproven
- **High**: Important but not make-or-break
- **Medium/Low**: Nice to verify but not urgent

**Output:** Populate `network_quality_assessment` and `verification_priorities` in JSON

**Quality check (Items 7-11):**
- [ ] Network quality assessed across breadth, depth, relevance
- [ ] Critical gaps identified with risk severity classification
- [ ] Verification priorities established with clear rationale
- [ ] Methodology limitations stated (partial capture, LinkedIn-only)
- [ ] JSON validates and markdown template renders correctly
- [ ] Specific people mentioned in claims-analysis.md searched

---

## Workflow Flexibility

**Minimum viable:** Phases 1-2 only (enrichment + stats) - for pure network research

**Standard:** Phases 1-3 (add strategic validation) - when claims exist to verify

**Comprehensive:** All phases including gap analysis - for due diligence context

Skip Phase 3 if no claims to validate. Skip Phase 4 if no due diligence required.

## Key Principles

1. **Evidence-Based Assessment**: Connection count is ONE signal, not proof. No connection ≠ no relationship. Focus on patterns, not individual data points.

2. **Connection Retention is Passive**: LinkedIn connections persist indefinitely—people rarely delete connections even when relationships lapse. Connection count shows *historical* touchpoints, not *active* relationships. Do not cite "maintained X connections post-departure" as evidence of ongoing relationship quality.

3. **Methodology Transparency**: This is "partial connection capture" - not complete network inventory. Frame as "evidence of relationships" not "complete census."

4. **Claim-Agnostic Design**: Workflow works with or without claims.json. Reference claim IDs when available.

5. **Graceful Degradation**: Analyze what's available. Note limitations if data incomplete.

6. **Privacy-Conscious**: Aggregate patterns, limit individual names (except key contacts at top firms).

7. **Firm-Type-Aware Seniority**: Title hierarchies vary by firm type. For VCs: only "General Partner (GP)", "Managing Partner", "Managing Director" are definitively senior—"Partner", "Investing Partner", "Investment Partner" may be junior at tier-1 VCs. For PE: "VP", "Associate", "Senior Associate" are junior; "Principal", "Director", "MD", "Partner" are senior. When uncertain, classify conservatively as junior.

8. **Context-Aware Interpretation**:
   - Institutional relationships vs personal connections
   - Timing: When formed vs when used
   - Direction: Who introduced whom (if knowable)

9. **Integration**: Complements claims-analysis and people-analysis. Cross-reference claim IDs. Don't duplicate credential verification.

## Network Facets Framework

Each CSV = one network facet. Analyze separately, then combine into `combined_deduped.csv`.

| CSV | Facet | Key Breakdowns | Claim Validation |
|-----|-------|----------------|------------------|
| harvard.csv | Alumni network | Category_I: founder/investor/operator | Prod founders search |
| vcpe.csv | VC/PE relationships | Seniority_I, Investment_Stage_I | Partnership depth, tier-1 |
| deeptech.csv | Technical ecosystem | Ecosystem_I, Quantum_Confidence_I | Quantum validation |
| **combined_deduped.csv** | **Aggregate stats** | Deduplicated by Profile URL | Top firms, total counts |

**Key principle:** Use `combined_deduped.csv` for ALL aggregate stats (top firms, totals). Use individual CSVs only for facet-specific claim validation.

**Output structure:**
- Section 1: Facet Drilldowns (per-CSV, no aggregate stats)
- Section 2: Deduplicated Overview (from combined_deduped.csv only)
- Section 3+: Strategic validation, key findings

## Quality Checklist

- [ ] CSVs enriched with `_I` columns (Seniority_I, Category_I, Ecosystem_I, etc.)
- [ ] Deduplicated by Profile URL → `combined_deduped.csv`
- [ ] Top firms calculated from deduped data (unique people per firm)
- [ ] Schools filtered from top_firms
- [ ] Facet sections link to rendered CSV view (not raw .csv)
- [ ] No duplicate stats between facet sections and overview
