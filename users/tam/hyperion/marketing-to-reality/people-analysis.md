---
title: People Analysis
---

# People Analysis: {{ hyperionPeople.fund_name }}

**Entity:** {{ hyperionPeople.entity_name }}
**General Partners:** {% for gp in hyperionPeople.general_partners %}{{ gp.name }} ({{ gp.role }}){% if not loop.last %}, {% endif %}{% endfor %}
**Analysis Date:** {{ hyperionPeople.analysis_date }}

**Analysis Goal:** {{ hyperionPeople.analysis_goal }}

**Sources:** {{ hyperionPeople.sources.dataroom }}, research/people ({{ hyperionPeople.sources.research_people }}), claims files ({{ hyperionPeople.sources.claims_files }}), independent sources ({{ hyperionPeople.sources.independent }})

**Process:** {{ hyperionPeople.sources.process }}

---

## Executive Summary

{{ hyperionPeople.risk_synthesis.summary }}

**{{ hyperionPeople.general_partners[0].name }} ({{ hyperionPeople.general_partners[0].role }}):** {{ hyperionPeople.executive_summary.dillon_summary }}

**{{ hyperionPeople.general_partners[1].name }} ({{ hyperionPeople.general_partners[1].role }}):** {{ hyperionPeople.executive_summary.henry_summary }}

**Investment Recommendation:** {{ hyperionPeople.executive_summary.investment_recommendation }}

---

## GP Profiles

{% for gp in hyperionPeople.general_partners %}
### {{ gp.name }} ({{ gp.role }})

**Background:**

Graduated {{ gp.verified_credentials.education.institution }} with {{ gp.verified_credentials.education.degree }} (Class of {{ gp.verified_credentials.education.graduation_year }}){% if gp.verified_credentials.education.additional %}, {{ gp.verified_credentials.education.additional }}{% endif %}{% if gp.verified_credentials.education.honors %}, {{ gp.verified_credentials.education.honors }}{% endif %}{% if gp.verified_credentials.education.secondary %} with secondary in {{ gp.verified_credentials.education.secondary }}{% endif %}. {% if gp.verified_credentials.education.additional_coursework %}Coursework in {{ gp.verified_credentials.education.additional_coursework }}. {% endif %}{% if gp.verified_credentials.education.activities %}Active in {{ gp.verified_credentials.education.activities }}{% if gp.verified_credentials.education.athletic_achievements %} with championship achievements including {{ gp.verified_credentials.education.athletic_achievements }}{% endif %}. {% endif %}Professional experience {% for job in gp.verified_credentials.employment %}at {{ job.company }} ({{ job.years }}){% if job.description %} {{ job.description }}{% endif %}{% if not loop.last %}, followed by {% else %}. {% endif %}{% endfor %}{% if gp.thought_leadership %}Launched {{ gp.thought_leadership.platform }} around {{ gp.thought_leadership.launch_date }} ({{ gp.thought_leadership.label }}) with {{ gp.thought_leadership.assessment }} (only {{ gp.thought_leadership.total_posts }} posts from {{ gp.thought_leadership.time_period }}—insufficient for credible thought leadership). {% endif %}{% if gp.personal_portfolio %}Personal angel portfolio of {{ gp.personal_portfolio.total_companies }} startups ({{ gp.personal_portfolio.time_period }}) with claimed {{ gp.personal_portfolio.claimed_tvpi }} TVPI / {{ gp.personal_portfolio.claimed_irr }} IRR ({{ gp.personal_portfolio.verification_status }}). {% endif %}{% if gp.network_validation %}Research captured network connections across {{ gp.network_validation.categories_captured | join(", ") }} categories, though this represents only a partial subset (total network size unknown). {% endif %}{% if gp.verified_credentials.employment[0].note %}Listed professional experience at {{ gp.verified_credentials.employment[0].company }} as "{{ gp.verified_credentials.employment[0].role }}" ({{ gp.verified_credentials.employment[0].note }}). {% if gp.verified_credentials.employment[0].claimed_work %}Claimed work {{ gp.verified_credentials.employment[0].claimed_work }}. {% endif %}{% endif %}{% if gp.verified_credentials.current_status %}Currently "{{ gp.verified_credentials.current_status }}". {% endif %}Approximately {{ gp.age_range }} with ~{{ gp.years_experience }} years professional experience.

**Key Claims vs Evidence:**

| Claim | Evidence Source | Status |
|-------|----------------|--------|
{%- for claim in gp.key_attribution_claims %}
| {{ claim.claim }} | {{ claim.verification_tier }} | {{ claim.status_text }} |
{%- endfor %}

**Material Concerns:**

{% for concern in gp.material_concerns %}
{{ loop.index }}. **{{ concern.title }}:** {{ concern.description }}

{% endfor %}
{% if gp.dataroom_presence %}
**Dataroom Presence:** Appears on {{ gp.dataroom_presence.pages }} pages, {{ gp.dataroom_presence.case_studies }} case studies, {{ gp.dataroom_presence.testimonials }} testimonials. {{ gp.dataroom_presence.role_definition }}

{% endif %}
---

{% endfor %}

## Team Structure

**Effective Model:** {{ hyperionPeople.team_structure_assessment.effective_model }}

**Critical Structural Concerns:**

- **Single point of failure:** All sourcing ({{ hyperionPeople.team_structure_assessment.single_point_of_failure.sourcing }}), technical diligence ({{ hyperionPeople.team_structure_assessment.single_point_of_failure.technical_diligence }}), and portfolio support ({{ hyperionPeople.team_structure_assessment.single_point_of_failure.portfolio_support }}, {{ hyperionPeople.team_structure_assessment.single_point_of_failure.case_studies }}) rest with one person. {{ hyperionPeople.team_structure_assessment.single_point_of_failure.redundancy }}.

- **Capacity constraints:** {{ hyperionPeople.team_structure_assessment.capacity_constraints.concern }}. Typical ratio: {{ hyperionPeople.team_structure_assessment.capacity_constraints.typical_ratio }}.

- **Economics alignment unclear:** If carry split is equal/near-equal, would not align with apparent {{ hyperionPeople.team_structure_assessment.economics_alignment.dillon_experience }} vs. {{ hyperionPeople.team_structure_assessment.economics_alignment.henry_experience }} experience and dramatic contribution disparity ({{ hyperionPeople.team_structure_assessment.economics_alignment.dillon_testimonials }} testimonials vs. {{ hyperionPeople.team_structure_assessment.economics_alignment.henry_testimonials }}, {{ hyperionPeople.team_structure_assessment.economics_alignment.dillon_case_studies }} case studies vs. {{ hyperionPeople.team_structure_assessment.economics_alignment.henry_case_studies }}, {{ hyperionPeople.team_structure_assessment.economics_alignment.dillon_background }} vs. {{ hyperionPeople.team_structure_assessment.economics_alignment.henry_background }} background).

- **Co-GP underrepresentation:** Material gap between "{{ hyperionPeople.team_structure_assessment.co_gp_underrepresentation.title }}" title and minimal dataroom presence ({{ hyperionPeople.team_structure_assessment.co_gp_underrepresentation.dataroom_pages }} pages) suggests {{ hyperionPeople.team_structure_assessment.co_gp_underrepresentation.concern }}.

**Strengths:** {% for strength in hyperionPeople.team_structure_assessment.strengths %}{{ strength }}. {% endfor %}

**Weaknesses:** {% for weakness in hyperionPeople.team_structure_assessment.weaknesses %}{{ weakness }}{% if not loop.last %}, {% else %}.{% endif %}{% endfor %}

---

## Required Validations

### Critical (Must Resolve Before Investment)

{% for gap in hyperionPeople.critical_people_gaps %}
{{ loop.index }}. **{{ gap.title }}**
   - **Why it matters:** {{ gap.why_it_matters }}
   - **What to ask:** {{ gap.what_to_ask }}

{% endfor %}

### Important (Helpful for Complete Assessment)

{% for validation in hyperionPeople.important_validations %}
- {{ validation }}
{% endfor %}
