# LinkedIn Network Verification Workflow

## Purpose
Verify claimed relationships and institutional network strength by cross-referencing claims in source documents against LinkedIn connection data.

## Required Inputs

1. **Institution Name**: The institution being analyzed (e.g., "Harvard", "Stanford", "YC")
2. **Source Documents Path**: Directory containing files with network claims (e.g., `users/tam/{fund}/dataroom/`)
3. **LinkedIn Connections CSV**: Path to CSV export of LinkedIn connections filtered by institution (e.g., `users/tam/{fund}/research/people/linkedin/connections_{institution}.csv`)
4. **Output Path**: Where to save verification analysis (e.g., `users/tam/{fund}/research/analysis/{institution}_network_verification.md`)

## CSV Format Requirements

The LinkedIn connections CSV must contain these columns:
- `Name` - Full name of connection
- `Title` - Current job title/company
- `Profile` - LinkedIn profile URL
- `Location` - Geographic location
- Optional: `Degree Connection`, `Mutual Connections Count`, `Mutual Connections Names`

## Process

### Step 1: Extract Network Claims

Read all source documents and identify specific relationship claims:
- **Person names** mentioned in claims
- **Company/organization affiliations** for each person
- **Relationship descriptors** (e.g., "close friend", "classmate", "co-founder")
- **Additional context** (graduation year, role, deal involvement)

Categorize claims by:
- **High-value claims**: Relationships with scaled companies ($1B+ valuations) or key strategic advantages
- **Secondary claims**: Emerging companies or general network breadth
- **Institutional access claims**: Access to accelerators, programs, or communities

### Step 2: Define Verification Strategy

For each claim, determine search methods:

**Primary searches**:
- Full name match (case-insensitive)
- Surname-only search (to find potential matches with different first names)
- Company name search (to find anyone at the organization)

**Compound searches** (when needed):
- Name + company combination
- Title keywords (e.g., "founder", "CEO", "CTO")
- Location filters (if person's location is known)

### Step 3: Execute Verification

For each claimed relationship:

1. **Search the CSV** using grep/pattern matching:
   ```bash
   grep -i "{full_name}" {csv_path}
   grep -i "{surname}" {csv_path}
   grep -i "{company}" {csv_path}
   ```

2. **Record results**:
   - ✅ **VERIFIED**: Exact name match found in connections
   - ⚠️ **PARTIAL**: Related connection found (same company, different person)
   - ❌ **NOT FOUND**: No matching connections found

3. **Extract connection details** when verified:
   - Name, Title, Location, Profile URL
   - Note any additional connections at the same company

### Step 4: Generate Analysis Report

Create structured markdown output with these sections:

#### **Executive Summary**
- Verification success rate (X of Y claims verified)
- Key findings (especially for high-value claims)
- Critical gaps or red flags

#### **Detailed Results by Claim**

For each claim, document:

**✅ VERIFIED CLAIM**:
```markdown
#### ✅ **CLAIM X: [Company] - [Person Name]**
- **Claimed relationship:** "[description from source]"
- **Search performed:** Full name, company search
- **Result:** **FOUND** ✅
- **LinkedIn data:**
  - Name: [name]
  - Title: [title]
  - Location: [location]
  - Profile: [URL]
- **Validation status:** ✅ **VERIFIED**
```

**❌ UNVERIFIED CLAIM**:
```markdown
#### ❌ **CLAIM X: [Company] - [Person Name]**
- **Claimed relationship:** "[description from source]"
- **Search performed:** Full name, surname, company search
- **Result:** **NOT FOUND**
- **Company search:** [results of broader company search]
- **Notes:** [any partial matches or related findings]
- **Validation status:** ❌ **CANNOT VERIFY**
```

#### **Key Findings & Red Flags**

Analyze patterns:
- Which claim categories verified vs. failed
- Whether highest-value claims are verifiable
- Systematic gaps (e.g., all claims from one source fail)
- Statistical summary (verification rates by category)

#### **Search Methodology**

Document all searches performed for reproducibility:
```markdown
### **[Person Name] ([Company])**
- Search: `grep -i "{surname}" {csv_file}`
- Search: `grep -i "{company}" {csv_file}`
- **Result:** [Found/Not Found]
```

#### **Limitations & Caveats**

Standard disclaimer about LinkedIn data:
- Not all relationships exist on LinkedIn
- Privacy settings may hide connections
- Timing issues (recent connections not yet added)
- Connection existence ≠ relationship quality
- Alternative relationship channels (email, phone, in-person)

#### **Recommended Next Steps**

Based on verification gaps:
- Reference checks with specific individuals
- Cross-platform verification (GitHub, Twitter, etc.)
- Interview questions to probe claimed relationships
- Additional data sources to check

## Output Quality Criteria

The verification report must:
1. **Be evidence-based**: Every claim linked to specific search results
2. **Be reproducible**: Include exact search commands used
3. **Be balanced**: Acknowledge limitations, not just failures
4. **Be actionable**: Provide clear next steps for unverified claims
5. **Quantify findings**: Include verification rates and statistical summaries

## Common Patterns

### Pattern 1: High-value claim verification failure
When prestigious/valuable claims can't be verified → **🚩 Major red flag** → Requires deeper investigation

### Pattern 2: Consistent verification within a category
If all claims from one source verify → **✅ Confidence boost**
If all claims from one source fail → **🚩 Source credibility issue**

### Pattern 3: Indirect relationship claims
Claims about "friend of founder's roommate" or non-founder relationships → **⚠️ Lower value** → Verify actual decision-maker access

### Pattern 4: Institutional access claims
Claims about access to programs/accelerators → Search for multiple people from that program to verify ecosystem depth

## Example Usage

```bash
# Given these inputs:
INSTITUTION="Harvard"
DATAROOM="users/tam/hyperion/dataroom/"
CONNECTIONS="users/tam/hyperion/research/people/linkedin/connections_harvard.csv"
OUTPUT="users/tam/hyperion/research/analysis/harvard_network_verification.md"

# The workflow should:
1. Read all .md files in DATAROOM
2. Extract every claimed relationship to Harvard affiliates
3. Search CONNECTIONS CSV for each person/company
4. Generate verification report at OUTPUT
```

## Success Metrics

A complete verification analysis includes:
- [ ] All specific relationship claims extracted and categorized
- [ ] Every claim has documented search attempts (minimum 2 search methods per claim)
- [ ] Clear verification status for each claim (✅/⚠️/❌)
- [ ] Statistical summary with verification rates
- [ ] Red flags and patterns identified
- [ ] Reproducible search commands documented
- [ ] Limitations and caveats acknowledged
- [ ] Actionable next steps provided
