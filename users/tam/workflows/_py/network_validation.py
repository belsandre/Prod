#!/usr/bin/env python3
"""
Network Validation Script - Phase 3-4: Strategic Validation & Gap Analysis
Template for analyze-network workflow

USAGE:
1. Run network_analysis.py first to generate enriched_all.csv
2. Update GP_NAME and paths below
3. Run: python3 network_validation.py
4. Outputs: network.json
"""

import pandas as pd
import json
from datetime import datetime
from collections import Counter

# ============================================================================
# CONFIGURATION - UPDATE THESE FOR YOUR ANALYSIS
# ============================================================================
GP_NAME = "gp-name"  # e.g., "dillon-dunteman"

# Input paths
ENRICHED_CSV = f'research/people/{GP_NAME}/network/enriched_all.csv'
CLAIMS_JSON = 'marketing-to-reality/_data/claims.json'  # Optional

# Output path
OUTPUT_JSON = "marketing-to-reality/_data/network.json"

# Key firms to validate (customize for your analysis)
KEY_FIRMS_TO_CHECK = [
    # Tier 1 VCs
    "Sequoia", "Founders Fund", "Coatue", "Benchmark", "a16z", "Andreessen Horowitz",
    # Early-stage deeptech VCs
    "Also Capital", "Tamarack", "DCVC", "Lux Capital", "Prime Movers Lab",
    # Add fund-specific firms here
]
# ============================================================================


# Load enriched data
print(f"Loading enriched data from {ENRICHED_CSV}...")
df = pd.read_csv(ENRICHED_CSV)
print(f"Loaded {len(df)} connections")

# Load claims (optional)
claims = None
try:
    with open(CLAIMS_JSON, 'r') as f:
        claims = json.load(f)
    print(f"Loaded claims from {CLAIMS_JSON}")
except FileNotFoundError:
    print(f"Note: {CLAIMS_JSON} not found - proceeding without claims validation")

print("\nStarting Strategic Relationship Validation...")
print("="*60)

# ============================================================================
# PHASE 3: Strategic Relationship Validation
# ============================================================================

print("\n1. VALIDATING KEY VC RELATIONSHIPS")
print("-"*60)

strategic_relationships = {
    "central_hub_partners": [],
    "deal_sources": [],
    "co_investors": [],
    "mentors": [],
    "high_value_connections": []
}

for firm_pattern in KEY_FIRMS_TO_CHECK:
    matching = df[df['Firm'].str.contains(firm_pattern, case=False, na=False)]

    if len(matching) > 0:
        senior = matching[matching['Seniority'].isin(['partner', 'founder', 'c_suite', 'principal'])]
        junior = matching[matching['Seniority'].isin(['associate', 'vp', 'director'])]

        if len(senior) >= 3:
            assessment = "Strong"
        elif len(senior) >= 1:
            assessment = "Moderate"
        elif len(junior) > 0:
            assessment = "Weak"
        else:
            assessment = "Unverified"

        key_contacts = []
        for _, row in senior.head(5).iterrows():
            title = row['Title'][:60] + "..." if len(str(row['Title'])) > 60 else row['Title']
            key_contacts.append(f"{row['Name']} ({title})")

        if not key_contacts:
            for _, row in junior.head(3).iterrows():
                title = row['Title'][:60] + "..." if len(str(row['Title'])) > 60 else row['Title']
                key_contacts.append(f"{row['Name']} ({title})")

        print(f"\n{firm_pattern}: {len(matching)} connections")
        print(f"  Senior: {len(senior)} | Junior: {len(junior)} | Assessment: {assessment}")

        if len(matching) >= 2:
            strategic_relationships["central_hub_partners"].append({
                "entity": firm_pattern,
                "claimed_relationship": "VC partnership / deal flow source",
                "claim_id": "SOURCING_EDGE",
                "connection_count": int(len(matching)),
                "connection_details": key_contacts[:5],
                "assessment": assessment,
                "verification_status": "verified" if assessment == "Strong" else "partial" if assessment == "Moderate" else "unverified",
                "notes": f"{len(senior)} senior, {len(junior)} junior connections"
            })

# ============================================================================
# PHASE 4: Network Quality Assessment
# ============================================================================

print("\n\n2. ECOSYSTEM ANALYSIS")
print("-"*60)

quantum = df[df['Ecosystem'] == 'quantum']
fusion = df[df['Ecosystem'] == 'fusion_energy']
robotics = df[df['Ecosystem'] == 'robotics_hardware']
ai = df[df['Ecosystem'] == 'ai']
biotech = df[df['Ecosystem'] == 'biotech']

print(f"Quantum: {len(quantum)} connections ({len(quantum[quantum['Seniority'] == 'founder'])} founders)")
print(f"Fusion/Energy: {len(fusion)} connections ({len(fusion[fusion['Seniority'] == 'founder'])} founders)")
print(f"Robotics/Hardware: {len(robotics)} connections ({len(robotics[robotics['Seniority'] == 'founder'])} founders)")
print(f"AI: {len(ai)} connections ({len(ai[ai['Seniority'] == 'founder'])} founders)")
print(f"Biotech: {len(biotech)} connections ({len(biotech[biotech['Seniority'] == 'founder'])} founders)")

# Calculate key metrics
tier1_vcs = df[df['Firm_Type'] == 'tier1_vc']
early_stage = df[df['Firm_Type'] == 'early_stage']
vc_firms = df[df['Firm_Type'].isin(['tier1_vc', 'early_stage'])]['Firm'].value_counts()
partner_level = df[df['Seniority'] == 'partner']
founder_level = df[df['Seniority'] == 'founder']

generalist_pct = len(df[df['Ecosystem'] == 'generalist']) / len(df) * 100
deeptech_pct = len(df[df['Ecosystem'].isin(['quantum', 'fusion_energy', 'robotics_hardware', 'biotech'])]) / len(df) * 100

print("\n\n3. NETWORK QUALITY ASSESSMENT")
print("-"*60)

strengths = []
gaps = []

# Strengths (customize based on your analysis)
strengths.append({
    "dimension": "breadth",
    "description": f"Broad network with {len(df)} total connections across multiple categories",
    "evidence": f"{len(df)} connections across {df['Category'].nunique()} categories",
    "significance": "Demonstrates network building capability"
})

strengths.append({
    "dimension": "breadth",
    "description": f"Early-stage VC network spanning {len(vc_firms)} unique firms",
    "evidence": f"{len(early_stage)} total early-stage VC connections across {len(vc_firms)} firms",
    "significance": "Supports VC partnership claims if partner-level relationships exist"
})

# Gaps
if len(quantum) < 20:
    quantum_founders = len(quantum[quantum['Seniority'] == 'founder'])
    gaps.append({
        "gap_type": "missing_ecosystem",
        "description": f"Limited quantum network ({len(quantum)} connections) - verify against claimed ecosystem depth",
        "claim_reference": "SOURCING_EDGE",
        "evidence": f"Only {len(quantum)} quantum-related connections, {quantum_founders} founders",
        "significance": f"Gap between claimed quantum network and {len(quantum)} LinkedIn connections. LinkedIn capture may be incomplete, but warrants verification.",
        "risk_severity": "red_flag" if len(quantum) < 10 else "yellow_flag"
    })

if deeptech_pct < 10:
    gaps.append({
        "gap_type": "network_mismatch",
        "description": f"Network skewed toward generalists ({generalist_pct:.1f}%) vs deeptech ({deeptech_pct:.1f}%)",
        "claim_reference": "COMPETITIVE_POSITIONING",
        "evidence": f"{generalist_pct:.1f}% generalist, {deeptech_pct:.1f}% deeptech (quantum+fusion+robotics+biotech)",
        "significance": "Network composition may not strongly support 'deeptech specialist' positioning",
        "risk_severity": "yellow_flag"
    })

partner_pct = len(partner_level) / len(df) * 100
gaps.append({
    "gap_type": "shallow_key_relationship",
    "description": f"Partner-level connections represent {partner_pct:.1f}% of network - verify partnership depth",
    "claim_reference": "SOURCING_EDGE",
    "evidence": f"{len(partner_level)} partner-level connections out of {len(df)} total",
    "significance": "Need to verify whether connections represent true partnerships or broader network",
    "risk_severity": "yellow_flag"
})

# Verification priorities
verification_priorities = [
    {
        "entity": "Ecosystem depth",
        "relationship_claimed": "Deep ecosystem networks in target verticals",
        "claim_id": "SOURCING_EDGE",
        "current_evidence": f"{len(quantum)} quantum, {len(fusion)} fusion, {len(ai)} AI connections",
        "priority": "critical",
        "verification_approach": "Reference checks with portfolio companies - how were deals sourced?",
        "rationale": "Validate claimed ecosystem depth against connection evidence"
    },
    {
        "entity": "VC partnerships",
        "relationship_claimed": "Partnerships with multiple VCs",
        "claim_id": "SOURCING_EDGE",
        "current_evidence": f"{len(vc_firms)} unique VC firms with connections, {len(partner_level)} partner-level",
        "priority": "high",
        "verification_approach": "Define 'partnership' criteria and verify through co-investment evidence",
        "rationale": "Validate whether connections represent true partnerships"
    },
    {
        "entity": "Founder referral network",
        "relationship_claimed": "Strong founder referral network",
        "claim_id": "SOURCING_EDGE",
        "current_evidence": f"{len(founder_level)} founder connections total",
        "priority": "high",
        "verification_approach": "Reference checks with founder testimonials",
        "rationale": "Validate sourcing thesis through founder interviews"
    }
]

print("\nStrengths identified:")
for s in strengths:
    print(f"  - {s['dimension'].upper()}: {s['description']}")

print("\nGaps identified:")
for g in gaps:
    severity = "🚩 RED FLAG" if g['risk_severity'] == 'red_flag' else "🟡 YELLOW FLAG"
    print(f"  - {severity}: {g['description']}")

# ============================================================================
# Generate Output
# ============================================================================

print("\n\n4. GENERATING OUTPUT")
print("-"*60)

# Get category counts from data
category_counts = df['Category'].value_counts().to_dict()

output = {
    "metadata": {
        "analysis_date": datetime.now().strftime("%Y-%m-%d"),
        "data_sources": [f"{cat}.csv ({count} connections)" for cat, count in category_counts.items()],
        "methodology_note": "Analysis based on partial LinkedIn connection captures - not complete network representation. LinkedIn connections are one signal of relationship depth, but absence of connection does not prove absence of relationship."
    },
    "overall_statistics": {
        "total_connections_analyzed": int(len(df)),
        "categories": {cat: int(count) for cat, count in category_counts.items()}
    },
    "network_composition": {
        "by_firm_type": [
            {"type": ft, "count": int(count), "percentage": f"{count/len(df)*100:.1f}%"}
            for ft, count in df['Firm_Type'].value_counts().items()
        ],
        "by_seniority": [
            {"level": level, "count": int(count), "percentage": f"{count/len(df)*100:.1f}%"}
            for level, count in df['Seniority'].value_counts().items()
        ],
        "by_ecosystem": [
            {
                "ecosystem": eco,
                "count": int(count),
                "percentage": f"{count/len(df)*100:.1f}%",
                "relevance_to_thesis": "high" if eco in ['quantum', 'fusion_energy', 'ai', 'robotics_hardware'] else "medium" if eco in ['biotech', 'infrastructure'] else "low"
            }
            for eco, count in df['Ecosystem'].value_counts().items()
        ]
    },
    "top_firms": [],
    "strategic_relationships": strategic_relationships,
    "network_quality_assessment": {
        "strengths": strengths,
        "gaps": gaps
    },
    "verification_priorities": verification_priorities
}

# Add top firms
for firm, count in df['Firm'].value_counts().head(30).items():
    if pd.notna(firm) and count >= 2:
        firm_df = df[df['Firm'] == firm]
        firm_type = firm_df['Firm_Type'].mode()[0] if len(firm_df) > 0 else "other"

        key_contacts = []
        senior = firm_df[firm_df['Seniority'].isin(['partner', 'founder', 'c_suite', 'principal'])]
        for _, row in senior.head(3).iterrows():
            title = str(row['Title'])[:50] + "..." if len(str(row['Title'])) > 50 else str(row['Title'])
            key_contacts.append(f"{row['Name']} ({title})")

        output['top_firms'].append({
            "firm": firm,
            "connections": int(count),
            "firm_type": firm_type,
            "key_contacts": key_contacts,
            "significance": "",
            "claim_references": []
        })

# Save JSON
with open(OUTPUT_JSON, 'w') as f:
    json.dump(output, f, indent=2)

print(f"✓ Generated {OUTPUT_JSON}")

print("\n" + "="*60)
print("ANALYSIS COMPLETE")
print("="*60)
print(f"\nKey findings:")
print(f"  - {len(df)} total connections")
print(f"  - {len(tier1_vcs)} tier-1 VC connections")
print(f"  - {len(quantum)} quantum, {len(fusion)} fusion, {len(ai)} AI connections")
print(f"  - {len(strengths)} strengths, {len(gaps)} gaps identified")
print(f"\nOutput: {OUTPUT_JSON}")
