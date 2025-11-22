# Network Analysis: Hyperion Ventures Fund I

**General Partners:** Dillon Dunteman (Founder & GP), Henry Bellew (Co-GP)
**Analysis Date:** {{ hyperionNetwork.metadata.analysis_date }}
**Data Sources:** {{ hyperionNetwork.metadata.data_sources | join(", ") }}

---

## Methodology

**Data Processing:** Three LinkedIn connection CSVs enriched with `_I` (inferred from titles) and `_D` (Distill-verified) columns for ecosystem classification. Combined and deduplicated by Profile URL ({{ hyperionNetwork.overall_statistics.unique_connections_deduped }} unique from {{ hyperionNetwork.overall_statistics.total_connections_analyzed }} raw).

**Distill Research:** {{ hyperionNetwork.facet_analysis.deeptech.distill_high_relevance }} profiles researched via Distill MCP for deeptech classification.

**Limitations:** LinkedIn connections represent a partial network capture. Absence of connection ≠ absence of relationship. Use as directional signal, not definitive inventory.

---

## Executive Summary

Network analysis of {{ hyperionNetwork.overall_statistics.total_connections_analyzed }} LinkedIn connections across three categories (Harvard: {{ hyperionNetwork.overall_statistics.categories.harvard }}, VCPE: {{ hyperionNetwork.overall_statistics.categories.vcpe }}, Deeptech: {{ hyperionNetwork.overall_statistics.categories.deeptech }}).

**Key Finding:** Network supports Harvard alumni positioning and broad VC relationships, but reveals **material gaps** between claimed deeptech specialist expertise and actual network composition.

---

## 1. Network Analysis by Facet

### 1.1 Harvard Network ({{ hyperionNetwork.overall_statistics.categories.harvard }} connections)

📁 [View data](/hyperion/research/people/dillon-dunteman/network/harvard/)

**Claim:** "Youngest Harvard-led GP with Prod accelerator access (Cursor $9.9B, Mercor $10B, Devin $10B)"

**Prod Founders Validation:**

| Company | Founders Searched | Found |
|---------|-------------------|-------|
{% for search in hyperionNetwork.facet_analysis.harvard.prod_validation %}| {{ search.company }} | {{ search.founders_searched }} | {{ search.connections_found }} |
{% endfor %}

**Composition:**

| Category | Count | % |
|----------|-------|---|
| Founders/CEOs | {{ hyperionNetwork.facet_analysis.harvard.founder_count }} | {{ hyperionNetwork.facet_analysis.harvard.founder_percentage }} |
| Investors | {{ hyperionNetwork.facet_analysis.harvard.investor_count }} | {{ hyperionNetwork.facet_analysis.harvard.investor_percentage }} |
| Operators | {{ hyperionNetwork.facet_analysis.harvard.operator_count }} | {{ hyperionNetwork.facet_analysis.harvard.operator_percentage }} |

**Founders by Company Stage:**

| Stage | Count | Notable |
|-------|-------|---------|
| Late-stage/Public | {{ hyperionNetwork.facet_analysis.harvard.by_company_stage.late_stage_public.count }} | {{ hyperionNetwork.facet_analysis.harvard.by_company_stage.late_stage_public.notable | join(", ") or "—" }} |
| Growth (Series C+) | {{ hyperionNetwork.facet_analysis.harvard.by_company_stage.growth.count }} | {{ hyperionNetwork.facet_analysis.harvard.by_company_stage.growth.notable | join(", ") or "—" }} |
| Early-stage | {{ hyperionNetwork.facet_analysis.harvard.by_company_stage.early_stage.count }} | {{ hyperionNetwork.facet_analysis.harvard.by_company_stage.early_stage.notable | join(", ") | truncate(60) }} |

**Assessment:** {{ hyperionNetwork.facet_analysis.harvard.assessment }}

---

### 1.2 VCPE Network ({{ hyperionNetwork.overall_statistics.categories.vcpe }} connections)

📁 [View data](/hyperion/research/people/dillon-dunteman/network/vcpe/)

**Claim:** "Collaborators with 14 early-stage deeptech VCs + partnerships with 40+ generalist VCs across tiers"

**By Seniority:**

| Level | Count | % |
|-------|-------|---|
| GP (General Partner, MD, Founding Partner) | {{ hyperionNetwork.facet_analysis.vcpe.gp_count }} | {{ hyperionNetwork.facet_analysis.vcpe.gp_percentage }} |
| Partner | {{ hyperionNetwork.facet_analysis.vcpe.partner_count }} | {{ hyperionNetwork.facet_analysis.vcpe.partner_percentage }} |
| Principal/VP | {{ hyperionNetwork.facet_analysis.vcpe.principal_count }} | {{ hyperionNetwork.facet_analysis.vcpe.principal_percentage }} |
| Associate | {{ hyperionNetwork.facet_analysis.vcpe.associate_count }} | {{ hyperionNetwork.facet_analysis.vcpe.associate_percentage }} |

**Tier-1 Presence:** {{ hyperionNetwork.facet_analysis.vcpe.tier1_count }} connections across {{ hyperionNetwork.facet_analysis.vcpe.tier1_firms }}

**Assessment:** {{ hyperionNetwork.facet_analysis.vcpe.assessment }}

---

### 1.3 Deeptech Network ({{ hyperionNetwork.overall_statistics.categories.deeptech }} connections in deeptech.csv)

📁 [View data](/hyperion/research/people/dillon-dunteman/network/deeptech/)

**Claim:** "Deep vertical networks: Quantum (120+ founders contacted, 23 calls), fusion (met 20 startups)"

**Ecosystem (deeptech.csv facet):**

| Ecosystem | Count |
|-----------|-------|
| Generalist | {{ hyperionNetwork.facet_analysis.deeptech.generalist_count }} |
| AI/ML | {{ hyperionNetwork.facet_analysis.deeptech.ai_count }} |
| Fusion/Energy | {{ hyperionNetwork.facet_analysis.deeptech.fusion_count }} |
| Quantum | {{ hyperionNetwork.facet_analysis.deeptech.quantum_count }} |
| Robotics/Hardware | {{ hyperionNetwork.facet_analysis.deeptech.robotics_count }} |
| Biotech | {{ hyperionNetwork.facet_analysis.deeptech.biotech_count }} |

_Note: Quantum count ({{ hyperionNetwork.facet_analysis.deeptech.quantum_count }}) is for deeptech.csv facet only. Network-wide quantum connections = 9 (includes harvard.csv and vcpe.csv)._

**Assessment:** {{ hyperionNetwork.facet_analysis.deeptech.assessment }}

---

## 2. Deduplicated Network Overview

📁 [View all](/hyperion/research/people/dillon-dunteman/network/combined_deduped/) — {{ hyperionNetwork.overall_statistics.unique_connections_deduped }} unique ({{ hyperionNetwork.overall_statistics.duplicates_removed }} duplicates removed)

**Top Firms:**

| Firm | Connections | Type | Key Contacts |
|------|-------------|------|--------------|
{% for firm in hyperionNetwork.top_firms %}{% if loop.index <= 10 %}| {{ firm.firm }} | {{ firm.connections }} | {{ firm.firm_type }} | {{ firm.key_contacts | join(", ") | truncate(40) }} |
{% endif %}{% endfor %}

---

## 3. Strategic Relationship Validation

{{ hyperionNetwork.strategic_relationships.dataroom_context }}

### Central Hub (Filter Recipients)

| Firm | Connections | Contacts |
|------|-------------|----------|
{% for vc in hyperionNetwork.strategic_relationships.central_hub %}| **{{ vc.firm }}** | {{ vc.connections }} | {{ vc.contacts | join(", ") | truncate(60) }} |
{% endfor %}

### Deeptech Collaborators (14 claimed)

| Firm | Connections | Contacts |
|------|-------------|----------|
{% for vc in hyperionNetwork.strategic_relationships.deeptech_collaborators %}| {{ vc.firm }} | {{ vc.connections }} | {{ vc.contacts | join(", ") | truncate(50) or "—" }} |
{% endfor %}

### Tier-1 Generalists (40+ claimed)

| Firm | Connections | Key Contacts |
|------|-------------|--------------|
{% for vc in hyperionNetwork.strategic_relationships.tier1_generalists %}| {{ vc.firm }} | {{ vc.connections }} | {{ vc.contacts | first }}{% if vc.contacts | length > 1 %} (+{{ vc.contacts | length - 1 }}){% endif %} |
{% endfor %}

**Summary:** Central Hub {{ hyperionNetwork.strategic_relationships.summary.central_hub_coverage }}, Deeptech Collaborators {{ hyperionNetwork.strategic_relationships.summary.deeptech_collaborator_coverage }}, Tier-1 {{ hyperionNetwork.strategic_relationships.summary.tier1_coverage }}. Total named VC connections: {{ hyperionNetwork.strategic_relationships.summary.total_named_vc_connections }}.

---

## 4. Key Findings

### Strengths

{% for strength in hyperionNetwork.network_quality_assessment.strengths %}- **{{ strength.dimension | capitalize }}**: {{ strength.description }}
{% endfor %}

### Gaps

{% for gap in hyperionNetwork.network_quality_assessment.gaps %}
- {% if gap.risk_severity == "red_flag" %}🚩{% else %}🟡{% endif %} **{{ gap.description }}** — {{ gap.evidence }}
{% endfor %}

### Synthesis

{{ hyperionNetwork.key_findings.synthesis }}

**Next Steps:** {{ hyperionNetwork.key_findings.next_steps }}

---

_Generated {{ hyperionNetwork.metadata.analysis_date }}. Data: `_data/network.json`._
