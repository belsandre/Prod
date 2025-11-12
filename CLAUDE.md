# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **multi-user job queue system** for Claude Code that allows users to submit jobs via a web interface, which are then processed by a local Claude Code instance. The system supports workflow-based processing, file uploads, threaded conversations, and role-based access control.

## Repository Structure

```
Prod/
├── web_interface/          # Flask web application
│   ├── app.py             # Main Flask application
│   ├── queue_manager.py   # Job queue management (SQLite)
│   ├── user_manager.py    # User authentication and management
│   ├── config.py          # Configuration settings
│   ├── queue_watcher.py   # CLI tool for processing jobs
│   ├── templates/         # HTML templates
│   ├── static/            # Static assets (CSS, JS)
│   ├── uploads/           # Legacy upload location (deprecated)
│   ├── outputs/           # Legacy output location (deprecated)
│   ├── jobs.db            # SQLite database (auto-created)
│   ├── users.json         # User accounts database
│   └── *.md               # Documentation (README, guides)
│
├── shared/                 # Resources accessible to all users
│   ├── inputs/            # Shared input files/data
│   ├── outputs/           # Shared output files/data
│   └── workflows/         # Shared workflow definitions (markdown files)
│
└── users/{username}/       # Per-user isolated resources
    ├── inputs/            # User-specific uploaded files
    ├── outputs/           # User-specific output files
    └── workflows/         # User-specific workflow definitions (markdown)
```

## Architecture

### Multi-Tenant Structure

- **web_interface/**: Flask web app with authentication, role-based access control, job submission/management UI, and Cloudflare Tunnel integration
- **shared/**: Workflows, inputs, and outputs accessible across all users (admin-managed)
- **users/{username}/**: Isolated workspaces with user-specific inputs, outputs, and workflows

### Job Queue System

SQLite-based job lifecycle:
1. **Submission**: Jobs can include prompts, file uploads, workflows, URLs, and priority settings
2. **Approval**: Manual (admin approval required) or auto mode
3. **Processing**: Queue watcher (`queue_watcher.py`) picks up approved jobs in interactive or watch mode
4. **Completion**: Results stored as text or files, viewable via web interface

### Workflows

Markdown files containing prompts/instructions for LLM processing, located in `shared/workflows/` or `users/{username}/workflows/`. Users select workflows when submitting jobs.

#### Available User Workflows

- **users/ashish/workflows/podcast-marketer.md**: Transforms podcast transcripts into LinkedIn posts and viral social media clips
- **users/tam/workflows/deal-prioritization.md**: Analyzes fund datarooms to create tiered portfolio company research prioritization
- **users/tam/workflows/vc-research.md**: Deep research on VC portfolio companies and GPs with relationship tracking and portfolio quality assessment (resumable)

### Threading System

Jobs support threaded conversations via `parent_job_id` for multi-turn interactions and iterative refinement.

### Skills

User-scoped Claude Code skills available via the Skill tool and located in `~/.claude/skills/`or `~/.claude/plugins/marketplaces/anthropic-agent-skills`:
- **deck-to-pdf**: Download presentation slides from Pitch.com, Google Slides, Figma Slides, and Canva as searchable PDFs
- **company-research**: Conduct thorough research on companies and key people using web search
- **video-downloader**: Extract clean article content from URLs and save as readable text
- **text-converter**: Convert folders with mixed media (images, PDFs, presentations) into faithful markdown
- **notebooklm**: Query Google NotebookLM notebooks for source-grounded, citation-backed answers
- **csv-data-summarizer**: Analyze CSV files, generate summary stats, and plot visualizations
- **market-assessment**: Analyze companies, identify competitors, assess competitive threats, and build competitive matrices
- **youtube-transcript**: Download YouTube video transcripts
- **skill-creator**: Guide for creating effective skills that extend Claude's capabilities with specialized knowledge, workflows, or tool integrations
- **document-skills (xlsx, docx, pptx, pdf)**: Comprehensive suite for creating, editing, and analyzing spreadsheets, documents, presentations, and PDFs with support for formulas, formatting, tracked changes, comments, and more

## Key Files

- **config.py**: Authentication, processing mode, file upload settings, path configurations
- **app.py**: Flask routes for authentication, dashboard, job submission/management, admin functions
- **queue_manager.py**: SQLite job queue operations, CRUD, status tracking, threading
- **user_manager.py**: User authentication, role-based permissions, folder mapping
- **queue_watcher.py**: CLI tool for processing jobs (interactive/watch modes)
- **jobs.db**: SQLite database with job metadata, status, files, outputs, threading info

## Development Workflow

**Adding Features**: Update schema in `queue_manager.py`, add routes in `app.py`, update templates/config, document changes

**User Data**: Respect user isolation (users access only their data; admins can access all). Use `Config.get_user_input_folder()` and `Config.get_user_output_folder()`

**Processing Jobs**: Run `queue_watcher.py`, read files from `users/{username}/inputs/`, process per instructions/workflows, save to `users/{username}/outputs/`, mark completed

## Security Considerations

Change default credentials, use strong SECRET_KEY, validate file uploads, prevent path traversal, enforce role-based access control, use HTTPS via Cloudflare Tunnel for public access.

## Documentation

See `web_interface/` for README.md, QUICKSTART.md, JOB_PROCESSING_GUIDE.md, and MULTI_USER_THREADS_GUIDE.md.

## Common Tasks

**Add User**: `cd web_interface && python3 manage_users.py`
**Run Web Interface**: `cd web_interface && python3 app.py` (http://localhost:5001)
**Process Jobs**: `cd web_interface && python3 queue_watcher.py [--watch|--stats]`
**Create Workflows**: Add markdown files to `shared/workflows/` or `users/{username}/workflows/`

## Migration Notes

`claude-code-webui` has been removed; `web_interface` is the active codebase. File uploads now use `users/{username}/inputs/` instead of legacy `web_interface/uploads/`.
