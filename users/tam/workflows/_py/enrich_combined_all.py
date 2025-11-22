#!/usr/bin/env python3
"""
Enrich combined_deduped.csv with ALL inferred columns regardless of source.
Also extracts founders list for Distill MCP enrichment.

Usage:
    python enrich_combined_all.py <network_dir>

Example:
    python enrich_combined_all.py ../hyperion/research/people/dillon-dunteman/network
"""

import pandas as pd
import sys
import re
from pathlib import Path

# ============ FIRM CLASSIFICATION DICTIONARIES ============

TIER1_VCS = {
    'sequoia', 'a16z', 'andreessen', 'benchmark', 'founders fund', 'greylock',
    'kleiner', 'accel', 'nea', 'bessemer', 'general catalyst', 'lightspeed',
    'index ventures', 'battery', 'spark capital', 'usv', 'union square',
    'khosla', 'menlo ventures', 'redpoint', 'ggv', 'norwest', 'mayfield',
    'dfj', 'matrix partners', 'bain capital ventures', 'insight partners'
}

SEED_FIRMS = {
    'first round', 'precursor', 'hustle fund', 'hof capital', 'soma capital',
    'initialized', 'y combinator', 'pear vc', 'floodgate', 'homebrew',
    'boldstart', 'lerer hippeau', 'betaworks', 'eniac', 'root ventures',
    'cowboy ventures', 'founder collective', 'maveron', 'uncork'
}

GROWTH_FIRMS = {
    'tiger global', 'coatue', 'd1 capital', 'altimeter', 'insight partners',
    'general atlantic', 'iconiq', 'wellington', 'fidelity', 't. rowe',
    'addition', 'dragoneer', 'durable capital'
}

PE_LMM_FIRMS = {
    'vista equity', 'thoma bravo', 'francisco partners', 'silver lake',
    'summit partners', 'ta associates', 'providence equity', 'hellman & friedman'
}

PE_LARGE_FIRMS = {
    'kkr', 'blackstone', 'apollo', 'carlyle', 'tpg', 'warburg pincus',
    'advent international', 'bain capital', 'permira', 'cvc capital'
}

HEDGE_FUNDS = {
    'point72', 'citadel', 'two sigma', 'de shaw', 'millennium', 'bridgewater',
    'renaissance', 'jane street', 'jump trading', 'hrt', 'tower research'
}

QUANTUM_COMPANIES = {
    'quantinuum', 'ionq', 'rigetti', 'q-ctrl', 'psiquantum', 'xanadu',
    'atom computing', 'coldquanta', 'zapata', 'classiq', 'aqora',
    'qubits ventures', 'cambridge quantum', 'alpine quantum', 'sandbox aq',
    'ibm quantum', 'google quantum', 'amazon braket', 'honeywell quantum'
}

# ============ CLASSIFICATION FUNCTIONS ============

def extract_firm_from_title(title):
    """Extract company/firm name from title."""
    title = str(title)
    # Try common separators
    for sep in [' at ', ' @ ', ' | ', ' - ']:
        if sep in title:
            parts = title.split(sep)
            if len(parts) > 1:
                # Take the part after separator, clean it up
                firm = parts[-1].split(',')[0].split('|')[0].strip()
                # Remove trailing descriptors
                firm = re.sub(r'\s*\([^)]*\)\s*$', '', firm)
                if len(firm) > 2 and len(firm) < 80:
                    return firm
    return ''

def extract_role_from_title(title):
    """Extract role from title."""
    title = str(title)
    # Try to get part before separator
    for sep in [' at ', ' @ ', ' | ', ' - ']:
        if sep in title:
            role = title.split(sep)[0].strip()
            if len(role) > 2:
                return role[:100]  # Truncate if too long
    return title[:100] if len(title) > 2 else ''

def classify_seniority(title):
    """Classify seniority from title."""
    title_lower = str(title).lower()

    # Partner level
    if any(x in title_lower for x in ['managing partner', 'general partner', 'gp at', 'gp @', 'managing director']):
        return 'partner'
    if 'partner' in title_lower and not any(x in title_lower for x in ['investing partner', 'investment partner', 'venture partner']):
        return 'partner'

    # Founder level
    if any(x in title_lower for x in ['founder', 'co-founder', 'cofounder']):
        return 'founder'

    # C-suite
    if any(x in title_lower for x in ['ceo', 'cto', 'cfo', 'coo', 'chief ']):
        return 'c_suite'

    # Principal
    if 'principal' in title_lower:
        return 'principal'

    # VP
    if any(x in title_lower for x in ['vice president', 'vp ']):
        return 'vp'

    # Associate
    if 'associate' in title_lower:
        return 'associate'

    # Director
    if 'director' in title_lower:
        return 'director'

    return 'other'

def classify_category(title):
    """Classify into founder/investor/operator."""
    title_lower = str(title).lower()

    # Founder indicators
    if any(x in title_lower for x in ['founder', 'co-founder', 'cofounder', 'ceo at', 'ceo @', 'ceo,']):
        return 'founder'

    # Investor indicators
    if any(x in title_lower for x in ['investor', 'vc', 'venture', 'investing', 'investment']):
        return 'investor'
    if any(x in title_lower for x in ['partner at', 'principal at', 'associate at']):
        # Check if it's a VC/PE firm
        if any(vc in title_lower for vc in ['capital', 'ventures', 'partners', 'equity']):
            return 'investor'

    return 'operator'

def classify_investment_stage(title, firm=''):
    """Classify VC/PE by investment stage."""
    combined = (str(title) + ' ' + str(firm)).lower()

    # Check against known firms
    for f in HEDGE_FUNDS:
        if f in combined:
            return 'hedge_fund'
    for f in PE_LARGE_FIRMS:
        if f in combined:
            return 'pe_large'
    for f in PE_LMM_FIRMS:
        if f in combined:
            return 'pe_lmm'
    for f in GROWTH_FIRMS:
        if f in combined:
            return 'growth'
    for f in SEED_FIRMS:
        if f in combined:
            return 'seed'
    for f in TIER1_VCS:
        if f in combined:
            return 'series_a'  # Default tier-1 to Series A

    # Keyword-based classification
    if any(x in combined for x in ['seed', 'pre-seed', 'angel', 'early stage', 'early-stage']):
        return 'seed'
    if any(x in combined for x in ['series a', 'series b']):
        return 'series_a'
    if any(x in combined for x in ['growth', 'late stage', 'late-stage']):
        return 'growth'
    if any(x in combined for x in ['private equity', 'pe ', 'buyout', 'lbo']):
        return 'pe_lmm'

    return ''  # Unknown

def classify_ecosystem(title):
    """Classify into technical ecosystem."""
    title_lower = str(title).lower()

    # Quantum - comprehensive check
    quantum_keywords = ['quantum', 'qubit', 'ion trap', 'superconducting', 'photonic',
                       'error correction', 'nisq', 'fault-tolerant', 'topological']
    for kw in quantum_keywords:
        if kw in title_lower:
            return 'quantum'
    for company in QUANTUM_COMPANIES:
        if company in title_lower:
            return 'quantum'

    # Energy
    if any(x in title_lower for x in ['fusion', 'nuclear', 'fission', 'grid', 'solar', 'battery', 'energy storage', 'clean energy']):
        return 'fusion_energy'

    # Robotics/Hardware
    if any(x in title_lower for x in ['robot', 'hardware', 'manufacturing', 'semiconductor', 'chip', 'foundry']):
        return 'robotics_hardware'

    # AI/ML
    if any(x in title_lower for x in [' ai ', ' ai,', ' ai|', 'ai ', 'artificial intelligence', 'ml ', 'machine learning',
                                       'deep learning', 'llm', 'gpt', 'neural', 'nlp']):
        return 'ai'

    # Biotech
    if any(x in title_lower for x in ['bio', 'life science', 'pharma', 'drug', 'therapeutic', 'genomic', 'crispr']):
        return 'biotech'

    # Infrastructure
    if any(x in title_lower for x in ['infrastructure', 'cloud', 'devops', 'platform', 'data center']):
        return 'infrastructure'

    return 'generalist'

def get_quantum_confidence(title, ecosystem):
    """Get confidence level for quantum classification."""
    if ecosystem != 'quantum':
        return ''

    title_lower = str(title).lower()

    # High confidence: explicit quantum + founder/leadership
    if 'quantum' in title_lower or 'qubit' in title_lower:
        if any(x in title_lower for x in ['founder', 'ceo', 'co-founder', 'cto']):
            return 'high'
        return 'medium'

    # Medium: quantum company name
    for company in QUANTUM_COMPANIES:
        if company in title_lower:
            return 'medium'

    return 'low'

def is_founder(title, category):
    """Check if person is a founder."""
    title_lower = str(title).lower()
    if any(x in title_lower for x in ['founder', 'co-founder', 'cofounder']):
        return 'yes'
    if category == 'founder':
        return 'yes'
    return 'no'

def enrich_dataframe(df):
    """Enrich all records with all _I columns."""

    # Extract Firm and Role from Title if empty
    df['Firm'] = df.apply(lambda r: r['Firm'] if pd.notna(r.get('Firm')) and str(r.get('Firm', '')).strip()
                          else extract_firm_from_title(r['Title']), axis=1)
    df['Role'] = df.apply(lambda r: r['Role'] if pd.notna(r.get('Role')) and str(r.get('Role', '')).strip()
                          else extract_role_from_title(r['Title']), axis=1)

    # Fill Seniority_I
    df['Seniority_I'] = df.apply(lambda r: r['Seniority_I'] if pd.notna(r.get('Seniority_I')) and str(r.get('Seniority_I', '')).strip() and r['Seniority_I'] != 'other'
                                  else classify_seniority(r['Title']), axis=1)

    # Fill Category_I
    df['Category_I'] = df.apply(lambda r: r['Category_I'] if pd.notna(r.get('Category_I')) and str(r.get('Category_I', '')).strip()
                                 else classify_category(r['Title']), axis=1)

    # Fill Investment_Stage_I
    df['Investment_Stage_I'] = df.apply(lambda r: r['Investment_Stage_I'] if pd.notna(r.get('Investment_Stage_I')) and str(r.get('Investment_Stage_I', '')).strip()
                                         else classify_investment_stage(r['Title'], r.get('Firm', '')), axis=1)

    # Fill Ecosystem_I
    df['Ecosystem_I'] = df.apply(lambda r: r['Ecosystem_I'] if pd.notna(r.get('Ecosystem_I')) and str(r.get('Ecosystem_I', '')).strip()
                                  else classify_ecosystem(r['Title']), axis=1)

    # Fill Quantum_Confidence_I
    df['Quantum_Confidence_I'] = df.apply(lambda r: r['Quantum_Confidence_I'] if pd.notna(r.get('Quantum_Confidence_I')) and str(r.get('Quantum_Confidence_I', '')).strip()
                                           else get_quantum_confidence(r['Title'], r['Ecosystem_I']), axis=1)

    # Fill Is_Founder_I
    df['Is_Founder_I'] = df.apply(lambda r: r['Is_Founder_I'] if pd.notna(r.get('Is_Founder_I')) and str(r.get('Is_Founder_I', '')).strip()
                                   else is_founder(r['Title'], r['Category_I']), axis=1)

    return df

def main(network_dir):
    network_path = Path(network_dir)
    combined_path = network_path / 'combined_deduped.csv'

    if not combined_path.exists():
        print(f"Error: {combined_path} not found")
        sys.exit(1)

    # Load CSV
    df = pd.read_csv(combined_path)
    print(f"Loaded {len(df)} records from {combined_path}")

    # Ensure all expected columns exist
    expected_cols = ['Firm', 'Role', 'Seniority_I', 'Category_I', 'Investment_Stage_I',
                     'Ecosystem_I', 'Is_Founder_I', 'Quantum_Confidence_I']
    for col in expected_cols:
        if col not in df.columns:
            df[col] = ''

    # Enrich
    df = enrich_dataframe(df)

    # Save enriched CSV
    df.to_csv(combined_path, index=False)
    print(f"Saved enriched CSV to {combined_path}")

    # Print statistics
    print("\n=== ENRICHMENT STATISTICS ===")
    print(f"\nSeniority distribution:")
    print(df['Seniority_I'].value_counts().to_string())

    print(f"\nCategory distribution:")
    print(df['Category_I'].value_counts().to_string())

    print(f"\nEcosystem distribution:")
    print(df['Ecosystem_I'].value_counts().to_string())

    print(f"\nInvestment Stage distribution (non-empty):")
    stage_counts = df[df['Investment_Stage_I'] != '']['Investment_Stage_I'].value_counts()
    print(stage_counts.to_string())

    # Extract founders for Distill research
    founders = df[df['Is_Founder_I'] == 'yes']
    print(f"\n=== FOUNDERS FOR DISTILL RESEARCH ===")
    print(f"Total founders: {len(founders)}")

    # Save founders list
    founders_path = network_path / 'founders_for_distill.csv'
    founders[['Name', 'Title', 'Firm', 'Profile', 'Ecosystem_I', 'Source_CSV_I']].to_csv(founders_path, index=False)
    print(f"Saved {len(founders)} founders to {founders_path}")

    # Print sample founders
    print(f"\nSample founders (first 10):")
    for _, row in founders.head(10).iterrows():
        print(f"  - {row['Name']}: {row['Title'][:60]}...")
        print(f"    LinkedIn: {row['Profile']}")

    # Quantum-specific stats
    quantum = df[df['Ecosystem_I'] == 'quantum']
    print(f"\n=== QUANTUM CONNECTIONS ({len(quantum)}) ===")
    for _, row in quantum.iterrows():
        print(f"  - {row['Name']}: {row['Title'][:60]}... [{row['Quantum_Confidence_I']}]")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1])
