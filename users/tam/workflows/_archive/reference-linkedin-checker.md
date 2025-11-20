# LinkedIn Reference Checker Workflow

## Objective
Transform generic firm-level references into specific individuals with LinkedIn profiles, seniority rankings, and warm intro paths.

## Input Requirements
1. **reference-check-targets.md** - Output from reference-identifier workflow containing prioritized investor firms
2. **LinkedIn connections CSV** - Export from LinkedIn with these columns:
   - Name
   - Title
   - Firm
   - Connection Degree (1st or 2nd)
   - Mutual Connections Count
   - Profile (LinkedIn URL)

## Processing Steps

### 1. Load Reference Targets
- Read reference-check-targets.md
- Extract all HIGH and MEDIUM priority firm names from the document
- Parse relationship claims and deal context for each firm
- Create master list of firms to cross-reference

### 2. Parse LinkedIn Connections
- Load LinkedIn CSV file
- Normalize firm names:
  - Remove suffixes: "Capital", "Ventures", "Partners", "Management", "LLC", "LP"
  - Handle abbreviations: "a16z" → "Andreessen Horowitz", "GV" → "Google Ventures"
  - Case-insensitive matching
  - Partial matching: "Vista Equity" matches "Vista Equity Partners"
- Create searchable index: Person → Firm → Title → Connection Degree → Mutuals → URL

### 3. Match Firms to Contacts

For each priority firm:

#### A. Find All Matches
- Search LinkedIn data for firm name (fuzzy matching, case-insensitive)
- Capture all individuals at the firm:
  - Full name
  - Current title
  - Connection degree (1st or 2nd)
  - Mutual connections count
  - LinkedIn profile URL

#### B. Classify by Seniority
Rank contacts by title into tiers:

- **Tier 1 (Highest Priority)**: C-Suite, Presidents, Managing Directors, Senior Managing Directors
- **Tier 2**: General Partners, Partners, Managing Partners
- **Tier 3**: Vice Presidents, Principals, Directors
- **Tier 4**: Associates, Senior Associates, Analysts

#### C. Rank by Connection Strength
Within each seniority tier, prioritize by network access:

- 🥇 **1st-degree connections** - Direct access (flag with ⭐)
- 🥈 **2nd-degree with 100+ mutuals** - Strong warm intro potential
- 🥉 **2nd-degree with 50-99 mutuals** - Moderate network overlap
- **2nd-degree with <50 mutuals** - Lower priority

#### D. Document Coverage Gaps
- Flag HIGH/MEDIUM priority firms with ZERO LinkedIn connections
- Note: These require alternative reference strategies (founder intros, cold outreach, etc.)

### 4. Generate Enhanced Outputs

#### Update reference-check-targets.md

For each firm with LinkedIn matches, replace generic entry with:

```markdown
### [Firm Name] → [Top Contact Name] ([Title])

- **LinkedIn Contacts** ([#] individuals found):

  **[Seniority Tier] (Top Priority):**
  1. **[Name]** - [Title], [#] mutual connections [⭐ if 1st-degree]
     - Profile: [LinkedIn URL]
     - Note: [Any special flags - 1st-degree, ONLY contact, formerly at firm, etc.]

  [Repeat for top 3-5 contacts, grouped by seniority tier]

- **Relationship**: [Original relationship type from dataroom]
- **Claim/Context**: [Original claim with verbatim quotes]
- **Source**: [Document name + page]
- **Deal Context**: [Portfolio company or deal]
- **Why Reference**: [Verification priorities]
- **Recommended First Contact**: [Specific name] ([Rationale: seniority + connection strength])
- **Warm Intro Path**: [If 1st-degree exists, describe how to leverage for intro to others]
```

For firms with ZERO matches:

```markdown
### [Firm Name] - NO LINKEDIN COVERAGE ❌

- **Coverage Gap**: Zero connections found at [Firm] despite [Priority] claim
- **Alternative Strategy**: [Suggest founder intros, cold outreach, or checking 2nd-degree manually]
- [Keep all original claim/context/source/deal context fields]
```

Add **LinkedIn Connection Analysis Summary** section at end:

```markdown
## LinkedIn Connection Analysis Summary

### Coverage Statistics
- Total LinkedIn contacts at priority firms: [#]
- HIGH PRIORITY firms: [#] contacts across [#] firms
- MEDIUM PRIORITY firms: [#] contacts across [#] firms
- 1st-degree connections: [#]
- Connection breakdown: [#] 1st-degree, [#] 2nd-degree

### Top 10 Most Connected Individuals
1. **[Name]** ([Firm]) - [#] mutuals, [Degree] [⭐ if 1st-degree]
2. [Continue for top 10...]

### Seniority Breakdown
- C-Suite/Presidents: [#]
- Managing Directors: [#]
- General Partners/Partners: [#]
- Vice Presidents/Principals: [#]
- Associates/Analysts: [#]

### Firms with NO LinkedIn Coverage
- **[Firm Name]** ([Priority]) - [Brief context why important]
- [Repeat for all gaps]

**Implication**: These firms require alternative reference strategies.

### Recommended Outreach Approach

**Week 1: High-Value Warm Intros**
1. Reach out to [1st-degree contact] for intro to [target person at same/related firm]
2. [Continue for all 1st-degree connections]

**Week 2: Critical Validations**
3. Contact [C-suite/senior person] at [critical firm] for [specific validation needed]
4. [Continue for highest-stakes references]

**Week 3: Co-Investor Validation**
5. Contact [Partner/GP] at [co-investor firm] for [deal-specific feedback]
6. [Continue for medium priority validations]

**Ongoing: Build Backup Options**
- For firms with multiple contacts, document 2nd/3rd backups if primary is unresponsive
- Use high mutual connection counts (100+) to identify best warm intro paths
```

#### Update investor-mention-map.csv

Add individual rows for each person found:

```csv
[Name] @ [Firm],Priority,[Title] + [Relationship Type],"[Title], [#] mutuals, [Degree], [Original claim context]",LinkedIn + [Source Doc],[LinkedIn URL],[Deal Context],Verification Priority
```

Examples:
```csv
Spencer Peterson @ Coatue,High,General Partner + Strategic partner,"GP with 212 mutuals, 2nd-degree, co-led Dirac seed",LinkedIn + Deeptech perspectives.md,linkedin.com/in/spencermpeterson,Dirac $6M seed,Critical
Matthew Mazzeo @ Coatue,High,Formerly Coatue + 1st-degree,"336+ mutuals, 1ST-DEGREE - WARM INTRO AVAILABLE, formerly at firm",LinkedIn,linkedin.com/in/matthewmazzeo,Coatue network warm intro,Critical - Use for warm intro to Spencer Peterson
David Breach @ Vista Equity,High,President/COO + LP investor,"President & COO, 18 mutuals, C-suite validation",LinkedIn + Fund I.md,linkedin.com/in/david-breach,Vista 2021-2025,Critical - C-suite LP commitment validation
```

### 5. Prioritize Outreach Strategy

Create tiered outreach plan based on actual LinkedIn data:

**Tier 1 Targets (Week 1 - Immediate Action):**
- All 1st-degree connections (can reach directly)
- Use 1st-degree to facilitate warm intros to others at same firm
- C-suite contacts at critical firms (former employers, key deal sources)

**Tier 2 Targets (Week 2 - High Stakes):**
- Partners/GPs with 100+ mutual connections
- Managing Directors at former employers
- Key deal flow partners (even if only 1 contact found)

**Tier 3 Targets (Week 3+ - Validation):**
- Mid-level contacts at co-investor firms
- Multiple contacts at same firm (backup options)
- Lower mutual connection counts but relevant roles

**Coverage Gaps (Ongoing - Alternative Strategies):**
- Firms with zero connections → request founder intros
- Consider cold outreach via mutual connections
- Check if portfolio company founders can facilitate intros

## Firm Name Matching Logic

### Common Abbreviations & Variations

| Dataroom Name | LinkedIn Variations to Match |
|---------------|----------------------------|
| a16z | Andreessen Horowitz, a16z, A16Z, AH |
| Coatue | Coatue Management, Coatue Capital |
| Lowercarbon | Lowercarbon Capital, Lowercarbon Cap, LC |
| GV | Google Ventures, GV |
| Alumni Ventures | Alumni Ventures Group, AV, Alumni Ventures |
| Vista Equity | Vista Equity Partners, Vista |

### Normalization Rules
1. Convert to lowercase for comparison
2. Remove common suffixes: "Capital", "Ventures", "Partners", "Management", "LLC", "LP", "Group"
3. Handle special characters: "&" → "and"
4. Trim whitespace
5. Check both full name and core name (e.g., "Vista" matches "Vista Equity Partners")

### Fuzzy Matching
- If exact match fails, try partial match on core firm name
- Example: "Lower" matches "Lowercarbon Capital"
- **Warning**: Manual verification recommended for close-but-not-exact matches

## Quality Checks

Before finalizing outputs, verify:

- ✅ **Valid LinkedIn URLs**: Every contact has working profile link
- ✅ **Mutual connections numeric**: Count is a number or "X+" format
- ✅ **1st-degree flagged**: All 1st-degree connections marked with ⭐
- ✅ **Coverage gaps documented**: All priority firms with zero matches explicitly noted
- ✅ **No duplicates**: Same person not listed multiple times
- ✅ **Seniority accurate**: Titles correctly classified into tiers
- ✅ **Cross-reference complete**: All HIGH/MEDIUM priority firms attempted (even if zero results)
- ✅ **CSV rows added**: investor-mention-map.csv updated with individual entries

## Output Deliverables

1. **Enhanced reference-check-targets.md** with:
   - Specific individuals replacing generic firm names
   - LinkedIn profile URLs for all contacts
   - 1st-degree connections flagged with ⭐
   - Warm intro paths documented
   - Coverage gaps explicitly identified
   - LinkedIn Connection Analysis Summary section

2. **Enhanced investor-mention-map.csv** with:
   - Individual rows for each person found
   - Seniority and connection strength indicators
   - Verification priority based on role + network

3. **Actionable insights**:
   - Which firms can be reached via warm intros
   - Which require alternative strategies
   - Week-by-week outreach plan

## Success Criteria

Output is complete when:
1. ✅ All HIGH/MEDIUM priority firms cross-referenced against LinkedIn data
2. ✅ Specific individuals identified (where connections exist)
3. ✅ All 1st-degree connections flagged for warm intro opportunities
4. ✅ Coverage gaps explicitly documented with alternative strategies
5. ✅ Outreach strategy reflects actual connection data (not generic recommendations)
6. ✅ LinkedIn Connection Analysis Summary added to reference-check-targets.md
7. ✅ investor-mention-map.csv updated with individual contact rows
8. ✅ Quality checks passed (valid URLs, no duplicates, accurate seniority)

## Example: Before & After

### Input (from reference-check-targets.md)

```markdown
### Coatue
- **Relationship**: Strategic partner, collaborator on early-stage opportunities
- **Claim/Context**: "Dillon is close with Coatue, co-led Dirac's $6M seed round"
- **Source**: Deeptech perspectives.md, Page 4
- **Deal Context**: Dirac - Advanced manufacturing AI
- **Why Reference**: Verify if Coatue views Dillon as "close" partner
```

### LinkedIn CSV Contains

```csv
Matthew Mazzeo,Formerly Coatue & Lowercase,Coatue,1st,336+,linkedin.com/in/matthewmazzeo
Spencer Peterson,General Partner,Coatue,2nd,212,linkedin.com/in/spencermpeterson
Lucas Swisher,Lead Growth Investing,Coatue Management,2nd,266,linkedin.com/in/lucasswisher
Elijah Sutanto,Vice President,Coatue,2nd,24,linkedin.com/in/elijah-sutanto
```

### Enhanced Output (in reference-check-targets.md)

```markdown
### Coatue → Spencer Peterson (GP) + Matthew Mazzeo (1st-degree)

- **LinkedIn Contacts** (4 individuals found):

  **1st-Degree Connections:**
  1. **Matthew Mazzeo** - Formerly Coatue & Lowercase, 336+ mutuals ⭐ 1ST-DEGREE
     - Profile: https://www.linkedin.com/in/matthewmazzeo/
     - Note: No longer at Coatue but can facilitate warm intros to current team

  **General Partners (Current):**
  2. **Spencer Peterson** - General Partner, 212 mutuals
     - Profile: https://www.linkedin.com/in/spencermpeterson/

  **Growth/Investment Team:**
  3. Lucas Swisher - Lead Growth Investing, 266 mutuals
     - Profile: https://www.linkedin.com/in/lucasswisher/
  4. Elijah Sutanto - Vice President, 24 mutuals
     - Profile: https://www.linkedin.com/in/elijah-sutanto

- **Relationship**: Strategic partner, collaborator on early-stage opportunities
- **Claim/Context**: "Dillon is close with Coatue, co-led Dirac's $6M seed round"
- **Source**: Deeptech perspectives.md, Page 4
- **Deal Context**: Dirac - Advanced manufacturing AI
- **Why Reference**: Verify if Coatue views Dillon as "close" partner
- **Recommended First Contact**: Spencer Peterson (GP - validates strategic partnership claim)
- **Warm Intro Path**: Leverage Matthew Mazzeo (1st-degree, 336+ mutuals) for warm introduction to Spencer Peterson
```

### CSV Rows Added (to investor-mention-map.csv)

```csv
Matthew Mazzeo @ Coatue,High,Formerly Coatue + 1st-degree,"Formerly Coatue & Lowercase, 336+ mutuals, 1ST-DEGREE - WARM INTRO AVAILABLE",LinkedIn,linkedin.com/in/matthewmazzeo,Coatue network warm intro,Critical - Use for warm intro to Spencer Peterson
Spencer Peterson @ Coatue,High,General Partner + Strategic partner,"GP with 212 mutuals, 2nd-degree, co-led Dirac seed, strategic partnership claim",LinkedIn + Deeptech perspectives.md,linkedin.com/in/spencermpeterson,Dirac $6M seed,Critical - Strategic partner validation
Lucas Swisher @ Coatue,High,Lead Growth + Strategic partner,"Lead Growth with 266 mutuals, highly connected backup contact",LinkedIn,linkedin.com/in/lucasswisher,Coatue network,High - Secondary contact
Elijah Sutanto @ Coatue,High,Vice President,"VP with 24 mutuals, junior backup",LinkedIn,linkedin.com/in/elijah-sutanto,Coatue network,Medium
```

## Notes

- **Run AFTER reference-identifier workflow** - This enhances, not replaces, the original reference analysis
- **LinkedIn data freshness**: CSV should be <6 months old for accuracy
- **Verify current employment**: Before outreach, spot-check that high-priority contacts still work at listed firms
- **1st-degree connections are golden**: Prioritize these for immediate warm intros
- **Coverage gaps aren't failures**: Documenting where you have NO connections is valuable intelligence
- **Manual review recommended**: For firms with 10+ contacts, manually review to ensure best contacts highlighted

## Troubleshooting

**No matches for high-priority firm?**
- Verify firm name variations in CSV (check abbreviations, suffixes)
- Try partial matching on core name
- Document as coverage gap and suggest alternatives

**Too many matches (10+)?**
- Group by seniority tier
- Limit display to top 3-5 per tier
- Summarize: "11 contacts ranging from President to Associate"

**1st-degree contact no longer at firm?**
- Still valuable! Flag as warm intro facilitator
- Note: "Can facilitate intro to current team despite departure"

**Missing mutual connections data?**
- Mark as "N/A" but still include if senior role
- Deprioritize slightly vs those with known high counts
