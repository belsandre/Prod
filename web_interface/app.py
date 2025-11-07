from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, jsonify
from functools import wraps
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from config import Config
from queue_manager import QueueManager
from user_manager import UserManager

app = Flask(__name__)
app.config.from_object(Config)

# Initialize managers
queue_manager = QueueManager()
user_manager = UserManager()

# Ensure required directories exist
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
os.makedirs(Config.OUTPUT_FOLDER, exist_ok=True)
os.makedirs(Config.SHARED_FOLDER, exist_ok=True)
os.makedirs(Config.USERS_FOLDER, exist_ok=True)


def login_required(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login', next=request.url))
        if session.get('role') != 'admin':
            flash('Access denied: Admin privileges required', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    """Home page - redirect to dashboard if logged in, else login"""
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = user_manager.authenticate(username, password)
        if user:
            session['logged_in'] = True
            session['username'] = user['username']
            session['role'] = user['role']
            session['user_folder'] = user['folder']
            session.permanent = True

            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Invalid credentials', 'error')

    return render_template('login.html')


@app.route('/logout')
def logout():
    """Logout"""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard showing queue status"""
    username = session.get('username')
    is_admin = session.get('role') == 'admin'

    # Get stats (all for admin, user-specific for users)
    stats = queue_manager.get_stats()

    # Get recent jobs (filtered by user unless admin)
    if is_admin:
        recent_jobs = queue_manager.list_jobs(limit=20)
    else:
        recent_jobs = queue_manager.list_jobs(username=username, limit=20)

    return render_template(
        'dashboard.html',
        stats=stats,
        recent_jobs=recent_jobs,
        processing_mode=Config.PROCESSING_MODE,
        username=username,
        is_admin=is_admin
    )


@app.route('/submit', methods=['GET', 'POST'])
@login_required
def submit_job():
    """Submit a new job"""
    parent_job_id = request.args.get('parent_id', type=int)
    parent_job = None

    if parent_job_id:
        parent_job = queue_manager.get_job(parent_job_id)
        # Verify user owns parent job or is admin
        if parent_job and parent_job['username'] != session['username'] and session.get('role') != 'admin':
            flash('You cannot reply to jobs you do not own', 'error')
            return redirect(url_for('dashboard'))

    if request.method == 'POST':
        job_type = request.form.get('job_type', 'general')
        prompt = request.form.get('prompt', '').strip()
        priority = int(request.form.get('priority', 0))
        parent_id = request.form.get('parent_job_id', type=int)

        # Get user's input folder
        user_folder = session.get('user_folder')
        upload_folder = Config.get_user_input_folder(user_folder)
        os.makedirs(upload_folder, exist_ok=True)

        file_paths = []
        files = request.files.getlist('files')

        # Handle file uploads
        for file in files:
            if file and file.filename:
                if Config.allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    # Add timestamp to avoid conflicts
                    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
                    filename = f"{timestamp}_{filename}"
                    filepath = os.path.join(upload_folder, filename)
                    file.save(filepath)
                    file_paths.append(filepath)
                else:
                    flash(f'File type not allowed: {file.filename}', 'error')
                    return redirect(url_for('submit_job'))

        # Validate submission
        if not prompt and not file_paths:
            flash('Please provide either a prompt or upload files', 'error')
            return redirect(url_for('submit_job', parent_id=parent_id) if parent_id else url_for('submit_job'))

        # Create job
        job_id = queue_manager.create_job(
            username=session['username'],
            job_type=job_type,
            prompt=prompt if prompt else None,
            file_paths=file_paths if file_paths else None,
            priority=priority,
            metadata={
                'submitted_from': request.remote_addr,
                'user_agent': request.headers.get('User-Agent')
            },
            parent_job_id=parent_id
        )

        if parent_id:
            flash(f'Reply #{job_id} submitted to conversation thread', 'success')
        elif Config.PROCESSING_MODE == 'auto':
            flash(f'Job #{job_id} submitted and queued for automatic processing', 'success')
        else:
            flash(f'Job #{job_id} submitted and pending approval', 'success')

        return redirect(url_for('view_job', job_id=job_id))

    return render_template('submit.html', parent_job=parent_job)


@app.route('/jobs')
@login_required
def list_jobs():
    """List all jobs with filtering"""
    status = request.args.get('status')
    page = int(request.args.get('page', 1))
    per_page = 50
    offset = (page - 1) * per_page

    username = session.get('username')
    is_admin = session.get('role') == 'admin'

    # Filter by user unless admin
    jobs = queue_manager.list_jobs(
        status=status,
        username=None if is_admin else username,
        limit=per_page,
        offset=offset
    )

    return render_template(
        'jobs.html',
        jobs=jobs,
        current_status=status,
        page=page,
        is_admin=is_admin
    )


@app.route('/job/<int:job_id>')
@login_required
def view_job(job_id):
    """View details of a specific job"""
    job = queue_manager.get_job(job_id)

    if not job:
        flash(f'Job #{job_id} not found', 'error')
        return redirect(url_for('dashboard'))

    # Check permissions (users can only view their own jobs, admin can view all)
    if job['username'] != session.get('username') and session.get('role') != 'admin':
        flash('Access denied: You can only view your own jobs', 'error')
        return redirect(url_for('dashboard'))

    # Get thread context if job is part of a thread
    thread = queue_manager.get_thread_for_job(job_id)
    can_reply = queue_manager.can_reply_to_job(job_id)

    return render_template(
        'job_detail.html',
        job=job,
        thread=thread,
        can_reply=can_reply,
        is_admin=session.get('role') == 'admin'
    )


@app.route('/job/<int:job_id>/approve', methods=['POST'])
@admin_required
def approve_job(job_id):
    """Approve a pending job (admin only)"""
    if queue_manager.approve_job(job_id):
        flash(f'Job #{job_id} approved', 'success')
    else:
        flash(f'Could not approve job #{job_id}', 'error')

    return redirect(url_for('view_job', job_id=job_id))


@app.route('/job/<int:job_id>/reject', methods=['POST'])
@admin_required
def reject_job(job_id):
    """Reject a pending job (admin only)"""
    reason = request.form.get('reason', 'Rejected by admin')

    if queue_manager.reject_job(job_id, reason):
        flash(f'Job #{job_id} rejected', 'info')
    else:
        flash(f'Could not reject job #{job_id}', 'error')

    return redirect(url_for('view_job', job_id=job_id))


@app.route('/job/<int:job_id>/output')
@login_required
def view_output(job_id):
    """View or download job output"""
    job = queue_manager.get_job(job_id)

    if not job:
        flash(f'Job #{job_id} not found', 'error')
        return redirect(url_for('dashboard'))

    if job['status'] != 'completed':
        flash(f'Job #{job_id} has not completed yet', 'info')
        return redirect(url_for('view_job', job_id=job_id))

    if job['output_type'] == 'file' and job['output_path']:
        if os.path.exists(job['output_path']):
            return send_file(job['output_path'], as_attachment=True)
        else:
            flash('Output file not found', 'error')
            return redirect(url_for('view_job', job_id=job_id))

    elif job['output_type'] == 'text' and job['output_text']:
        return render_template('output_text.html', job=job)

    else:
        flash('No output available', 'info')
        return redirect(url_for('view_job', job_id=job_id))


@app.route('/queue/pending')
@admin_required
def pending_queue():
    """View pending jobs requiring approval (admin only)"""
    pending_jobs = queue_manager.list_jobs(status='pending', limit=100)
    return render_template('pending_queue.html', jobs=pending_jobs)


@app.route('/api/stats')
@login_required
def api_stats():
    """API endpoint for queue statistics"""
    stats = queue_manager.get_stats()
    return jsonify(stats)


@app.route('/api/next_job')
@login_required
def api_next_job():
    """API endpoint to get next approved job (for queue watcher)"""
    job = queue_manager.get_next_approved_job()
    if job:
        return jsonify(job)
    return jsonify({'message': 'No jobs in queue'}), 404


@app.route('/config')
@login_required
def config_page():
    """View and manage configuration"""
    return render_template(
        'config.html',
        processing_mode=Config.PROCESSING_MODE,
        max_concurrent=Config.MAX_CONCURRENT_JOBS
    )


@app.template_filter('datetime')
def format_datetime(value):
    """Template filter to format ISO datetime strings"""
    if not value:
        return 'N/A'
    try:
        dt = datetime.fromisoformat(value)
        return dt.strftime('%Y-%m-%d %H:%M:%S UTC')
    except:
        return value


@app.template_filter('filesize')
def format_filesize(path):
    """Template filter to format file size"""
    if not path or not os.path.exists(path):
        return 'N/A'
    size = os.path.getsize(path)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


if __name__ == '__main__':
    # Run on all interfaces to be accessible via Cloudflare Tunnel
    # Using port 5001 since macOS often uses 5000 for AirPlay
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
