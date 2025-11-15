# LinkedIn Network Analyzer - Investment Stage & Firm Type Analysis

## Overview
This workflow analyzes LinkedIn connections CSV files to categorize contacts by investment stage and firm type (early-stage VC, multi-stage VC, growth equity, private equity, LPs, etc.). It provides comprehensive breakdowns of network composition with firm categorization based on intrinsic knowledge of hundreds of VC/PE firms.

## Purpose
- Analyze the composition of a LinkedIn network by investment focus
- Categorize firms into: Early-Stage VC, Multi-Stage VC, Growth-Stage VC, Growth Equity, Private Equity, LPs/Fund of Funds, Corporate VC
- Generate detailed reports showing firm distribution and top connections
- Output analysis in markdown format for easy sharing and documentation

## Input Requirements
- A processed LinkedIn connections CSV file with **Firm** and **Role** columns already extracted
- The CSV must have been processed by the `linkedin-csv-processor.md` workflow first
- Input file should include columns: Name, Title, Firm, Role (at minimum)

## Output
- A comprehensive markdown report (`network_analysis.md`) containing:
  - Overview statistics (total connections, coverage rates)
  - Breakdown by investment stage/firm type (table format)
  - Top 30 firms by number of connections
  - Detailed breakdown by category with firm lists
- Analysis saved to the same directory as the input file

## Prerequisites

### Required Scripts
1. **parse_titles.py** - Already created by `linkedin-csv-processor.md` workflow
2. **analyze_network_stages.py** - Network analysis script (created by this workflow)

Both scripts are located at: `users/tam/workflows/`

## Processing Instructions

When the user requests network analysis on a LinkedIn connections CSV file, follow these steps:

### 1. Verify Prerequisites

First, check that the CSV has been processed with firm/role extraction:

```bash
# Check if the CSV has Firm and Role columns
head -1 <input_csv>
```

**If the CSV does NOT have Firm and Role columns**, run the `linkedin-csv-processor.md` workflow first:
```bash
python3 users/tam/workflows/parse_titles.py <input_csv> <output_csv>
```

### 2. Verify Analysis Script Exists

Check if the network analysis script exists:
- **Location**: `users/tam/workflows/analyze_network_stages.py`

If the script doesn't exist, it needs to be created. The script contains:
- Comprehensive firm categorization database (300+ firms)
- Investment stage classification logic
- Markdown and text output formatting
- Statistical analysis and reporting

**Script capabilities**:
- Categorizes firms by: early_vc, multi_stage_vc, growth_vc, growth_equity, pe, lp, corporate, other
- Uses intrinsic knowledge of firm investment strategies
- Generates both text and markdown formatted output
- Provides detailed breakdowns by category

### 3. Run the Network Analysis

Execute the analysis script in markdown mode:

```bash
python3 users/tam/workflows/analyze_network_stages.py <processed_csv> --markdown > <output_directory>/network_analysis.md
```

**Parameters**:
- `<processed_csv>`: Path to the CSV file with Firm and Role columns
- `--markdown` or `-md`: Output in markdown format (recommended)
- Without `--markdown`: Outputs plain text format with borders

**Examples**:
```bash
# Generate markdown report
python3 users/tam/workflows/analyze_network_stages.py connections_vcpe_processed.csv --markdown > network_analysis.md

# Generate text report
python3 users/tam/workflows/analyze_network_stages.py connections_vcpe_processed.csv > network_analysis.txt
```

### 4. Review and Validate Results

Read the generated markdown file to verify:
- Total connection count matches expectations
- Firm categorization appears accurate
- Coverage rates are reasonable (typically 35-40% categorized, 60-65% unknown for diverse networks)
- Top firms are correctly categorized
- Category breakdowns include expected firms

**Expected Coverage**:
- **Well-known VC/PE firms**: High categorization rate (80-90%)
- **Boutique/emerging firms**: Lower categorization rate (20-30%)
- **Overall network**: 35-65% categorization rate depending on network composition

### 5. Report Results to User

Provide the user with:
- Path to the generated markdown file
- Summary statistics (total connections, breakdown by category)
- Top 5-10 firms by connection count
- Key insights about network composition
- Any notable patterns (e.g., "VC-weighted", "PE-heavy", "early-stage focused")

## Firm Categorization Database

The analysis script includes categorization for 300+ firms across:

### Early-Stage VC (Seed, Series A)
- Examples: First Round Capital, Benchmark, 8VC (seed), Spark Capital, Slow Ventures
- Focus: Seed through Series A/B
- Typical check sizes: $500K - $10M

### Multi-Stage VC (Series A-C+)
- Examples: Andreessen Horowitz, Sequoia, Accel, Greylock, Kleiner Perkins
- Focus: Series A through growth rounds
- Typical check sizes: $5M - $100M+

### Growth-Stage VC (Late-stage venture)
- Examples: Tiger Global, DST Global, Dragoneer, Meritech Capital
- Focus: Late-stage venture, pre-IPO
- Typical check sizes: $50M - $500M+

### Growth Equity (Pre-IPO, growth buyouts)
- Examples: Vista Equity, Insight Partners, TCV, Coatue, General Atlantic, TA Associates
- Focus: Profitable/near-profitable growth companies, take minority stakes
- Typical check sizes: $25M - $500M

### Private Equity (Buyouts)
- Examples: KKR, Blackstone, Apollo, Carlyle, Bain Capital (PE), TPG
- Focus: Control buyouts, mature companies
- Typical check sizes: $100M - $10B+

### Limited Partners / Fund of Funds
- Examples: Industry Ventures, HarbourVest, StepStone, Adams Street
- Focus: Invest in VC/PE funds, secondaries
- Typical commitments: $10M - $500M per fund

### Corporate VC
- Examples: Google Ventures, Intel Capital, Salesforce Ventures
- Focus: Strategic investments aligned with parent company

## Output Format

### Markdown Report Structure

```markdown
# LinkedIn Network Analysis: Investment Stage & Firm Type

## Overview
- Total Connections: X
- Connections with Firm Data: Y (Z%)
- Connections without Firm Data: A (B%)

## Breakdown by Investment Stage / Firm Type
[Table with categories, counts, percentages]

## Top 30 Firms by Number of Connections
[Table with firm names, connection counts, categories]

## Detailed Breakdown by Category
[Sections for each category with firm tables]
```

## Workflow Extensibility

This workflow can be extended to:

### Add New Firms
Edit `users/tam/workflows/analyze_network_stages.py` and add firms to the `FIRM_CATEGORIES` dictionary:
```python
FIRM_CATEGORIES = {
    'New Firm Name': 'category',  # e.g., 'early_vc', 'multi_stage_vc', etc.
    # ...
}
```

### Add New Categories
1. Add category to `category_names` dictionary in the script
2. Update firm categorization logic
3. Add firms to new category in `FIRM_CATEGORIES`

### Export to Different Formats
- Modify the `print_analysis()` function to support JSON, CSV, or Excel output
- Add new command-line flags for different export formats

### Integration with Other Tools
- Output can be imported into Notion, Google Docs, Confluence
- JSON export could feed into dashboards or CRM systems
- CSV export for further analysis in Excel/Sheets

## Quality Standards

**Categorization Accuracy**:
- Known tier-1 firms: 95%+ accuracy
- Known tier-2 firms: 85%+ accuracy
- Emerging/boutique firms: Best-effort (may be "unknown")

**Coverage Expectations**:
- Tier-1 VC/PE heavy network: 50-70% categorization rate
- Diverse network (operators, angels, etc.): 30-50% categorization rate
- Emerging ecosystem network: 20-40% categorization rate

**No False Positives**:
- Never guess or hallucinate firm categories
- "Unknown" is acceptable and expected for firms not in database

## Troubleshooting

**Issue**: Low categorization rate (<20%)
- **Cause**: Network may be operator-heavy, non-institutional, or emerging market focused
- **Solution**: This is expected; unknown firms can be manually categorized if needed

**Issue**: Firm miscategorized
- **Cause**: Firm may have changed strategy, or database info is outdated
- **Solution**: Update `FIRM_CATEGORIES` dictionary in the script

**Issue**: Script fails with encoding errors
- **Cause**: CSV has special characters or non-UTF8 encoding
- **Solution**: Re-save CSV with UTF-8 encoding

**Issue**: Missing Firm column
- **Cause**: CSV hasn't been processed with `linkedin-csv-processor.md` workflow
- **Solution**: Run `parse_titles.py` first to extract Firm and Role columns

## Usage Examples

### Example 1: Complete Pipeline (CSV → Firm Extraction → Network Analysis)

```bash
# Step 1: Extract firms and roles from raw LinkedIn CSV
python3 users/tam/workflows/parse_titles.py connections.csv connections_processed.csv

# Step 2: Analyze network composition
python3 users/tam/workflows/analyze_network_stages.py connections_processed.csv --markdown > network_analysis.md

# Step 3: Review the results
cat network_analysis.md
```

### Example 2: Re-run Analysis on Previously Processed CSV

```bash
# If CSV already has Firm and Role columns, skip to analysis
python3 users/tam/workflows/analyze_network_stages.py connections_processed.csv --markdown > network_analysis.md
```

### Example 3: Generate Both Text and Markdown Reports

```bash
# Text format for terminal viewing
python3 users/tam/workflows/analyze_network_stages.py connections_processed.csv > network_analysis.txt

# Markdown format for documentation
python3 users/tam/workflows/analyze_network_stages.py connections_processed.csv --markdown > network_analysis.md
```

## Success Criteria

- ✅ Network analysis completes without errors
- ✅ Markdown file generated with proper formatting
- ✅ Statistics are accurate (counts, percentages add up correctly)
- ✅ Top firms are correctly categorized
- ✅ Category breakdowns show expected distribution
- ✅ Report is readable and well-formatted
- ✅ User receives actionable insights about their network composition

## Integration with Other Workflows

### Prerequisites
- **linkedin-csv-processor.md**: Must be run first to extract Firm and Role columns

### Downstream Workflows
- Results can inform targeted outreach strategies
- Category breakdowns can guide fundraising approaches
- Firm lists can be exported for CRM import
- Analysis can be combined with deal flow data for pattern recognition

## Files Referenced

- **Parser Script**: `users/tam/workflows/parse_titles.py` (from linkedin-csv-processor workflow)
- **Analysis Script**: `users/tam/workflows/analyze_network_stages.py` (this workflow)
- **Input**: Any LinkedIn connections CSV with Firm and Role columns
- **Output**: `network_analysis.md` (or `.txt` if text format preferred)

## Performance Notes

- **Processing time**: ~1-2 seconds for 500-1000 connections
- **Memory usage**: Minimal (<50MB for typical networks)
- **Scalability**: Can handle 10,000+ connections without issues

---

**Last Updated**: 2025-01-15
**Version**: 1.0
**Dependencies**:
- `parse_titles.py` from linkedin-csv-processor workflow
- Python 3.x with csv, collections modules (standard library)
**Tested With**: LinkedIn connections CSV exports (standard format, processed)
