const fs = require('fs');
const path = require('path');

module.exports = function() {
  const jsonPath = path.resolve(__dirname, '../../../users/tam/hyperion/marketing-to-reality/_data/claims.json');

  try {
    const jsonContent = fs.readFileSync(jsonPath, 'utf-8');
    const claimsData = JSON.parse(jsonContent);
    console.log('[DATA] Loaded hyperionClaims with', claimsData.key_claims?.length, 'key claims');
    return claimsData;
  } catch (error) {
    console.warn(`Warning: Could not load claims.json: ${error.message}`);
    return {
      metadata: {},
      executive_summary: {},
      critical_issues: [],
      key_claims: [],
      summary: {},
      recommendations: []
    };
  }
};
