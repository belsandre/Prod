# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Structure

This repository appears to be a workspace for agent-based workflows organized by user and shared resources.

```
Prod/
├── Shared/
│   ├── Inputs/      # Shared input files/data
│   ├── Outputs/     # Shared output files/data
│   └── Workflows/   # Shared workflow definitions
└── Users/
    └── Tam/
        ├── Inputs/      # User-specific input files/data
        ├── Outputs/     # User-specific output files/data
        └── Workflows/   # User-specific workflow definitions
```

## Architecture

The codebase follows a multi-tenant structure:
- **Shared/**: Contains resources accessible across all users
- **Users/{username}/**: Contains user-specific resources isolated by user
- Each section has three subdirectories:
  - **Inputs/**: Source data or configuration files
  - **Outputs/**: Generated results or artifacts
  - **Workflows/**: Workflow definitions or orchestration logic

This structure suggests a system where workflows process inputs to generate outputs, with the ability to share workflows and data across users or keep them private.

## Development Notes

The repository currently contains only directory structure. When adding code:
- Maintain the separation between Shared and Users namespaces
- Keep user-specific data isolated within their respective directories
- Place reusable workflows and resources in Shared/ when appropriate
