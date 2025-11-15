# Reference Check Identifier Workflow

## Objective
Analyze a GP/fund dataroom to identify investors who should be reference-checked, prioritized by relationship value and claims made.

## Input Requirements
- Path to dataroom folder containing pitch decks, track records, marketing materials, investor updates, or other documents
- (Optional) GP/fund name for context

## Processing Instructions

### 1. Dataroom Analysis
Systematically scan all documents for investor mentions:
- **Text extraction**: Use text-converter skill for PDFs/presentations if needed
- **Document types**: Prioritize pitch decks, track records, case studies, investor letters, portfolio updates
- **Search patterns**: Look for investor names, firm names, co-investment language, relationship descriptors

### 2. Relationship Classification & Prioritization

Extract investors into three priority tiers:

#### **HIGH PRIORITY** - Special Relationships
Investors with claimed special interactions or highlighted relationships:
- **Mentors or advisors** ("X mentors us", "guidance from Y")
- **Deal flow partners** ("brings us deals", "we source from", "refers opportunities")
- **Tracking relationships** ("tracks our deals", "follows our investments closely")
- **Preferential access** ("anchor investor", "first call", "strategic partner")
- **Frequent co-investors** (mentioned in 3+ deals)
- **Explicitly highlighted** (testimonials, featured prominently, case studies)

#### **MEDIUM PRIORITY** - Transactional Relationships
Investors with concrete investment history:
- **Co-investors** (invested alongside in specific deals)
- **Follow-on investors** (backed portfolio companies in later rounds)
- **Named in multiple contexts** (appears 2-3 times across documents)

#### **LOW PRIORITY** - Tangential Mentions
- Single mentions without context
- General network references
- Passive relationships

### 3. Evidence Collection

For each identified investor, capture:
1. **Investor name/firm**
2. **Priority tier** (High/Medium/Low)
3. **Relationship type** (specific: co-investor, mentor, deal flow source, etc.)
4. **Exact claim/context** (verbatim quote or paraphrase)
5. **Source document** (filename, page/slide number if available)
6. **Deal/portfolio context** (which company/investment triggered the mention)

### 4. Output Format

Create a markdown file: `reference-check-targets.md`

Structure:
```markdown
# Reference Check Targets: [GP/Fund Name]

## Summary
- Total investors identified: X
- High priority: X | Medium priority: X | Low priority: X

---

## HIGH PRIORITY REFERENCES

### [Investor/Firm Name]
- **Relationship**: [e.g., Deal flow partner, Mentor, Frequent co-investor]
- **Claim/Context**: "[Exact quote or detailed paraphrase]"
- **Source**: [filename.pdf, page X / slide X]
- **Deal Context**: [Portfolio company name if applicable]
- **Why Reference**: [Brief explanation of what to verify]

[Repeat for each high-priority investor]

---

## MEDIUM PRIORITY REFERENCES

### [Investor/Firm Name]
- **Relationship**: [e.g., Co-investor, Follow-on investor]
- **Context**: "[Brief description]"
- **Source**: [filename.pdf]
- **Deal Context**: [Portfolio company name]

[Repeat for each medium-priority investor]

---

## LOW PRIORITY REFERENCES
[Brief list format acceptable for low-priority]
- [Investor Name]: [One-line context] - Source: [filename]

---

## Red Flags / Notes
[Any suspicious patterns, exaggerations, or verification priorities]
```

### 5. Quality Standards

**CRITICAL REQUIREMENTS**:
- ✅ **Source every claim**: Each investor mention must cite specific document + location
- ✅ **Verbatim quotes for high-priority**: Use exact language for key claims
- ✅ **Distinguish fact from claim**: Note what GP claims vs. what's objectively stated
- ✅ **Flag vague language**: Highlight weasel words ("several investors", "top-tier funds" without names)
- ✅ **Cross-reference**: Note if investor appears in multiple documents (strengthens priority)
- ✅ **Track deal context**: Always link investor mentions to specific portfolio companies when applicable

**What NOT to include**:
- ❌ Generic LP lists without specific claims
- ❌ Conference/event co-attendees without interaction claims
- ❌ Industry name-drops without direct relationship evidence
- ❌ Inferred relationships (only explicit claims or documented co-investments)

### 6. Verification Focus Areas

For each high-priority reference, suggest specific questions:
- **Mentors**: "How frequently do you interact? What specific guidance have you provided?"
- **Deal flow**: "How many deals have you shared? What's the quality/conversion rate?"
- **Co-investors**: "What's your assessment of their diligence/value-add? Would you co-invest again?"
- **Tracking claims**: "Do you actively track this GP? What's your level of engagement?"

## Output Deliverables

1. **reference-check-targets.md** - Main structured output (as formatted above)
2. **investor-mention-map.csv** (optional) - Spreadsheet with columns:
   - Investor Name | Priority | Relationship Type | Claim | Source | Page | Deal Context

## Notes for Processing

- **Speed vs. thoroughness**: For large datarooms (50+ docs), prioritize pitch decks, track records, and case studies first
- **Name normalization**: Watch for same investor mentioned different ways (e.g., "a16z" vs "Andreessen Horowitz")
- **Confidence levels**: If a relationship is ambiguous, note it and tier conservatively
- **Resume capability**: If interrupted, document which files have been processed

## Success Criteria

Output is complete when:
1. All key documents scanned (pitch deck, track record, portfolio materials)
2. Every investor mention is classified and sourced
3. High-priority references have verbatim quotes + context
4. Clear verification questions provided for each tier
5. No unsourced claims in final output
