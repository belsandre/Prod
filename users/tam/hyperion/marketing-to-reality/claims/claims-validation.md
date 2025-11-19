# Hyperion Ventures Claims Validation

**Last Updated**: {{ hyperionClaims.metadata.extraction_date }}
**Data Source**: [claims.json](/_data/claims.json)
**Methodology**: {{ hyperionClaims.metadata.methodology }}

---

## Executive Summary

This analysis validates {{ hyperionClaims.metadata.total_claims }} sub-claims across {{ hyperionClaims.metadata.key_claims }} key GP marketing claims by cross-referencing dataroom statements against independently verified timeline evidence using a 3-tier source classification system.

### Validation Results

| Status | Count | Percentage | Icon |
|--------|-------|------------|------|
| **Verified** | {{ hyperionClaims.executive_summary.verified.count }} | {{ hyperionClaims.executive_summary.verified.percentage }} | ✅ |
| **Partially Verified** | {{ hyperionClaims.executive_summary.partially_verified.count }} | {{ hyperionClaims.executive_summary.partially_verified.percentage }} | ⚠️ |
| **Unverified** | {{ hyperionClaims.executive_summary.unverified.count }} | {{ hyperionClaims.executive_summary.unverified.percentage }} | ❓ |
| **Conflicting Evidence** | {{ hyperionClaims.executive_summary.conflicting.count }} | {{ hyperionClaims.executive_summary.conflicting.percentage }} | ❌ |
| **Timing Issues** | {{ hyperionClaims.executive_summary.timing_issues.count }} | {{ hyperionClaims.executive_summary.timing_issues.percentage }} | 🕐 |

### Critical Issues Identified

{% if hyperionClaims.critical_issues %}
{% for issue in hyperionClaims.critical_issues %}
{{ loop.index }}. {{ issue }}
{% endfor %}
{% endif %}

---

## Verification Legend

| Icon | Status | Definition |
|------|--------|------------|
| ✅ | **Verified** | Multiple independent sources (Tier 3) confirm claim |
| ⚠️ | **Partial** | Claim confirmed by limited sources or with caveats/discrepancies |
| ❓ | **Unverified** | Only Tier 1 (dataroom) sources, no independent validation |
| ❌ | **Conflicting** | Evidence contradicts claim |
| 🕐 | **Timing Issue** | Timeline evidence challenges narrative sequencing |

**Source Tiers**:
- **Tier 1** (Entity-Controlled): Dataroom, GP website, pitch deck — lowest credibility
- **Tier 2** (Affiliated): LinkedIn, personal blogs, company websites — medium credibility
- **Tier 3** (Independent): News articles, funding announcements, third-party reports — highest credibility

---

## Claim-by-Claim Analysis

{% if hyperionClaims.key_claims %}
{% for claim in hyperionClaims.key_claims %}
### KEY CLAIM {{ claim.claim_id }}: {{ claim.claim_name }}

**Main Claim**: "{{ claim.main_claim }}"

**Overall Assessment**: {{ claim.status_icon }} **{{ claim.overall_assessment | capitalize }}**

---

{% if claim.sub_claims %}
{% for sub in claim.sub_claims %}
#### {{ sub.id }}: {{ sub.claim }}

**Status**: {{ sub.status_icon }} **{{ sub.status | replace("_", " ") | capitalize }}**

{% if sub.evidence %}
**Evidence**:
{% if sub.evidence.verified and sub.evidence.verified.length %}
- ✅ Verified: {{ sub.evidence.verified | formatArray }}
{% endif %}
{% if sub.evidence.partial and sub.evidence.partial.length %}
- ⚠️ Partial: {{ sub.evidence.partial | formatArray }}
{% endif %}
{% if sub.evidence.unverified and sub.evidence.unverified.length %}
- ❓ Unverified: {{ sub.evidence.unverified | formatArray }}
{% endif %}
{% endif %}

{% if sub.critical_gap %}
**Critical Gap**: {{ sub.critical_gap }}
{% endif %}

{% if sub.sources %}
**Sources**:
{% if sub.sources.tier_3 %}
- Tier 3 (Independent): {{ sub.sources.tier_3 | formatArray }}
{% endif %}
{% if sub.sources.tier_2 %}
- Tier 2 (Affiliated): {{ sub.sources.tier_2 | formatArray }}
{% endif %}
{% if sub.sources.tier_1 %}
- Tier 1 (Entity-Controlled): {{ sub.sources.tier_1 | formatArray }}
{% endif %}
{% endif %}

---

{% endfor %}
{% endif %}
{% endfor %}
{% endif %}

## Summary: Key Findings

{% if hyperionClaims.summary %}
### What's Verified ✅

{% if hyperionClaims.summary.verified %}
{% for item in hyperionClaims.summary.verified %}
{{ loop.index }}. {{ item }}
{% endfor %}
{% endif %}

### What's Unverified ❓

{% if hyperionClaims.summary.unverified %}
{% for item in hyperionClaims.summary.unverified %}
{{ loop.index }}. {{ item }}
{% endfor %}
{% endif %}

### What's Concerning ⚠️❌

{% if hyperionClaims.summary.concerning %}
{% for item in hyperionClaims.summary.concerning %}
{{ loop.index }}. {{ item }}
{% endfor %}
{% endif %}
{% endif %}

---

## Recommendations

{% if hyperionClaims.recommendations %}
{% for rec in hyperionClaims.recommendations %}
### {{ rec.priority }} Priority

{% if rec.items %}
{% for item in rec.items %}
{{ loop.index }}. **{{ item.title }}** — {{ item.description }}
{% endfor %}
{% endif %}
{% endfor %}
{% endif %}

---

## Methodology Notes

**3-Tier Source Classification**:
- **Tier 1** (Entity-Controlled): Dataroom, GP website — lowest credibility
- **Tier 2** (Affiliated): LinkedIn, company websites — medium credibility
- **Tier 3** (Independent): News, funding announcements, third-party reports — highest credibility

**Research Limitations**:
- Only 6 of 24 companies (25%) have detailed research
- Private company data scarce for early-stage investments
- Cannot verify internal communications or private interactions
- Fusion investment dates unknown (4 companies undated)

**Key Pattern**: 100% of GP value-add claims sourced from Tier 1 (dataroom) only with ZERO Tier 3 verification. This is the most critical due diligence gap.

---

**Related Documents**:
- [Portfolio Assessment](/hyperion/findings/portfolio-assessment/) — Company-by-company quality analysis
- [GP Analysis](/hyperion/findings/gp-analysis/) — Detailed assessment of both General Partners
- [Network Analysis](/hyperion/findings/network-analysis/) — LinkedIn connections and deal flow relationships
- [Timeline](/hyperion/findings/timeline/) — Chronological events with source verification
- [Claims Data](/hyperion/findings/_data/claims/) — Complete structured data
