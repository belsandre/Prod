const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const USERS_DIR = path.join(__dirname, '..', 'users');
const SITES_DIR = path.join(__dirname, '..', 'sites');

// Get all user directories
const users = fs.readdirSync(USERS_DIR).filter(file => {
  const userPath = path.join(USERS_DIR, file);
  return fs.statSync(userPath).isDirectory() && !file.startsWith('.');
});

console.log(`Building sites for ${users.length} users: ${users.join(', ')}\n`);

let successCount = 0;
let failCount = 0;

users.forEach(username => {
  const siteDir = path.join(SITES_DIR, username);

  if (!fs.existsSync(siteDir)) {
    console.log(`⚠️  Site directory not found for ${username}, skipping...`);
    failCount++;
    return;
  }

  try {
    console.log(`Building ${username}'s site...`);
    execSync('npm run build', {
      cwd: siteDir,
      stdio: 'inherit'
    });
    console.log(`✓ Successfully built ${username}'s site\n`);
    successCount++;
  } catch (error) {
    console.error(`✗ Failed to build ${username}'s site\n`);
    failCount++;
  }
});

console.log(`\n${'='.repeat(50)}`);
console.log(`Build Summary: ${successCount} successful, ${failCount} failed`);
console.log(`${'='.repeat(50)}\n`);

if (failCount > 0) {
  process.exit(1);
}
