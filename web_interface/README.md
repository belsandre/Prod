# Claude Code Job Queue System

A web-based job queue system that allows users to submit jobs over the internet, which are then processed by your local Claude Code instance.

## Features

- **Web interface** with basic authentication
- **Job submission** via text prompts and/or file uploads
- **Two processing modes**:
  - **Manual mode**: Jobs require approval before processing
  - **Auto mode**: Jobs are automatically approved and queued
- **Queue management** with priority support
- **Job tracking** with detailed status and history
- **Output handling** for both text and file outputs
- **Cloudflare Tunnel** integration for secure public access

## Architecture

```
Internet Users
      ↓
Cloudflare Tunnel (secure, free public URL)
      ↓
Flask Web Server (localhost:5001)
      ↓
SQLite Job Queue
      ↓
Queue Watcher Script → Claude Code processes jobs
      ↓
Output Storage
```

## Quick Start

### 1. Install Dependencies

```bash
cd web_interface
pip3 install -r requirements.txt
```

### 2. Configure Authentication

**IMPORTANT**: Change the default credentials before deploying!

Create a `.env` file or set environment variables:

```bash
export AUTH_USERNAME="your_username"
export AUTH_PASSWORD="your_secure_password"
export SECRET_KEY="your_random_secret_key_here"
export PROCESSING_MODE="manual"  # or "auto"
```

Or create a `.env` file:

```bash
# .env
AUTH_USERNAME=admin
AUTH_PASSWORD=your_secure_password_here
SECRET_KEY=change_this_to_random_string
PROCESSING_MODE=manual
MAX_CONCURRENT_JOBS=1
```

### 3. Start the Web Server

```bash
python3 app.py
```

The server will start on `http://localhost:5001` (port 5001 is used because macOS reserves 5000 for AirPlay)

### 4. Set Up Cloudflare Tunnel (for public access)

#### Install Cloudflare Tunnel (cloudflared)

**macOS:**
```bash
brew install cloudflare/cloudflare/cloudflared
```

**Linux:**
```bash
wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb
```

**Windows:**
Download from: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/

#### Authenticate Cloudflare

```bash
cloudflared tunnel login
```

This will open a browser window. Log in to your Cloudflare account (free account works fine).

#### Create a Tunnel

```bash
cloudflared tunnel create claude-code-queue
```

Note the Tunnel ID that is displayed.

#### Create Tunnel Configuration

Create a file `~/.cloudflared/config.yml`:

```yaml
tunnel: <YOUR_TUNNEL_ID>
credentials-file: /Users/<your_username>/.cloudflared/<YOUR_TUNNEL_ID>.json

ingress:
  - hostname: your-subdomain.example.com
    service: http://localhost:5001
  - service: http_status:404
```

Replace:
- `<YOUR_TUNNEL_ID>` with your actual tunnel ID
- `<your_username>` with your system username
- `your-subdomain.example.com` with your desired hostname

#### Route DNS to Your Tunnel

```bash
cloudflared tunnel route dns claude-code-queue your-subdomain.example.com
```

#### Run the Tunnel

```bash
cloudflared tunnel run claude-code-queue
```

Or run as a service (stays running in background):

```bash
cloudflared service install
cloudflared service start
```

Now your web interface will be accessible at `https://your-subdomain.example.com`!

## Processing Jobs with Claude Code

### Method 1: Interactive Mode (Recommended for Manual Processing)

Run the queue watcher in interactive mode:

```bash
python3 queue_watcher.py
```

This will:
1. Show queue statistics
2. Display the next approved job
3. Let you choose how to proceed

### Method 2: Watch Mode (Automatic Checking)

Continuously monitor for new jobs:

```bash
python3 queue_watcher.py --watch
```

This will check for new approved jobs every 10 seconds and display them when found.

### Method 3: Command Line (For Scripting)

Check queue stats:
```bash
python3 queue_watcher.py --stats
```

View specific job:
```bash
python3 queue_watcher.py --job 5
```

Start processing a job:
```bash
python3 queue_watcher.py --start 5
```

Mark job as completed with text output:
```bash
python3 queue_watcher.py --complete 5 --output-text "Job completed successfully!"
```

Mark job as completed with file output:
```bash
python3 queue_watcher.py --complete 5 --output-file "/path/to/output.txt"
```

Mark job as failed:
```bash
python3 queue_watcher.py --fail 5 --error "Something went wrong"
```

## Processing Workflow

### Manual Mode (Default)

1. User submits a job via web interface
2. Job enters "pending" status
3. You (or admin) review the job in the web interface
4. Approve or reject the job
5. If approved, job moves to "approved" queue
6. Run `python3 queue_watcher.py` to see next job
7. Process the job with Claude Code
8. Mark job as complete with output

### Auto Mode

1. User submits a job via web interface
2. Job is automatically approved and enters queue
3. Run `python3 queue_watcher.py` to see next job
4. Process the job with Claude Code
5. Mark job as complete with output

## Typical Claude Code Processing Workflow

Here's how you would typically process jobs with Claude Code:

1. **Check for jobs**:
   ```bash
   python3 queue_watcher.py
   ```

2. **When a job appears**, you'll see details like:
   ```
   JOB #5
   Type:        file_processing
   Instructions:
   Please analyze this CSV file and create a summary report

   UPLOADED FILES:
     - data.csv (15,234 bytes)
       Path: /path/to/uploads/20250106_143022_data.csv
   ```

3. **Start the job**:
   ```bash
   python3 queue_watcher.py --start 5
   ```

4. **Process with Claude Code**:
   - Read the uploaded files
   - Follow the instructions in the prompt
   - Create output files or generate text response

5. **Mark as complete**:
   ```bash
   # If you generated a file
   python3 queue_watcher.py --complete 5 --output-file "outputs/report.pdf"

   # If you have text output
   python3 queue_watcher.py --complete 5 --output-text "Analysis complete. Found 3 anomalies..."
   ```

## File Locations

- **Uploads**: `web_interface/uploads/` - Files uploaded by users
- **Outputs**: `web_interface/outputs/` - Files you create as job outputs
- **Database**: `web_interface/jobs.db` - SQLite database with all jobs
- **Logs**: Check console output

## Configuration Options

All configuration is in `config.py` or via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `AUTH_USERNAME` | `admin` | Login username |
| `AUTH_PASSWORD` | `changeme123` | Login password |
| `SECRET_KEY` | `dev-secret-key...` | Flask session secret |
| `PROCESSING_MODE` | `manual` | `manual` or `auto` |
| `MAX_CONCURRENT_JOBS` | `1` | Max jobs processing at once |
| `MAX_CONTENT_LENGTH` | `50MB` | Max file upload size |

## Security Considerations

1. **Change default credentials** before deployment
2. **Use strong passwords** for production
3. **Keep SECRET_KEY secret** - generate a random one
4. **Enable HTTPS** via Cloudflare Tunnel (automatic)
5. **Review jobs carefully** in manual mode before approving
6. **Validate file uploads** - check for malicious files
7. **Don't expose SQLite database** to the internet

## Troubleshooting

### Can't connect to web interface

1. Check if server is running: `ps aux | grep app.py`
2. Check if port 5001 is in use: `lsof -i :5001`
3. Try accessing: `http://localhost:5001`
4. If port 5001 is blocked, set PORT env var: `export PORT=5002 && python3 app.py`

### Cloudflare Tunnel not working

1. Check tunnel status: `cloudflared tunnel info claude-code-queue`
2. Check tunnel logs: `cloudflared tunnel run claude-code-queue` (see output)
3. Verify DNS: `nslookup your-subdomain.example.com`

### Jobs not appearing

1. Check queue stats: `python3 queue_watcher.py --stats`
2. Check if job was approved (manual mode)
3. Check database: `sqlite3 jobs.db "SELECT * FROM jobs;"`

### Database locked errors

1. Only one process should write at a time
2. Close any SQLite browser tools
3. Restart the web server

## Advanced Usage

### Running Multiple Workers

You can run multiple instances of the queue watcher to process jobs in parallel:

```bash
# Terminal 1
python3 queue_watcher.py --watch

# Terminal 2
python3 queue_watcher.py --watch
```

### Custom Job Types

Edit `templates/submit.html` to add your own job types to the dropdown.

### Backing Up the Database

```bash
# Backup
sqlite3 jobs.db ".backup jobs_backup.db"

# Restore
sqlite3 jobs.db ".restore jobs_backup.db"
```

### API Access

The system includes basic API endpoints:

- `GET /api/stats` - Queue statistics (JSON)
- `GET /api/next_job` - Next approved job (JSON)

Both require authentication (logged in session).

## Running as a Service

### macOS (launchd)

Create `~/Library/LaunchAgents/com.claudecode.queue.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.claudecode.queue</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/changxu/Agents/Prod/web_interface/app.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

Load it:
```bash
launchctl load ~/Library/LaunchAgents/com.claudecode.queue.plist
```

### Linux (systemd)

Create `/etc/systemd/system/claudecode-queue.service`:

```ini
[Unit]
Description=Claude Code Job Queue
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/web_interface
Environment="PATH=/usr/bin:/usr/local/bin"
ExecStart=/usr/bin/python3 app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable claudecode-queue
sudo systemctl start claudecode-queue
```

## Support

For issues or questions:
1. Check this README
2. Review the code comments
3. Check Flask and Cloudflare Tunnel documentation

## License

This is a custom tool created for personal use. Modify as needed for your use case.
