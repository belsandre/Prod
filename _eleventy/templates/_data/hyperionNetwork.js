const fs = require('fs');
const path = require('path');

module.exports = function() {
  const jsonPath = path.resolve(__dirname, '../../../users/tam/hyperion/marketing-to-reality/_data/network.json');

  try {
    const jsonContent = fs.readFileSync(jsonPath, 'utf-8');
    const networkData = JSON.parse(jsonContent);
    console.log('[DATA] Loaded hyperionNetwork with', networkData.top_firms?.length, 'top firms');
    return networkData;
  } catch (error) {
    console.warn(`Warning: Could not load network.json: ${error.message}`);
    return {
      metadata: {},
      overall_statistics: {},
      top_firms: [],
      strategic_relationships: [],
      network_gaps: [],
      verification_priorities: [],
      summary: {}
    };
  }
};
