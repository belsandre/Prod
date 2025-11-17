const fs = require('fs');
const path = require('path');

const username = process.argv[2];

if (!username) {
  console.error('Usage: node scripts/copy-functions.js <username>');
  process.exit(1);
}

const ROOT_DIR = path.join(__dirname, '..');
const SOURCE_DIR = path.join(ROOT_DIR, 'sites', username, 'functions');
const BUILD_DIR = path.join(ROOT_DIR, '_site', username);
const DEST_DIR = path.join(BUILD_DIR, 'functions');

if (!fs.existsSync(SOURCE_DIR)) {
  console.warn(`No functions directory found for ${username}, skipping auth middleware copy.`);
  process.exit(0);
}

if (!fs.existsSync(BUILD_DIR)) {
  console.warn(`Build output for ${username} not found, skipping auth middleware copy.`);
  process.exit(0);
}

fs.rmSync(DEST_DIR, { recursive: true, force: true });
fs.mkdirSync(DEST_DIR, { recursive: true });

fs.cpSync(SOURCE_DIR, DEST_DIR, { recursive: true });

console.log(`✓ Copied auth middleware to _site/${username}/functions`);

const workerPath = path.join(BUILD_DIR, '_worker.js');
const workerCode = `// Cloudflare Pages _worker.js for HTTP Basic Auth
const REALM = 'Secure Area';

function unauthorized(message = 'Authentication required') {
  return new Response(message, {
    status: 401,
    headers: {
      'WWW-Authenticate': \`Basic realm="\${REALM}"\`,
    },
  });
}

export default {
  async fetch(request, env, ctx) {
    const authorization = request.headers.get('Authorization');

    if (!authorization) {
      return unauthorized();
    }

    const [scheme, encoded] = authorization.split(' ');

    if (scheme !== 'Basic' || !encoded) {
      return unauthorized('Invalid authentication');
    }

    try {
      const buffer = Uint8Array.from(atob(encoded), c => c.charCodeAt(0));
      const decoded = new TextDecoder().decode(buffer);
      const separatorIndex = decoded.indexOf(':');

      if (separatorIndex === -1) {
        return unauthorized('Invalid authentication payload');
      }

      const username = decoded.slice(0, separatorIndex);
      const password = decoded.slice(separatorIndex + 1);

      const validUser =
        (username === env.AUTH_USERNAME && password === env.AUTH_PASSWORD) ||
        (username === env.ADMIN_USERNAME && password === env.ADMIN_PASSWORD);

      if (!validUser) {
        return unauthorized('Invalid credentials');
      }
    } catch (error) {
      return unauthorized('Invalid authentication payload');
    }

    return env.ASSETS.fetch(request);
  },
};
`;

fs.writeFileSync(workerPath, workerCode);
console.log(`✓ Created _worker.js for ${username}`);
