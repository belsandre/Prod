# Cloudflare Pages Setup Guide

Step-by-step instructions for setting up Cloudflare Pages and authentication.

## Prerequisites

- Cloudflare account (free tier works)
- GitHub repository with push access
- Repository already has the Eleventy setup (see STATIC_SITES_README.md)

## Part 1: Create Cloudflare Pages Projects

### Step 1: Create First Project (Ashish)

1. Log into Cloudflare Dashboard: https://dash.cloudflare.com
2. In the sidebar, click **Pages**
3. Click **Create a project**
4. Click **Connect to Git**
5. Click **GitHub** and authorize Cloudflare to access your GitHub account
   - You'll be redirected to GitHub to grant permissions
   - Select which repositories to grant access (you can select just this repo or all repos)
   - Click **Install & Authorize**
6. Back in Cloudflare, select your repository from the list
7. Configure build settings:
   - **Project name**: `ashish`
   - **Production branch**: `main`
   - **Framework preset**: `None` (or select `Eleventy` if available)
   - **Build command**: `npm run build:ashish`
   - **Build output directory**: `_site/ashish`
   - **Root directory (advanced)**: Leave blank
   - **Environment variables**: Leave empty for now (we'll add these after project creation)
8. Click **Save and Deploy**
9. Cloudflare will start the first build - this may take a few minutes
   - ⚠️ The first build may fail if you haven't run `npm run setup` locally yet - that's okay, we'll fix it in Part 2

### Step 2: Create Additional Projects

Repeat Step 1 for each user, with these settings:

**For Tam:**
- **Project name**: `tam`
- **Production branch**: `main`
- **Build command**: `npm run build:tam`
- **Build output directory**: `_site/tam`

**For Yani:**
- **Project name**: `yani`
- **Production branch**: `main`
- **Build command**: `npm run build:yani`
- **Build output directory**: `_site/yani`

You should now have three projects:
- ashish.pages.dev
- tam.pages.dev
- yani.pages.dev

**Note:** Each project is connected to the same repository but builds a different user's site using a different build command.

## Part 2: Configure Authentication

### Step 1: Set Up Environment Variables for Ashish

1. Go to **Pages** → Click **ashish** project
2. Click **Settings** tab
3. Scroll to **Environment variables**
4. Click **Add variable**

Add these four variables (for Production and Preview):

| Variable Name | Value | Environment |
|--------------|-------|-------------|
| `AUTH_USERNAME` | `ashish` | Production and Preview |
| `AUTH_PASSWORD` | [Create strong password] | Production and Preview |
| `ADMIN_USERNAME` | `admin` | Production and Preview |
| `ADMIN_PASSWORD` | [Create admin password] | Production and Preview |

**Important Notes:**
- Use a **strong, unique** password for `AUTH_PASSWORD`
- Use the **same** `ADMIN_USERNAME` and `ADMIN_PASSWORD` across ALL projects
- Save these passwords securely (password manager recommended)
- Click "Add variable" after each entry

### Step 2: Set Up Environment Variables for Tam

1. Go to **Pages** → Click **tam** project
2. Click **Settings** tab → **Environment variables**
3. Add the same four variables:

| Variable Name | Value | Environment |
|--------------|-------|-------------|
| `AUTH_USERNAME` | `tam` | Production and Preview |
| `AUTH_PASSWORD` | [Create strong password - DIFFERENT from ashish] | Production and Preview |
| `ADMIN_USERNAME` | `admin` | Production and Preview |
| `ADMIN_PASSWORD` | [SAME as ashish's admin password] | Production and Preview |

### Step 3: Set Up Environment Variables for Yani

1. Go to **Pages** → Click **yani** project
2. Click **Settings** tab → **Environment variables**
3. Add the same four variables:

| Variable Name | Value | Environment |
|--------------|-------|-------------|
| `AUTH_USERNAME` | `yani` | Production and Preview |
| `AUTH_PASSWORD` | [Create strong password - DIFFERENT from others] | Production and Preview |
| `ADMIN_USERNAME` | `admin` | Production and Preview |
| `ADMIN_PASSWORD` | [SAME as others' admin password] | Production and Preview |

### Password Summary

You should have created:
- 3 unique user passwords (one for ashish, tam, yani)
- 1 shared admin password (same across all sites)
- Total: 4 passwords to save securely

**Example:**
```
ashish.pages.dev:
  - Username: ashish, Password: StrongPass123!
  - Username: admin, Password: AdminSecure456!

tam.pages.dev:
  - Username: tam, Password: UniquePass789!
  - Username: admin, Password: AdminSecure456! (same)

yani.pages.dev:
  - Username: yani, Password: DifferentPass012!
  - Username: admin, Password: AdminSecure456! (same)
```

## Part 3: Get Cloudflare API Credentials

### Step 1: Create API Token

1. In Cloudflare Dashboard, click your profile icon (top right)
2. Click **My Profile**
3. Click **API Tokens** (left sidebar)
4. Click **Create Token**
5. Find **Cloudflare Pages** template and click **Use template**
6. Configuration should be:
   - **Token name**: GitHub Actions Pages Deploy
   - **Permissions**: Cloudflare Pages - Edit
   - **Account Resources**: Include → Your Account
7. Click **Continue to summary**
8. Click **Create Token**
9. **Copy the token** - you won't see it again!
   - Format: `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - Save it securely

### Step 2: Get Account ID

1. Go back to **Pages** in Cloudflare Dashboard
2. Click any project (e.g., ashish)
3. Look at the URL in your browser:
   ```
   https://dash.cloudflare.com/YOUR_ACCOUNT_ID/pages/view/ashish
   ```
4. Copy the `YOUR_ACCOUNT_ID` part (32-character hexadecimal string)
5. Save it securely

## Part 4: Configure GitHub Secrets

### Step 1: Add Secrets to GitHub

1. Go to your GitHub repository
2. Click **Settings** tab
3. In the sidebar, click **Secrets and variables** → **Actions**
4. Click **New repository secret**

### Step 2: Add CLOUDFLARE_API_TOKEN

1. Name: `CLOUDFLARE_API_TOKEN`
2. Secret: [Paste the API token from Part 3, Step 1]
3. Click **Add secret**

### Step 3: Add CLOUDFLARE_ACCOUNT_ID

1. Click **New repository secret**
2. Name: `CLOUDFLARE_ACCOUNT_ID`
3. Secret: [Paste the Account ID from Part 3, Step 2]
4. Click **Add secret**

## Part 5: Test the Setup

### Step 1: Initial Deployment

1. In your local repository, make a small change:
   ```bash
   echo "# Test" >> users/ashish/workflows/test.md
   ```

2. Commit and push:
   ```bash
   git add .
   git commit -m "Test static site deployment"
   git push origin main
   ```

3. Watch GitHub Actions:
   - Go to GitHub repository → **Actions** tab
   - You should see "Deploy User Sites" workflow running
   - Click on it to see progress

### Step 2: Verify Build

The workflow should:
- ✅ Detect changes in users/ashish
- ✅ Build ashish site only
- ✅ Upload to Cloudflare Pages
- ✅ Deploy successfully

### Step 3: Test Authentication

1. Open https://ashish.pages.dev in your browser
2. You should see a login prompt
3. Enter credentials:
   - Username: `ashish`
   - Password: [ashish's password you set]
4. You should see the site!

### Step 4: Test Admin Access

1. Open https://tam.pages.dev in your browser
2. At the login prompt, enter:
   - Username: `admin`
   - Password: [admin password you set]
3. You should see tam's site!
4. Admin credentials work on ALL sites

## Troubleshooting

### "Invalid credentials" error

**Check:**
1. Cloudflare Pages → [project] → Settings → Environment variables
2. Verify `AUTH_USERNAME` and `AUTH_PASSWORD` are set correctly
3. Make sure you selected "Production and Preview" when adding variables
4. Try in incognito/private browsing mode (clears cached auth)

### "404 Not Found" on site

**Possible causes:**
1. First deployment hasn't happened yet - check GitHub Actions
2. Build failed - check GitHub Actions logs
3. Project name mismatch - verify Cloudflare project names are exactly: `ashish`, `tam`, `yani`

### GitHub Actions workflow fails

**Check:**
1. GitHub Secrets are set correctly (exact names: `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_ACCOUNT_ID`)
2. API token has "Cloudflare Pages - Edit" permissions
3. Account ID is correct (32-character hex string)

**View logs:**
1. GitHub → Actions → Click failed workflow
2. Click failed job
3. Expand failed step to see error message

### Deployment succeeds but shows blank page

**Check:**
1. Cloudflare Pages → [project] → View deployment
2. Look for "Functions" tab - middleware should be present
3. Verify `functions/_middleware.js` exists in deployment
4. Check browser console for errors (F12 → Console)

## Verification Checklist

Use this checklist to ensure everything is set up correctly:

- [ ] Three Cloudflare Pages projects created (ashish, tam, yani)
- [ ] Each project has 4 environment variables set (AUTH_USERNAME, AUTH_PASSWORD, ADMIN_USERNAME, ADMIN_PASSWORD)
- [ ] Admin password is the SAME across all three projects
- [ ] User passwords are DIFFERENT for each project
- [ ] API token created with Cloudflare Pages - Edit permissions
- [ ] Account ID copied from Cloudflare dashboard
- [ ] Two GitHub secrets added (CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID)
- [ ] Test commit pushed to main branch
- [ ] GitHub Actions workflow ran successfully
- [ ] All three sites accessible at .pages.dev URLs
- [ ] Authentication prompts appear when visiting sites
- [ ] User credentials work on their respective sites
- [ ] Admin credentials work on all sites

## Next Steps

Once setup is complete:

1. **Customize content**: Add markdown files to `users/{username}/`
2. **Monitor builds**: Check GitHub Actions after each push
3. **Manage passwords**: Store securely, rotate periodically
4. **Optional**: Set up custom domains (see Cloudflare Pages docs)

## Custom Domains (Optional)

If you want to use your own domains instead of .pages.dev:

1. Go to Cloudflare Pages → [project] → **Custom domains**
2. Click **Set up a custom domain**
3. Enter domain: `ashish.yourdomain.com`
4. Follow DNS configuration steps
5. Repeat for tam and yani

**Requirements:**
- Domain must be managed by Cloudflare DNS
- You need access to add DNS records

## Support Resources

- **Cloudflare Pages Docs**: https://developers.cloudflare.com/pages/
- **Cloudflare Pages Functions**: https://developers.cloudflare.com/pages/functions/
- **API Token Docs**: https://developers.cloudflare.com/fundamentals/api/get-started/create-token/

## Security Best Practices

1. **Use strong passwords**: Minimum 16 characters, mix of letters/numbers/symbols
2. **Store securely**: Use a password manager
3. **Rotate regularly**: Change passwords every 90 days
4. **Limit API token scope**: Only grant Cloudflare Pages permissions
5. **Monitor access**: Check Cloudflare Analytics regularly
6. **Enable 2FA**: On your Cloudflare account

## Password Reset Procedure

If you need to reset a user's password:

1. Go to Cloudflare Pages → [project] → Settings → Environment variables
2. Find `AUTH_PASSWORD`
3. Click **Edit**
4. Enter new password
5. Click **Save**
6. Password takes effect immediately (no redeploy needed)

**Note**: Changes to environment variables in Cloudflare Pages take effect immediately for new requests, but existing authenticated sessions may remain active until they expire or the user clears cookies.
