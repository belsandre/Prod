# Source Documentation Standards

**Purpose**: Universal standards for documenting sources across all research workflows to ensure quality, verification, and appropriate skepticism.

---

## Source Template Format

Every source must be documented in a separate markdown file using this template:

```markdown
# Source: [Brief Title]

**URL**: [Full URL]

**Date**: [Publication/Last Updated Date in YYYY-MM-DD format]

**Source Type**: [LinkedIn Profile / News Article / Interview / Company Website / Press Release / etc.]

**Objectivity Level**: [High / Medium / Low]

**Reliability Assessment**: [Brief assessment of source credibility and relevance]

---

## Key Information

[Bullet points of key facts, metrics, quotes, or insights extracted from this source]

---

## Critical Assessment

**Strengths**: [What makes this source valuable]

**Limitations**: [What's missing, potential biases, caveats]

**Verification Status**: [Verified / Unverified / Partially Verified]

[Note any inconsistencies with other sources or claims requiring validation]

---

## Raw Content

[Full extracted content from the source for reference and verification]
```

---

## Evidence Tier Classification

**Purpose**: Distinguish between independent external sources and interested-party controlled sources to ensure objective assessment and appropriate skepticism for unverified claims.

### Tier 1 - External (Highest Credibility) ✅

**Definition**: Independent third-party sources with no financial interest or control by subject

**Examples**:
- Third-party media quotes (TechCrunch, Bloomberg, WSJ, etc.)
- Independent case studies or analyst reports
- Public customer/partner testimonials (not company-controlled)
- Verified public board roles or governance positions
- Academic publications or conference presentations
- Regulatory filings or court documents

**Treatment**: Can be cited as primary evidence with high confidence

**Citation Format**:
```markdown
✅ **[Subject] quoted in [Publication]**: "[Exact quote]"
- **Source**: [Article Title](URL) | Publication: [Outlet] | Date: YYYY-MM-DD
- **Source Type**: ✅ External (Tier 1 - independent)
- **Context**: [Funding announcement / Interview / Analysis]
- **Reliability**: High - independent third-party source
```

---

### Tier 2 - Public But Company-Controlled (Medium Credibility) ⚠️

**Definition**: Publicly available but created/controlled by the subject company or entity

**Examples**:
- Company press releases
- Company blog posts or website content
- Public founder/executive social media posts
- Company-hosted events or webinars
- Company-produced case studies or testimonials

**Treatment**:
- Acceptable as supporting evidence
- Must note company-controlled source
- May reflect marketing/positioning vs. comprehensive assessment

**Citation Format**:
```markdown
⚠️ **[Subject] featured in company materials**: "[Exact quote]"
- **Source**: [Company blog/press release], Date: YYYY-MM-DD
- **Source Type**: ⚠️ Company-controlled (Tier 2)
- **Context**: [Company announcement / Marketing materials]
- **Limitation**: Company-controlled source; may reflect positioning
```

---

### Tier 3 - Dataroom/Fundraising Materials (Lowest Credibility) ⚠️⚠️

**Definition**: Private materials provided by interested parties for fundraising or business development purposes

**Examples**:
- Dataroom testimonials or case studies
- Fund marketing materials or pitch decks
- Internal reports or assessments
- Solicited references for fundraising purposes
- LP presentation materials

**Treatment**:
- MUST be clearly labeled as "dataroom claim" or "fundraising material"
- MUST attempt external validation
- If no external validation found, document this limitation explicitly

**Citation Format**:
```markdown
⚠️⚠️ **DATAROOM CLAIM**: [Subject] stated: "[Exact quote]"
- **Source**: [Fund Name] dataroom materials | Document: [filename]
- **Source Type**: ⚠️⚠️ Fundraising materials (Tier 3)
- **External validation**: [None found / Partially corroborated by [source]]
- **Verification status**: ❌ Unverified / ✅ Verified / ⚠️ Partially verified
- **Context**: Testimonial likely solicited for fundraising/LP materials
- **Limitation**: Cannot verify accuracy; may reflect fundraising positioning vs. ongoing reality
```

---

## Quality Criteria

**Excellent Source** (prioritize these):
- **Primary**: Company website, financial filings, official announcements
- **Recent**: Within 12 months for fast-moving companies, 24 months for stable industries
- **Substantive**: 500+ words, specific metrics/details, not just mentions
- **Credible**: Established publication or verified company material
- **Relevant**: Directly addresses research questions

**Mediocre Source** (supplement only):
- Brief mentions without context
- Outdated information (3+ years old)
- Aggregator sites without original reporting
- Unverified claims without corroboration

**Quality > Quantity**: Better 3 excellent sources than 6 mediocre ones.

---

## High-Value Claims Requiring Verification

When dataroom or company materials make specific, verifiable claims, attempt external validation:

### 1. Network Introduction Claims
**Claim**: "GP introduced Company to [Customer/Partner]"
**Verification**:
- Search for public evidence of resulting relationship
- Check press releases, partnerships, customer announcements
- Review LinkedIn connections/interactions
- Document: ✅ Verified | ⚠️ Partially verified | ❌ No evidence found

### 2. Customer Introduction Claims
**Claim**: "GP helped secure [Customer Name] as customer"
**Verification**:
- Search for customer on company website
- Look for case study or public reference
- Check if customer publicly announced partnership
- Document: ✅ Verified | ⚠️ Partially verified | ❌ No evidence found

### 3. Fundraising Impact Claims
**Claim**: "GP helped raise [Amount] from [Investors]"
**Verification**:
- Verify round actually closed (amount, timing matches)
- Check if GP's firm participated in round
- Assess if GP quoted in funding announcement
- Document: ✅ Verified | ⚠️ Partially verified | ❌ No evidence found

### 4. Board/Governance Role Claims
**Claim**: "GP serves on board" or "GP is board observer"
**Verification**:
- Check company LinkedIn for board members
- Search Crunchbase/PitchBook for board composition
- Look for public filings (if applicable)
- Document: ✅ Verified | ⚠️ Partially verified | ❌ No evidence found

### 5. Technical/Domain Expertise Claims
**Claim**: "GP provided technical expertise in [Domain]"
**Verification**:
- Cross-reference with GP background research
- Assess if claim plausible given GP's experience
- Look for public evidence of GP domain expertise
- Document: ✅ Plausible + verified | ⚠️ Plausible but unverified | ❌ Inconsistent

---

## Documentation of Verification Failures

**When high-value claims cannot be verified externally, this MUST be documented as a research limitation:**

```markdown
## Research Limitations

⚠️ **UNVERIFIED CLAIMS**: The following claims from dataroom materials could not be verified through external sources:

1. **[Claim description]**
   - **Source**: [Dataroom document]
   - **Verification Attempted**: [Searches performed, sources checked]
   - **Result**: No public evidence found
   - **Implication**: [Cannot confirm/refute; requires direct validation with company/GP]

2. **[Additional unverified claims...]**
```

---

## Source Quality Thresholds by Research Type

### Deep Research (e.g., Tier 1 Companies, Key GPs)
- **Minimum**: 5+ sources
- **Distribution**: At least 1 Tier 1 (external), at least 1 primary (company website/official)
- **Recency**: Majority within 12-18 months
- **Depth**: At least 2 sources with substantial content (500+ words)

### Standard Research (e.g., Tier 2 Companies, Secondary GPs)
- **Minimum**: 3+ sources
- **Distribution**: At least 1 external or primary source
- **Recency**: At least 1 recent source (within 18 months)
- **Depth**: At least 1 source with substantial content

### Quick Research (e.g., Tier 3 Companies, Background Checks)
- **Minimum**: 2+ sources
- **Distribution**: At least 1 reliable source (external or primary)
- **Recency**: Best effort
- **Depth**: Focus on key facts validation

---

## Usage in Workflows

**Reference this template by including**:
```markdown
## Source Documentation
Follow `templates/source-documentation.md` for:
- Source template format
- Evidence tier classification
- Citation formats
- Verification requirements
```

**Workflow-specific extensions**: Workflows can add specific requirements or adjust thresholds while maintaining core standards.
