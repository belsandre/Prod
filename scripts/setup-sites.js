const fs = require('fs');
const path = require('path');

const USERS_DIR = path.join(__dirname, '..', 'users');
const SITES_DIR = path.join(__dirname, '..', 'sites');
const TEMPLATE_DIR = path.join(__dirname, '..', '_eleventy');

// Ensure sites directory exists
if (!fs.existsSync(SITES_DIR)) {
  fs.mkdirSync(SITES_DIR, { recursive: true });
}

// Get all user directories
const users = fs.readdirSync(USERS_DIR).filter(file => {
  const userPath = path.join(USERS_DIR, file);
  return fs.statSync(userPath).isDirectory() && !file.startsWith('.');
});

console.log(`Found ${users.length} users: ${users.join(', ')}`);

// Create site configuration for each user
users.forEach(username => {
  const siteDir = path.join(SITES_DIR, username);
  const functionsDir = path.join(siteDir, 'functions');

  // Create site directory
  if (!fs.existsSync(siteDir)) {
    fs.mkdirSync(siteDir, { recursive: true });
  }

  // Create functions directory for Cloudflare Pages
  if (!fs.existsSync(functionsDir)) {
    fs.mkdirSync(functionsDir, { recursive: true });
  }

  // Create .eleventy.js
  const eleventyConfig = `const configTemplate = require('../../_eleventy/config-template.js');

module.exports = function(eleventyConfig) {
  const username = '${username}';

  // Set environment variable for templates
  process.env.SITE_USERNAME = username;

  // Apply base configuration
  return configTemplate(eleventyConfig, username);
};
`;

  fs.writeFileSync(path.join(siteDir, '.eleventy.js'), eleventyConfig);
  console.log(`✓ Created .eleventy.js for ${username}`);

  // Create package.json
  const packageJson = {
    name: `site-${username}`,
    version: "1.0.0",
    private: true,
    scripts: {
      "build": "eleventy",
      "serve": "eleventy --serve",
      "debug": "DEBUG=Eleventy* eleventy"
    }
  };

  fs.writeFileSync(
    path.join(siteDir, 'package.json'),
    JSON.stringify(packageJson, null, 2)
  );
  console.log(`✓ Created package.json for ${username}`);

  // Copy index.njk to user's directory if it doesn't exist
  const userIndexPath = path.join(USERS_DIR, username, 'index.njk');
  if (!fs.existsSync(userIndexPath)) {
    const indexTemplate = fs.readFileSync(
      path.join(TEMPLATE_DIR, 'templates', 'index.njk'),
      'utf8'
    );
    fs.writeFileSync(userIndexPath, indexTemplate);
    console.log(`✓ Created index.njk for ${username}`);
  }

  // Copy directory.njk to user's directory if it doesn't exist
  const userDirectoryPath = path.join(USERS_DIR, username, 'directory.njk');
  if (!fs.existsSync(userDirectoryPath)) {
    const directoryTemplate = fs.readFileSync(
      path.join(TEMPLATE_DIR, 'templates', 'directory.njk'),
      'utf8'
    );
    fs.writeFileSync(userDirectoryPath, directoryTemplate);
    console.log(`✓ Created directory.njk for ${username}`);
  }

  // Create HTTP Basic Auth middleware
  const middlewareCode = `// HTTP Basic Auth for Cloudflare Pages
export async function onRequest(context) {
  const { request, env, next } = context;

  // Get authorization header
  const authorization = request.headers.get('Authorization');

  if (!authorization) {
    return new Response('Authentication required', {
      status: 401,
      headers: {
        'WWW-Authenticate': 'Basic realm="Secure Area"',
      },
    });
  }

  // Parse credentials
  const [scheme, encoded] = authorization.split(' ');

  if (!encoded || scheme !== 'Basic') {
    return new Response('Invalid authentication', {
      status: 401,
      headers: {
        'WWW-Authenticate': 'Basic realm="Secure Area"',
      },
    });
  }

  // Decode credentials
  const buffer = Uint8Array.from(atob(encoded), c => c.charCodeAt(0));
  const decoded = new TextDecoder().decode(buffer);
  const [username, password] = decoded.split(':');

  // Check credentials against environment variables
  const validUser = (
    (username === env.AUTH_USERNAME && password === env.AUTH_PASSWORD) ||
    (username === env.ADMIN_USERNAME && password === env.ADMIN_PASSWORD)
  );

  if (!validUser) {
    return new Response('Invalid credentials', {
      status: 401,
      headers: {
        'WWW-Authenticate': 'Basic realm="Secure Area"',
      },
    });
  }

  // Authentication successful, continue to next middleware/page
  return next();
}
`;

  fs.writeFileSync(path.join(functionsDir, '_middleware.js'), middlewareCode);
  console.log(`✓ Created auth middleware for ${username}`);
});

console.log(`\\n✅ Setup complete! Created configurations for ${users.length} users.`);
console.log('\\nNext steps:');
console.log('1. Run: npm install');
console.log('2. Test locally: npm run serve:ashish (or tam/yani)');
console.log('3. Build all sites: npm run build');
