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
os.makedirs(os.path.join(Config.SHARED_FOLDER, 'workflows'), exist_ok=True)


def _list_workflow_files(directory):
    """Return display/value pairs for workflows in a directory"""
    if not directory or not os.path.isdir(directory):
        return []

    workflows = []
    for entry in sorted(os.listdir(directory)):
        full_path = os.path.join(directory, entry)
        if os.path.isfile(full_path) and entry.lower().endswith('.md'):
            workflows.append({
                'label': entry,
                'value': os.path.relpath(full_path, Config.PROJECT_ROOT)
            })
    return workflows


def get_workflow_groups(username: str, user_folder: str, is_admin: bool):
    """Build workflow option groups and the allowed values set"""
    groups = []
    allowed_values = set()

    shared_dir = os.path.join(Config.SHARED_FOLDER, 'workflows')
    shared_workflows = _list_workflow_files(shared_dir)
    if shared_workflows:
        groups.append({
            'label': 'Shared workflows',
            'options': shared_workflows
        })
        allowed_values.update([wf['value'] for wf in shared_workflows])

    if is_admin:
        # Admins can see every user's workflows
        for user in user_manager.list_users():
            folder = user.get('folder')
            if not folder:
                continue
            workflow_dir = os.path.join(Config.PROJECT_ROOT, folder, 'workflows')
            user_workflows = _list_workflow_files(workflow_dir)
            if user_workflows:
                groups.append({
                    'label': f"{user['username']} workflows",
                    'options': user_workflows
                })
                allowed_values.update([wf['value'] for wf in user_workflows])
    else:
        workflow_dir = Config.get_user_workflow_folder(user_folder)
        user_workflows = _list_workflow_files(workflow_dir)
        if user_workflows:
            groups.append({
                'label': 'Your workflows',
                'options': user_workflows
            })
            allowed_values.update([wf['value'] for wf in user_workflows])

    return groups, allowed_values


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
    stats = queue_manager.get_stats(username=None if is_admin else username)

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
    username = session.get('username')
    user_folder = session.get('user_folder')
    is_admin = session.get('role') == 'admin'
    workflow_groups, allowed_workflows = get_workflow_groups(
        username=username,
        user_folder=user_folder,
        is_admin=is_admin
    )

    if parent_job_id:
        parent_job = queue_manager.get_job(parent_job_id)
        # Verify user owns parent job or is admin
        if parent_job and parent_job['username'] != username and not is_admin:
            flash('You cannot reply to jobs you do not own', 'error')
            return redirect(url_for('dashboard'))

    if request.method == 'POST':
        parent_id = request.form.get('parent_job_id', type=int)
        if parent_id and (not parent_job or parent_job['id'] != parent_id):
            parent_job = queue_manager.get_job(parent_id)

        if parent_job and parent_job['username'] != username and not is_admin:
            flash('You cannot reply to jobs you do not own', 'error')
            return redirect(url_for('dashboard'))

        job_type = request.form.get('job_type') or (parent_job['job_type'] if parent_job else 'general')
        custom_instructions = request.form.get('custom_instructions', '').strip()
        priority = int(request.form.get('priority', 0))
        input_urls = request.form.get('input_urls', '').strip()
        selected_workflows = [
            workflow for workflow in request.form.getlist('workflows')
            if workflow in allowed_workflows
        ]

        # Get user's input folder
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
        if not custom_instructions and not file_paths and not input_urls:
            flash('Please add custom instructions, share URLs, or upload files', 'error')
            return redirect(url_for('submit_job', parent_id=parent_id) if parent_id else url_for('submit_job'))

        metadata = {
            'submitted_from': request.remote_addr,
            'user_agent': request.headers.get('User-Agent')
        }
        if input_urls:
            metadata['input_urls'] = input_urls
        if selected_workflows:
            metadata['selected_workflows'] = selected_workflows

        # Create job
        job_id = queue_manager.create_job(
            username=username,
            job_type=job_type,
            prompt=custom_instructions if custom_instructions else None,
            file_paths=file_paths if file_paths else None,
            priority=priority,
            metadata=metadata,
            parent_job_id=parent_id
        )

        if parent_id:
            flash(f'Reply #{job_id} submitted to conversation thread', 'success')
        elif Config.PROCESSING_MODE == 'auto':
            flash(f'Job #{job_id} submitted and queued for automatic processing', 'success')
        else:
            flash(f'Job #{job_id} submitted and pending approval', 'success')

        return redirect(url_for('view_job', job_id=job_id))

    return render_template(
        'submit.html',
        parent_job=parent_job,
        workflow_groups=workflow_groups,
        processing_mode=Config.PROCESSING_MODE
    )


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
    can_edit = session.get('role') == 'admin' or (
        job['username'] == session.get('username') and job['status'] == 'pending'
    )

    return render_template(
        'job_detail.html',
        job=job,
        thread=thread,
        can_reply=can_reply,
        is_admin=session.get('role') == 'admin',
        can_edit=can_edit
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


@app.route('/job/<int:job_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_job(job_id):
    """Edit an existing job"""
    job = queue_manager.get_job(job_id)

    if not job:
        flash(f'Job #{job_id} not found', 'error')
        return redirect(url_for('dashboard'))

    username = session.get('username')
    is_admin = session.get('role') == 'admin'

    if not is_admin and job['username'] != username:
        flash('You can only edit jobs you submitted', 'error')
        return redirect(url_for('view_job', job_id=job_id))

    if not is_admin and job['status'] != 'pending':
        flash('Only pending jobs can be edited', 'error')
        return redirect(url_for('view_job', job_id=job_id))

    workflow_groups, allowed_workflows = get_workflow_groups(
        username=username,
        user_folder=session.get('user_folder'),
        is_admin=is_admin
    )

    job_metadata = job.get('metadata') or {}
    existing_files = list(job.get('file_paths') or [])

    def render_edit(form_data, selected_workflows):
        return render_template(
            'edit_job.html',
            job=job,
            form_data=form_data,
            selected_workflows=selected_workflows,
            workflow_groups=workflow_groups,
            existing_files=existing_files,
            is_admin=is_admin
        )

    if request.method == 'POST':
        form_custom_instructions = request.form.get('custom_instructions', '').strip()
        form_input_urls = request.form.get('input_urls', '').strip()
        form_priority_raw = request.form.get('priority', job.get('priority', 0))
        selected_workflows = [
            value for value in request.form.getlist('workflows')
            if value in allowed_workflows
        ]

        try:
            form_priority = int(form_priority_raw)
        except ValueError:
            flash('Priority must be a number', 'error')
            form_data = {
                'custom_instructions': form_custom_instructions,
                'input_urls': form_input_urls,
                'priority': form_priority_raw
            }
            return render_edit(form_data, selected_workflows)

        owner_folder = user_manager.get_user_folder(job['username'])
        upload_folder = Config.get_user_input_folder(owner_folder)
        os.makedirs(upload_folder, exist_ok=True)

        file_paths = list(existing_files)
        newly_saved = []
        files = request.files.getlist('files')
        for file in files:
            if file and file.filename:
                if Config.allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
                    filename = f"{timestamp}_{filename}"
                    filepath = os.path.join(upload_folder, filename)
                    file.save(filepath)
                    newly_saved.append(filepath)
                    file_paths.append(filepath)
                else:
                    flash(f'File type not allowed: {file.filename}', 'error')
                    for path in newly_saved:
                        if os.path.exists(path):
                            os.remove(path)
                    form_data = {
                        'custom_instructions': form_custom_instructions,
                        'input_urls': form_input_urls,
                        'priority': form_priority_raw
                    }
                    return render_edit(form_data, selected_workflows)

        if not form_custom_instructions and not form_input_urls and not file_paths:
            flash('Please provide instructions, URLs, or upload files', 'error')
            for path in newly_saved:
                if os.path.exists(path):
                    os.remove(path)
            form_data = {
                'custom_instructions': form_custom_instructions,
                'input_urls': form_input_urls,
                'priority': form_priority_raw
            }
            return render_edit(form_data, selected_workflows)

        updated_metadata = dict(job_metadata)
        if form_input_urls:
            updated_metadata['input_urls'] = form_input_urls
        else:
            updated_metadata.pop('input_urls', None)

        if selected_workflows:
            updated_metadata['selected_workflows'] = selected_workflows
        else:
            updated_metadata.pop('selected_workflows', None)

        # Preserve submission metadata fields
        for key in ['submitted_from', 'user_agent']:
            if key in job_metadata and key not in updated_metadata:
                updated_metadata[key] = job_metadata[key]

        success = queue_manager.update_job(
            job_id,
            prompt=form_custom_instructions if form_custom_instructions else None,
            file_paths=file_paths if file_paths else None,
            priority=form_priority,
            metadata=updated_metadata if updated_metadata else None
        )

        if not success:
            flash(f'Could not update job #{job_id}', 'error')
            for path in newly_saved:
                if os.path.exists(path):
                    os.remove(path)
            form_data = {
                'custom_instructions': form_custom_instructions,
                'input_urls': form_input_urls,
                'priority': form_priority_raw
            }
            return render_edit(form_data, selected_workflows)

        flash(f'Job #{job_id} updated successfully', 'success')
        return redirect(url_for('view_job', job_id=job_id))

    form_data = {
        'custom_instructions': job.get('prompt') or '',
        'input_urls': job_metadata.get('input_urls', ''),
        'priority': job.get('priority', 0)
    }
    selected_workflows = job_metadata.get('selected_workflows', [])

    return render_edit(form_data, selected_workflows)


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


@app.route('/job/<int:job_id>/start_processing', methods=['POST'])
@admin_required
def admin_start_job(job_id):
    """Mark an approved job as processing"""
    job = queue_manager.get_job(job_id)

    if not job:
        flash(f'Job #{job_id} not found', 'error')
    elif job['status'] != 'approved':
        flash('Only approved jobs can be moved to processing', 'error')
    elif queue_manager.start_job(job_id):
        flash(f'Job #{job_id} marked as processing', 'success')
    else:
        flash(f'Could not update job #{job_id}', 'error')

    return redirect(url_for('view_job', job_id=job_id))


@app.route('/job/<int:job_id>/complete', methods=['POST'])
@admin_required
def admin_complete_job(job_id):
    """Mark a processing job as completed with output"""
    job = queue_manager.get_job(job_id)

    if not job:
        flash(f'Job #{job_id} not found', 'error')
        return redirect(url_for('dashboard'))

    if job['status'] != 'processing':
        flash('Only processing jobs can be completed', 'error')
        return redirect(url_for('view_job', job_id=job_id))

    output_type = request.form.get('output_type')
    output_text = request.form.get('output_text', '').strip()
    output_path = request.form.get('output_path', '').strip()

    if output_type not in {'text', 'file'}:
        flash('Select an output type (text or file)', 'error')
        return redirect(url_for('view_job', job_id=job_id))

    if output_type == 'text' and not output_text:
        flash('Provide the output text', 'error')
        return redirect(url_for('view_job', job_id=job_id))

    if output_type == 'file' and not output_path:
        flash('Provide the output file path', 'error')
        return redirect(url_for('view_job', job_id=job_id))

    if queue_manager.complete_job(
        job_id,
        output_type=output_type,
        output_path=output_path if output_type == 'file' else None,
        output_text=output_text if output_type == 'text' else None
    ):
        flash(f'Job #{job_id} marked as completed', 'success')
    else:
        flash(f'Could not complete job #{job_id}', 'error')

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
