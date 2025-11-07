"""
Job Processor - Helper module for processing jobs from Claude Code conversation

Usage:
    from job_processor import get_next_job, start_processing, save_output

    # Get next job
    job = get_next_job()

    # Start processing
    start_processing(job['id'])

    # Save output
    save_output(job['id'], 'text', 'Your output here')
    # or
    save_output(job['id'], 'file', '/path/to/output.pdf')
"""

import os
import sys
from datetime import datetime
from typing import Optional, Dict, List

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from queue_manager import QueueManager
from config import Config

class JobProcessor:
    """Simplified interface for processing jobs in Claude Code conversation"""

    def __init__(self):
        self.queue = QueueManager()

    def get_next_job(self) -> Optional[Dict]:
        """Get the next approved job to process"""
        job = self.queue.get_next_approved_job()

        if not job:
            print("\n" + "="*70)
            print("NO JOBS IN QUEUE")
            print("="*70)
            print("There are no approved jobs waiting to be processed.")
            print("\nCheck the web interface:")
            print("  - Are there pending jobs that need approval?")
            print("  - Has anyone submitted jobs recently?")
            print("="*70 + "\n")
            return None

        # Display the job
        self._display_job(job)

        return job

    def _display_job(self, job: Dict):
        """Display job details in a readable format"""
        print("\n" + "="*70)
        print(f"NEXT JOB IN QUEUE")
        print("="*70)
        print(f"Job ID:      #{job['id']}")
        print(f"User:        {job['username']}")
        print(f"Type:        {job['job_type']}")
        print(f"Priority:    {job['priority']}")
        print(f"Created:     {job['created_at']}")
        print(f"Status:      {job['status']}")

        # Check if part of a thread
        if job.get('thread_id'):
            thread = self.queue.get_thread(job['thread_id'])
            if len(thread) > 1:
                print(f"Thread:      Part of conversation (Message {len([j for j in thread if j['id'] <= job['id']])}/{len(thread)})")

        print("="*70)

        # Display prompt
        if job.get('prompt'):
            print("\nPROMPT:")
            print("-" * 70)
            print(job['prompt'])
            print("-" * 70)

        # Display uploaded files
        if job.get('file_paths'):
            print("\nFILES:")
            for filepath in job['file_paths']:
                filename = os.path.basename(filepath)
                if os.path.exists(filepath):
                    size = os.path.getsize(filepath)
                    print(f"  📄 {filepath}")
                    print(f"     Size: {self._format_size(size)}")
                else:
                    print(f"  ⚠️  {filepath} [NOT FOUND]")

        # Display thread context if this is a reply
        if job.get('thread_id'):
            self._display_thread_context(job)

        print("\n" + "="*70)
        print("Ready to process this job!")
        print("="*70 + "\n")

    def _display_thread_context(self, job: Dict):
        """Display conversation thread context"""
        if not job.get('thread_id'):
            return

        thread = self.queue.get_thread(job['thread_id'])

        # Only show context if there are previous jobs
        if len(thread) <= 1:
            return

        print("\n" + "="*70)
        print("CONVERSATION THREAD CONTEXT")
        print("="*70)
        print("This job is part of a conversation. Here's the history:\n")

        for i, thread_job in enumerate(thread, 1):
            is_current = thread_job['id'] == job['id']

            if is_current:
                print(f"📍 [Message {i}/{len(thread)}] Job #{thread_job['id']} ⬅️ CURRENT JOB")
            else:
                print(f"💬 [Message {i}/{len(thread)}] Job #{thread_job['id']}")

            print(f"   User: {thread_job['username']}")
            print(f"   Date: {thread_job['created_at'][:19]}")

            if thread_job.get('prompt'):
                prompt_preview = thread_job['prompt'][:100]
                if len(thread_job['prompt']) > 100:
                    prompt_preview += "..."
                print(f"   Prompt: {prompt_preview}")

            if thread_job.get('file_paths'):
                print(f"   Files: {', '.join([os.path.basename(f) for f in thread_job['file_paths']])}")

            if thread_job['status'] == 'completed' and not is_current:
                if thread_job.get('output_text'):
                    output_preview = thread_job['output_text'][:150]
                    if len(thread_job['output_text']) > 150:
                        output_preview += "..."
                    print(f"   ✅ Response: {output_preview}")
                elif thread_job.get('output_path'):
                    print(f"   ✅ Response: {os.path.basename(thread_job['output_path'])} (file)")

            if not is_current:
                print()

        print("="*70)
        print("💡 You have full context of the conversation above")

        # Show all files available in the thread
        all_files = self.queue.get_thread_files(job['thread_id'])
        if all_files:
            print("\n📦 ALL FILES AVAILABLE IN THIS THREAD:")
            for filepath in all_files:
                if os.path.exists(filepath):
                    print(f"  • {filepath}")
                else:
                    print(f"  • {filepath} [NOT FOUND]")

        print("="*70)

    def start_processing(self, job_id: int) -> bool:
        """Mark a job as being processed"""
        if self.queue.start_job(job_id):
            print(f"\n✓ Job #{job_id} marked as PROCESSING\n")
            return True
        else:
            print(f"\n✗ Could not start job #{job_id}\n")
            return False

    def save_output(self, job_id: int, output_type: str, content: str) -> bool:
        """
        Save job output and mark as complete

        Args:
            job_id: The job ID
            output_type: 'text' or 'file'
            content: For text - the text content
                    For file - the file path
        """
        if output_type == 'text':
            success = self.queue.complete_job(job_id, 'text', output_text=content)
        elif output_type == 'file':
            if not os.path.exists(content):
                print(f"\n✗ File not found: {content}\n")
                return False
            success = self.queue.complete_job(job_id, 'file', output_path=content)
        else:
            print(f"\n✗ Invalid output_type: {output_type}. Must be 'text' or 'file'\n")
            return False

        if success:
            print(f"\n✅ Job #{job_id} marked as COMPLETED")
            print(f"   Output type: {output_type}")
            if output_type == 'file':
                print(f"   Output file: {content}")
            print(f"\n   User can now view the output in the web interface.\n")
            return True
        else:
            print(f"\n✗ Could not complete job #{job_id}\n")
            return False

    def fail_job(self, job_id: int, error_message: str) -> bool:
        """Mark a job as failed"""
        if self.queue.fail_job(job_id, error_message):
            print(f"\n⚠️  Job #{job_id} marked as FAILED")
            print(f"   Error: {error_message}\n")
            return True
        else:
            print(f"\n✗ Could not fail job #{job_id}\n")
            return False

    def get_job_details(self, job_id: int) -> Optional[Dict]:
        """Get details of a specific job"""
        job = self.queue.get_job(job_id)
        if job:
            self._display_job(job)
        return job

    def _format_size(self, size: int) -> str:
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"


# Convenience functions for direct import
_processor = JobProcessor()

def get_next_job() -> Optional[Dict]:
    """Get the next approved job to process"""
    return _processor.get_next_job()

def start_processing(job_id: int) -> bool:
    """Mark a job as being processed"""
    return _processor.start_processing(job_id)

def save_output(job_id: int, output_type: str, content: str) -> bool:
    """
    Save job output and mark as complete

    Args:
        job_id: The job ID
        output_type: 'text' or 'file'
        content: For text - the text content, for file - the file path
    """
    return _processor.save_output(job_id, output_type, content)

def fail_job(job_id: int, error_message: str) -> bool:
    """Mark a job as failed"""
    return _processor.fail_job(job_id, error_message)

def get_job(job_id: int) -> Optional[Dict]:
    """Get details of a specific job"""
    return _processor.get_job_details(job_id)


if __name__ == '__main__':
    # Quick test/demo
    print("Job Processor - Interactive Mode")
    print("="*70)

    job = get_next_job()

    if job:
        print(f"\nTo process this job:")
        print(f"  1. start_processing({job['id']})")
        print(f"  2. Do your work...")
        print(f"  3. save_output({job['id']}, 'text', 'Your result')")
        print(f"     or save_output({job['id']}, 'file', '/path/to/output.pdf')")
