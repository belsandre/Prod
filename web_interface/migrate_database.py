#!/usr/bin/env python3
"""
Database Migration Script

Adds thread_id and parent_job_id columns to existing jobs table.
"""

import sqlite3
import os
from config import Config

def migrate():
    """Add thread columns to existing database"""
    db_path = Config.DATABASE_PATH

    if not os.path.exists(db_path):
        print("No existing database found. No migration needed.")
        return

    print(f"Migrating database: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(jobs)")
        columns = [row[1] for row in cursor.fetchall()]

        needs_migration = False

        if 'thread_id' not in columns:
            print("  Adding thread_id column...")
            cursor.execute('ALTER TABLE jobs ADD COLUMN thread_id INTEGER')
            needs_migration = True

        if 'parent_job_id' not in columns:
            print("  Adding parent_job_id column...")
            cursor.execute('ALTER TABLE jobs ADD COLUMN parent_job_id INTEGER')
            needs_migration = True

        if needs_migration:
            # For existing jobs, set thread_id to their own id (each is its own thread)
            cursor.execute('''
                UPDATE jobs
                SET thread_id = id
                WHERE thread_id IS NULL
            ''')

            # Create indexes
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_thread_id ON jobs(thread_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_parent_job_id ON jobs(parent_job_id)')

            conn.commit()
            print("✓ Migration completed successfully")
        else:
            print("✓ Database already up to date")

    except Exception as e:
        print(f"✗ Migration failed: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == '__main__':
    migrate()
