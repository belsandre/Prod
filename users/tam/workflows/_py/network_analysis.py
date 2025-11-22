#!/usr/bin/env python3
"""
Network Analysis Script - Phase 1-2: CSV Enrichment & Statistical Analysis
Template for analyze-network workflow

USAGE:
1. Copy this script to your analysis directory
2. Update GP_NAME and file paths below
3. Activate venv: source venv/bin/activate
4. Run: python3 network_analysis.py
5. Then run network_validation.py for Phase 3-4
"""

import pandas as pd
import json
import re
from collections import Counter, defaultdict
from datetime import datetime

# ============================================================================
# CONFIGURATION - UPDATE THESE FOR YOUR ANALYSIS
# ============================================================================
GP_NAME = "gp-name"  # e.g., "dillon-dunteman"

# Input paths (relative to analysis directory)
HARVARD_CSV = f"research/people/{GP_NAME}/network/harvard.csv"
VCPE_CSV = f"research/people/{GP_NAME}/network/vcpe.csv"
DEEPTECH_CSV = f"research/people/{GP_NAME}/network/deeptech.csv"

# Output path
ENRICHED_CSV = f"research/people/{GP_NAME}/network/enriched_all.csv"
# ============================================================================


def extract_firm_from_title(title):
    """Extract firm name from title using @ or 'at' patterns"""
    if pd.isna(title):
        return None

    patterns = [
        r'@\s+([^,|]+)',
        r'\bat\s+([^,|]+)',
    ]

    for pattern in patterns:
        match = re.search(pattern, title, re.IGNORECASE)
        if match:
            firm = match.group(1).strip()
            firm = re.sub(r'\s*\([^)]*\)$', '', firm)  # Remove trailing (...)
            return firm

    return None


def categorize_firm_type(title, firm):
    """Categorize firm type based on title and firm name"""
    if pd.isna(title):
        return "other"

    title_lower = title.lower()
    firm_lower = str(firm).lower() if firm and not pd.isna(firm) else ""

    # Tier 1 VC firms (extend this list as needed)
    tier1_firms = ['sequoia', 'a16z', 'andreessen', 'benchmark', 'founders fund', 'accel',
                   'greylock', 'kleiner', 'lightspeed', 'nea', 'bessemer', 'general catalyst',
                   'index ventures', 'khosla', 'y combinator', 'yc']

    for t1 in tier1_firms:
        if t1 in firm_lower or t1 in title_lower:
            return "tier1_vc"

    # VC indicators
    vc_keywords = ['vc', 'venture capital', 'ventures', 'investor', 'investment', 'capital partners']
    if any(kw in title_lower for kw in vc_keywords):
        if 'corporate' in title_lower or 'cvc' in title_lower:
            return "corporate_vc"
        if 'growth' in title_lower or 'growth equity' in title_lower:
            return "growth_equity"
        if 'early' in title_lower or 'seed' in title_lower or 'pre-seed' in title_lower:
            return "early_stage"
        return "early_stage"

    # PE indicators
    if 'private equity' in title_lower or 'pe ' in title_lower:
        return "pe"

    # LP indicators
    if 'endowment' in title_lower or 'foundation' in title_lower or 'family office' in title_lower:
        return "lp"

    # Operator indicators
    if any(kw in title_lower for kw in ['founder', 'ceo', 'cto', 'cfo', 'chief', 'vp', 'director', 'head of', 'engineer', 'scientist', 'researcher']):
        return "operator"

    # Academic indicators
    if any(kw in title_lower for kw in ['professor', 'phd student', 'postdoc', 'researcher', 'lab', 'university']):
        return "academic"

    return "other"


def extract_seniority(title):
    """Extract seniority level from title"""
    if pd.isna(title):
        return "other"

    title_lower = title.lower()

    if 'partner' in title_lower or 'gp' in title_lower or 'general partner' in title_lower:
        return "partner"
    if 'founder' in title_lower or 'ceo' in title_lower or 'chief executive' in title_lower:
        return "founder"
    if any(kw in title_lower for kw in ['chief', 'cto', 'cfo', 'coo', 'cmo', 'cpo']):
        return "c_suite"
    if 'principal' in title_lower:
        return "principal"
    if 'vp' in title_lower or 'vice president' in title_lower:
        return "vp"
    if 'associate' in title_lower or 'analyst' in title_lower:
        return "associate"
    if 'director' in title_lower or 'manager' in title_lower or 'head of' in title_lower:
        return "director"

    return "other"


def categorize_ecosystem(title, firm):
    """Categorize technical ecosystem based on title and firm"""
    if pd.isna(title):
        return "other"

    firm_str = str(firm) if firm and not pd.isna(firm) else ""
    text = (title + " " + firm_str).lower()

    if any(kw in text for kw in ['ai', 'artificial intelligence', 'machine learning', 'ml', 'deep learning', 'llm', 'nlp']):
        return "ai"
    if any(kw in text for kw in ['quantum', 'qubit']):
        return "quantum"
    if any(kw in text for kw in ['fusion', 'nuclear', 'energy', 'battery', 'grid']):
        return "fusion_energy"
    if any(kw in text for kw in ['bio', 'health', 'medical', 'pharma', 'therapeutics', 'diagnostics']):
        return "biotech"
    if any(kw in text for kw in ['robot', 'hardware', 'semiconductor', 'chip', 'sensor']):
        return "robotics_hardware"
    if any(kw in text for kw in ['infrastructure', 'enterprise', 'saas', 'cloud', 'data', 'security', 'cyber']):
        return "infrastructure"

    return "generalist"


def assess_relevance(firm_type, ecosystem, seniority):
    """Assess relevance to deeptech early-stage fund thesis"""
    score = 0

    if firm_type in ['tier1_vc', 'early_stage']:
        score += 3
    elif firm_type in ['growth_equity', 'corporate_vc', 'operator', 'academic']:
        score += 2
    elif firm_type == 'lp':
        score += 1

    if ecosystem in ['quantum', 'fusion_energy', 'robotics_hardware', 'ai']:
        score += 3
    elif ecosystem in ['biotech', 'infrastructure']:
        score += 2

    if seniority in ['partner', 'founder', 'c_suite']:
        score += 2
    elif seniority in ['principal', 'vp']:
        score += 1

    if score >= 6:
        return "high"
    elif score >= 3:
        return "medium"
    else:
        return "low"


def enrich_dataframe(df, category_name):
    """Add characterization columns to dataframe"""
    print(f"\nEnriching {category_name} data...")

    if 'Firm' not in df.columns:
        df['Firm'] = df['Title'].apply(extract_firm_from_title)

    df['Firm_Type'] = df.apply(lambda row: categorize_firm_type(row['Title'], row.get('Firm')), axis=1)
    df['Seniority'] = df['Title'].apply(extract_seniority)
    df['Ecosystem'] = df.apply(lambda row: categorize_ecosystem(row['Title'], row.get('Firm')), axis=1)
    df['Relevance'] = df.apply(lambda row: assess_relevance(row['Firm_Type'], row['Ecosystem'], row['Seniority']), axis=1)
    df['Category'] = category_name

    return df


def load_and_enrich_data():
    """Load all CSV files and enrich them"""
    print("Loading CSV files...")

    harvard_df = pd.read_csv(HARVARD_CSV)
    vcpe_df = pd.read_csv(VCPE_CSV)
    deeptech_df = pd.read_csv(DEEPTECH_CSV)

    print(f"Loaded: {len(harvard_df)} harvard, {len(vcpe_df)} vcpe, {len(deeptech_df)} deeptech connections")

    harvard_df = enrich_dataframe(harvard_df, 'harvard')
    vcpe_df = enrich_dataframe(vcpe_df, 'vcpe')
    deeptech_df = enrich_dataframe(deeptech_df, 'deeptech')

    all_connections = pd.concat([harvard_df, vcpe_df, deeptech_df], ignore_index=True)

    return all_connections, harvard_df, vcpe_df, deeptech_df


def main():
    """Main analysis function"""
    print(f"Starting Network Analysis for {GP_NAME}...")
    print("="*60)

    # Load and enrich data
    all_df, harvard_df, vcpe_df, deeptech_df = load_and_enrich_data()

    # Calculate statistics
    print("\nCalculating statistics...")
    total = len(all_df)

    print("\n" + "="*60)
    print("RESULTS")
    print("="*60)
    print(f"\nTotal connections: {total}")
    print(f"  Harvard: {len(harvard_df)}")
    print(f"  VCPE: {len(vcpe_df)}")
    print(f"  Deeptech: {len(deeptech_df)}")

    # Firm type distribution
    print(f"\nFirm type distribution:")
    for ft, count in all_df['Firm_Type'].value_counts().head(5).items():
        print(f"  {ft}: {count} ({count/total*100:.1f}%)")

    # Seniority distribution
    print(f"\nSeniority distribution:")
    for sen, count in all_df['Seniority'].value_counts().head(5).items():
        print(f"  {sen}: {count} ({count/total*100:.1f}%)")

    # Ecosystem distribution
    print(f"\nEcosystem distribution:")
    for eco, count in all_df['Ecosystem'].value_counts().items():
        relevance = "high" if eco in ['quantum', 'fusion_energy', 'ai', 'robotics_hardware'] else "medium" if eco in ['biotech', 'infrastructure'] else "low"
        print(f"  {eco}: {count} ({count/total*100:.1f}%) - {relevance} relevance")

    # Top firms
    print(f"\nTop 10 firms by connection count:")
    for i, (firm, count) in enumerate(all_df['Firm'].value_counts().head(10).items(), 1):
        if pd.notna(firm):
            print(f"  {i}. {firm}: {count} connections")

    # Save enriched data
    print(f"\nSaving enriched data to {ENRICHED_CSV}...")
    all_df.to_csv(ENRICHED_CSV, index=False)

    print(f"\n✓ Phase 1-2 complete. Run network_validation.py for Phase 3-4.")
    return all_df


if __name__ == "__main__":
    main()
