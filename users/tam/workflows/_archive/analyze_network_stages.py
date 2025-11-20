#!/usr/bin/env python3
"""
Analyze LinkedIn connections to categorize by investment stage and firm type.
Uses comprehensive knowledge of VC/PE firms.
"""

import csv
from collections import defaultdict, Counter
from typing import Dict

# Comprehensive firm categorization based on known investment strategies
FIRM_CATEGORIES = {
    # Early-Stage VC (Seed, Series A, sometimes B)
    'Cyrus Ventures': 'early_vc',
    'JDY Capital': 'early_vc',
    '021': 'early_vc',
    'FJ Labs': 'early_vc',
    'Linse Capital': 'early_vc',
    'First Round Capital': 'early_vc',
    'Benchmark': 'early_vc',
    'Lowercase Capital': 'early_vc',
    'SV Angel': 'early_vc',
    'Y Combinator': 'early_vc',
    'Initialized Capital': 'early_vc',
    'Homebrew': 'early_vc',
    'Boldstart Ventures': 'early_vc',
    'Root Ventures': 'early_vc',
    'Precursor Ventures': 'early_vc',
    'Susa Ventures': 'early_vc',
    'Unusual Ventures': 'early_vc',
    'Village Global': 'early_vc',
    'Amplify Partners': 'early_vc',
    'Eclipse': 'early_vc',
    'SOSV': 'early_vc',
    'Techstars': 'early_vc',
    '500 Global': 'early_vc',
    '500 Startups': 'early_vc',
    'Lerer Hippeau': 'early_vc',
    'Cowboy Ventures': 'early_vc',
    'Floodgate': 'early_vc',
    'True Ventures': 'early_vc',
    'BoxGroup': 'early_vc',
    'Slow Ventures': 'early_vc',
    'Greycroft': 'early_vc',
    'RRE Ventures': 'early_vc',
    'Primary Venture Partners': 'early_vc',
    'Operator Partners': 'early_vc',
    'Haystack': 'early_vc',
    'Abstract Ventures': 'early_vc',
    'Afore Capital': 'early_vc',
    'Alpha Bridge Ventures': 'early_vc',
    'Decibel': 'early_vc',
    'Basis Set Ventures': 'early_vc',
    'Character': 'early_vc',
    'Costanoa Ventures': 'early_vc',
    'Quiet Capital': 'early_vc',
    'Freestyle Capital': 'early_vc',
    'Chapter One': 'early_vc',
    'Pear VC': 'early_vc',
    'SignalFire': 'early_vc',
    'NFX': 'early_vc',
    'Fuel Capital': 'early_vc',
    'Notation Capital': 'early_vc',
    'Designer Fund': 'early_vc',
    'Foundry Group': 'early_vc',
    'Upfront Ventures': 'early_vc',
    'Felicis': 'early_vc',
    'Forerunner Ventures': 'early_vc',
    'XYZ Venture Capital': 'early_vc',
    'Craft Ventures': 'early_vc',
    'Alpha Partners': 'early_vc',
    'Discipulus Ventures': 'early_vc',
    'Makers Fund': 'early_vc',
    'betaworks': 'early_vc',
    'Spark Capital': 'early_vc',
    'Union Square Ventures': 'multi_stage_vc',  # Actually does seed-B
    'USV': 'multi_stage_vc',

    # Multi-Stage VC (Series A through growth, flexible)
    '8VC': 'multi_stage_vc',
    'HOF Capital': 'multi_stage_vc',
    'Altimeter Capital': 'multi_stage_vc',
    'Kleiner Perkins': 'multi_stage_vc',
    'BCV': 'multi_stage_vc',  # Bain Capital Ventures
    'Bain Capital Ventures': 'multi_stage_vc',
    'ICONIQ Capital': 'multi_stage_vc',
    'Lux Capital': 'multi_stage_vc',
    'Accel': 'multi_stage_vc',
    'Andreessen Horowitz': 'multi_stage_vc',
    'a16z': 'multi_stage_vc',
    'Sequoia Capital': 'multi_stage_vc',
    'Sequoia': 'multi_stage_vc',
    'Greylock Partners': 'multi_stage_vc',
    'Greylock': 'multi_stage_vc',
    'Lightspeed Venture Partners': 'multi_stage_vc',
    'Lightspeed': 'multi_stage_vc',
    'Khosla Ventures': 'multi_stage_vc',
    'Index Ventures': 'multi_stage_vc',
    'General Catalyst': 'multi_stage_vc',
    'NEA': 'multi_stage_vc',
    'Founders Fund': 'multi_stage_vc',
    'Bessemer Venture Partners': 'multi_stage_vc',
    'Bessemer': 'multi_stage_vc',
    'GGV Capital': 'multi_stage_vc',
    'Matrix Partners': 'multi_stage_vc',
    'Mayfield': 'multi_stage_vc',
    'Norwest Venture Partners': 'multi_stage_vc',
    'Norwest': 'multi_stage_vc',
    'Redpoint Ventures': 'multi_stage_vc',
    'Redpoint': 'multi_stage_vc',
    'IVP': 'multi_stage_vc',
    'Battery Ventures': 'multi_stage_vc',
    'Canaan Partners': 'multi_stage_vc',
    'CRV': 'multi_stage_vc',
    'Charles River Ventures': 'multi_stage_vc',
    'DCVC': 'multi_stage_vc',
    'Data Collective': 'multi_stage_vc',
    'Eclipse Ventures': 'multi_stage_vc',
    'Emergence Capital': 'multi_stage_vc',
    'GV': 'multi_stage_vc',
    'Google Ventures': 'multi_stage_vc',
    'Intel Capital': 'multi_stage_vc',
    'Menlo Ventures': 'multi_stage_vc',
    'New Enterprise Associates': 'multi_stage_vc',
    'Shasta Ventures': 'multi_stage_vc',
    'Threshold Ventures': 'multi_stage_vc',
    'DFJ': 'multi_stage_vc',
    'Draper Fisher Jurvetson': 'multi_stage_vc',
    'Sapphire Ventures': 'multi_stage_vc',
    'Uncork Capital': 'multi_stage_vc',
    'Wing VC': 'multi_stage_vc',
    'Wing': 'multi_stage_vc',
    'Salesforce Ventures': 'multi_stage_vc',
    'Scale Venture Partners': 'multi_stage_vc',
    'Scale': 'multi_stage_vc',
    'Storm Ventures': 'multi_stage_vc',
    'Trinity Ventures': 'multi_stage_vc',
    'Venrock': 'multi_stage_vc',
    'Accomplice': 'multi_stage_vc',
    'Eniac Ventures': 'multi_stage_vc',
    'Fidelity': 'multi_stage_vc',
    'Point72 Ventures': 'multi_stage_vc',
    'Breyer Capital': 'multi_stage_vc',
    'Ribbit Capital': 'multi_stage_vc',
    'Tribe Capital': 'multi_stage_vc',
    'Coatue Management': 'growth_equity',  # Actually more growth
    'Sound Ventures': 'multi_stage_vc',
    'B Capital Group': 'multi_stage_vc',
    'B Capital': 'multi_stage_vc',
    'Bullpen Capital': 'multi_stage_vc',
    'Heavybit': 'early_vc',
    'Work-Bench': 'early_vc',

    # Growth-Stage VC / Late-Stage VC
    'Avenir Growth Capital': 'growth_vc',
    'Avenir': 'growth_vc',
    'Meritech Capital': 'growth_vc',
    'Sapphire Sport': 'growth_vc',
    'DST Global': 'growth_vc',
    'Dragoneer': 'growth_vc',
    'Tiger Global': 'growth_vc',
    'Tiger Global Management': 'growth_vc',

    # Growth Equity (later stage, pre-IPO, some buyouts)
    'Insight Partners': 'growth_equity',
    'Insight': 'growth_equity',
    'TCV': 'growth_equity',
    'Technology Crossover Ventures': 'growth_equity',
    'Coatue': 'growth_equity',
    'General Atlantic': 'growth_equity',
    'TA Associates': 'growth_equity',
    'Summit Partners': 'growth_equity',
    'Vista Equity Partners': 'growth_equity',
    'Vista': 'growth_equity',
    'Accel-KKR': 'growth_equity',
    'Francisco Partners': 'growth_equity',
    'Vector Capital': 'growth_equity',
    'Riverwood Capital': 'growth_equity',
    'Silver Lake': 'growth_equity',
    'Silver Lake Partners': 'growth_equity',
    'Silverlake': 'growth_equity',
    'Hellman & Friedman': 'growth_equity',
    'H&F': 'growth_equity',
    'Thoma Bravo': 'growth_equity',
    'Advent International': 'growth_equity',
    'Warburg Pincus': 'growth_equity',
    'TPG Growth': 'growth_equity',
    'L Catterton': 'growth_equity',
    'ABRY Partners': 'growth_equity',
    'Great Hill Partners': 'growth_equity',
    'JMI Equity': 'growth_equity',
    'Spectrum Equity': 'growth_equity',
    'PSG': 'growth_equity',
    'Providence Equity': 'growth_equity',
    'Providence Strategic Growth': 'growth_equity',

    # Private Equity (primarily buyouts)
    'Apollo Global Management': 'pe',
    'Apollo': 'pe',
    'Bain Capital': 'pe',
    'KKR': 'pe',
    'Blackstone': 'pe',
    'Carlyle Group': 'pe',
    'Carlyle': 'pe',
    'TPG': 'pe',
    'TPG Capital': 'pe',
    'EQT': 'pe',
    'EQT Partners': 'pe',
    'CVC Capital Partners': 'pe',
    'CVC': 'pe',
    'Advent': 'pe',
    'Permira': 'pe',
    'Apax Partners': 'pe',
    'Apax': 'pe',
    'Cinven': 'pe',
    'PAI Partners': 'pe',
    'Ardian': 'pe',
    'BC Partners': 'pe',
    'Bridgepoint': 'pe',
    'Nordic Capital': 'pe',
    'Platinum Equity': 'pe',
    'Leonard Green & Partners': 'pe',
    'LGP': 'pe',
    'Clayton Dubilier & Rice': 'pe',
    'CD&R': 'pe',
    'Genstar Capital': 'pe',
    'GTCR': 'pe',
    'Cerberus Capital': 'pe',
    'Cerberus': 'pe',
    'Sun Capital': 'pe',
    'American Securities': 'pe',
    'Roark Capital': 'pe',
    'Audax Group': 'pe',
    'Clearlake Capital': 'pe',
    'Clearlake': 'pe',
    'Centerbridge Partners': 'pe',
    'Centerbridge': 'pe',

    # LPs / Fund of Funds / Secondaries
    'Industry Ventures': 'lp',
    'ArchPoint Investors': 'lp',
    'Sapphire Partners': 'lp',
    'StepStone Group': 'lp',
    'StepStone': 'lp',
    'HarbourVest': 'lp',
    'HarbourVest Partners': 'lp',
    'Adams Street Partners': 'lp',
    'Adams Street': 'lp',
    'Horsley Bridge': 'lp',
    'Horsley Bridge Partners': 'lp',
    'Hamilton Lane': 'lp',
    'Greenspring Associates': 'lp',
    'Greenspring': 'lp',
    'Lexington Partners': 'lp',
    'Coller Capital': 'lp',
    'AlpInvest Partners': 'lp',
    'AlpInvest': 'lp',
    'Pantheon': 'lp',
    'Pantheon Ventures': 'lp',
    'Goldman Sachs Asset Management': 'lp',
    'Goldman Sachs Private Equity': 'lp',
    'JP Morgan Asset Management': 'lp',
    'BlackRock Private Equity Partners': 'lp',
    'Neuberger Berman': 'lp',
    'Paul Capital': 'lp',
    'Top Tier Capital Partners': 'lp',
    'Top Tier': 'lp',
    'Vintage Investment Partners': 'lp',

    # Corporate VC
    'Flex': 'corporate',
    'Qualcomm Ventures': 'corporate',
    'Samsung Ventures': 'corporate',
    'Cisco Investments': 'corporate',
    'Dell Technologies Capital': 'corporate',
    'Microsoft Ventures': 'corporate',
    'Comcast Ventures': 'corporate',

    # Additional firms from the network analysis
    # More Early-Stage VC
    'NextView Ventures': 'early_vc',
    'NextView': 'early_vc',
    'Collaborative Fund': 'early_vc',
    '645 Ventures': 'early_vc',
    'February Capital': 'early_vc',
    'Formation': 'early_vc',
    '26North': 'early_vc',
    'Include Ventures': 'early_vc',
    'Obvious Ventures': 'early_vc',
    'Nex Cubed': 'early_vc',
    'Faction': 'early_vc',
    'Also Capital': 'early_vc',
    'Alt Capital': 'early_vc',
    'LDVP': 'early_vc',
    'Dark Arts VC': 'early_vc',
    'Elephant': 'early_vc',
    'Sunset VC': 'early_vc',
    'What If Ventures': 'early_vc',
    'Friends & Family Capital': 'early_vc',

    # More Multi-Stage VC
    'Radical Ventures': 'multi_stage_vc',
    'Riot Ventures': 'multi_stage_vc',
    'Heartland Ventures': 'multi_stage_vc',
    'Valhalla Ventures': 'multi_stage_vc',
    'Valor Equity Partners': 'multi_stage_vc',
    'Legion VC': 'multi_stage_vc',
    'Infinity Ventures': 'multi_stage_vc',
    'Asymmetric': 'multi_stage_vc',
    'Five Elms Capital': 'multi_stage_vc',
    'Morgenthaler Ventures': 'multi_stage_vc',
    'FirstMark': 'multi_stage_vc',
    'CIV': 'multi_stage_vc',
    'SoftBank Investment Advisers': 'multi_stage_vc',
    'Story Capital': 'multi_stage_vc',
    'Planeteer Capital': 'multi_stage_vc',
    'equation': 'multi_stage_vc',
    'FPV Ventures': 'multi_stage_vc',

    # More Growth VC/Equity
    'Tola Capital': 'growth_equity',
    'Lead Edge Capital': 'growth_equity',
    'Raine Ventures': 'growth_equity',
    'Stripes': 'growth_equity',
    'Durable Capital Partners': 'growth_equity',
    'Durable Capital Partners LP': 'growth_equity',
    'Benchstrength': 'growth_equity',
    'Dune': 'growth_equity',
    'RTP': 'growth_equity',
    'Spring Tide': 'growth_equity',
    'Morgan Creek Capital Management': 'growth_equity',

    # More PE
    'Cerberus': 'pe',
    'Cerberus Capital Management': 'pe',
    'Ares Management': 'pe',
    'Ares Management Corporation': 'pe',
    'The Jordan Company': 'pe',

    # Angel Networks / Other VC
    'Sand Hill Angels': 'early_vc',
    'Starship Ventures': 'early_vc',
    'Foothill Ventures': 'early_vc',
    'CVF': 'multi_stage_vc',
    'Solari Capital': 'early_vc',
    'talipot': 'lp',

    # Other/Services
    'McKinsey & Company': 'other',
    'Red Antler': 'other',
    'Artisanal Talent': 'other',
    'Sydecar': 'other',
    'Format One': 'other',
    'IQDX Capital Management': 'other',
    'Kearny Jackson': 'other',
    'Tower Research Capital': 'other',
    'LaFamilia Foundation': 'other',
    'Tamarack Global': 'other',
    'Carta': 'other',
    'Executive Search': 'other',
}


def categorize_firm(firm_name: str) -> str:
    """
    Categorize a firm by type/stage based on name.
    Returns: early_vc, multi_stage_vc, growth_vc, growth_equity, pe, lp, corporate, or unknown
    """
    if not firm_name:
        return 'unknown'

    # Direct lookup
    if firm_name in FIRM_CATEGORIES:
        return FIRM_CATEGORIES[firm_name]

    # Try partial matches for common abbreviations
    firm_lower = firm_name.lower()
    for known_firm, category in FIRM_CATEGORIES.items():
        if known_firm.lower() == firm_lower:
            return category

    return 'unknown'


def analyze_network(csv_file: str) -> Dict:
    """
    Analyze the LinkedIn network CSV and categorize connections.
    """
    categories = defaultdict(list)
    firm_counts = Counter()
    connections_without_firm = 0
    total_rows = 0

    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            total_rows += 1
            name = row.get('Name', '')
            firm = row.get('Firm', '').strip()
            title = row.get('Title', '')
            role = row.get('Role', '')

            if not firm:
                connections_without_firm += 1
                continue

            # Categorize the firm
            category = categorize_firm(firm)
            categories[category].append({
                'name': name,
                'firm': firm,
                'title': title,
                'role': role
            })

            firm_counts[firm] += 1

    results = {
        'total_connections': total_rows,
        'connections_with_firm': sum(len(v) for v in categories.values()),
        'connections_without_firm': connections_without_firm,
        'categories': categories,
        'firm_counts': firm_counts,
        'category_counts': {cat: len(conns) for cat, conns in categories.items()}
    }

    return results


def print_analysis(results: Dict, markdown: bool = False):
    """
    Print a formatted analysis of the network.
    """
    total = results['total_connections']

    if markdown:
        print("# LinkedIn Network Analysis: Investment Stage & Firm Type")
        print()
        print("## Overview")
        print()
        print(f"- **Total Connections:** {total}")
        print(f"- **Connections with Firm Data:** {results['connections_with_firm']} ({results['connections_with_firm']/total*100:.1f}%)")
        print(f"- **Connections without Firm Data:** {results['connections_without_firm']} ({results['connections_without_firm']/total*100:.1f}%)")
        print()
        print("## Breakdown by Investment Stage / Firm Type")
        print()
    else:
        print("=" * 80)
        print("LINKEDIN NETWORK ANALYSIS: Investment Stage & Firm Type")
        print("=" * 80)
        print()

        print(f"Total Connections: {total}")
        print(f"Connections with Firm Data: {results['connections_with_firm']} ({results['connections_with_firm']/total*100:.1f}%)")
        print(f"Connections without Firm Data: {results['connections_without_firm']} ({results['connections_without_firm']/total*100:.1f}%)")
        print()

        # Category breakdown
        print("=" * 80)
        print("BREAKDOWN BY INVESTMENT STAGE / FIRM TYPE")
        print("=" * 80)
        print()

    category_names = {
        'early_vc': 'Early-Stage VC (Seed, Series A)',
        'multi_stage_vc': 'Multi-Stage VC (Series A-C+)',
        'growth_vc': 'Growth-Stage VC (Late-stage venture)',
        'growth_equity': 'Growth Equity (Pre-IPO, growth buyouts)',
        'pe': 'Private Equity (Buyouts)',
        'lp': 'Limited Partners / Fund of Funds',
        'corporate': 'Corporate VC',
        'other': 'Other (Consulting, Services, etc.)',
        'unknown': 'Unknown / Uncategorized'
    }

    # Sort by count descending
    sorted_categories = sorted(results['category_counts'].items(), key=lambda x: x[1], reverse=True)

    if markdown:
        print("| Category | Count | Percentage |")
        print("|----------|-------|------------|")
        for cat, count in sorted_categories:
            if count > 0:
                cat_name = category_names.get(cat, cat)
                pct = count / results['connections_with_firm'] * 100 if results['connections_with_firm'] > 0 else 0
                print(f"| {cat_name} | {count} | {pct:.1f}% |")
        print()
    else:
        for cat, count in sorted_categories:
            if count > 0:
                cat_name = category_names.get(cat, cat)
                pct = count / results['connections_with_firm'] * 100 if results['connections_with_firm'] > 0 else 0
                print(f"{cat_name:50} {count:4} ({pct:5.1f}%)")

        print()

    # Top firms by number of connections
    if markdown:
        print("## Top 30 Firms by Number of Connections")
        print()
        print("| Firm | Connections | Category |")
        print("|------|-------------|----------|")
        top_firms = results['firm_counts'].most_common(30)
        for firm, count in top_firms:
            category = categorize_firm(firm)
            cat_name = category_names.get(category, category)
            print(f"| {firm} | {count} | {cat_name} |")
        print()
    else:
        print("=" * 80)
        print("TOP 30 FIRMS BY NUMBER OF CONNECTIONS")
        print("=" * 80)
        print()

        top_firms = results['firm_counts'].most_common(30)
        for firm, count in top_firms:
            # Find category
            category = categorize_firm(firm)
            cat_name = category_names.get(category, category)
            print(f"{firm:50} {count:3} connections  [{cat_name}]")

        print()

    # Category details
    if markdown:
        print("## Detailed Breakdown by Category")
        print()
        for cat, count in sorted_categories:
            if count > 0:
                cat_name = category_names.get(cat, cat)
                print(f"### {cat_name} ({count} connections)")
                print()

                # Get unique firms in this category
                firms_in_cat = defaultdict(int)
                for conn in results['categories'][cat]:
                    firms_in_cat[conn['firm']] += 1

                # Sort by count
                sorted_firms = sorted(firms_in_cat.items(), key=lambda x: x[1], reverse=True)

                print("| Firm | Connections |")
                print("|------|-------------|")
                for firm, firm_count in sorted_firms[:20]:  # Show top 20 firms per category
                    print(f"| {firm} | {firm_count} |")

                if len(sorted_firms) > 20:
                    remaining = len(sorted_firms) - 20
                    remaining_count = sum(c for f, c in sorted_firms[20:])
                    print(f"| *...and {remaining} more firms* | *{remaining_count}* |")
                print()
    else:
        print("=" * 80)
        print("DETAILED BREAKDOWN BY CATEGORY")
        print("=" * 80)

        for cat, count in sorted_categories:
            if count > 0:
                cat_name = category_names.get(cat, cat)
                print(f"\n{cat_name} ({count} connections)")
                print("-" * 80)

                # Get unique firms in this category
                firms_in_cat = defaultdict(int)
                for conn in results['categories'][cat]:
                    firms_in_cat[conn['firm']] += 1

                # Sort by count
                sorted_firms = sorted(firms_in_cat.items(), key=lambda x: x[1], reverse=True)

                for firm, firm_count in sorted_firms[:20]:  # Show top 20 firms per category
                    print(f"  {firm:50} {firm_count:2} connection(s)")

                if len(sorted_firms) > 20:
                    remaining = len(sorted_firms) - 20
                    remaining_count = sum(c for f, c in sorted_firms[20:])
                    print(f"  ... and {remaining} more firms ({remaining_count} connections)")

        print()
        print("=" * 80)


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 analyze_network_stages.py <processed_csv> [--markdown]")
        print("\nExample:")
        print("  python3 analyze_network_stages.py connections_vcpe_processed.csv")
        print("  python3 analyze_network_stages.py connections_vcpe_processed.csv --markdown")
        sys.exit(1)

    csv_file = sys.argv[1]
    markdown = '--markdown' in sys.argv or '-md' in sys.argv

    results = analyze_network(csv_file)
    print_analysis(results, markdown=markdown)
