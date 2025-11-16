# LinkedIn Industry Analysis Workflow

## Purpose
Analyze a target entity's (fund, GP, company) main industry focus areas from dataroom materials and map them to LinkedIn industry codes, producing two categorized lists: **Most Relevant** (direct matches) and **Potentially Relevant** (adjacent/related) industry codes for LinkedIn targeting and network analysis.

## When to Use This Workflow
- **LinkedIn Profile Optimization**: Identifying appropriate industry tags for GP or fund profiles
- **Network Targeting**: Finding relevant industry segments for connection outreach
- **Competitive Intelligence**: Understanding which LinkedIn industries contain competitors or peers
- **Portfolio Analysis**: Mapping portfolio company sectors to LinkedIn's taxonomy
- **Signal Detection**: Identifying which industries to monitor for deal flow signals

## Output Location
`users/tam/{target-name}/outputs/linkedin-industry-analysis.md`

## Workflow Information
- **Version**: 1.0
- **Maintainer**: tam
- **Estimated Time**: 1-2 hours
- **Resumability**: Not required (single-pass analysis)

---

## Prerequisites

### Required Materials
- **Dataroom Location**: Path to target's dataroom (e.g., `users/tam/hyperion/dataroom/`)
- **Industry Codes Reference**: `users/tam/workflows/linkedin-industry-codes.csv` (488 industry codes)

### Recommended Dataroom Contents
- Investment thesis documents (e.g., "Deeptech perspectives.md")
- Portfolio summaries or company lists
- Sourcing/network maps
- GP biographies (for expertise areas)
- Case studies or investment memos

### Skills/Tools Used
- Read tool (for accessing dataroom files and CSV)
- Grep tool (for searching industry codes)
- Text analysis (extracting investment themes)

### Expected Timeline
- Phase 0 (Setup): 5 minutes
- Phase 1 (Extract Investment Thesis): 20-30 minutes
- Phase 2 (Map to Industry Codes): 30-45 minutes
- Phase 3 (Generate Output): 15-20 minutes

---

## Phase 0: Setup and Validation

### Step 1: Identify Dataroom Location
- [ ] Confirm dataroom path (e.g., `users/tam/{target-name}/dataroom/`)
- [ ] Verify dataroom contains sufficient materials for analysis
- [ ] Note target entity type: Fund, GP, Company, or Other

### Step 2: Load Industry Codes Reference
- [ ] Read `users/tam/workflows/linkedin-industry-codes.csv`
- [ ] Verify CSV structure: `status, industry_id, label, hierarchy, description`
- [ ] Filter to Active codes only (ignore Inactive)
- [ ] Total active codes: ~470+

### Step 3: Create Output Directory
- [ ] Ensure output directory exists: `users/tam/{target-name}/outputs/`
- [ ] Prepare output file path: `linkedin-industry-analysis.md`

**Checkpoint**: You have dataroom location, loaded industry codes, and output path ready.

---

## Phase 1: Extract Investment Thesis & Focus Areas

### Objective
Systematically analyze dataroom materials to identify all industry focus areas, technology domains, and sector themes that define the target's investment/business strategy.

### Step 1: Identify Core Thesis Documents
Read the following files from the dataroom (if available):

- [ ] **Investment Thesis**: Files like "Investment Thesis.md", "Deeptech perspectives.md", "Strategy.md"
- [ ] **Portfolio Summary**: "Portfolio Summary.xlsx", "Portfolio Companies.md", "Company List.md"
- [ ] **Sourcing/Network Maps**: "Sourcing Differentiation.md", "Network Map.md"
- [ ] **GP/Team Bios**: "GP Bio.md", "Team.md" (for expertise areas)
- [ ] **Case Studies**: "Case Studies.md", investment memos, company research summaries

### Step 2: Extract Investment Focus Areas
For each document, identify and record:

**Technology Domains**:
- Core technologies (e.g., "AI", "Robotics", "Quantum Computing", "Fusion Energy")
- Application areas (e.g., "Cybersecurity", "Manufacturing Automation", "Renewable Energy")
- Enabling technologies (e.g., "Semiconductors", "Advanced Materials", "Software Infrastructure")

**Industry Sectors**:
- Vertical markets (e.g., "Defense", "Energy & Utilities", "Healthcare", "Financial Services")
- Horizontal categories (e.g., "SaaS", "Hardware", "Infrastructure", "Services")

**Portfolio Company Analysis** (if applicable):
- List all portfolio companies mentioned
- Note each company's primary industry/technology focus
- Identify clustering patterns (multiple companies in same domain = strong signal)

### Step 3: Categorize Focus Areas by Strength
Classify each identified focus area:

**Tier 1 - Core Focus** (Most Relevant):
- [ ] Explicitly stated in investment thesis
- [ ] Multiple portfolio companies in this area (3+)
- [ ] GP has stated expertise/background in this domain
- [ ] Featured in case studies or key materials

**Tier 2 - Secondary Focus** (Potentially Relevant):
- [ ] Mentioned in materials but not core thesis
- [ ] 1-2 portfolio companies in this area
- [ ] Adjacent to core focus areas
- [ ] Emerging interest or exploratory investments

**Tier 3 - Tangential** (Context Only):
- [ ] Related to portfolio companies' customer industries
- [ ] Supply chain or enabling technologies
- [ ] Mentioned once or in passing

### Step 4: Document Evidence
For each focus area, record:

```
**Focus Area**: [Name, e.g., "Fusion Energy"]
- **Evidence**: [Quote or summary from source document]
- **Source**: [Document name and section]
- **Strength**: [Tier 1/2/3]
- **Portfolio Examples**: [Company names, if applicable]
```

**Checkpoint**: You have a comprehensive list of all investment focus areas with source citations and strength classification.

---

## Phase 2: Map to LinkedIn Industry Codes

### Objective
Match each investment focus area to specific LinkedIn industry codes, creating two tiers: Most Relevant (direct matches) and Potentially Relevant (adjacent industries).

### Step 1: Search Industry Codes for Direct Matches

For each **Tier 1 (Core Focus)** area from Phase 1:

1. **Search by Label**: Grep `linkedin-industry-codes.csv` for keywords from the focus area
   - Example: Focus area "Robotics" → search for "robot", "robotics", "automation"

2. **Review Matches**: For each matching industry code, record:
   - `industry_id`: Numeric ID
   - `label`: Industry name
   - `hierarchy`: Full category path
   - `description`: What entities in this industry do

3. **Validate Relevance**: Does this code directly describe:
   - [ ] What the target invests in?
   - [ ] What portfolio companies do?
   - [ ] What the GP's expertise area is?

4. **Classify as Most Relevant** if:
   - Direct match to core investment thesis
   - Multiple portfolio companies would tag themselves with this industry
   - GP would use this tag on their own profile

**Example Mapping**:
```
**Focus Area**: Fusion Energy (Tier 1)
**Matched Codes**:
- Nuclear Electric Power Generation (386)
  - Hierarchy: Manufacturing > Utilities > Electric Power Generation > Nuclear Electric Power Generation
  - Rationale: Portfolio companies Zap Energy, Hephaestus, Avalanche, Marathon Fusion are developing fusion reactors for power generation
  - Source: Deeptech perspectives.md, "Fusion Energy" section

- Renewable Energy Power Generation (3240)
  - Hierarchy: Manufacturing > Utilities > Electric Power Generation > Renewable Energy Power Generation
  - Rationale: Fusion is a form of clean/renewable energy; adjacent to renewable energy sector
  - Source: Deeptech perspectives.md
```

### Step 2: Identify Adjacent/Related Codes (Potentially Relevant)

For each **Tier 1** focus area, also identify:

**Upstream Industries** (suppliers, enablers):
- Technologies that portfolio companies depend on
- Example: If focus is "Robotics", upstream = "Semiconductor Manufacturing", "Sensor Manufacturing"

**Downstream Industries** (customers, applications):
- Industries that use the target's portfolio technologies
- Example: If focus is "AI Cybersecurity", downstream = "Computer and Network Security", "IT Services and IT Consulting"

**Adjacent Technologies**:
- Related but not identical technology domains
- Example: If focus is "Quantum Computing", adjacent = "Semiconductor Manufacturing", "Computer Hardware Manufacturing"

**Broader Categories**:
- Higher-level industry groupings in the hierarchy
- Example: "Technology, Information and Media" as parent for multiple tech subcategories

### Step 3: Map Tier 2 (Secondary Focus) Areas

For **Tier 2 (Secondary Focus)** areas from Phase 1:
- Follow same process as Step 1
- Most Tier 2 focus areas → **Potentially Relevant** industry codes
- Only promote to **Most Relevant** if there's very strong evidence

### Step 4: Review and Deduplicate

- [ ] Ensure no duplicate industry codes across lists
- [ ] Verify "Most Relevant" list is focused (10-20 codes max)
- [ ] Verify "Potentially Relevant" list captures adjacencies (15-30 codes)
- [ ] Check that every code has clear rationale and source citation

### Step 5: Quality Checks

**Most Relevant Codes** must meet ALL criteria:
- [ ] Direct match to Tier 1 investment focus area
- [ ] Supported by dataroom evidence (thesis docs, portfolio companies)
- [ ] Would be appropriate for GP or fund profile
- [ ] Active status in LinkedIn (not Inactive)

**Potentially Relevant Codes** must meet ONE OR MORE criteria:
- [ ] Match to Tier 2 investment focus area
- [ ] Adjacent/related to Tier 1 focus (upstream, downstream, related tech)
- [ ] Relevant for network targeting but not core identity
- [ ] Customer or supplier industries

**Checkpoint**: You have two categorized lists of industry codes with rationale and source citations.

---

## Phase 3: Generate Output

### Objective
Create structured markdown output with fund focus summary, tiered industry codes, and methodology documentation.

### Output Template

```markdown
# LinkedIn Industry Analysis: [Target Name]

**Analysis Date**: [YYYY-MM-DD]
**Dataroom Location**: `users/tam/{target-name}/dataroom/`
**Analyst**: Claude Code (Workflow: linkedin-industry-analysis v1.0)

---

## Executive Summary

[2-3 paragraph summary of target's investment focus and industry positioning]

**Primary Investment Themes**:
- [Theme 1]: [Brief description]
- [Theme 2]: [Brief description]
- [Theme 3]: [Brief description]

**Portfolio Composition**: [Number] companies across [X] core technology domains
**GP Expertise**: [Key areas from bio/background]

---

## Investment Focus Analysis

### Core Investment Thesis
[Detailed summary extracted from thesis documents with source citations]

**Source**: [Document name, section]

### Portfolio Technology Breakdown
[Table or list of portfolio companies grouped by technology/sector]

| Technology Domain | Portfolio Companies | Count |
|-------------------|---------------------|-------|
| [Domain 1] | [Company A, Company B, ...] | X |
| [Domain 2] | [Company C, Company D, ...] | Y |

**Source**: [Portfolio summary document, network map, etc.]

---

## Most Relevant Industry Codes (Tier 1)

*Direct matches to core investment focus. Appropriate for GP/fund LinkedIn profiles.*

### 1. [Industry Label] (ID: [industry_id])
- **Hierarchy**: [Full hierarchy path]
- **Status**: Active
- **Rationale**: [Why this code directly matches the target's core focus]
- **Portfolio Evidence**: [Which portfolio companies operate in this industry]
- **Use Case**: [How this code would be used - profile tag, network search, etc.]
- **Source**: [Dataroom document citations]

### 2. [Industry Label] (ID: [industry_id])
[Repeat structure for each Most Relevant code]

[Continue for 10-20 codes]

---

## Potentially Relevant Industry Codes (Tier 2)

*Adjacent, related, or customer/supplier industries. Useful for network targeting and ecosystem mapping.*

### 1. [Industry Label] (ID: [industry_id])
- **Hierarchy**: [Full hierarchy path]
- **Status**: Active
- **Relationship to Core Focus**: [Upstream/Downstream/Adjacent/Customer Industry]
- **Rationale**: [Why this code is potentially relevant]
- **Use Case**: [Network targeting, ecosystem analysis, etc.]
- **Source**: [Dataroom document citations or logical inference]

### 2. [Industry Label] (ID: [industry_id])
[Repeat structure for each Potentially Relevant code]

[Continue for 15-30 codes]

---

## Methodology & Data Sources

### Analysis Approach
1. **Phase 1**: Extracted investment focus areas from dataroom materials
2. **Phase 2**: Mapped focus areas to LinkedIn industry codes using keyword matching and domain expertise
3. **Phase 3**: Classified codes into Tier 1 (Most Relevant) and Tier 2 (Potentially Relevant) based on evidence strength

### Dataroom Sources Analyzed
- [Document 1]: [Brief description of what was extracted]
- [Document 2]: [Brief description]
- [Document 3]: [Brief description]

### Industry Code Reference
- **Source**: `users/tam/workflows/linkedin-industry-codes.csv`
- **Total Active Codes**: [Number]
- **Codes Identified**: [Number in Tier 1] Most Relevant + [Number in Tier 2] Potentially Relevant

### Classification Criteria

**Most Relevant (Tier 1)**:
- Direct match to stated investment thesis
- Supported by multiple portfolio company examples (3+)
- GP has expertise/background in this domain
- Appropriate for fund or GP LinkedIn profile

**Potentially Relevant (Tier 2)**:
- Adjacent or related to core focus areas
- Customer or supplier industries for portfolio companies
- Secondary investment areas (1-2 portfolio companies)
- Useful for network targeting but not core identity

---

## Appendices

### Appendix B: Industry Clusters
[Optional: Group related codes by technology theme or sector]

**Cluster 1: [Theme Name]**
- [Industry 1]
- [Industry 2]
- [Industry 3]

---

## Quality Checklist

- [ ] All Most Relevant codes have strong dataroom evidence
- [ ] All industry codes are Active status (not Inactive)
- [ ] No duplicate codes across Tier 1 and Tier 2
- [ ] Source citations provided for all classifications
- [ ] Most Relevant list is focused (10-20 codes)
- [ ] Potentially Relevant list captures ecosystem (15-30 codes)
- [ ] Rationale is clear and evidence-based for each code
- [ ] Output is ready for LinkedIn targeting decisions

---

**Analysis Complete**: [Timestamp]
```

### Step 1: Fill Output Template
Using your research from Phase 1 and 2:

1. **Executive Summary**: Synthesize 2-3 paragraph overview of target's focus
2. **Investment Focus Analysis**: Detailed thesis and portfolio breakdown with sources
3. **Most Relevant Industry Codes**: List all Tier 1 codes with full details
4. **Potentially Relevant Industry Codes**: List all Tier 2 codes with full details
5. **Methodology**: Document your process and sources

### Step 2: Validate Output Quality
Check that output meets quality standards:

- [ ] **Source Attribution**: Every industry code selection cites specific dataroom document
- [ ] **Evidence-Based**: No speculation; all classifications supported by data
- [ ] **Completeness**: All major investment themes have corresponding industry codes
- [ ] **Actionability**: Clear distinction between Tier 1 (profile tags) and Tier 2 (network targeting)
- [ ] **Accuracy**: Industry code IDs, labels, and hierarchies match CSV exactly

### Step 3: Save Output
- [ ] Save completed analysis to `users/tam/{target-name}/outputs/linkedin-industry-analysis.md`
- [ ] Verify file is readable and properly formatted
- [ ] Optional: Export CSV of industry codes for filtering/import

**Checkpoint**: Analysis complete, output saved, ready for LinkedIn targeting decisions.

---

## Success Criteria

An analysis meets success criteria when:

1. **Comprehensive Coverage**: All major investment thesis areas have corresponding LinkedIn industry codes
2. **Clear Tiering**: Distinction between Most Relevant (10-20 codes) and Potentially Relevant (15-30 codes) is evidence-based
3. **Strong Attribution**: Every industry code selection has clear rationale with dataroom source citation
4. **LinkedIn-Ready**: Output can be immediately used for:
   - Profile optimization (Tier 1 codes)
   - Network targeting searches (Tier 2 codes)
   - Competitive intelligence (identifying peer industries)
   - Signal detection (monitoring relevant sectors)
5. **Portfolio-Grounded**: Industry code selections directly relate to actual portfolio companies and stated thesis
6. **No Inactive Codes**: All selected codes have "Active" status in LinkedIn
7. **Actionable**: Industry code lists are well-organized and ready for immediate use

---

## Troubleshooting

### Issue: Dataroom Lacks Investment Thesis Documents
**Solution**:
- Rely more heavily on portfolio company analysis
- Read any available research summaries in `research/deals/tier-1/` or `tier-2/`
- Infer thesis from company clustering patterns
- Check GP bio for expertise areas
- Note in output that thesis was inferred rather than explicitly stated

### Issue: Too Many or Too Few Industry Code Matches
**Too Many** (30+ Most Relevant codes):
- Apply stricter criteria: require 3+ portfolio companies OR explicit thesis mention
- Move borderline codes to Potentially Relevant tier
- Focus on deeptech/specialized codes rather than generic categories

**Too Few** (< 5 Most Relevant codes):
- Expand search terms: try synonyms, related technologies
- Consider broader parent categories in hierarchy
- Check if you're being too restrictive with evidence requirements
- Review industry code descriptions (not just labels) for matches

### Issue: Industry Code CSV Structure Changed
**Solution**:
- Verify CSV columns: should be `status, industry_id, label, hierarchy, description`
- Check for header row
- If structure is different, document changes and adapt search approach
- Ensure you're filtering to Active codes only

### Issue: Unclear How to Classify a Code (Tier 1 vs Tier 2)
**Decision Framework**:
- **Tier 1 if**: Would the GP add this to their personal LinkedIn profile? Would 3+ portfolio companies use this tag?
- **Tier 2 if**: Useful for finding relevant people/companies but not core identity. Adjacent/related domain.
- **Exclude if**: No clear connection to investment focus. Generic parent category with no specific relevance.

### Issue: Can't Find Match for Obvious Investment Area
**Example**: Fund invests heavily in "AI Infrastructure" but no exact code exists

**Solution**:
- Search for related codes: "Software Development", "IT System Custom Software Development", "Computer Hardware Manufacturing"
- Use hierarchy to find parent or child categories
- Check descriptions (not just labels) for conceptual matches
- Document in output that exact match wasn't available and rationale for substitute codes

### Issue: Target Has Highly Specialized Focus Not Well-Represented in LinkedIn Taxonomy
**Example**: "Quantum Error Correction" or "Fusion Reactor Materials Science"

**Solution**:
- Use closest available codes: "Nanotechnology Research", "Semiconductor Manufacturing", "Nuclear Electric Power Generation"
- Note in Tier 1 rationale that these are closest available matches
- Consider adding broader tech categories: "Technology, Information and Internet", "Research Services"
- Document limitation in Methodology section

---

## Related Workflows

**Prerequisite Workflows**:
- None required (can run independently)

**Complementary Workflows**:
- `vc-research.md`: Deep research on portfolio companies produces detailed company profiles that can enhance industry mapping
- `deal-prioritization.md`: Prioritized portfolio research provides strong signal for which industries are most important

**Follow-up Workflows**:
- Use industry code lists for LinkedIn connection targeting
- Monitor industries for deal flow signals and market trends
- Identify potential co-investors or advisors in relevant industries

**Validation**:
- `validator.md`: Can be used to check output completeness and source attribution quality

---

## Version History

**v1.0** (2025-11-16)
- Initial workflow creation
- Phase-based approach: Extract thesis → Map to codes → Generate output
- Two-tier classification: Most Relevant vs Potentially Relevant
- Source attribution requirements
- Quality checklist and troubleshooting guide
