# Timeline Analysis - {{ hyperionTimeline.metadata.entity }}

**Last Updated**: {{ hyperionTimeline.metadata.extraction_date }}
**Coverage**: {{ hyperionTimeline.metadata.coverage_period }}
**Events**: {{ hyperionTimeline.metadata.total_events }} ({{ hyperionTimeline.metadata.source_distribution.independent }} independent, {{ hyperionTimeline.metadata.source_distribution.affiliated }} affiliated, {{ hyperionTimeline.metadata.source_distribution.dataroom }} dataroom)

---

## Key Findings

{% for finding in hyperionTimeline.findings %}
{% if finding.severity == "green" %}### ✅ {{ finding.title }}{% elif finding.severity == "yellow" %}### 🟡 {{ finding.title }}{% elif finding.severity == "red" %}### 🔴 {{ finding.title }}{% endif %}

{{ finding.description }}

**Implication**: {{ finding.implication }}

{% endfor %}

---

## Verification Priorities

{% for priority in hyperionTimeline.verification_priorities %}
{{ loop.index }}. {{ priority }}
{% endfor %}

---

## Chronology

{% for event in hyperionTimeline.timeline %}
**{{ event.date }}** | {{ event.event }}
- Claims: {{ event.claim_linkage | join(", ") }}
- Source: {{ event.source }} ({{ event.source_type | capitalize }}) | {% if event.verification == "verified" %}✓ Verified{% elif event.verification == "partial" %}⚠ Partial{% elif event.verification == "unverified" %}? Unverified{% elif event.verification == "conflicting" %}✗ Conflicting{% else %}{{ event.verification }}{% endif %}{% if event.note %}
- Note: {{ event.note }}{% endif %}

{% endfor %}

---

## Source Quality

| Source Type | Count | % |
|-------------|-------|---|
| Independent | {{ hyperionTimeline.metadata.source_distribution.independent }} | {{ ((hyperionTimeline.metadata.source_distribution.independent / hyperionTimeline.metadata.total_events) * 100) | round }}% |
| Affiliated | {{ hyperionTimeline.metadata.source_distribution.affiliated }} | {{ ((hyperionTimeline.metadata.source_distribution.affiliated / hyperionTimeline.metadata.total_events) * 100) | round }}% |
| Dataroom | {{ hyperionTimeline.metadata.source_distribution.dataroom }} | {{ ((hyperionTimeline.metadata.source_distribution.dataroom / hyperionTimeline.metadata.total_events) * 100) | round }}% |

**Verification Legend**: ✓ Verified (independent confirmation) | ⚠ Partial (directionally true) | ? Unverified (dataroom only) | ✗ Conflicting

---

## Related Documents

- [Claims Analysis](./claims-analysis)
- [People Analysis](./people-analysis)
- [Portfolio Analysis](./portfolio-analysis)
- [Network Analysis](./network-analysis)
