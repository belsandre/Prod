# Portfolio Assessment - {{ hyperionPortfolio.fund_name }}

**Date**: {{ hyperionPortfolio.analysis_date }}
**Companies Analyzed**: {{ hyperionPortfolio.portfolio_overview.researched }} of {{ hyperionPortfolio.portfolio_overview.total_companies }} (winners + emerging = effective full portfolio coverage)
**Overall Health**: **✅ {{ hyperionPortfolio.overall_health }}** ({{ hyperionPortfolio.health_descriptor }})

---

## Executive Summary

{{ hyperionPortfolio.executive_summary.strength }}

**Primary Risk**: {{ hyperionPortfolio.executive_summary.primary_risk }}

**Investment Thesis**: {{ hyperionPortfolio.executive_summary.thesis }}

---

## Portfolio Composition

_See [portfolio.json](../_data/portfolio/) for complete data_

### By Category

| Category | Count | % | Examples |
|----------|-------|---|----------|
| **Winners** | {{ hyperionPortfolio.portfolio_overview.by_category.winners }} | {{ ((hyperionPortfolio.portfolio_overview.by_category.winners / hyperionPortfolio.portfolio_overview.researched) * 100) | round }}% | {% for c in hyperionPortfolio.companies.winners %}{{ c.name }}{% if not loop.last %}, {% endif %}{% endfor %} |
| **Emerging** | {{ hyperionPortfolio.portfolio_overview.by_category.emerging }} | {{ ((hyperionPortfolio.portfolio_overview.by_category.emerging / hyperionPortfolio.portfolio_overview.researched) * 100) | round }}% | {% for c in hyperionPortfolio.companies.emerging %}{{ c.name }}{% if not loop.last %}, {% endif %}{% endfor %} |
| **Other** | {{ hyperionPortfolio.portfolio_overview.by_category.other }} | {{ ((hyperionPortfolio.portfolio_overview.by_category.other / hyperionPortfolio.portfolio_overview.researched) * 100) | round }}% | {% for c in hyperionPortfolio.companies.other %}{{ c.name }}{% if not loop.last %}, {% endif %}{% endfor %} |
| **Red Flags** | {{ hyperionPortfolio.portfolio_overview.by_category.red_flags }} | {{ ((hyperionPortfolio.portfolio_overview.by_category.red_flags / hyperionPortfolio.portfolio_overview.researched) * 100) | round }}% | {% for c in hyperionPortfolio.companies.red_flags %}{{ c.name }}{% if not loop.last %}, {% endif %}{% endfor %} |
| **No Research** | {{ hyperionPortfolio.portfolio_overview.by_category.unresearched }} | {{ ((hyperionPortfolio.portfolio_overview.by_category.unresearched / hyperionPortfolio.portfolio_overview.total_companies) * 100) | round }}% | Includes {{ hyperionPortfolio.portfolio_overview.writedowns }} writedowns to $0 |

**Thesis Coherence**: ✅ **Strong**

Portfolio shows coherent deeptech focus (quantum, AI robotics, fusion, semiconductors). Winners and emerging companies analyzed represent most important holdings for thesis assessment. Known writedowns ({{ hyperionPortfolio.portfolio_overview.writedowns }} companies to $0) are normal for VC portfolios and don't indicate thesis incoherence.

### By Sector

| Sector | Count | Notable Companies |
|--------|-------|-------------------|
{% for sector in hyperionPortfolio.by_sector %}| **{{ sector.sector }}** | {{ sector.count }} | {{ sector.notable | join(", ") }} |
{% endfor %}

Note: All {{ hyperionPortfolio.portfolio_overview.total_companies }} companies from dataroom xlsx. Notable column highlights researched companies.

**Analysis**: Strong concentration in **deeptech** (quantum, AI, fusion, semiconductors). Enterprise SaaS and Fintech represent diversification. If Figure and Quantinuum compress, no clear backup winners visible.

### Stage Evolution

| Stage | Count at Entry | Count Today |
|-------|----------------|-------------|
| Pre-Seed/Seed | {{ hyperionPortfolio.stage_evolution.at_entry.pre_seed_seed }} | {{ hyperionPortfolio.stage_evolution.current.pre_seed_seed }} |
| Series A | {{ hyperionPortfolio.stage_evolution.at_entry.series_a }} | {{ hyperionPortfolio.stage_evolution.current.series_a }} |
| Series B/C | {{ hyperionPortfolio.stage_evolution.at_entry.series_bc }} | {{ hyperionPortfolio.stage_evolution.current.series_bc }} |
| Late Stage (Series C+) | {{ hyperionPortfolio.stage_evolution.at_entry.late_stage }} | {{ hyperionPortfolio.stage_evolution.current.late_stage }} |

Note: All {{ hyperionPortfolio.portfolio_overview.total_companies }} companies from dataroom xlsx

**Thesis Coherence**: ✅ **Strong early-stage focus**

{{ hyperionPortfolio.stage_evolution.analysis }}

---

## Defensibility Assessment

**Primary Moat Types** (researched companies):
| Moat Type | Count | Assessment |
|-----------|-------|------------|
{% for moat in hyperionPortfolio.defensibility.by_moat %}| **{{ moat.type }}** | {{ moat.count }} | {{ moat.assessment }} ({{ moat.notes }}) |
{% endfor %}

**Analysis**: {{ hyperionPortfolio.defensibility.analysis }}

---

## Performance Analysis

### Winners (Major Fund Drivers)

{% for company in hyperionPortfolio.companies.winners %}
#### {{ company.name }} {{ company.icon }}
- **Dataroom**: {{ company.dataroom.check }} check at {{ company.dataroom.moic }}x MOIC (based on {{ company.dataroom.valuation_basis }} valuation){% if company.research %}; research shows {{ company.research.current_valuation }} valuation - {{ company.research.valuation_note }}{% endif %} [Source: {% for src in company.sources %}{% if src.type == "dataroom" %}{{ src.name }} ({{ src.date }}){% endif %}{% endfor %}{% for src in company.sources %}{% if src.type == "research" %}, [{{ src.name }}]({{ src.path }}){% endif %}{% endfor %}]
- **Portfolio Contribution**: {{ company.portfolio_contribution }}
- **Status**: {{ company.status }}
- **Strength**: {{ company.strength }}
- **Risk**: ⚠️ **{{ company.risk.level }}** - {{ company.risk.description }}
{% endfor %}

---

### Emerging (Featured Portfolio)

{% for company in hyperionPortfolio.companies.emerging %}
#### {{ company.name }} {{ company.icon }}
- **Dataroom**: {{ company.dataroom.check }} check{% if company.dataroom.check_note %} ({{ company.dataroom.check_note }}){% endif %} at {{ company.dataroom.moic }}x MOIC{% if company.dataroom.moic_note %} ({{ company.dataroom.moic_note }}){% endif %} → {{ company.dataroom.current_valuation }} current valuation [Source: {% for src in company.sources %}{% if src.type == "dataroom" %}{{ src.name }} ({{ src.date }}){% endif %}{% endfor %}]
- **Status**: {{ company.status }}
- **Opportunity**: {{ company.opportunity }}
- **Risk**: {{ company.risk }} [Source: {% for src in company.sources %}{% if src.type == "research" %}[{{ src.name }}]({{ src.path }}){% if not loop.last %}, {% endif %}{% endif %}{% endfor %}]
{% endfor %}

---

### Red Flags

{% for company in hyperionPortfolio.companies.red_flags %}
#### {{ company.name }} {{ company.icon }}
- **Dataroom**: {{ company.dataroom.check }} check{% if company.dataroom.check_note %} ({{ company.dataroom.check_note }}){% endif %} at {{ company.dataroom.moic }}x MOIC{% if company.dataroom.moic_note %} ({{ company.dataroom.moic_note }}){% endif %} → {{ company.dataroom.current_valuation }} current valuation [Source: {% for src in company.sources %}{% if src.type == "dataroom" %}{{ src.name }} ({{ src.date }}){% endif %}{% endfor %}]
- **Status**: {{ company.status }}
- **Opportunity**: {{ company.opportunity }}
- **Concern**: {{ company.concern }}
- **Evidence**: {{ company.evidence }}
- **Pattern**: {{ company.pattern }}
{% endfor %}

---

### Other (Stable/Early)

{% for company in hyperionPortfolio.companies.other %}
**{{ company.name }}**: {{ company.status }} [Source: {% for src in company.sources %}{% if src.type == "dataroom" %}{{ src.name }} ({{ src.date }}){% endif %}{% if src.type == "research" %}, [{{ src.name }}]({{ src.path }}){% endif %}{% endfor %}]

{% endfor %}

---

### Companies Without Research ({{ hyperionPortfolio.portfolio_overview.by_category.unresearched }} companies, {{ ((hyperionPortfolio.portfolio_overview.by_category.unresearched / hyperionPortfolio.portfolio_overview.total_companies) * 100) | round }}%)

Includes **{{ hyperionPortfolio.portfolio_overview.writedowns }} writedowns to $0** ({% for c in hyperionPortfolio.companies.unresearched %}{% if c.moic == 0 %}{{ c.name }}{% if not loop.last %}, {% endif %}{% endif %}{% endfor %}) and **{{ hyperionPortfolio.portfolio_overview.by_category.unresearched - hyperionPortfolio.portfolio_overview.writedowns }} other companies** with limited data. Notable:

{% for c in hyperionPortfolio.companies.unresearched %}{% if c.moic > 1.5 %}- **{{ c.name }}**: {{ c.entry }} entry → {{ c.current }} current ({{ c.moic }}x){% if c.note %} - {{ c.note }}{% endif %}
{% endif %}{% endfor %}
{% for c in hyperionPortfolio.companies.unresearched %}{% if c.moic == 1.0 %}- **{{ c.name }}**: {{ c.entry }} entry → {{ c.current }} current ({{ c.moic }}x){% if c.note %} - {{ c.note }}{% endif %}
{% endif %}{% endfor %}

**Assessment**: Lack of research on {{ ((hyperionPortfolio.portfolio_overview.by_category.unresearched / hyperionPortfolio.portfolio_overview.total_companies) * 100) | round }}% of portfolio prevents full health assessment, but presence of {{ hyperionPortfolio.portfolio_overview.writedowns }} writedowns and flat companies suggests execution challenges beyond the two winners.

---

## Key Risk

### {{ hyperionPortfolio.key_risk.title }} ⚠️

**Problem**: {{ hyperionPortfolio.key_risk.problem }}

**Evidence**:
{% for evidence in hyperionPortfolio.key_risk.evidence %}
- {{ evidence }}
{% endfor %}

**Recommendation**: {{ hyperionPortfolio.key_risk.recommendation }}

---

## Recommendations

### Critical Actions

{% for action in hyperionPortfolio.recommendations.critical %}
{{ loop.index }}. **{{ action.action }}**: {{ action.details }}
{% endfor %}

### Further Investigation

{% for item in hyperionPortfolio.recommendations.further_investigation %}
{{ loop.index }}. **{{ item.area }}**: {{ item.why }} | Questions: {% for q in item.questions %}{{ q }}{% if not loop.last %} {% endif %}{% endfor %}
{% endfor %}

---

**Data**: [portfolio.json](../_data/portfolio/)
**Source Tiers**: {{ hyperionPortfolio.source_tier_summary.independent }} independent, {{ hyperionPortfolio.source_tier_summary.affiliated }} affiliated, {{ hyperionPortfolio.source_tier_summary.dataroom }} dataroom
**Version**: {{ hyperionPortfolio.version }} | **Updated**: {{ hyperionPortfolio.last_updated }}
