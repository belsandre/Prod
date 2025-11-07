import sqlite3
import json
import os
from datetime import datetime
from typing import Optional, List, Dict, Any
from config import Config

class QueueManager:
    """Manages the job queue using SQLite database"""

    def __init__(self, db_path: str = None):
        self.db_path = db_path or Config.DATABASE_PATH
        self.init_db()

    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn

    def init_db(self):
        """Initialize database schema"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Jobs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                job_type TEXT NOT NULL,
                prompt TEXT,
                file_paths TEXT,
                status TEXT NOT NULL DEFAULT 'pending',
                priority INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                approved_at TEXT,
                started_at TEXT,
                completed_at TEXT,
                output_type TEXT,
                output_path TEXT,
                output_text TEXT,
                error_message TEXT,
                metadata TEXT,
                thread_id INTEGER,
                parent_job_id INTEGER,
                FOREIGN KEY (parent_job_id) REFERENCES jobs(id)
            )
        ''')

        # Create indexes for faster queries
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_status ON jobs(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_created_at ON jobs(created_at)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_username ON jobs(username)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_thread_id ON jobs(thread_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_parent_job_id ON jobs(parent_job_id)')

        conn.commit()
        conn.close()

    def create_job(
        self,
        username: str,
        job_type: str,
        prompt: str = None,
        file_paths: List[str] = None,
        priority: int = 0,
        metadata: Dict[str, Any] = None,
        parent_job_id: int = None
    ) -> int:
        """Create a new job in the queue"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Determine initial status based on processing mode
        initial_status = 'approved' if Config.PROCESSING_MODE == 'auto' else 'pending'

        # Determine thread_id
        thread_id = None
        if parent_job_id:
            # Get parent job to inherit thread_id
            cursor.execute('SELECT thread_id FROM jobs WHERE id = ?', (parent_job_id,))
            row = cursor.fetchone()
            if row:
                thread_id = row[0]

        cursor.execute('''
            INSERT INTO jobs (
                username, job_type, prompt, file_paths, status,
                priority, created_at, metadata, thread_id, parent_job_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            username,
            job_type,
            prompt,
            json.dumps(file_paths) if file_paths else None,
            initial_status,
            priority,
            datetime.utcnow().isoformat(),
            json.dumps(metadata) if metadata else None,
            thread_id,
            parent_job_id
        ))

        job_id = cursor.lastrowid

        # If this is a new thread (no parent), set thread_id to self
        if not parent_job_id:
            cursor.execute('UPDATE jobs SET thread_id = ? WHERE id = ?', (job_id, job_id))

        conn.commit()
        conn.close()

        return job_id

    def get_job(self, job_id: int) -> Optional[Dict]:
        """Get a specific job by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM jobs WHERE id = ?', (job_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return self._row_to_dict(row)
        return None

    def list_jobs(
        self,
        status: str = None,
        username: str = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict]:
        """List jobs with optional filtering"""
        conn = self.get_connection()
        cursor = conn.cursor()

        query = 'SELECT * FROM jobs WHERE 1=1'
        params = []

        if status:
            query += ' AND status = ?'
            params.append(status)

        if username:
            query += ' AND username = ?'
            params.append(username)

        query += ' ORDER BY priority DESC, created_at ASC LIMIT ? OFFSET ?'
        params.extend([limit, offset])

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        return [self._row_to_dict(row) for row in rows]

    def approve_job(self, job_id: int) -> bool:
        """Approve a pending job"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE jobs
            SET status = 'approved', approved_at = ?
            WHERE id = ? AND status = 'pending'
        ''', (datetime.utcnow().isoformat(), job_id))

        success = cursor.rowcount > 0
        conn.commit()
        conn.close()

        return success

    def reject_job(self, job_id: int, reason: str = None) -> bool:
        """Reject a pending job"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE jobs
            SET status = 'rejected', error_message = ?
            WHERE id = ? AND status = 'pending'
        ''', (reason, job_id))

        success = cursor.rowcount > 0
        conn.commit()
        conn.close()

        return success

    def start_job(self, job_id: int) -> bool:
        """Mark job as processing"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE jobs
            SET status = 'processing', started_at = ?
            WHERE id = ? AND status = 'approved'
        ''', (datetime.utcnow().isoformat(), job_id))

        success = cursor.rowcount > 0
        conn.commit()
        conn.close()

        return success

    def complete_job(
        self,
        job_id: int,
        output_type: str,
        output_path: str = None,
        output_text: str = None
    ) -> bool:
        """Mark job as completed with output"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE jobs
            SET status = 'completed',
                completed_at = ?,
                output_type = ?,
                output_path = ?,
                output_text = ?
            WHERE id = ? AND status = 'processing'
        ''', (
            datetime.utcnow().isoformat(),
            output_type,
            output_path,
            output_text,
            job_id
        ))

        success = cursor.rowcount > 0
        conn.commit()
        conn.close()

        return success

    def fail_job(self, job_id: int, error_message: str) -> bool:
        """Mark job as failed with error message"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE jobs
            SET status = 'failed',
                completed_at = ?,
                error_message = ?
            WHERE id = ?
        ''', (datetime.utcnow().isoformat(), error_message, job_id))

        success = cursor.rowcount > 0
        conn.commit()
        conn.close()

        return success

    def get_next_approved_job(self) -> Optional[Dict]:
        """Get the next approved job to process (highest priority, oldest first)"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM jobs
            WHERE status = 'approved'
            ORDER BY priority DESC, created_at ASC
            LIMIT 1
        ''')

        row = cursor.fetchone()
        conn.close()

        if row:
            return self._row_to_dict(row)
        return None

    def get_stats(self) -> Dict[str, int]:
        """Get job queue statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()

        stats = {}
        for status in ['pending', 'approved', 'processing', 'completed', 'failed', 'rejected']:
            cursor.execute('SELECT COUNT(*) FROM jobs WHERE status = ?', (status,))
            stats[status] = cursor.fetchone()[0]

        conn.close()
        return stats

    def get_thread(self, thread_id: int) -> List[Dict]:
        """Get all jobs in a thread, ordered chronologically"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM jobs
            WHERE thread_id = ?
            ORDER BY created_at ASC
        ''', (thread_id,))

        rows = cursor.fetchall()
        conn.close()

        return [self._row_to_dict(row) for row in rows]

    def get_thread_for_job(self, job_id: int) -> List[Dict]:
        """Get the full thread for a specific job"""
        job = self.get_job(job_id)
        if not job or not job.get('thread_id'):
            return [job] if job else []

        return self.get_thread(job['thread_id'])

    def get_thread_files(self, thread_id: int) -> List[str]:
        """Get all file paths from all jobs in a thread"""
        thread_jobs = self.get_thread(thread_id)
        all_files = []

        for job in thread_jobs:
            if job.get('file_paths'):
                all_files.extend(job['file_paths'])

        return all_files

    def can_reply_to_job(self, job_id: int) -> bool:
        """Check if a job can be replied to (must be completed)"""
        job = self.get_job(job_id)
        return job and job['status'] == 'completed'

    def _row_to_dict(self, row: sqlite3.Row) -> Dict:
        """Convert database row to dictionary"""
        job = dict(row)

        # Parse JSON fields
        if job.get('file_paths'):
            job['file_paths'] = json.loads(job['file_paths'])
        if job.get('metadata'):
            job['metadata'] = json.loads(job['metadata'])

        return job
