# Static Sites Setup & Maintenance Guide

This repository automatically generates and deploys static sites for each user using Eleventy and Cloudflare Pages.

## Overview

- **Users**: ashish, tam, yani
- **Site URLs**:
  - https://ashish.pages.dev
  - https://tam.pages.dev
  - https://yani.pages.dev
- **Authentication**: HTTP Basic Auth (user-specific credentials)
- **Build Trigger**: Automatic on push to main (only rebuilds changed sites)
- **Content**: .md, .json, .csv files (videos/large files excluded)

## Architecture

```
Prod/
├── _eleventy/                  # Shared Eleventy templates & config
│   ├── config-template.js      # Base Eleventy configuration
│   └── templates/              # Layouts and includes
│       ├── _includes/layouts/  # Base, page layouts
│       ├── _data/              # Global data files
│       └── index.njk           # Homepage template
├── scripts/
│   ├── setup-sites.js          # Generate site configs
│   └── build-all-sites.js      # Build all sites locally
├── sites/ (gitignored)         # Generated per-user configs
│   └── {username}/
│       ├── .eleventy.js        # User-specific config
│       ├── package.json        # User-specific dependencies
│       └── functions/
│           └── _middleware.js  # HTTP Basic Auth
├── users/{username}/           # Source content (existing)
│   ├── workflows/
│   ├── outputs/
│   └── inputs/
└── _site/ (gitignored)         # Build output
    └── {username}/             # Static site files
```

## Initial Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Generate Site Configurations

```bash
npm run setup
```

This will:
- Create `sites/{username}/` directories for each user
- Generate `.eleventy.js` configurations
- Create HTTP Basic Auth middleware
- Copy homepage templates to user directories

### 3. Configure Cloudflare

#### A. Create Cloudflare Pages Projects

1. Go to Cloudflare Dashboard → Pages
2. Create three new projects:
   - Name: `ashish` (will be ashish.pages.dev)
   - Name: `tam` (will be tam.pages.dev)
   - Name: `yani` (will be yani.pages.dev)
3. For each project:
   - Build configuration: **None** (using GitHub Actions)
   - Build command: Leave empty
   - Build output directory: Leave empty

#### B. Set Environment Variables

For each Cloudflare Pages project, add these environment variables:

**For ashish.pages.dev:**
```
AUTH_USERNAME=ashish
AUTH_PASSWORD=[strong-unique-password]
ADMIN_USERNAME=admin
ADMIN_PASSWORD=[admin-password-same-for-all]
```

**For tam.pages.dev:**
```
AUTH_USERNAME=tam
AUTH_PASSWORD=[strong-unique-password]
ADMIN_USERNAME=admin
ADMIN_PASSWORD=[admin-password-same-for-all]
```

**For yani.pages.dev:**
```
AUTH_USERNAME=yani
AUTH_PASSWORD=[strong-unique-password]
ADMIN_USERNAME=admin
ADMIN_PASSWORD=[admin-password-same-for-all]
```

#### C. Get Cloudflare API Credentials

1. Go to Cloudflare Dashboard → My Profile → API Tokens
2. Create a new token with "Cloudflare Pages - Edit" permissions
3. Copy the token and your Account ID (found in Pages URL)

### 4. Configure GitHub Secrets

Add these secrets to your GitHub repository (Settings → Secrets and variables → Actions):

```
CLOUDFLARE_API_TOKEN=your-cloudflare-api-token
CLOUDFLARE_ACCOUNT_ID=your-cloudflare-account-id
```

## Testing Locally

### Build and Serve Individual Sites

```bash
# Ashish's site
npm run serve:ashish
# Visit http://localhost:8080

# Tam's site
npm run serve:tam

# Yani's site
npm run serve:yani
```

### Build All Sites

```bash
npm run build
```

This will generate static files in `_site/{username}/` for each user.

## How It Works

### Automatic Builds

When you push to the `main` branch:

1. **Change Detection**: GitHub Actions detects which user folders changed
   - If `users/ashish/` changed → builds ashish site only
   - If `users/tam/` changed → builds tam site only
   - If `_eleventy/` changed → rebuilds ALL sites

2. **Conditional Build**: Only changed sites are built (saves time & resources)

3. **Deploy**: Built sites are uploaded to Cloudflare Pages

4. **Authentication**: Each site requires username/password to access

### Content Organization

Eleventy automatically discovers and organizes content from `users/{username}/`:

- **Workflows**: `users/{username}/workflows/*.md` → `/workflows/` on site
- **Outputs**: `users/{username}/outputs/*.md` → `/outputs/` on site
- **Other folders**: Automatically included and navigable
- **File types**: Only `.md`, `.json`, `.csv` files are included (videos/large files excluded)

## Adding a New User

1. Create the user directory structure:
   ```bash
   mkdir -p users/newuser/{workflows,outputs,inputs}
   ```

2. Add some content:
   ```bash
   echo "# Test Workflow" > users/newuser/workflows/test.md
   ```

3. Regenerate site configurations:
   ```bash
   npm run setup
   ```

4. Update GitHub Actions workflow (`.github/workflows/deploy-sites.yml`):
   - Add `newuser` to detect-changes job outputs
   - Add `build-newuser` job
   - Add `deploy-newuser` job

5. Create Cloudflare Pages project named `newuser`

6. Set environment variables for `newuser.pages.dev`

7. Update npm scripts in root `package.json`:
   ```json
   "build:newuser": "cd sites/newuser && npm run build",
   "serve:newuser": "cd sites/newuser && npm run serve"
   ```

## Customizing Templates

### Global Styling

Edit `_eleventy/templates/_includes/layouts/base.njk` to change:
- Colors and fonts
- Navigation structure
- Header/footer content
- CSS styles

Changes apply to all user sites.

### Per-User Customization

Create user-specific layouts in `users/{username}/_includes/layouts/`:

```njk
---
layout: layouts/base.njk
---
<div class="custom-user-style">
  {{ content | safe }}
</div>
```

## Authentication Management

### Changing User Passwords

1. Go to Cloudflare Dashboard → Pages → [project-name]
2. Settings → Environment variables
3. Update `AUTH_PASSWORD` value
4. Redeploy (push to main or manual GitHub Actions trigger)

### Admin Access

The admin credentials (`ADMIN_USERNAME` / `ADMIN_PASSWORD`) allow access to ALL sites. Keep these secure and consistent across all projects.

## Troubleshooting

### Build Fails

**Check Node version:**
```bash
node --version  # Should be >= 18.0.0
```

**Clear and rebuild:**
```bash
rm -rf node_modules package-lock.json sites _site
npm install
npm run setup
npm run build
```

### Site Not Updating

**Manual rebuild:**
1. Go to GitHub → Actions
2. Click "Deploy User Sites"
3. Click "Run workflow" → Run workflow

**Check if changes are in correct path:**
- Changes must be in `users/{username}/` to trigger rebuild
- Changes to `.md`, `.json`, or `.csv` files

### Authentication Not Working

**Verify environment variables:**
1. Cloudflare Pages project settings
2. Check `AUTH_USERNAME` and `AUTH_PASSWORD` are set correctly
3. Try incognito/private browsing mode

**Check middleware:**
```bash
cat sites/{username}/functions/_middleware.js
```

### Content Not Showing

**Check file types:**
- Only `.md`, `.json`, `.csv` files are included
- PDFs, videos, and large files are excluded

**Verify frontmatter:**
Markdown files should have frontmatter:
```md
---
title: My Document
date: 2025-01-16
---

Content here...
```

## Monitoring

### Build Status

Check GitHub Actions:
- https://github.com/[your-repo]/actions

### Deployment Status

Check Cloudflare Pages:
- https://dash.cloudflare.com/[account-id]/pages

### Analytics

Enable Cloudflare Web Analytics:
1. Cloudflare Pages → [project] → Analytics
2. Enable Web Analytics (free, privacy-focused)

## File Structure Reference

### Content File Types

**Included:**
- `.md` - Markdown documents (rendered as HTML)
- `.json` - JSON data (syntax highlighted)
- `.csv` - CSV data (syntax highlighted)
- `.png`, `.jpg`, `.gif`, `.svg` - Images

**Excluded:**
- `.mp4`, `.mov`, `.avi` - Videos (too large)
- `.pdf` - PDFs (large files)
- `.zip`, `.tar`, `.gz` - Archives

### Special Files

- `users/{username}/index.njk` - Homepage (auto-generated if missing)
- `users/{username}/_data/` - Custom data files
- `users/{username}/_includes/` - User-specific templates

## Best Practices

1. **Commit frequently**: Each push triggers automatic builds for changed sites

2. **Use meaningful filenames**: Files are displayed based on their names
   - Good: `company-research-summary.md`
   - Bad: `output_1.md`

3. **Add frontmatter**: Improves site organization
   ```md
   ---
   title: Readable Title
   date: 2025-01-16
   tags: [research, analysis]
   ---
   ```

4. **Keep files organized**: Use folders to structure content
   ```
   users/tam/
   ├── workflows/
   ├── outputs/
   │   └── hyperion/
   │       ├── tier1/
   │       └── tier2/
   └── inputs/
   ```

5. **Test locally first**: Run `npm run serve:{username}` before pushing

## Support

For issues or questions:
- Check GitHub Actions logs for build errors
- Check Cloudflare Pages deployment logs
- Review this documentation
- Check Eleventy docs: https://www.11ty.dev/docs/

## Maintenance Schedule

- **Weekly**: Review build logs for errors
- **Monthly**: Update dependencies (`npm update`)
- **Quarterly**: Review and rotate passwords
- **As needed**: Add new users or customize templates
