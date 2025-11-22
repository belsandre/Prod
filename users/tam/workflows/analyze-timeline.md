# Analyze Timeline Workflow

## Purpose

Construct an objective timeline that validates (or contradicts) the fund's marketing narrative. Extract only claims-relevant events, apply timing analysis, and identify critical gaps.

**Key insight**: Timing reveals truth. Claims about being "early" or "prescient" can be verified against when events actually happened.

## Inputs

| Input | Description |
|-------|-------------|
| Dataroom folder | Primary source materials (decks, memos, etc.) |
| Research folder | External research, news, filings |
| claims-analysis.md | KEY claims to validate (already extracted) |

## Outputs

| File | Purpose |
|------|---------|
| `_data/timeline.json` | All content (events, findings, priorities) |
| `timeline-analysis.md` | Pure template (no substantive content) |

---

## Methodology

### Phase 1: Claims-Anchored Event Extraction

Extract events **only if they validate or invalidate a KEY claim** from claims-analysis.md.

For each event, capture:
- `date`: YYYY-MM-DD, YYYY-MM, or YYYY-QX
- `event`: Brief description (one line)
- `claim_linkage`: Which KEY claim(s) this validates
- `source`: Where this came from
- `source_type`: dataroom | affiliated | independent
- `verification`: verified | partial | unverified | conflicting
- `note`: Optional concern or context

**Extraction priorities**:
1. Investment dates and outcomes (track record)
2. Exits and returns (performance)
3. Thought leadership / publications (expertise timing)
4. Employment and organizational changes (experience)

### Phase 2: Timing Validation & Gap Analysis

1. Apply timing rules to each event
2. Flag discrepancies between claimed timing and actual timing
3. Identify critical omissions (failed investments, gaps, conflicts)
4. Generate verification priorities

---

## Source Types & Verification

| Source Type | Description | Verification Impact |
|-------------|-------------|---------------------|
| **Dataroom** | Entity-controlled (decks, website) | Claims remain "unverified" if only source |
| **Affiliated** | Portfolio co descriptions, co-investor quotes | Supports "partial" verification |
| **Independent** | News, SEC filings, third-party databases | Required for "verified" status |

| Status | Meaning |
|--------|---------|
| ✓ Verified | Independent sources confirm claim AND timing |
| ⚠ Partial | Directionally true but timing uncertain, or only affiliated sources |
| ? Unverified | Only dataroom sources support claim |
| ✗ Conflicting | Independent sources contradict claim |

---

## Timing Rules (Quick Reference)

**"Early Investor"**: >90 days before consensus = verified; <90 days = partial; after consensus = conflicting

**"Thought Leadership"**: Publication >30 days before investment = predictive; within ±30 days = concurrent; after = retroactive

---

## Output Schema

```json
{
  "metadata": {
    "entity": "Fund Name",
    "extraction_date": "YYYY-MM-DD",
    "coverage_period": "YYYY to YYYY",
    "total_events": 0,
    "source_distribution": {"dataroom": 0, "affiliated": 0, "independent": 0}
  },
  "timeline": [
    {
      "date": "YYYY-MM-DD",
      "event": "Brief description",
      "claim_linkage": ["CLAIM_ID"],
      "source": "Document name",
      "source_type": "dataroom|affiliated|independent",
      "verification": "verified|partial|unverified|conflicting",
      "note": "Optional"
    }
  ],
  "findings": [
    {
      "type": "verified|concern",
      "severity": "green|yellow|red",
      "title": "Short title",
      "description": "What was found",
      "implication": "Why it matters"
    }
  ],
  "verification_priorities": ["Items to investigate"]
}
```

---

## Quality Checklist

- [ ] Every event links to at least one KEY claim
- [ ] No redundant events (each fact appears once)
- [ ] Source type assigned to every event
- [ ] Findings section consolidates patterns and gaps (no redundancy)
- [ ] JSON validates properly
- [ ] Template renders without hardcoded content

---

## Key Principles

1. **Claims-driven** — Skip events that don't validate/invalidate claims
2. **One fact, one place** — Never repeat information
3. **Source-conscious** — Always note who said it
4. **Gaps matter** — What's missing is as important as what's present
5. **30-50 events max** — Not exhaustive chronology
