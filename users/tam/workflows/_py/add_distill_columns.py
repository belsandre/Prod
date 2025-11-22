#!/usr/bin/env python3
"""
Add Distill enrichment columns (_D suffix) to combined_deduped.csv
using cached deeptech classifications from distill_profiles.json.

Columns added:
  - Ecosystem_D: Primary deeptech sector (quantum, ai, fusion_energy, etc.)
  - Relevance_D: Deeptech relevance level (high/medium/low/none)
  - Sector_D: Specific sub-sector (ion-trap computing, ML infrastructure, etc.)
  - Role_D: Role type (founder/investor/operator/academic)

Usage:
    python add_distill_columns.py <network_dir>

Example:
    python add_distill_columns.py /path/to/network
"""

import pandas as pd
import json
import sys
from pathlib import Path

def main(network_dir):
    network_path = Path(network_dir)
    csv_path = network_path / 'combined_deduped.csv'
    json_path = network_path / 'distill_profiles.json'

    if not csv_path.exists():
        print(f"Error: {csv_path} not found")
        sys.exit(1)

    if not json_path.exists():
        print(f"Error: {json_path} not found")
        sys.exit(1)

    # Load CSV
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} records from {csv_path}")

    # Load Distill profiles
    with open(json_path, 'r') as f:
        distill_data = json.load(f)

    profiles = distill_data.get('profiles', {})
    print(f"Loaded {len(profiles)} Distill profiles from {json_path}")

    # Ensure _D columns exist (deeptech-focused)
    for col in ['Ecosystem_D', 'Relevance_D', 'Sector_D', 'Role_D']:
        if col not in df.columns:
            df[col] = ''

    # Match profiles to CSV records by LinkedIn URL
    matched = 0
    for idx, row in df.iterrows():
        profile_url = str(row.get('Profile', ''))

        # Try exact match, normalized (no trailing slash), and with trailing slash
        profile = None
        for url_variant in [profile_url, profile_url.rstrip('/'), profile_url.rstrip('/') + '/']:
            if url_variant in profiles:
                profile = profiles[url_variant]
                break

        if profile:
            df.at[idx, 'Ecosystem_D'] = profile.get('ecosystem', '')
            df.at[idx, 'Relevance_D'] = profile.get('deeptech_relevance', '')
            df.at[idx, 'Sector_D'] = profile.get('sector_specifics', '')
            df.at[idx, 'Role_D'] = profile.get('role_type', '')
            matched += 1

    print(f"Matched {matched} profiles to CSV records")

    # Save updated CSV
    df.to_csv(csv_path, index=False)
    print(f"Saved updated CSV with _D columns to {csv_path}")

    # Print summary by ecosystem
    enriched = df[(df['Ecosystem_D'].notna()) & (df['Ecosystem_D'] != '')]
    if len(enriched) > 0:
        print(f"\n=== DEEPTECH CLASSIFICATIONS ({len(enriched)} profiles) ===")

        # Group by ecosystem
        ecosystem_counts = enriched['Ecosystem_D'].value_counts()
        print("\nBy Ecosystem:")
        for eco, count in ecosystem_counts.items():
            print(f"  {eco}: {count}")

        # Group by relevance
        if 'Relevance_D' in enriched.columns:
            relevance_counts = enriched[enriched['Relevance_D'] != '']['Relevance_D'].value_counts()
            if len(relevance_counts) > 0:
                print("\nBy Deeptech Relevance:")
                for rel, count in relevance_counts.items():
                    print(f"  {rel}: {count}")

        # Show high-relevance deeptech
        high_relevance = enriched[enriched['Relevance_D'] == 'high']
        if len(high_relevance) > 0:
            print(f"\n=== HIGH-RELEVANCE DEEPTECH ({len(high_relevance)}) ===")
            for _, row in high_relevance.iterrows():
                name = row['Name']
                eco = row['Ecosystem_D']
                sector = row.get('Sector_D', '') or ''
                print(f"  - {name}: {eco}" + (f" ({sector})" if sector else ""))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    main(sys.argv[1])
