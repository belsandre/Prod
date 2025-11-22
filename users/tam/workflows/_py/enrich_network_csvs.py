#!/usr/bin/env python3
"""
Enrich network CSV files with inferred columns for filtering/sorting.
Columns suffixed with _I are inferred (not from original data).

Usage:
    python enrich_network_csvs.py <network_dir>

Example:
    python enrich_network_csvs.py ../hyperion/research/people/dillon-dunteman/network
"""

import pandas as pd
import sys
import re
from pathlib import Path

# Tier-1 VC firms for classification
TIER1_VCS = {
    'sequoia', 'a16z', 'andreessen', 'benchmark', 'founders fund', 'greylock',
    'kleiner', 'accel', 'nea', 'bessemer', 'general catalyst', 'lightspeed',
    'index ventures', 'battery', 'spark capital', 'usv', 'union square'
}

# Investment stage classification by firm
SEED_FIRMS = {'first round', 'precursor', 'hustle fund', 'hof capital', 'soma capital', 'initialized', 'y combinator'}
GROWTH_FIRMS = {'tiger', 'coatue', 'd1', 'altimeter', 'insight partners', 'general atlantic'}
PE_LMM_FIRMS = {'vista equity', 'thoma bravo', 'francisco partners', 'silver lake'}
PE_LARGE_FIRMS = {'kkr', 'blackstone', 'apollo', 'carlyle', 'tpg', 'warburg'}
HEDGE_FUNDS = {'point72', 'citadel', 'two sigma', 'de shaw', 'millennium', 'bridgewater'}

# Quantum companies for comprehensive search
QUANTUM_COMPANIES = {
    'quantinuum', 'ionq', 'rigetti', 'q-ctrl', 'psiquantum', 'xanadu',
    'atom computing', 'coldquanta', 'zapata', 'classiq', 'aqora', 'qubits ventures',
    'cambridge quantum', 'alpine quantum', 'sandbox aq'
}

def classify_seniority(title):
    """Classify seniority from title."""
    title_lower = str(title).lower()
    if any(x in title_lower for x in ['partner', 'gp', 'general partner', 'managing director']):
        return 'partner'
    if any(x in title_lower for x in ['founder', 'co-founder', 'cofounder']):
        return 'founder'
    if any(x in title_lower for x in ['ceo', 'cto', 'cfo', 'coo', 'chief']):
        return 'c_suite'
    if 'principal' in title_lower:
        return 'principal'
    if any(x in title_lower for x in ['vice president', 'vp ']):
        return 'vp'
    if 'associate' in title_lower:
        return 'associate'
    if 'director' in title_lower:
        return 'director'
    return 'other'

def classify_category_harvard(title):
    """Classify Harvard connections into founder/investor/operator."""
    title_lower = str(title).lower()
    if any(x in title_lower for x in ['founder', 'co-founder', 'cofounder', 'ceo at', 'ceo @', 'ceo,', 'ceo |']):
        return 'founder'
    if any(x in title_lower for x in ['investor', 'vc', 'venture', 'partner at', 'principal at', 'associate at', 'investing']):
        return 'investor'
    return 'operator'

def classify_investment_stage(title, firm=''):
    """Classify VC/PE by investment stage."""
    combined = (str(title) + ' ' + str(firm)).lower()

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

    # Default classification by title keywords
    if any(x in combined for x in ['seed', 'pre-seed', 'angel']):
        return 'seed'
    if any(x in combined for x in ['series a', 'early stage', 'early-stage']):
        return 'series_a'
    if any(x in combined for x in ['growth', 'late stage', 'late-stage']):
        return 'growth'
    if any(x in combined for x in ['private equity', 'pe ', 'buyout']):
        return 'pe_lmm'

    return 'series_a'  # Default for VCs

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

    if any(x in title_lower for x in ['fusion', 'energy', 'nuclear', 'fission', 'grid', 'solar', 'battery']):
        return 'fusion_energy'
    if any(x in title_lower for x in ['robot', 'hardware', 'manufacturing', 'semiconductor', 'chip']):
        return 'robotics_hardware'
    if any(x in title_lower for x in ['ai', 'ml', 'machine learning', 'deep learning', 'llm', 'gpt', 'neural']):
        return 'ai'
    if any(x in title_lower for x in ['bio', 'life science', 'pharma', 'drug', 'health', 'medical']):
        return 'biotech'

    return 'generalist'

def get_quantum_confidence(title):
    """Get confidence level for quantum classification."""
    title_lower = str(title).lower()

    # High confidence: explicit quantum keywords
    high_keywords = ['quantum', 'qubit']
    for kw in high_keywords:
        if kw in title_lower:
            if any(x in title_lower for x in ['founder', 'ceo', 'co-founder']):
                return 'high'
            return 'medium'

    # Medium: quantum company names
    for company in QUANTUM_COMPANIES:
        if company in title_lower:
            return 'medium'

    return 'n/a'

def is_founder(title):
    """Check if person is a founder."""
    title_lower = str(title).lower()
    return 'yes' if any(x in title_lower for x in ['founder', 'co-founder', 'cofounder']) else 'no'

def enrich_harvard(df):
    """Enrich Harvard CSV with inferred columns."""
    df['Seniority_I'] = df['Title'].apply(classify_seniority)
    df['Category_I'] = df['Title'].apply(classify_category_harvard)
    # Startup stage only meaningful for founders - leave blank for others
    df['Startup_Stage_I'] = ''  # Would need web lookup to determine - mark as unknown
    return df

def enrich_vcpe(df):
    """Enrich VCPE CSV with inferred columns."""
    firm_col = 'Firm' if 'Firm' in df.columns else None
    df['Seniority_I'] = df['Title'].apply(classify_seniority)
    if firm_col:
        df['Investment_Stage_I'] = df.apply(lambda r: classify_investment_stage(r['Title'], r.get('Firm', '')), axis=1)
    else:
        df['Investment_Stage_I'] = df['Title'].apply(lambda t: classify_investment_stage(t))
    return df

def enrich_deeptech(df):
    """Enrich Deeptech CSV with inferred columns."""
    df['Ecosystem_I'] = df['Title'].apply(classify_ecosystem)
    df['Is_Founder_I'] = df['Title'].apply(is_founder)
    df['Quantum_Confidence_I'] = df['Title'].apply(get_quantum_confidence)
    return df

def main(network_dir):
    network_path = Path(network_dir)

    # Enrich Harvard
    harvard_path = network_path / 'harvard.csv'
    if harvard_path.exists():
        df = pd.read_csv(harvard_path)
        df = enrich_harvard(df)
        df.to_csv(harvard_path, index=False)
        print(f"Enriched {harvard_path}: {len(df)} rows")
        print(f"  Categories: {df['Category_I'].value_counts().to_dict()}")

    # Enrich VCPE
    vcpe_path = network_path / 'vcpe.csv'
    if vcpe_path.exists():
        df = pd.read_csv(vcpe_path)
        df = enrich_vcpe(df)
        df.to_csv(vcpe_path, index=False)
        print(f"Enriched {vcpe_path}: {len(df)} rows")
        print(f"  Seniority: {df['Seniority_I'].value_counts().to_dict()}")

    # Enrich Deeptech
    deeptech_path = network_path / 'deeptech.csv'
    if deeptech_path.exists():
        df = pd.read_csv(deeptech_path)
        df = enrich_deeptech(df)
        df.to_csv(deeptech_path, index=False)
        print(f"Enriched {deeptech_path}: {len(df)} rows")
        print(f"  Ecosystems: {df['Ecosystem_I'].value_counts().to_dict()}")
        quantum = df[df['Ecosystem_I'] == 'quantum']
        print(f"  Quantum connections ({len(quantum)}):")
        for _, row in quantum.iterrows():
            print(f"    - {row['Name']}: {row['Title'][:60]}... [{row['Quantum_Confidence_I']}]")

    # Create deduplicated combined CSV
    all_dfs = []
    for csv_name, source in [('harvard.csv', 'harvard'), ('vcpe.csv', 'vcpe'), ('deeptech.csv', 'deeptech')]:
        csv_path = network_path / csv_name
        if csv_path.exists():
            df = pd.read_csv(csv_path)
            df['Source_CSV_I'] = source
            all_dfs.append(df)

    if all_dfs:
        combined = pd.concat(all_dfs, ignore_index=True)
        # Deduplicate by Profile URL
        before = len(combined)
        combined = combined.drop_duplicates(subset=['Profile'], keep='first')
        after = len(combined)
        combined.to_csv(network_path / 'combined_deduped.csv', index=False)
        print(f"\nCombined & deduplicated: {before} -> {after} rows (removed {before-after} duplicates)")

        # Compute top firms from deduplicated data
        print("\n=== TOP FIRMS (from deduplicated data) ===")
        # Extract firm from Title if Firm column not present
        def extract_firm(row):
            if 'Firm' in row and pd.notna(row['Firm']) and str(row['Firm']).strip():
                return str(row['Firm']).strip()
            title = str(row.get('Title', ''))
            # Try to extract firm after "at " or "@ "
            for sep in [' at ', ' @ ', ' | ']:
                if sep in title:
                    parts = title.split(sep)
                    if len(parts) > 1:
                        return parts[-1].split(',')[0].split('|')[0].strip()[:50]
            return 'Unknown'

        combined['Firm_Extracted'] = combined.apply(extract_firm, axis=1)

        # Filter out schools and generic entries
        school_keywords = ['harvard', 'stanford', 'mit', 'yale', 'princeton', 'columbia',
                          'wharton', 'school', 'university', 'college', 'institute']
        def is_school(firm):
            return any(kw in firm.lower() for kw in school_keywords)

        firms_df = combined[~combined['Firm_Extracted'].apply(is_school)]
        firms_df = firms_df[firms_df['Firm_Extracted'] != 'Unknown']

        # Count unique people per firm
        top_firms = firms_df.groupby('Firm_Extracted').agg({
            'Profile': 'nunique',
            'Name': lambda x: list(x.head(3))  # Top 3 contacts
        }).rename(columns={'Profile': 'unique_connections', 'Name': 'key_contacts'})
        top_firms = top_firms.sort_values('unique_connections', ascending=False).head(25)

        print(f"\nTop 15 firms by unique connections:")
        for firm, row in top_firms.head(15).iterrows():
            print(f"  {firm}: {row['unique_connections']} connections")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1])
