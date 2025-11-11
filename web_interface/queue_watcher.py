#!/usr/bin/env python3
"""
Queue Watcher - Monitor and process jobs from the Claude Code job queue

This script helps you (or Claude Code) monitor the job queue and process jobs.

Usage:
    python3 queue_watcher.py                 # Interactive mode - shows next job
    python3 queue_watcher.py --watch         # Watch mode - continuously check for jobs
    python3 queue_watcher.py --job <id>      # Process specific job
    python3 queue_watcher.py --stats         # Show queue statistics
"""

import argparse
import time
import os
import sys
from datetime import datetime
from queue_manager import QueueManager
from config import Config

class QueueWatcher:
    def __init__(self):
        self.queue = QueueManager()

    def show_stats(self):
        """Display queue statistics"""
        stats = self.queue.get_stats()

        print("\n" + "="*60)
        print("QUEUE STATISTICS")
        print("="*60)
        print(f"Pending Approval:  {stats['pending']}")
        print(f"Approved:          {stats['approved']}")
        print(f"Processing:        {stats['processing']}")
        print(f"Completed:         {stats['completed']}")
        print(f"Failed:            {stats['failed']}")
        print(f"Rejected:          {stats['rejected']}")
        print(f"\nProcessing Mode:   {Config.PROCESSING_MODE.upper()}")
        print("="*60 + "\n")

    def show_job(self, job, show_thread=True):
        """Display job details in a readable format"""
        print("\n" + "="*60)
        print(f"JOB #{job['id']}")
        print("="*60)
        print(f"Type:        {job['job_type']}")
        print(f"Status:      {job['status']}")
        print(f"Priority:    {job['priority']}")
        print(f"User:        {job['username']}")
        print(f"Created:     {job['created_at']}")

        metadata = job.get('metadata')
        if not isinstance(metadata, dict):
            metadata = {}

        # Show thread info if part of a thread
        if show_thread and job.get('thread_id'):
            thread = self.queue.get_thread(job['thread_id'])
            if len(thread) > 1:
                print(f"Thread:      Part of conversation (Job #{thread[0]['id']})")
                print(f"             {len(thread)} message(s) in thread")

        if job.get('prompt'):
            print(f"\nINSTRUCTIONS:")
            print("-" * 60)
            print(job['prompt'])
            print("-" * 60)

        input_urls = metadata.get('input_urls')
        if input_urls:
            print(f"\nINPUT URLS & ACCESS NOTES:")
            print("-" * 60)
            print(input_urls)
            print("-" * 60)

        selected_workflows = metadata.get('selected_workflows') or []
        if selected_workflows:
            print(f"\nSELECTED WORKFLOWS:")
            for workflow in selected_workflows:
                print(f"  - {workflow}")

        if job.get('file_paths'):
            print(f"\nUPLOADED FILES:")
            for filepath in job['file_paths']:
                filename = os.path.basename(filepath)
                if os.path.exists(filepath):
                    size = os.path.getsize(filepath)
                    print(f"  - {filename} ({size:,} bytes)")
                    print(f"    Path: {filepath}")
                else:
                    print(f"  - {filename} [FILE NOT FOUND]")

        # Show full thread context if this job is part of a thread
        if show_thread and job.get('thread_id'):
            self.show_thread_context(job)

        print("="*60 + "\n")

    def show_thread_context(self, job):
        """Show full conversation thread context for a job"""
        if not job.get('thread_id'):
            return

        thread = self.queue.get_thread(job['thread_id'])

        # Only show context if there are previous jobs in the thread
        if len(thread) <= 1:
            return

        print(f"\nCONVERSATION THREAD CONTEXT:")
        print("="*60)
        print("Claude Code: You are processing a job in a conversation thread.")
        print("Below is the full conversation history to give you context.\n")

        for i, thread_job in enumerate(thread, 1):
            is_current = thread_job['id'] == job['id']
            marker = ">>> CURRENT JOB <<<" if is_current else ""

            print(f"\n[Message {i}/{len(thread)}] Job #{thread_job['id']} {marker}")
            print(f"User: {thread_job['username']}")
            print(f"Created: {thread_job['created_at']}")
            print(f"Status: {thread_job['status']}")

            if thread_job.get('prompt'):
                print(f"\nPrompt:")
                print(f"  {thread_job['prompt']}")

            if thread_job.get('file_paths'):
                print(f"\nFiles:")
                for filepath in thread_job['file_paths']:
                    print(f"  - {os.path.basename(filepath)}")

            if thread_job['status'] == 'completed':
                if thread_job.get('output_text'):
                    print(f"\nClaude's Response:")
                    # Show first 200 chars of output
                    output = thread_job['output_text']
                    if len(output) > 200:
                        print(f"  {output[:200]}...")
                    else:
                        print(f"  {output}")
                elif thread_job.get('output_path'):
                    print(f"\nClaude's Response: (file)")
                    print(f"  {thread_job['output_path']}")

            if not is_current:
                print("-" * 60)

        print("\n" + "="*60)
        print("End of conversation history. Process the current job with this context.")
        print("="*60 + "\n")

    def get_next_job(self):
        """Get and display the next job to process"""
        job = self.queue.get_next_approved_job()

        if not job:
            print("No approved jobs in queue.")
            return None

        self.show_job(job)
        return job

    def start_job(self, job_id):
        """Mark a job as started"""
        if self.queue.start_job(job_id):
            print(f"✓ Job #{job_id} marked as PROCESSING")
            return True
        else:
            print(f"✗ Could not start job #{job_id}")
            return False

    def complete_job(self, job_id, output_type, output_path=None, output_text=None):
        """Mark a job as completed with output"""
        if self.queue.complete_job(job_id, output_type, output_path, output_text):
            print(f"✓ Job #{job_id} marked as COMPLETED")
            return True
        else:
            print(f"✗ Could not complete job #{job_id}")
            return False

    def fail_job(self, job_id, error_message):
        """Mark a job as failed"""
        if self.queue.fail_job(job_id, error_message):
            print(f"✓ Job #{job_id} marked as FAILED")
            return True
        else:
            print(f"✗ Could not fail job #{job_id}")
            return False

    def watch_mode(self, interval=10):
        """Continuously watch for new jobs"""
        print(f"Watching queue every {interval} seconds. Press Ctrl+C to stop.\n")

        try:
            while True:
                job = self.queue.get_next_approved_job()

                if job:
                    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] New job found!")
                    self.show_job(job)
                    print(f"Use 'python queue_watcher.py --job {job['id']}' to process this job.")
                    print("-" * 60)

                time.sleep(interval)

        except KeyboardInterrupt:
            print("\n\nStopped watching queue.")

    def interactive_mode(self):
        """Interactive mode for processing jobs"""
        self.show_stats()

        job = self.get_next_job()

        if not job:
            return

        print("ACTIONS:")
        print("  1. Start processing this job")
        print("  2. Skip this job (leave for later)")
        print("  3. View full job details")
        print("  4. Exit")

        try:
            choice = input("\nSelect action (1-4): ").strip()

            if choice == '1':
                if self.start_job(job['id']):
                    print("\nJob started! Now process the job and then mark it as complete.")
                    print("\nTo mark as COMPLETED with text output:")
                    print(f'  python queue_watcher.py --complete {job["id"]} --output-text "Your output here"')
                    print("\nTo mark as COMPLETED with file output:")
                    print(f'  python queue_watcher.py --complete {job["id"]} --output-file "/path/to/output.txt"')
                    print("\nTo mark as FAILED:")
                    print(f'  python queue_watcher.py --fail {job["id"]} --error "Error message"')

            elif choice == '2':
                print("Job skipped. It will remain in the approved queue.")

            elif choice == '3':
                self.show_job(job)
                self.interactive_mode()  # Show menu again

            elif choice == '4':
                print("Exiting.")
                return

        except (KeyboardInterrupt, EOFError):
            print("\n\nExiting.")


def main():
    parser = argparse.ArgumentParser(description='Claude Code Queue Watcher')

    parser.add_argument('--watch', action='store_true',
                        help='Watch mode - continuously check for new jobs')
    parser.add_argument('--interval', type=int, default=10,
                        help='Watch interval in seconds (default: 10)')
    parser.add_argument('--stats', action='store_true',
                        help='Show queue statistics')
    parser.add_argument('--job', type=int, metavar='ID',
                        help='Show specific job by ID')
    parser.add_argument('--start', type=int, metavar='ID',
                        help='Mark job as started/processing')
    parser.add_argument('--complete', type=int, metavar='ID',
                        help='Mark job as completed')
    parser.add_argument('--output-text', type=str,
                        help='Text output for completed job')
    parser.add_argument('--output-file', type=str,
                        help='File path for completed job output')
    parser.add_argument('--fail', type=int, metavar='ID',
                        help='Mark job as failed')
    parser.add_argument('--error', type=str,
                        help='Error message for failed job')

    args = parser.parse_args()
    watcher = QueueWatcher()

    # Show stats
    if args.stats:
        watcher.show_stats()
        return

    # Watch mode
    if args.watch:
        watcher.watch_mode(args.interval)
        return

    # Show specific job
    if args.job:
        job = watcher.queue.get_job(args.job)
        if job:
            watcher.show_job(job)
        else:
            print(f"Job #{args.job} not found.")
        return

    # Start job
    if args.start:
        watcher.start_job(args.start)
        return

    # Complete job
    if args.complete:
        if args.output_text:
            watcher.complete_job(args.complete, 'text', output_text=args.output_text)
        elif args.output_file:
            if os.path.exists(args.output_file):
                watcher.complete_job(args.complete, 'file', output_path=args.output_file)
            else:
                print(f"Error: File not found: {args.output_file}")
        else:
            print("Error: Must provide either --output-text or --output-file")
        return

    # Fail job
    if args.fail:
        error_msg = args.error or "Job failed"
        watcher.fail_job(args.fail, error_msg)
        return

    # Default: Interactive mode
    watcher.interactive_mode()


if __name__ == '__main__':
    main()
