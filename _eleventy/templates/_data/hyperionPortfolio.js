const fs = require('fs');
const path = require('path');

module.exports = function() {
  const jsonPath = path.resolve(__dirname, '../../../users/tam/hyperion/marketing-to-reality/_data/portfolio.json');

  try {
    const jsonContent = fs.readFileSync(jsonPath, 'utf-8');
    const portfolioData = JSON.parse(jsonContent);
    console.log('[DATA] Loaded hyperionPortfolio with', portfolioData.portfolio_overview?.total_companies, 'companies');
    return portfolioData;
  } catch (error) {
    console.warn(`Warning: Could not load portfolio.json: ${error.message}`);
    return {
      fund_name: "",
      analysis_date: "",
      overall_health: "",
      health_descriptor: "",
      portfolio_overview: {},
      executive_summary: {},
      by_sector: [],
      stage_evolution: {},
      defensibility: {},
      companies: { winners: [], emerging: [], red_flags: [], other: [], unresearched: [] },
      key_risk: {},
      recommendations: {},
      source_tier_summary: {}
    };
  }
};
