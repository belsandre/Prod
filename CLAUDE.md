# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **workflow and user data repository** for Claude Code processing. It contains organized workflows (prompt templates and instructions), user-specific input/output directories, and shared resources accessible across all users. This repository is designed to work with a separate web interface that manages job submission and processing.

## Repository Structure

```
Prod/
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

**Note**: The web interface (Flask application, job queue management, authentication, etc.) has been moved to a separate repository.

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

### Workflows

Markdown files containing prompts/instructions for LLM processing, located in `shared/workflows/` or `users/{username}/workflows/`. These workflows define reusable templates for common tasks and processing patterns.

#### Available User Workflows

- **users/ashish/workflows/podcast-marketer.md**: Transforms podcast transcripts into LinkedIn posts and viral social media clips
- **users/tam/workflows/conflict-resolver.md**: Systematically resolve situations where multiple portfolio companies have identical or similar names, investigating dataroom sources and applying decision frameworks
- **users/tam/workflows/deal-prioritization.md**: Analyzes fund datarooms to create tiered portfolio company research prioritization
- **users/tam/workflows/validator.md**: Auto-detects requirements from workflows/skills and validates their outputs against quality standards (source documentation, file structure, completeness, attribution)
- **users/tam/workflows/vc-research.md**: Deep research on VC portfolio companies and GPs with relationship tracking and portfolio quality assessment (resumable)

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

## Development Workflow

**Creating Workflows**: Add markdown files to `shared/workflows/` (for all users) or `users/{username}/workflows/` (user-specific). Workflows should contain clear instructions, prompts, and templates for LLM processing.

**Managing User Data**: Respect user isolation - users should only access their own data in `users/{username}/`. Shared resources in `shared/` are accessible across all users.

**Processing Jobs**: When processing jobs via the web interface, read input files from `users/{username}/inputs/`, process according to workflow instructions, and save results to `users/{username}/outputs/`.

## Security Considerations

- **Data Isolation**: Maintain strict separation between user directories. Processing code should only access `users/{username}/` data when working on that user's jobs.
- **Path Traversal**: Validate all file paths to prevent access outside designated user/shared directories.
- **Sensitive Data**: Be cautious with files in user directories that may contain credentials, API keys, or other sensitive information.

## Common Tasks

**Create Global Workflow**: Add markdown file to `shared/workflows/` - accessible to all users
**Create User Workflow**: Add markdown file to `users/{username}/workflows/` - specific to that user
**Add User Directory**: Create new directory structure: `users/{username}/` with subdirectories for `inputs/`, `outputs/`, and `workflows/`
**Organize User Files**: Place input files in `users/{username}/inputs/` and outputs will be generated in `users/{username}/outputs/`

## Migration Notes

- **Web Interface Separated**: The Flask web application (`web_interface/`) has been moved to a separate repository. This repository now focuses solely on workflow definitions and user data storage.
- **Data Structure**: All user data follows the structure `users/{username}/inputs/` and `users/{username}/outputs/`. Legacy paths like `web_interface/uploads/` are no longer used.
- **Workflow Management**: Workflows are organized in `shared/workflows/` (global) and `users/{username}/workflows/` (user-specific).
