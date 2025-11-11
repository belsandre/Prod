# Multi-User & Conversation Threads Guide

## Overview

The Claude Code Job Queue now supports:
1. **Multiple users** with role-based access (admin/user)
2. **Conversation threads** - users can reply to completed jobs for back-and-forth interactions
3. **User-specific workspaces** - each user has their own inputs/outputs/workflows folders
4. **Full conversation context** - Claude Code sees the entire thread history when processing replies

## New Features

### 1. User Management

**Two user roles:**
- **Admin**: Can approve/reject jobs, see all jobs, manage system
- **User**: Can only submit and view their own jobs

**User accounts:**
- `admin` / `changeme123` - Admin account (change password!)
- `tam` / `tam123` - First user account (maps to users/tam folder)

### 2. Conversation Threads

Users can now have back-and-forth conversations with Claude Code:

```
User submits Job #1: "Analyze this data file"
  ↓
Claude processes and completes with analysis
  ↓
User clicks "Reply to this Job"
  ↓
User submits Job #2: "Now create a chart of the top 5 findings"
  ↓
Claude processes Job #2 WITH FULL CONTEXT from Job #1
  ↓
User can continue the conversation...
```

**How it works:**
- When you reply to a job, it creates a conversation thread
- All jobs in the thread share the same `thread_id`
- When processing a reply, Claude Code sees:
  - All previous prompts in the thread
  - All previous outputs/responses
  - All files uploaded in any part of the thread
  - Full chronological conversation history

### 3. User Workspaces

Each user has their own folder structure in the Prod/ directory:

```
Prod/
├── shared/           # Shared resources (admin access)
│   ├── inputs/
│   ├── outputs/
│   └── workflows/
└── users/
    └── tam/          # Tam's workspace
        ├── inputs/   # Tam's uploaded files go here
        ├── outputs/  # Tam's output files go here
        └── workflows/
```

**Automatic file organization:**
- When a user uploads files, they go to `users/{username}/inputs/`
- When creating outputs, save to `users/{username}/outputs/`
- Admin can access all folders
- Users can only access their own folder

## Setup Instructions

### Step 1: Install Dependencies

```bash
cd web_interface
pip3 install -r requirements.txt
```

### Step 2: Create Tam User

```bash
python3 manage_users.py add tam tam123 --folder users/tam
```

The folder structure is already created at `/Users/changxu/Agents/Prod/users/tam/`

### Step 3: Start the Server

```bash
./start.sh
```

Or manually:
```bash
python3 app.py
```

Access at `http://localhost:5001`

### Step 4: Test Multi-User Features

**As Admin (admin/changeme123):**
- Can see all jobs
- Can approve/reject pending jobs
- Has "Pending Queue" and "Config" menu items
- Can view any user's jobs

**As Tam (tam/tam123):**
- Can only see their own jobs
- Can submit jobs (they go to pending if in manual mode)
- Files upload to `users/tam/inputs/`
- No "Pending Queue" or "Config" menu

## Using Conversation Threads

### Scenario: Data Analysis Conversation

**Step 1: Submit initial job**
```
User (tam): "Analyze this sales_data.csv file and summarize key trends"
[Uploads: sales_data.csv]
```

**Step 2: Admin approves, Claude processes**
```
Claude Code:
- Reads users/tam/inputs/sales_data.csv
- Analyzes the data
- Creates summary
- Marks job complete with text output
```

**Step 3: User sees output and wants to follow up**
- User views Job #1 (completed)
- Clicks "Reply to this Job" button
- Gets taken to submit form with Job #1 as parent

**Step 4: User submits follow-up**
```
User (tam): "Create a bar chart showing the top 5 products by revenue"
[No new files needed - uses sales_data.csv from thread]
```

**Step 5: Claude processes with full context**
When you run `python3 queue_watcher.py`, you'll see:

```
JOB #2
Type:        general
User:        tam
Thread:      Part of conversation (Job #1)
             2 message(s) in thread

INSTRUCTIONS:
Create a bar chart showing the top 5 products by revenue

CONVERSATION THREAD CONTEXT:
============================================================
Claude Code: You are processing a job in a conversation thread.
Below is the full conversation history to give you context.

[Message 1/2] Job #1
User: tam
Prompt:
  Analyze this sales_data.csv file and summarize key trends
Files:
  - sales_data.csv
Claude's Response:
  Based on the analysis of sales_data.csv, here are the key trends...

[Message 2/2] Job #2 >>> CURRENT JOB <<<
User: tam
Prompt:
  Create a bar chart showing the top 5 products by revenue
============================================================
End of conversation history. Process the current job with this context.
```

**Step 6: Claude creates chart with context**
```
Claude Code:
- Has full context from Job #1 (knows about the data analysis)
- Can access sales_data.csv from thread
- Creates chart
- Saves to users/tam/outputs/revenue_chart.png
- Marks job complete
```

**Step 7: Continue the conversation**
User can keep replying for iterative refinements!

## User Management Commands

### List all users
```bash
python3 manage_users.py list
```

### Add a new user
```bash
python3 manage_users.py add username password
python3 manage_users.py add username password --admin  # Create as admin
```

### Change password
```bash
python3 manage_users.py password username new_password
```

### Delete user
```bash
python3 manage_users.py delete username
```

## Processing Jobs with Threads

When you run `python3 queue_watcher.py`, jobs that are part of a thread will show:

1. **Thread indicator** in the job header
2. **Full conversation history** with all previous messages
3. **All files from the thread** (not just current job)
4. **Previous outputs** so you have context

**Example workflow:**

```bash
# Check for jobs
python3 queue_watcher.py

# You see Job #2 (a reply to Job #1)
# The output shows the ENTIRE conversation thread

# Start processing
python3 queue_watcher.py --start 2

# Process the job with full context
# You can read all files from any job in the thread

# Complete with output
python3 queue_watcher.py --complete 2 --output-file "users/tam/outputs/chart.png"
```

## Database Changes

The jobs table now has:
- `thread_id` - Links all jobs in a conversation
- `parent_job_id` - Points to the job this is replying to

Migration was automatically run to update the existing database.

## Security & Permissions

**User isolation:**
- Users can only see their own jobs
- Users can only reply to their own completed jobs
- File paths are scoped to user folders

**Admin privileges:**
- See all jobs from all users
- Approve/reject any pending job
- Access pending queue
- View system configuration

**Thread security:**
- Users can only create threads on jobs they own
- Thread members must be the same user
- Admin can view any thread

## File Organization Tips

### For Users (like Tam)

When submitting jobs:
- Files are automatically saved to `users/tam/inputs/`
- Reference them in prompts as needed
- Claude Code has access to your inputs folder

When receiving outputs:
- Files are saved to `users/tam/outputs/`
- Download via web interface
- Organized by timestamp

### For Claude Code (when processing)

When processing Tam's job:
```python
# User's uploaded file is at:
/Users/changxu/Agents/Prod/users/tam/inputs/20251106_143022_data.csv

# Save outputs to:
/Users/changxu/Agents/Prod/users/tam/outputs/result.pdf
```

When processing a threaded job:
- Check all files in the thread using queue_watcher output
- You have access to ALL files uploaded in any message of the thread
- This enables iterative work on the same dataset

## Troubleshooting

### "Access denied" when viewing a job
- You might be trying to view another user's job
- Only admin can view all jobs

### Can't see "Reply" button
- Button only appears on completed jobs
- Must be your own job (or admin viewing any job)

### Files not found in thread
- Check the conversation thread context in queue_watcher
- Files are listed with full paths
- All files from all jobs in thread are accessible

### Migration issues
If you had jobs before the update:
```bash
python3 migrate_database.py
```

This adds thread_id and parent_job_id to existing jobs.

## Best Practices

### For Users

1. **Start conversations clearly** - Give good context in the first message
2. **Use threads for related work** - Don't start new jobs for follow-ups
3. **Reference previous outputs** - "Based on the analysis from your last response..."
4. **Upload files once** - Files from earlier in the thread are still accessible

### For Processing (Claude Code)

1. **Read the thread context** - It's shown automatically in queue_watcher
2. **Understand the conversation flow** - See what was asked and answered before
3. **Access thread files** - All files from the thread are available
4. **Save outputs to user folder** - Use the correct user's output directory

## Example Conversations

### Data Analysis Thread

```
Job #1: "Analyze customer_feedback.csv for sentiment trends"
→ Claude analyzes and provides summary

Job #2 (Reply): "Focus on negative feedback - what are the top complaints?"
→ Claude has context from Job #1, knows the data

Job #3 (Reply): "Create an action plan to address the top 3 complaints"
→ Claude has full thread context, can create targeted plan
```

### Code Review Thread

```
Job #1: "Review this Python script for bugs" [uploads: script.py]
→ Claude reviews and finds 3 issues

Job #2 (Reply): "Fix the bugs you found and explain the changes"
→ Claude knows about the bugs from Job #1, fixes them

Job #3 (Reply): "Add unit tests for the fixed functions"
→ Claude has context of original code + fixes, writes tests
```

## Architecture Summary

```
Web Interface (Port 5001)
    ↓
User Authentication (users.json)
    ↓
Role-Based Access Control
    ↓
Job Submission → Queue (SQLite)
    ↓
Thread Management (thread_id, parent_job_id)
    ↓
User Workspace (users/{username}/)
    ↓
Queue Watcher (shows thread context)
    ↓
Claude Code Processes with Full Context
    ↓
Output to User Workspace
```

## Next Steps

1. Change default passwords
2. Add more users as needed
3. Test conversation threads
4. Set up Cloudflare Tunnel for remote access
5. Customize job types in submit.html

## Support

- See README.md for full documentation
- See QUICKSTART.md for getting started
- Use `python3 manage_users.py --help` for user management
- Use `python3 queue_watcher.py --help` for queue commands
