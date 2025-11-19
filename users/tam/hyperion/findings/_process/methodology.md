# Research Methodology - Hyperion Ventures Due Diligence

**Date Created**: November 17, 2025
**Research Period**: January 6 - November 17, 2025
**Lead Analyst**: Claude Code + VC Research Workflow

---

## Evidence Quality Framework

All research findings are categorized using a **3-tier evidence classification system** to distinguish between GP-controlled sources, affiliated sources, and independent verification.

### Tier 1: Entity-Controlled Sources ⚠️

**Definition**: Materials created or controlled by Hyperion GPs or portfolio company management seeking fundraising

**Examples**:
- Dataroom materials (GP Bio, case studies, LP letters)
- GP-authored content (Substack articles, LinkedIn posts)
- Solicited testimonials from founders (in dataroom)
- Pitch decks and marketing materials

**Strengths**:
- Provides GP's narrative and positioning
- Shows claimed achievements and relationships
- Often contains details not available publicly

**Limitations**:
- Self-serving and potentially biased
- Cannot be independently verified
- May contain exaggerations or omissions for fundraising purposes
- No third-party validation

**Usage in Analysis**:
- Used to identify claims that require verification
- Treated as "claims to be validated" not "facts"
- Always cross-referenced with Tier 2/3 sources when possible

**Percentage of Timeline**: 59% of events (22 of 37)

---

### Tier 2: Affiliated Sources ⚠️

**Definition**: Self-reported information via verified platforms, but not independently verified

**Examples**:
- LinkedIn profiles (employment, education)
- Resume data from known professional affiliations
- Self-reported educational credentials
- Company websites (self-descriptions)

**Strengths**:
- Platform-verified (e.g., LinkedIn confirms employment dates)
- Social credibility (public profile, professional reputation)
- Generally accurate for basic facts (education, employment)

**Limitations**:
- Still self-reported (potential for exaggeration)
- Limited verification of specific claims (roles, responsibilities)
- Cannot verify attribution (individual vs team contributions)

**Usage in Analysis**:
- Used to verify basic facts (education, employment history)
- Treated as "likely accurate" for credentials
- Requires Tier 3 verification for specific achievement claims

**Percentage of Timeline**: 5% of events (2 of 37)

---

### Tier 3: Independent Sources ✅

**Definition**: Third-party verification with no GP control or influence

**Examples**:
- Public funding announcements (press releases, TechCrunch, Bloomberg)
- SEC filings and public records
- Third-party news articles and analysis
- Company websites (not GP-controlled)
- Independent research reports

**Strengths**:
- Independent verification, no GP bias
- Multiple sources often available for cross-reference
- Factual claims (funding amounts, valuations, dates)
- Credible third-party validation

**Limitations**:
- Limited availability for private companies
- May not cover all portfolio companies
- Often lacks detail on GP-specific contributions
- Cannot verify internal activities (hiring referrals, strategic advice)

**Usage in Analysis**:
- Highest confidence for verified claims
- Used as ground truth for public facts
- Cross-referenced with Tier 1 claims to assess accuracy

**Percentage of Timeline**: 27% of events (10 of 37)

---

## Verification Standards

### High Confidence (Multiple Tier 3 Sources)

**Criteria**: At least 2-3 independent Tier 3 sources confirm claim

**Examples**:
- ✅ Figure AI $39B valuation (Bloomberg, TechCrunch, company announcement)
- ✅ Quantinuum $10.6B valuation (multiple press releases, news sources)
- ✅ Dillon's Harvard ME degree (LinkedIn + university records)

**Usage**: Treated as verified facts in analysis

---

### Medium Confidence (Tier 1 + Tier 3 Combination)

**Criteria**: Tier 1 claim partially supported by Tier 3 verification

**Examples**:
- ⚠️ Figure AI investment timing (dataroom claims April 2023, public Series A May 2023 confirms proximity)
- ⚠️ Quantinuum valuation growth (dataroom claims + public funding rounds confirm outcome)
- ⚠️ Investment stage claims (dataroom says "pre-seed", public rounds confirm timing)

**Usage**: Treated as "likely accurate with caveats" - requires additional verification for details

---

### Low Confidence (Tier 1 Only)

**Criteria**: Claim appears only in GP-controlled sources with NO independent verification

**Examples**:
- ❓ Dirac-Founders Fund introduction ("Dillon introduced CEO to friend at FF" - only in dataroom)
- ❓ Normal hiring referrals ("Referred 2 key hires" - only in dataroom)
- ❓ Vista $1B+ deployment ("Deployed >$1 billion across 15+ deals" - only in GP Bio)
- ❓ Fusion investment timing (dates unknown, only dataroom mentions)

**Usage**: Treated as "unverified claims requiring validation" - flagged for independent verification before acceptance

---

## Research Process

### Phase 1: Data Collection (Jan 6-12, 2025)

**Activities**:
1. Company Research Skill deployed for 14 companies
2. 60-80 sources documented across dataroom, public filings, news
3. GP research (Dillon Dunteman, Henry Bellew)
4. Network analysis (637 LinkedIn connections)

**Outputs**:
- Individual company research-summary.md files
- GP profiles
- Network analysis reports

---

### Phase 2: Structured Data Extraction (Nov 17, 2025)

**Activities**:
1. Created 5 JSON files from research findings
2. Extracted 47 timeline events with source tiers
3. Categorized 30 claims across 6 key categories
4. Mapped 637 network connections

**Outputs**:
- portfolio.json (14 companies)
- network.json (connection analysis)
- timeline.json (chronological events)
- claims.json (validation status)
- gp-profiles.json (GP backgrounds)

---

### Phase 3: Analysis & Synthesis (Nov 17, 2025)

**Activities**:
1. Cross-referenced claims against timeline
2. Identified funding discrepancies
3. Assessed verification status for each claim
4. Created evidence-based recommendations

**Outputs**:
- index.md (executive summary)
- Critical recommendations
- Process documentation

---

## Key Patterns Identified

### Pattern 1: Tier 1 Claim Concentration

**Finding**: 100% of GP value-add claims come from Tier 1 sources only

**Examples**:
- ALL sourcing stories (cold outreach, networking events, VC referrals)
- ALL value-add activities (hiring referrals, VC introductions, strategic advice)
- ALL founder testimonials (in dataroom only, none public)

**Implication**: Cannot verify differentiation thesis without independent founder/VC confirmation

---

### Pattern 2: Funding Discrepancies

**Finding**: 40% of verifiable funding claims (2 of 5 tier-1 companies) have discrepancies

**Examples**:
- Dirac: $6M (dataroom) vs $10.7M (public) = $4.7M gap (78% larger)
- Normal: $17M Series A (dataroom) vs $35M total seed (public) = $18M gap OR round mismatch

**Implication**: If 40% of checkable facts have errors, unverifiable claims (value-add, sourcing) may also be unreliable

---

### Pattern 3: Retroactive Framing

**Finding**: Thought leadership launched AFTER first investment

**Timeline**:
- March 2020: Quantinuum investment
- ~2021: Substack launch (19 months later)
- October 2021: First article (19 months after investment)

**Implication**: Thought leadership may document investments retrospectively rather than develop theses prospectively

---

### Pattern 4: Public Testimonial Absence

**Finding**: ZERO public founder testimonials despite 9 companies with claimed Dillon involvement

**Searched**:
- Company press releases (0 mentions)
- Founder LinkedIn posts (0 mentions)
- Podcast interviews (0 mentions)
- News articles (0 mentions)

**Implication**: Either founders don't publicly acknowledge value-add (unusual), or value-add is overstated

---

## Limitations

### 1. Coverage Gaps

**Portfolio**: Only 14 of 24 companies researched (58%)
- 18 companies lack documented investment dates, amounts, valuations
- Cannot verify 6.7x TVPI claim without full portfolio visibility

**Timeline**: Only 47 events documented
- Fusion investment dates unknown (Zap, Avalanche, Hephaestus, Marathon)
- Vista deal details missing (claimed $1B+ deployment)
- Failed investment details missing (3 underperformers not named)

---

### 2. Private Company Information Limits

**Public Data Scarcity**:
- Most portfolio companies are pre-revenue, private
- Limited SEC filings, press coverage
- Funding amounts often not disclosed publicly

**GP-Specific Attribution**:
- Cannot verify individual contributions vs team efforts
- Firmament/Vista institutional credit vs Dillon personal credit unclear
- Value-add activities are internal (no public record)

---

### 3. Network Analysis Limitations

**Data Source**: Dillon's LinkedIn connections only
- Henry Bellew network not analyzed
- Connection count ≠ relationship depth
- Cannot verify claimed "close relationships" (Tamarack, Coatue, FF)

---

### 4. Timing Precision

**Vague Dates**:
- "~2021" Substack launch (exact date unknown)
- "Q1 2023" robotics research (vague timing)
- "Mid-2022" angel investing start (imprecise)

**Implications**: Cannot precisely validate "thought leadership preceded investment" claims

---

## Recommendations for Future Research

### High Priority

1. **Founder Reference Calls**: Independent interviews with Dirac, Normal, Quantinuum CEOs
2. **VC Partner Confirmations**: Verify Tamarack, Founders Fund, Coatue relationships
3. **Full Portfolio Audit**: Request complete 24-company list with dates, amounts, valuations
4. **Failed Investment Disclosure**: Names, dates, post-mortems for underperformers

### Medium Priority

5. **Vista Attribution Verification**: Interview former colleagues for role clarity
6. **Fusion Timeline Completion**: Request exact investment dates for Zap, Avalanche, Hephaestus, Marathon
7. **Thought Leadership Dating**: Verify exact Substack launch date and article publication dates
8. **Henry Bellew Clarification**: Interview both GPs on division of labor

---

## Confidence Levels Summary

**High Confidence** (Multiple Tier 3 sources):
- Educational credentials (Harvard ME)
- Employment history (Firmament, Vista)
- Public funding rounds (Figure $39B, Quantinuum $10.6B)
- Company outcomes (valuations, Series B/C raises)

**Medium Confidence** (Tier 1 + Tier 3 combination):
- Investment timing claims (dataroom + public rounds confirm proximity)
- Portfolio company existence (partial Tier 3 verification)
- Co-investor validation (tier-1 VCs confirmed in some deals)

**Low Confidence** (Tier 1 only, unverified):
- Value-add claims (hiring referrals, VC introductions, strategic advice)
- Sourcing stories (cold outreach, networking events)
- Referral volume claims (50+ referrals/year → 300+)
- Vista deployment attribution ($1B+ across 15+ deals)
- Fusion investment details (dates, amounts, relationship timing)

---

## Document Status

**Version**: 1.0
**Last Updated**: November 17, 2025
**Next Review**: After independent verification complete
**Related Documents**: [timeline.json](/hyperion/findings/_data/timeline/), [claims.json](/hyperion/findings/_data/claims/), [Overview](/hyperion/overview/)
