const fs = require('fs');
const path = require('path');

const username = process.argv[2];

if (!username) {
  console.error('Usage: node scripts/copy-functions.js <username>');
  process.exit(1);
}

const ROOT_DIR = path.join(__dirname, '..');
const SOURCE_DIR = path.join(ROOT_DIR, 'sites', username, 'functions');
const DEST_DIR = path.join(ROOT_DIR, '_site', username, 'functions');

if (!fs.existsSync(SOURCE_DIR)) {
  console.warn(`No functions directory found for ${username}, skipping auth middleware copy.`);
  process.exit(0);
}

if (!fs.existsSync(path.join(ROOT_DIR, '_site', username))) {
  console.warn(`Build output for ${username} not found, skipping auth middleware copy.`);
  process.exit(0);
}

fs.rmSync(DEST_DIR, { recursive: true, force: true });
fs.mkdirSync(DEST_DIR, { recursive: true });

fs.cpSync(SOURCE_DIR, DEST_DIR, { recursive: true });

console.log(`✓ Copied auth middleware to _site/${username}/functions`);
