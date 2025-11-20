# Industry Network Analysis Workflow

## Purpose
Analyze LinkedIn network strength within a specific industry focus area by mapping connections against defined investment thesis categories, identifying gaps versus claimed relationships, and assessing strategic value for specific use cases.

## Required Inputs

1. **Industry Definition Document**: Path to document defining the industry scope and categories (e.g., `users/tam/{fund}/outputs/linkedin-industry-analysis.md`)
2. **LinkedIn Connections CSV**: Path to CSV of connections filtered for the industry (e.g., `users/tam/{fund}/research/people/linkedin/connections_{industry}.csv`)
3. **Source Documents Path**: Directory containing claims about relationships or portfolio companies (e.g., `users/tam/{fund}/dataroom/`)
4. **Output Path**: Where to save the network analysis (e.g., `users/tam/{fund}/outputs/network-analysis-{industry}.md`)

## CSV Format Requirements

The LinkedIn connections CSV must contain these columns:
- `Name` - Full name of connection
- `Title` - Current job title/company
- `Location` - Geographic location
- `Profile` - LinkedIn profile URL

**IMPORTANT:** IGNORE "Degree Connection" and "Mutual Connections" columns - these are irrelevant for analysis.

## Process

### Step 1: Extract Industry Definition

Read the industry definition document and identify:

**Core Categories/Thesis Areas:**
- Primary investment focus areas (e.g., "Fusion Energy", "AI Robotics", "Quantum Computing")
- Specific subcategories within each area
- Technologies, sectors, or business models included
- What makes a connection "relevant" to each category

**Secondary Categories:**
- Adjacent or supporting industries
- Enabling technologies
- Customer/supplier ecosystems
- Related investment areas

**Reference Framework:**
Document the source of industry definitions - use their language and categorization scheme, not your own interpretation.

### Step 2: Analyze Connections by Category

For each core and secondary category:

**A. Identify Relevant Connections:**
- Search CSV for companies matching the category (use company names in Title field)
- Search for role keywords (e.g., "fusion", "quantum", "robotics", "CEO", "CTO", "Founder")
- Group connections by:
  - Specific companies
  - Roles (Founder/CEO/CTO vs. operator vs. technical staff)
  - Subsectors within the category

**B. Assess Connection Quality:**
- **Decision-maker access**: CEO, Founder, CTO level vs. mid-level operators
- **Company stage**: Early-stage startup vs. scaled platform vs. established company
- **Strategic relevance**: Direct match to thesis vs. adjacent ecosystem
- **Notable exceptions**: Particularly valuable individual connections

**C. Document Findings:**
```markdown
### **CATEGORY NAME: [Category]**

**Assessment:** ⭐⭐⭐⭐⭐ **[Rating] - [One sentence summary]**

**Key Connections ([X] total):**
- **Company Name** (Person Name - Role, description)
- **Company Name** (Person Name - Role, description)
[List 5-10 most notable connections]

**Additional Coverage:**
- [Broader description of ecosystem connections]
- [Quantify breadth: "10+ connections in X", "Multiple connections in Y"]

**Strengths:**
- [Specific advantages this network provides]
- [Quality over quantity observations]
- [Strategic positioning strengths]

**Gaps:**
- [Missing connections in this category]
- [Companies/people expected but not found]
- [Stage or subsector gaps]
```

**Star Rating Scale:**
- ⭐⭐⭐⭐⭐ **Elite** - Exceptional access, founder-level, multiple scaled companies
- ⭐⭐⭐⭐ **Strong** - CEO/founder access, good coverage, some scaled presence
- ⭐⭐⭐ **Moderate** - Adequate connections, mostly early-stage or operational roles
- ⭐⭐ **Limited** - Minimal presence, few relevant connections
- ⭐ **Minimal/None** - Essentially no network in this category

### Step 3: Cross-Cutting Analysis

Identify themes that span multiple categories:

**A. Investor/Capital Access:**
- VC/PE investors in the network
- Capital allocators across relevant sectors
- Co-investment and fundraising opportunities

**B. Enabling Technologies:**
- Infrastructure providers used across multiple categories
- Technical talent that supports portfolio companies
- Platform technologies (e.g., AI infrastructure for robotics + cybersecurity)

**C. Ecosystem Strengths:**
- Accelerator networks (YC, Techstars, etc.)
- University/research connections
- Geographic or community clusters

### Step 4: Gap Analysis vs. Claims

**A. Extract Claimed Relationships:**
From source documents, identify:
- Specific portfolio companies mentioned
- Named individuals and their relationships
- Companies claimed as "network advantages"
- Ecosystem access claims (e.g., "PROD accelerator", "Harvard founders")

**B. Verify Against Network:**
For each claim, search the CSV:
```bash
grep -i "{company_name}" {csv_path}
grep -i "{person_surname}" {csv_path}
```

**C. Document Verification Status:**
- ✅ **Validated**: Connection found in network
- ⚠️ **Partially Validated**: Related connection found (different person at same company, adjacent role)
- ❌ **Cannot Verify**: No matching connection found

**D. Quantify Gap:**
- Total claims vs. verified connections
- Missing portfolio companies (list by name)
- Claimed high-value relationships not found
- Patterns in what's missing (e.g., all Series B+ companies absent)

### Step 5: Strategic Value Assessment

**A. Define Use Cases:**
Based on the person/organization's goals, assess network value for:
- Deal sourcing (finding new investment opportunities)
- Technical diligence (accessing domain experts)
- Portfolio support (helping companies with customers, talent, partnerships)
- Fundraising (accessing capital providers)
- Competitive intelligence (understanding market landscape)
- [Other specific use cases]

**B. Rate Each Use Case:**
```markdown
### **Use Case: [Name]** ⭐⭐⭐⭐

**Strengths:**
- [How network supports this use case]
- [Specific examples]

**Gaps:**
- [What's missing for this use case]
- [How gaps limit effectiveness]

**Overall Assessment:** [One paragraph on network fit for this use case]
```

**C. Identify Optimization Pattern:**
Determine what the network is **optimized for**:
- Early-stage sourcing vs. later-stage access
- Emerging categories vs. established markets
- Technical depth vs. broad coverage
- Founder relationships vs. operator relationships
- Ecosystem breadth vs. portfolio depth

### Step 6: Generate Final Report

Structure the output as:

```markdown
# [Person/Organization]'s [Industry] Network Analysis

**Dataset:** [X] LinkedIn connections filtered for [industry] sectors
**Note:** This represents a subset of connections relevant to [industry] focus areas, not complete network

**Industry Definition:** Per [source document], [industry] encompasses: [list categories]

---

## Network Analysis by Category

[For each core category: assessment, connections, strengths, gaps]

---

## Secondary Focus Areas

[For each secondary category: brief assessment]

---

## Cross-Cutting Strengths

[Investors, enabling technologies, ecosystem themes]

---

## Key Network Characteristics

### **Strengths:**
1. [Numbered list of 5-8 key strengths]

### **Gaps:**
1. [Numbered list of 5-8 key gaps]

---

## Strategic Value Assessment

**For [Use Case 1]:** ⭐⭐⭐⭐⭐
- [Assessment paragraph]

**For [Use Case 2]:** ⭐⭐⭐
- [Assessment paragraph]

[Repeat for all use cases]

---

## Overall Assessment

**Network Optimization:** [One paragraph describing what this network is optimized for vs. what it's weak at]

**Strategic Fit:** [One paragraph on fit for stated goals]

**Verification Status vs. Claims:**
- ✅ **Validated:** [What claims were verified]
- ⚠️ **Partially Validated:** [What has mixed evidence]
- ❌ **Cannot Verify:** [What claims couldn't be verified, with count]
```

## Analysis Guidelines

### DO:
- **Use industry's own definitions** - Reference the industry definition document, don't create your own categories
- **Ignore connection degree** - Never reference "1st degree", "2nd degree", or mutual connections
- **Avoid percentages** - This is a subset network, so percentages are misleading (use "high concentration", "multiple", "limited" instead)
- **Be specific** - Name actual companies and people found
- **Quantify gaps** - List specific missing portfolio companies by name
- **Assess strategically** - Focus on whether network supports stated goals
- **Provide evidence** - Every conclusion should be backed by specific examples

### DON'T:
- Don't invent your own notion of what the industry includes
- Don't calculate percentages (X% are founders, Y% are at big companies)
- Don't reference connection degrees or mutual connections
- Don't make assumptions about relationship strength from connection existence
- Don't inflate strengths or minimize gaps - be balanced and evidence-based

## Output Quality Criteria

A complete industry network analysis must include:

- [ ] Industry definition sourced from reference document, not invented
- [ ] Analysis organized by categories from industry definition
- [ ] Star ratings (⭐) for each category with clear assessment
- [ ] 5-10 specific connection examples per major category
- [ ] Quantified gaps (list missing portfolio companies by name)
- [ ] Strategic value assessment for 3+ relevant use cases
- [ ] Overall assessment of network optimization pattern
- [ ] Verification status vs. any claims (with specific counts)
- [ ] No references to "degree connection" or "mutual connections"
- [ ] No misleading percentages (since this is a subset)

## Success Metrics

**Completeness:**
- All core categories from industry definition analyzed
- All secondary categories at least mentioned
- Cross-cutting themes identified
- Gap analysis vs. claims completed

**Specificity:**
- Concrete examples for every strength claim
- Named companies/people missing from network
- Quantified assessments ("10+ connections", not "many")
- Clear star ratings with justification

**Strategic Insight:**
- Network optimization pattern identified
- Use case fit assessments actionable
- Gaps tied to specific limitations
- Verification status affects credibility assessment

**Objectivity:**
- Balanced: acknowledges both strengths and gaps
- Evidence-based: every claim backed by specific examples
- Transparent: methodology clear, sources cited
- Honest: doesn't inflate network value or minimize weaknesses

## Example Usage

```bash
# Inputs:
INDUSTRY_DEF="users/tam/hyperion/outputs/linkedin-industry-analysis.md"
CONNECTIONS_CSV="users/tam/hyperion/research/people/linkedin/connections_deeptech.csv"
DATAROOM="users/tam/hyperion/dataroom/"
OUTPUT="users/tam/hyperion/outputs/network-analysis-deeptech.md"

# The workflow produces:
1. Analysis organized by 6 core thesis areas (Fusion, Robotics, Cybersecurity,
   Quantum, Semiconductors, Manufacturing) + 3 secondary areas
2. Star ratings for each category (⭐⭐⭐⭐⭐ for Quantum, ⭐⭐⭐ for Cybersecurity)
3. Specific connections listed (Quantinuum founder Ilyas Khan, Zap Energy CEO Benj Conway)
4. Gap analysis: 12+ portfolio companies not found in network
5. Strategic assessment: "optimized for early-stage sourcing vs. portfolio support"
6. Verification: Quantum validated ✅, most portfolio companies cannot verify ❌
```

## Common Patterns

### Pattern 1: Strong Ecosystem, Weak Portfolio
- Many relevant industry connections
- Few connections at claimed portfolio companies
- **Interpretation**: Good for sourcing, questionable portfolio relationship claims

### Pattern 2: Founder-Heavy Network
- Most connections are CEO/CTO/Founder level
- Limited mid-level operators or technical staff
- **Interpretation**: Decision-maker access strong, operational support limited

### Pattern 3: Early-Stage Optimization
- Strong in emerging category leaders
- Weak at scaled ($1B+) companies
- **Interpretation**: Optimized for pre-seed to Series A, not growth stage

### Pattern 4: Geographic Cluster
- Concentrated in specific locations (SF, NYC, etc.)
- Limited international or distributed presence
- **Interpretation**: Regional network advantage, global coverage gaps

### Pattern 5: Investor-Rich Network
- High concentration of VC/PE connections
- Multiple capital allocators across stages
- **Interpretation**: Strong for fundraising and co-investment, portfolio support depends on other factors

## Workflow Outputs

The final analysis should answer:

1. **How strong is this network in each category?** (Star ratings + specific examples)
2. **What is this network optimized for?** (Sourcing vs. support, early vs. late stage, etc.)
3. **What gaps exist vs. claims?** (List specific missing portfolio companies)
4. **How valuable is this for intended use cases?** (Strategic assessment per use case)
5. **What should you believe/question?** (Verification status on key claims)

This enables decisions about:
- Network claims credibility
- Sourcing capability in specific sectors
- Portfolio support potential
- Due diligence needs (reference checks, relationship verification)
- Strategic value of the relationship/partnership
