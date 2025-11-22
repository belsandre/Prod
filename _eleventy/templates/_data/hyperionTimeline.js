const fs = require('fs');
const path = require('path');

module.exports = function() {
  // Load timeline data for Hyperion analysis
  const jsonPath = path.resolve(__dirname, '../../../users/tam/hyperion/marketing-to-reality/_data/timeline.json');

  try {
    const jsonContent = fs.readFileSync(jsonPath, 'utf-8');
    const timelineData = JSON.parse(jsonContent);
    console.log('[DATA] Loaded hyperionTimeline with', timelineData.timeline?.length, 'events');
    return timelineData;
  } catch (error) {
    console.warn(`Warning: Could not load timeline.json: ${error.message}`);
    return {
      metadata: { source_distribution: {} },
      timeline: [],
      findings: [],
      verification_priorities: []
    };
  }
};
