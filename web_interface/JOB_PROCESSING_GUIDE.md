# Job Processing from Claude Code Conversation

## New Workflow - No More queue_watcher.py!

You can now process jobs directly in this Claude Code conversation.

## Quick Start

### Step 1: Tell me to check for jobs

Just say:
```
"process next job"
or
"check for jobs"
or
"get next job"
```

I'll automatically:
- Check the queue
- Show you the next job details
- Display thread context if it's a conversation
- Show all files and prompts

### Step 2: Tell me to start

When you see the job and want me to process it, say:
```
"go"
or
"start"
or
"yes, process it"
```

I'll mark it as "processing" in the database.

### Step 3: I do the work

I'll use my tools (Read, Write, Bash, etc.) to complete the task.

### Step 4: I ask for confirmation

When done, I'll show you what I created and ask:
```
"Save this as the output?"
```

### Step 5: You confirm

Say:
```
"yes"
or
"save it"
or
"looks good"
```

I'll automatically save the output and mark the job complete!

## Full Example

**You:** "process next job"

**Me:**
```
======================================================================
NEXT JOB IN QUEUE
======================================================================
Job ID:      #7
User:        tam
Type:        data_analysis
Priority:    0
Created:     2025-11-06T14:30:00
Status:      approved
======================================================================

PROMPT:
----------------------------------------------------------------------
Analyze the sales data and create a summary report
----------------------------------------------------------------------

FILES:
  📄 /Users/changxu/Agents/Prod/users/tam/inputs/sales_data.csv
     Size: 45.2 KB

======================================================================
Ready to process this job!
======================================================================

Should I start processing Job #7?
```

**You:** "yes"

**Me:**
```
✓ Job #7 marked as PROCESSING

[I read the CSV file using Read tool]
[I analyze the data]
[I create a summary]

I've completed the analysis. Here's the summary:

"Sales Analysis Summary:
- Total revenue: $125,000
- Top product: Widget A (35% of sales)
- Growth rate: 15% vs last quarter
- Key insight: Mobile sales increased 40%"

Should I save this as text output for Job #7?
```

**You:** "save it"

**Me:**
```
✅ Job #7 marked as COMPLETED
   Output type: text

   User can now view the output in the web interface.
```

Done! The user (tam) can now see the output on the web interface.

## Commands I Understand

**To get a job:**
- "process next job"
- "check for jobs"
- "get next job"
- "what's in the queue"
- "any jobs?"

**To start processing:**
- "go"
- "start"
- "yes"
- "process it"
- "do it"

**To save output:**
- "yes"
- "save it"
- "looks good"
- "save this"

**To mark as failed:**
- "this failed because..."
- "mark it as failed: [reason]"
- "can't complete this: [reason]"

## Advanced: Direct Python Usage

You can also ask me to run Python code directly:

**You:** "Run this Python code to check for jobs:"

```python
from job_processor import get_next_job, start_processing, save_output

# Get next job
job = get_next_job()

# Process it
if job:
    start_processing(job['id'])
    # ... do work ...
    save_output(job['id'], 'text', 'Result here')
```

## For Conversation Threads

When processing a job that's part of a conversation thread, I automatically show:

```
======================================================================
CONVERSATION THREAD CONTEXT
======================================================================
This job is part of a conversation. Here's the history:

💬 [Message 1/3] Job #5
   User: tam
   Prompt: Analyze sales_data.csv
   ✅ Response: Revenue up 15%, top product is Widget A

💬 [Message 2/3] Job #6
   User: tam
   Prompt: Create a chart of top 5 products
   ✅ Response: chart.png (file)

📍 [Message 3/3] Job #7 ⬅️ CURRENT JOB
   User: tam
   Prompt: Make the chart blue instead

======================================================================
💡 You have full context of the conversation above

📦 ALL FILES AVAILABLE IN THIS THREAD:
  • /Users/changxu/Agents/Prod/users/tam/inputs/sales_data.csv
  • /Users/changxu/Agents/Prod/users/tam/outputs/chart.png
======================================================================
```

I can access ALL files from the entire conversation thread!

## Tips

1. **Natural language works** - Just talk to me naturally about processing jobs
2. **I show everything** - You'll see the full job details, thread context, and all files
3. **Confirmation at key steps** - I ask before starting and before saving
4. **Automatic file organization** - Outputs are saved to the correct user folder
5. **Thread-aware** - I automatically understand conversation context

## Comparison: Old vs New

### Old Way (queue_watcher.py)
```bash
# Terminal 1
python3 queue_watcher.py
# See job details, manually note them down

# Terminal 2 (Claude Code conversation)
# Do the work manually

# Back to Terminal 1
python3 queue_watcher.py --start 7
python3 queue_watcher.py --complete 7 --output-text "Result"
```

### New Way (This Conversation)
```
You: "process next job"
Me: [Shows job] Should I start?
You: "yes"
Me: [Does the work] Save this?
You: "yes"
Me: ✅ Done!
```

**Much simpler!** 🎉

## Troubleshooting

**"No jobs in queue"**
- Check the web interface - are there pending jobs?
- In manual mode, admin needs to approve jobs first
- Make sure someone has submitted jobs

**File not found errors**
- Check the file paths shown in the job details
- Files should be in users/{username}/inputs/
- For threads, check "ALL FILES AVAILABLE IN THIS THREAD"

**Can't save output**
- Make sure the job is marked as "processing" first
- For file outputs, the file must exist before saving
- Use full absolute paths for files
