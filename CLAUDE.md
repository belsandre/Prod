# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Structure

This repository appears to be a workspace for agent-based workflows organized by user and shared resources.

```
Prod/
├── shared/
│   ├── inputs/      # Shared input files/data
│   ├── outputs/     # Shared output files/data
│   └── workflows/   # Shared workflow definitions
└── users/
    └── tam/
        ├── inputs/      # User-specific input files/data
        ├── outputs/     # User-specific output files/data
        └── workflows/   # User-specific workflow definitions
```

## Architecture

The codebase follows a multi-tenant structure:
- **shared/**: Contains resources accessible across all users
- **users/{username}/**: Contains user-specific resources isolated by user
- Each section has three subdirectories:
  - **inputs/**: Source data or configuration files
  - **outputs/**: Generated results or artifacts
  - **workflows/**: Workflow definitions or orchestration logic

This structure suggests a system where workflows process inputs to generate outputs, with the ability to share workflows and data across users or keep them private.

## Development Notes

The repository currently contains only directory structure. When adding code:
- Maintain the separation between shared and users namespaces
- Keep user-specific data isolated within their respective directories
- Place reusable workflows and resources in shared/ when appropriate
