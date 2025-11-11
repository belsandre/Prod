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

- **web_interface/**: Flask-based web application with:
  - User authentication (username/password)
  - Role-based access control (admin/user)
  - Job submission and management UI
  - Queue monitoring and statistics
  - Cloudflare Tunnel integration for public access

- **shared/**: Resources accessible across all users
  - Workflows: Markdown files containing prompts/instructions for LLM processing
  - Inputs/Outputs: Shared data that all users can access
  - Admins can manage shared resources

- **users/{username}/**: User-specific isolated workspaces
  - Each user has their own inputs, outputs, and workflows directories
  - File uploads are stored in `users/{username}/inputs/`
  - Job outputs are stored in `users/{username}/outputs/`
  - Users can only access their own resources (except admins)

### Job Queue System

The system uses SQLite to manage jobs with the following lifecycle:

1. **Submission**: User submits a job via web interface
   - Can include custom instructions (prompt)
   - Can upload files
   - Can select workflows
   - Can specify URLs as inputs
   - Can set priority

2. **Approval** (manual mode) or Auto-approval (auto mode):
   - Manual mode: Admin must approve jobs before processing
   - Auto mode: Jobs are automatically approved

3. **Processing**: Queue watcher picks up approved jobs
   - `python3 queue_watcher.py` - Interactive mode
   - `python3 queue_watcher.py --watch` - Continuous monitoring
   - Job is marked as "processing"

4. **Completion**: Job marked as completed with output
   - Output can be text or file
   - Users can view/download results via web interface

### Workflows

Workflows are **markdown files** containing prompts and instructions for LLM processing:
- Located in `shared/workflows/` (accessible to all) or `users/{username}/workflows/` (user-specific)
- Example: `shared/workflows/podcast_linkedin_posts.md` - Contains 6 prompts for generating LinkedIn posts from podcast transcripts
- Users select workflows when submitting jobs
- Workflows provide structured, reusable prompts for common tasks

### Threading System

Jobs can be organized into conversation threads:
- A job can have a `parent_job_id` to create threaded conversations
- Threads allow multi-turn interactions and iterative refinement
- Useful for back-and-forth collaboration on complex tasks

## Key Files

### Configuration
- **web_interface/config.py**: Core configuration
  - Authentication credentials (default: admin/changeme123)
  - Processing mode (manual/auto)
  - File upload settings
  - Path configurations

### Core Components
- **web_interface/app.py**: Flask application with routes for:
  - Authentication (`/login`, `/logout`)
  - Dashboard (`/dashboard`)
  - Job submission (`/submit`)
  - Job management (`/job/<id>`, `/job/<id>/edit`)
  - Admin functions (approve, reject, complete jobs)

- **web_interface/queue_manager.py**: Job queue operations
  - SQLite database management
  - Job CRUD operations
  - Status tracking and transitions
  - Thread management

- **web_interface/user_manager.py**: User management
  - Authentication
  - Role-based permissions
  - User folder mapping

- **web_interface/queue_watcher.py**: CLI tool for processing jobs
  - Interactive mode for viewing next job
  - Watch mode for continuous monitoring
  - Commands for starting/completing/failing jobs

### Database Schema

SQLite database (`web_interface/jobs.db`) with jobs table:
- `id`: Job ID (auto-increment)
- `username`: Job owner
- `job_type`: Category/type of job
- `prompt`: Custom instructions
- `file_paths`: JSON array of uploaded file paths
- `status`: pending/approved/processing/completed/rejected/failed
- `priority`: Higher numbers = higher priority
- `created_at`, `approved_at`, `started_at`, `completed_at`: Timestamps
- `output_type`: text/file
- `output_path`, `output_text`: Job results
- `metadata`: JSON with additional info (URLs, workflows, etc.)
- `thread_id`, `parent_job_id`: For conversation threading

## Development Workflow

### Adding New Features

When adding features to the web interface:
1. Update database schema in `queue_manager.py` if needed
2. Add routes in `app.py`
3. Create/update templates in `templates/`
4. Update configuration in `config.py` if needed
5. Document in appropriate README/guide files

### Working with User Data

- **Always respect user isolation**: Users should only access their own data
- **Admin override**: Admin role can access all users' data for management
- **File paths**: Use `Config.get_user_input_folder()` and `Config.get_user_output_folder()`
- **Workflows**: Use `get_workflow_groups()` to properly scope workflow access

### Processing Jobs

Typical workflow for processing jobs with Claude Code:
1. Run `python3 queue_watcher.py` to see next job
2. Read uploaded files from `users/{username}/inputs/`
3. Process according to instructions and selected workflows
4. Save outputs to `users/{username}/outputs/`
5. Mark job as completed with output reference

## Security Considerations

- Change default credentials before deployment (see web_interface/README.md)
- Use strong SECRET_KEY for Flask sessions
- File upload validation (allowed extensions, size limits)
- Path traversal protection (secure_filename)
- Role-based access control throughout
- HTTPS via Cloudflare Tunnel (recommended for public access)

## Documentation

Primary documentation located in `web_interface/`:
- **README.md**: Complete setup and usage guide
- **QUICKSTART.md**: Quick start guide
- **JOB_PROCESSING_GUIDE.md**: Guide for processing jobs
- **MULTI_USER_THREADS_GUIDE.md**: Guide for multi-user and threading features

## Common Tasks

### Adding a New User
```bash
cd web_interface
python3 manage_users.py
```

### Running the Web Interface
```bash
cd web_interface
python3 app.py  # Runs on http://localhost:5001
```

### Processing Jobs
```bash
cd web_interface
python3 queue_watcher.py          # Interactive mode
python3 queue_watcher.py --watch  # Continuous monitoring
python3 queue_watcher.py --stats  # View queue statistics
```

### Creating Workflows
1. Create markdown file in `shared/workflows/` or `users/{username}/workflows/`
2. Include prompts, instructions, and examples
3. Reference from web interface when submitting jobs

## Migration Notes

The project previously included `claude-code-webui` which has been removed. The current `web_interface` is the active codebase.

File uploads now go to user-specific directories (`users/{username}/inputs/`) rather than the legacy `web_interface/uploads/` location.
