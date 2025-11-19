# Analysis Flow & Dependencies

**Created**: 2025-11-18
**Purpose**: Document how analyses feed into each other and the order of completion

---

## Analysis Flow

```mermaid
flowchart TD
    subgraph Sources["Research Sources"]
        DR[Dataroom Materials]
        LI[LinkedIn Network Data]
        PR[Public Records & News]
        CO[Company Research]
    end

    subgraph Extraction["Data Extraction"]
        TL[Timeline<br/>47 events]
        NW[Network<br/>637 connections]
        PF[Portfolio<br/>14 companies]
        CL[Claims<br/>30 sub-claims]
        GP[GP Profiles<br/>2 GPs]
    end

    subgraph Analysis["Analysis Layer"]
        TA[Timeline Analysis<br/>Retroactive framing risk]
        NA[Network Analysis<br/>Connection gaps]
        PA[Portfolio Assessment<br/>Concentration risk]
        CV[Claims Validation<br/>40% error rate]
        GA[GP Analysis<br/>Henry zero involvement]
    end

    subgraph Findings["Key Findings"]
        F1[Figure AI concentration >50%]
        F2[GP value-add 100% unverified]
        F3[Funding discrepancies]
        F4[Harvard network gaps 0/3 verified]
        F5[Henry Bellew zero portfolio involvement]
    end

    subgraph Recommendations["Action Items"]
        CR[Critical<br/>7 items]
        HP[High-Priority<br/>3 items]
        RC[Reference Check List]
    end

    ES[Executive Summary<br/>7.5/10 Assessment]

    %% Source to Extraction
    DR --> TL & PF & CL & GP
    LI --> NW & GP
    PR --> TL & PF & CV
    CO --> PF & CV

    %% Extraction to Analysis
    TL --> TA
    NW --> NA
    PF --> PA
    CL --> CV
    GP --> GA

    %% Analysis to Findings
    PA --> F1
    CV --> F2 & F3
    NA --> F4
    GA --> F5

    %% Findings to Recommendations
    F1 --> CR
    F2 --> CR
    F3 --> CR
    F4 --> CR
    F5 --> CR
    PA --> HP
    TA --> HP

    %% Recommendations to Summary
    CR --> ES
    HP --> ES
    RC --> ES

    %% Cross-dependencies
    CV -.-> PA
    NA -.-> GA
    TA -.-> CV
```

---

## Analysis Order (Chronological)

### Phase 1: Data Collection
1. **Dataroom ingestion** - Convert raw materials to markdown
2. **LinkedIn export** - Extract 637 connections
3. **Company research** - 14 companies, 3-9 sources each
4. **Public records search** - Funding announcements, news articles

### Phase 2: Data Extraction
5. **Timeline extraction** - 47 events from all sources
6. **Network mapping** - Categorize 637 connections by firm type
7. **Portfolio structuring** - 14 companies with metrics
8. **Claims inventory** - 30 sub-claims across 6 categories
9. **GP profiles** - Dillon & Henry backgrounds and involvement

### Phase 3: Analysis
10. **Timeline analysis** - Identify retroactive framing patterns
11. **Network analysis** - Map deal flow gaps and relationship depth
12. **Portfolio assessment** - Quality scoring, concentration risk
13. **Claims validation** - Cross-reference against evidence
14. **GP analysis** - Involvement patterns, Henry absence

### Phase 4: Synthesis
15. **Critical findings identification** - 5 key issues
16. **Recommendations development** - Priority-organized actions
17. **Executive summary** - 7.5/10 overall assessment

---

## Key Dependencies

| Analysis | Depends On | Feeds Into |
|----------|------------|------------|
| Timeline | Dataroom, Public Records | Claims Validation, Retroactive Framing |
| Network | LinkedIn Data | GP Analysis, Deal Flow Assessment |
| Portfolio | Company Research, Dataroom | Concentration Risk, Co-investor Validation |
| Claims | Timeline, Portfolio | Funding Discrepancies, Value-add Verification |
| GP | Network, Portfolio | Henry Role Questions, Team Assessment |

---

## Critical Cross-Validations

1. **Claims vs Timeline**: Sequencing of thought leadership vs investments
2. **Network vs GP Claims**: LinkedIn connections vs claimed relationships
3. **Portfolio vs Claims**: Funding amounts in dataroom vs public announcements
4. **Timeline vs Network**: When relationships formed vs when deals occurred

---

## Document Version
- **Version**: 1.0
- **Last Updated**: 2025-11-18
