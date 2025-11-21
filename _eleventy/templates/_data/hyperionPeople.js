const fs = require('fs');
const path = require('path');

module.exports = function() {
  const jsonPath = path.resolve(__dirname, '../../../users/tam/hyperion/marketing-to-reality/_data/people.json');

  try {
    const jsonContent = fs.readFileSync(jsonPath, 'utf-8');
    const peopleData = JSON.parse(jsonContent);
    console.log('[DATA] Loaded hyperionPeople with', peopleData.general_partners?.length, 'general partners');
    return peopleData;
  } catch (error) {
    console.warn(`Warning: Could not load people.json: ${error.message}`);
    return {
      entity_name: "",
      fund_name: "",
      analysis_date: "",
      general_partners: [],
      critical_people_gaps: [],
      team_structure_assessment: {},
      risk_synthesis: {},
      executive_summary: {}
    };
  }
};
