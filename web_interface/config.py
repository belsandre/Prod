import os
from datetime import timedelta

class Config:
    """Configuration for the web interface and job queue system"""

    # Basic Authentication
    # IMPORTANT: Change these credentials before deploying!
    USERNAME = os.environ.get('AUTH_USERNAME', 'admin')
    PASSWORD = os.environ.get('AUTH_PASSWORD', 'changeme123')

    # Flask Settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)

    # Paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.dirname(BASE_DIR)  # Parent directory (Prod/)
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    OUTPUT_FOLDER = os.path.join(BASE_DIR, 'outputs')
    DATABASE_PATH = os.path.join(BASE_DIR, 'jobs.db')
    USERS_JSON_PATH = os.path.join(BASE_DIR, 'users.json')

    # User folder paths (in Prod/ directory)
    SHARED_FOLDER = os.path.join(PROJECT_ROOT, 'shared')
    USERS_FOLDER = os.path.join(PROJECT_ROOT, 'users')

    # Upload Settings
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max file size
    ALLOWED_EXTENSIONS = {
        'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif',
        'csv', 'json', 'xml', 'md', 'py', 'js',
        'html', 'css', 'zip', 'tar', 'gz'
    }

    # Job Processing Mode
    # Options: 'manual' or 'auto'
    # manual: Jobs require approval before processing
    # auto: Jobs are automatically processed by queue watcher
    PROCESSING_MODE = os.environ.get('PROCESSING_MODE', 'manual')

    # Queue Settings
    MAX_CONCURRENT_JOBS = int(os.environ.get('MAX_CONCURRENT_JOBS', 1))

    @staticmethod
    def allowed_file(filename):
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

    @staticmethod
    def get_user_input_folder(user_folder: str) -> str:
        """Get user's input folder path"""
        if not user_folder:
            return Config.UPLOAD_FOLDER
        return os.path.join(Config.PROJECT_ROOT, user_folder, 'inputs')

    @staticmethod
    def get_user_output_folder(user_folder: str) -> str:
        """Get user's output folder path"""
        if not user_folder:
            return Config.OUTPUT_FOLDER
        return os.path.join(Config.PROJECT_ROOT, user_folder, 'outputs')

    @staticmethod
    def get_user_workflow_folder(user_folder: str) -> str:
        """Get user's workflow folder path"""
        if not user_folder:
            return None
        return os.path.join(Config.PROJECT_ROOT, user_folder, 'workflows')
