import json
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional, Dict, List

class UserManager:
    """Manages user authentication and user data"""

    def __init__(self, users_file: str = None):
        self.users_file = users_file or os.path.join(
            os.path.dirname(__file__), 'users.json'
        )
        self._ensure_users_file()

    def _ensure_users_file(self):
        """Ensure users.json exists"""
        if not os.path.exists(self.users_file):
            self._create_default_users()

    def _create_default_users(self):
        """Create default users file with admin user"""
        default_data = {
            "users": [
                {
                    "username": "admin",
                    "password_hash": generate_password_hash("changeme123"),
                    "role": "admin",
                    "folder": None,
                    "created_at": datetime.utcnow().isoformat()
                }
            ]
        }
        self._save_users(default_data)

    def _load_users(self) -> Dict:
        """Load users from JSON file"""
        with open(self.users_file, 'r') as f:
            return json.load(f)

    def _save_users(self, data: Dict):
        """Save users to JSON file"""
        with open(self.users_file, 'w') as f:
            json.dump(data, f, indent=2)

    def get_user(self, username: str) -> Optional[Dict]:
        """Get user by username"""
        data = self._load_users()
        for user in data['users']:
            if user['username'] == username:
                return user
        return None

    def authenticate(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate user and return user data if successful"""
        user = self.get_user(username)
        if user and check_password_hash(user['password_hash'], password):
            # Return user data without password hash
            return {
                'username': user['username'],
                'role': user['role'],
                'folder': user['folder']
            }
        return None

    def create_user(self, username: str, password: str, role: str = 'user', folder: str = None) -> bool:
        """Create a new user"""
        data = self._load_users()

        # Check if user already exists
        if any(u['username'] == username for u in data['users']):
            return False

        # Create user
        new_user = {
            'username': username,
            'password_hash': generate_password_hash(password),
            'role': role,
            'folder': folder or f'users/{username}',
            'created_at': datetime.utcnow().isoformat()
        }

        data['users'].append(new_user)
        self._save_users(data)

        # Create user directories
        if new_user['folder']:
            self._create_user_directories(new_user['folder'])

        return True

    def _create_user_directories(self, folder: str):
        """Create directory structure for user"""
        base_path = os.path.join(os.path.dirname(__file__), '..', folder)

        for subdir in ['inputs', 'outputs', 'workflows']:
            dir_path = os.path.join(base_path, subdir)
            os.makedirs(dir_path, exist_ok=True)

            # Create .gitkeep files
            gitkeep = os.path.join(dir_path, '.gitkeep')
            if not os.path.exists(gitkeep):
                open(gitkeep, 'a').close()

    def delete_user(self, username: str) -> bool:
        """Delete a user (does not delete their files)"""
        if username == 'admin':
            return False  # Cannot delete admin

        data = self._load_users()
        original_count = len(data['users'])
        data['users'] = [u for u in data['users'] if u['username'] != username]

        if len(data['users']) < original_count:
            self._save_users(data)
            return True
        return False

    def update_password(self, username: str, new_password: str) -> bool:
        """Update user password"""
        data = self._load_users()

        for user in data['users']:
            if user['username'] == username:
                user['password_hash'] = generate_password_hash(new_password)
                self._save_users(data)
                return True

        return False

    def list_users(self) -> List[Dict]:
        """List all users (without password hashes)"""
        data = self._load_users()
        return [
            {
                'username': u['username'],
                'role': u['role'],
                'folder': u['folder'],
                'created_at': u['created_at']
            }
            for u in data['users']
        ]

    def is_admin(self, username: str) -> bool:
        """Check if user is admin"""
        user = self.get_user(username)
        return user and user['role'] == 'admin'

    def get_user_folder(self, username: str) -> Optional[str]:
        """Get user's folder path"""
        user = self.get_user(username)
        return user['folder'] if user else None
