# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **workflow and user data repository** for Claude Code processing. It contains organized workflows (prompt templates and instructions), user-specific input/output directories, and shared resources accessible across all users. User content is published as static sites via Eleventy SSG and deployed to Cloudflare Pages.

## Repository Structure

```
Prod/
├── .claude/                # Claude Code configuration
│   ├── settings.local.json # Permissions config
│   └── skills/            # Project-scoped skills
│
├── _eleventy/              # Eleventy SSG configuration and templates
│   ├── config-template.js # Base Eleventy config
│   └── templates/         # Shared layouts and templates
│
├── _site/                  # Generated static sites (gitignored)
│   └── {username}/        # Per-user built site
│
├── sites/                  # Per-user site configs (gitignored)
│   └── {username}/        # Auto-generated .eleventy.js, package.json, auth middleware
│
├── scripts/                # Build automation
│   ├── setup-sites.js     # Generate per-user configs
│   └── build-all-sites.js # Build all user sites
│
├── shared/                 # Resources accessible to all users
│   ├── inputs/            # Shared input files/data
│   ├── outputs/           # Shared output files/data
│   └── workflows/         # Shared workflow definitions
│
└── users/{username}/       # Per-user isolated resources
    ├── inputs/            # User-specific uploaded files
    ├── outputs/           # User-specific output files
    └── workflows/         # User-specific workflow definitions
```

## Architecture

### Data Organization

- **shared/**: Workflows, inputs, and outputs accessible across all users (admin-managed)
  - `shared/workflows/`: Global workflow templates available to all users
  - `shared/inputs/`: Shared input files and data
  - `shared/outputs/`: Shared output files and results
- **users/{username}/**: Isolated workspaces with user-specific inputs, outputs, and workflows
  - `users/{username}/workflows/`: User-specific workflow templates
  - `users/{username}/inputs/`: User-uploaded files and data
  - `users/{username}/outputs/`: User-specific output files and results

### Static Site Generation

Each user's content is published as a static site using Eleventy SSG:

- **Tech Stack**: Eleventy 3.0, Markdown-it, Prism syntax highlighting
- **Build System**: Node.js (>=18.0.0) with npm workspaces
- **Deployment**: GitHub Actions with smart change detection → Cloudflare Pages
- **Authentication**: HTTP Basic Auth per user via Cloudflare environment variables
- **Content Features**:
  - CSV files rendered as HTML tables with passthrough for raw downloads
  - Automatic file routing (`users/tam/workflows/test.md` → `/workflows/test/`)
  - Passthrough copy for JSON, CSV, images (PNG, JPG, SVG)
- **Per-User Sites**: ashish, tam, yani (each deployed to separate Cloudflare project)

**GitHub Actions CI/CD**: Smart builds trigger only for affected users:
- Changes in `users/ashish/` → builds ashish only
- Changes in `_eleventy/` or `scripts/` → rebuilds all sites
- Manual trigger → builds all sites

### Workflows

Markdown files containing prompts/instructions for LLM processing, located in `shared/workflows/` or `users/{username}/workflows/`. These workflows define reusable templates for common tasks and processing patterns.

#### Available User Workflows

- **users/ashish/workflows/podcast-marketer.md**: Transforms podcast transcripts into LinkedIn posts and viral social media clips
- **users/tam/workflows/conflict-resolver.md**: Systematically resolve situations where multiple portfolio companies have identical or similar names, investigating dataroom sources and applying decision frameworks
- **users/tam/workflows/deal-prioritization.md**: Analyzes fund datarooms to create tiered portfolio company research prioritization
- **users/tam/workflows/validator.md**: Auto-detects requirements from workflows/skills and validates their outputs against quality standards (source documentation, file structure, completeness, attribution)
- **users/tam/workflows/vc-research.md**: Deep research on VC portfolio companies and GPs with relationship tracking and portfolio quality assessment (resumable)

### Skills

#### Project-Scoped Skills (`.claude/skills/`)

Custom skills available to this project via the Skill tool:

- **article-extractor**: Extract clean article content from URLs
- **company-research**: Conduct thorough research on companies and key people using web search
- **csv-data-summarizer**: Analyze CSV files, generate summary stats, and plot visualizations
- **deck-to-pdf**: Download presentation slides from Pitch.com, Google Slides, Figma Slides, and Canva as searchable PDFs
- **market-assessment**: Analyze companies, identify competitors, assess competitive threats, and build competitive matrices
- **notebooklm**: Query Google NotebookLM notebooks for source-grounded, citation-backed answers
- **text-converter**: Convert folders with mixed media (images, PDFs, presentations) into faithful markdown
- **timeline-constructor**: Validate entity marketing narratives by comparing claims against objective timelines
- **video-downloader**: Extract clean article content from URLs and save as readable text
- **youtube-transcript**: Download YouTube video transcripts

#### User-Scoped Anthropic Plugins (`~/.claude/plugins/`)

Official Anthropic skills available globally (managed by plugin system):

- **example-skills**: skill-creator, mcp-builder, canvas-design, algorithmic-art, internal-comms, webapp-testing, artifacts-builder, slack-gif-creator, theme-factory, brand-guidelines
- **document-skills**: xlsx, docx, pptx, pdf - Comprehensive suite for creating, editing, and analyzing spreadsheets, documents, presentations, and PDFs

## Development Workflow

**Setup** (one-time or when adding users):
```bash
npm install
npm run setup  # Generates per-user site configs in sites/{username}/
```

**Local Development**:
```bash
npm run serve:ashish  # Start dev server for specific user
npm run serve:tam
npm run serve:yani
```

**Building**:
```bash
npm run build           # Build all user sites
npm run build:ashish   # Build specific user site
```

**Creating Workflows**: Add markdown files to `shared/workflows/` (global) or `users/{username}/workflows/` (user-specific). Workflows contain prompts and templates for LLM processing.

**Managing User Data**: Respect user isolation - only access data in `users/{username}/`. Shared resources in `shared/` are accessible across all users.

**Deployment**: Automatic via GitHub Actions on push. Sites deploy to Cloudflare Pages.

## Security Considerations

- **Data Isolation**: Maintain strict separation between user directories. Processing code should only access `users/{username}/` data when working on that user's jobs.
- **Path Traversal**: Validate all file paths to prevent access outside designated user/shared directories.
- **Sensitive Data**: Be cautious with files in user directories that may contain credentials, API keys, or other sensitive information.

## Common Tasks

**Create Global Workflow**: Add markdown file to `shared/workflows/` - accessible to all users

**Create User Workflow**: Add markdown file to `users/{username}/workflows/` - specific to that user

**Add New User**:
1. Create directory: `users/{username}/` with subdirectories `inputs/`, `outputs/`, `workflows/`
2. Run `npm run setup` to generate site config
3. Add deployment secrets to Cloudflare Pages (AUTH_USERNAME, AUTH_PASSWORD)

**Test Changes Locally**: Run `npm run serve:{username}` to preview site before deploying

**Add New Content**: Place files in `users/{username}/` - markdown, CSV, JSON, images auto-processed

## Documentation

- **STATIC_SITES_README.md**: Comprehensive guide to Eleventy setup, architecture, and maintenance
- **CLOUDFLARE_SETUP.md**: Step-by-step Cloudflare Pages deployment configuration
- **QUICKSTART.md**: 30-minute quick start guide for new users
- **CLAUDE.md** (this file): Repository structure and Claude Code guidance

## Architecture Notes

- **Static Site Focus**: Repository generates static sites from user content via Eleventy SSG
- **Data Structure**: User data in `users/{username}/inputs/` and `users/{username}/outputs/`
- **Workflow Organization**: `shared/workflows/` (global) and `users/{username}/workflows/` (user-specific)
- **Automated Deployment**: GitHub Actions CI/CD with smart change detection → Cloudflare Pages
- **No Server Required**: Pure static sites with authentication via Cloudflare Pages Functions
