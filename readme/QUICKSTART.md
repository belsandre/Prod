# Quick Start Guide

Get your static sites up and running in 30 minutes.

## 1. Install Dependencies (2 minutes)

```bash
cd /Users/changxu/Agents/Prod
npm install
```

## 2. Generate Site Configurations (1 minute)

```bash
npm run setup
```

This creates configuration files for ashish, tam, and yani.

## 3. Test Locally (5 minutes)

```bash
# Test ashish's site
npm run serve:ashish
# Open http://localhost:8080 in your browser

# In another terminal, test tam's site
npm run serve:tam

# Test yani's site
npm run serve:yani
```

## 4. Set Up Cloudflare (15 minutes)

Follow **CLOUDFLARE_SETUP.md** for detailed steps. Summary:

1. Create 3 Cloudflare Pages projects: `ashish`, `tam`, `yani`
2. Add environment variables to each project:
   - `AUTH_USERNAME` = username
   - `AUTH_PASSWORD` = unique password
   - `ADMIN_USERNAME` = admin
   - `ADMIN_PASSWORD` = same admin password for all
3. Get API token and Account ID from Cloudflare
4. Add GitHub secrets:
   - `CLOUDFLARE_API_TOKEN`
   - `CLOUDFLARE_ACCOUNT_ID`

## 5. Deploy (5 minutes)

```bash
# Make a test change
echo "# Test Page" > users/ashish/workflows/test.md

# Commit and push
git add .
git commit -m "Test static site deployment"
git push origin main
```

Watch the deployment:
- GitHub: https://github.com/[your-repo]/actions
- Should see "Deploy User Sites" workflow running
- Only ashish site will build (since only ashish folder changed)

## 6. Access Your Sites

Visit in your browser:
- https://ashish.pages.dev
- https://tam.pages.dev
- https://yani.pages.dev

Login with:
- Username: `ashish` (or `tam`, `yani`)
- Password: [password you set]

Or use admin credentials to access any site:
- Username: `admin`
- Password: [admin password you set]

## Daily Usage

### Add Content

```bash
# Add a new workflow
echo "---
title: My New Workflow
date: 2025-01-16
---

# My Workflow

Instructions here..." > users/tam/workflows/my-workflow.md

# Add research output
echo "# Company Analysis" > users/tam/outputs/research/company-analysis.md

# Commit and push
git add .
git commit -m "Add new workflow and research"
git push origin main
```

Only tam's site will rebuild (since only tam folder changed).

### View Changes

- Changes appear on site within 2-3 minutes
- Check build status: GitHub → Actions
- Check deployment: Cloudflare → Pages → [project]

## File Types

**Included in sites:**
- ✅ `.md` - Markdown (rendered as HTML)
- ✅ `.json` - JSON data
- ✅ `.csv` - CSV data
- ✅ `.png`, `.jpg`, `.svg` - Images

**Excluded from sites:**
- ❌ `.mp4`, `.mov` - Videos (too large)
- ❌ `.pdf` - PDFs (too large)
- ❌ `.zip`, `.tar` - Archives

## Folder Structure

Your existing folders work automatically:

```
users/ashish/
├── workflows/          → ashish.pages.dev/workflows/
├── outputs/            → ashish.pages.dev/outputs/
├── inputs/             → ashish.pages.dev/inputs/
└── [any-folder]/       → ashish.pages.dev/[any-folder]/
```

## Common Commands

```bash
# Regenerate site configs (after adding new user)
npm run setup

# Build all sites locally
npm run build

# Serve specific site locally
npm run serve:ashish  # or tam, yani

# Check build output
ls -la _site/ashish/
```

## Troubleshooting

**Build fails:**
```bash
rm -rf node_modules package-lock.json sites _site
npm install
npm run setup
npm run build
```

**Authentication not working:**
- Check Cloudflare → Pages → [project] → Settings → Environment variables
- Try incognito/private browsing mode

**Site not updating:**
- Check GitHub Actions for errors
- Verify changes are in `users/{username}/` directory
- Manually trigger workflow: GitHub → Actions → Deploy User Sites → Run workflow

## Documentation

- **Full setup guide**: STATIC_SITES_README.md
- **Cloudflare setup**: CLOUDFLARE_SETUP.md
- **This file**: QUICKSTART.md

## What Happens on Push

1. **Detect changes**: Which user folder changed?
2. **Conditional build**: Only build sites that changed
   - Changed `users/ashish/` → Build ashish only ✅
   - Changed `users/tam/` → Build tam only ✅
   - Changed `_eleventy/` → Build ALL sites ✅
3. **Deploy**: Upload to Cloudflare Pages
4. **Live**: Sites update automatically

**Example:**
```bash
# Edit tam's content
echo "# Update" >> users/tam/workflows/vc-research.md
git add . && git commit -m "Update" && git push

# Result:
# ✅ tam site builds and deploys
# ⏭️  ashish site skipped (no changes)
# ⏭️  yani site skipped (no changes)
```

## Next Steps

1. ✅ Complete Cloudflare setup (CLOUDFLARE_SETUP.md)
2. ✅ Push test commit to verify deployment
3. ✅ Add real content to user folders
4. ✅ Customize templates if needed (STATIC_SITES_README.md)
5. ✅ Share site URLs with users

## Support

- Check GitHub Actions logs for build errors
- Check Cloudflare Pages deployment logs
- Review STATIC_SITES_README.md for details
- Check Eleventy docs: https://www.11ty.dev/docs/
