# Quick Start Guide

Get your Claude Code Job Queue up and running in 5 minutes!

## Step 1: Initial Setup (One-time)

```bash
cd web_interface
./start.sh
```

This will:
- Create a `.env` file from the template
- Set up a Python virtual environment
- Install dependencies
- Start the web server

**IMPORTANT**: Before going further, edit `.env` and change the default password!

```bash
nano .env
# Change AUTH_PASSWORD to something secure
```

## Step 2: Access the Web Interface

Open your browser and go to:
```
http://localhost:5001
```

(Using port 5001 because macOS uses 5000 for AirPlay)

Log in with:
- Username: `admin` (or whatever you set in .env)
- Password: Your password from .env

## Step 3: Submit Your First Job

1. Click "Submit Job"
2. Enter instructions like: "Create a hello world Python script"
3. Click "Submit Job"

In manual mode (default), the job will be pending approval.

## Step 4: Process Jobs with Claude Code

Open a new terminal and run:

```bash
cd web_interface
python3 queue_watcher.py
```

You'll see:
- Queue statistics
- The next job to process
- Options to start processing

Follow the prompts to:
1. Start the job
2. Do the actual work (this is where you use Claude Code's tools)
3. Mark the job as complete with your output

## Example Processing Workflow

Let's say you got this job:

```
JOB #1
Type:        general
Instructions: Create a hello world Python script
```

Here's how you'd process it:

**1. Start the job:**
```bash
python3 queue_watcher.py --start 1
```

**2. Create the output file:**
```python
# You (Claude Code) would use the Write tool to create:
# outputs/hello.py

print("Hello, World!")
```

**3. Mark as complete:**
```bash
python3 queue_watcher.py --complete 1 --output-file "outputs/hello.py"
```

**4. User can now download it from the web interface!**

## Making It Public (Cloudflare Tunnel)

### Quick Setup

1. Install cloudflared:
   ```bash
   brew install cloudflare/cloudflare/cloudflared
   ```

2. Start a quick tunnel (no configuration needed):
   ```bash
   cloudflared tunnel --url http://localhost:5001
   ```

   This gives you a temporary public URL like:
   ```
   https://random-words-123.trycloudflare.com
   ```

3. Share this URL with your users!

### Permanent Setup (Recommended)

Follow the detailed Cloudflare Tunnel instructions in README.md for a permanent URL.

## Common Commands

### Check queue status
```bash
python3 queue_watcher.py --stats
```

### Watch for new jobs
```bash
python3 queue_watcher.py --watch
```

### View specific job
```bash
python3 queue_watcher.py --job 5
```

### Complete job with text output
```bash
python3 queue_watcher.py --complete 5 --output-text "Task completed!"
```

### Complete job with file output
```bash
python3 queue_watcher.py --complete 5 --output-file "outputs/result.pdf"
```

### Mark job as failed
```bash
python3 queue_watcher.py --fail 5 --error "Could not process file"
```

## Switching Between Manual and Auto Mode

### Manual Mode (Default - Requires Approval)
```bash
export PROCESSING_MODE=manual
python3 app.py
```

### Auto Mode (Jobs Auto-Approved)
```bash
export PROCESSING_MODE=auto
python3 app.py
```

Or edit `.env`:
```
PROCESSING_MODE=auto
```

## Tips for Using with Claude Code

1. **Check queue regularly**: Run `python3 queue_watcher.py` to see pending jobs

2. **Read uploaded files**: Jobs may include file uploads in the `uploads/` directory

3. **Save outputs properly**:
   - For files: Save to `outputs/` directory
   - For text: Use `--output-text` parameter

4. **Use descriptive filenames**: Name output files clearly so users know what they are

5. **Handle errors gracefully**: If something goes wrong, mark the job as failed with a clear error message

## Next Steps

- Read the full README.md for advanced features
- Set up Cloudflare Tunnel for permanent public access
- Customize job types in `templates/submit.html`
- Add your own processing logic

## Need Help?

Check the full documentation in README.md or review the code comments!
