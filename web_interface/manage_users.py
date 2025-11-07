#!/usr/bin/env python3
"""
User Management CLI Tool

Manage users for the Claude Code Job Queue system.

Usage:
    python manage_users.py list                           # List all users
    python manage_users.py add <username> <password>      # Add a user
    python manage_users.py add <username> <password> --admin  # Add an admin user
    python manage_users.py delete <username>              # Delete a user
    python manage_users.py password <username> <new_password>  # Change password
"""

import argparse
import sys
from user_manager import UserManager

def main():
    parser = argparse.ArgumentParser(description='Manage users for Claude Code Job Queue')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # List users
    list_parser = subparsers.add_parser('list', help='List all users')

    # Add user
    add_parser = subparsers.add_parser('add', help='Add a new user')
    add_parser.add_argument('username', help='Username')
    add_parser.add_argument('password', help='Password')
    add_parser.add_argument('--admin', action='store_true', help='Create as admin user')
    add_parser.add_argument('--folder', help='Custom folder path (default: users/<username>)')

    # Delete user
    delete_parser = subparsers.add_parser('delete', help='Delete a user')
    delete_parser.add_argument('username', help='Username to delete')

    # Change password
    password_parser = subparsers.add_parser('password', help='Change user password')
    password_parser.add_argument('username', help='Username')
    password_parser.add_argument('new_password', help='New password')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    user_manager = UserManager()

    # List users
    if args.command == 'list':
        users = user_manager.list_users()
        if not users:
            print("No users found.")
            return

        print(f"\n{'Username':<15} {'Role':<10} {'Folder':<30} {'Created':<25}")
        print("-" * 80)
        for user in users:
            folder = user['folder'] or 'N/A'
            created = user['created_at'][:19] if user.get('created_at') else 'N/A'
            print(f"{user['username']:<15} {user['role']:<10} {folder:<30} {created:<25}")
        print()

    # Add user
    elif args.command == 'add':
        role = 'admin' if args.admin else 'user'
        folder = args.folder

        if user_manager.create_user(args.username, args.password, role, folder):
            print(f"✓ User '{args.username}' created successfully")
            print(f"  Role: {role}")
            print(f"  Folder: {folder or f'users/{args.username}'}")

            # Show folder structure
            user_folder = folder or f'users/{args.username}'
            print(f"\nUser directory structure created:")
            print(f"  {user_folder}/inputs/")
            print(f"  {user_folder}/outputs/")
            print(f"  {user_folder}/workflows/")
        else:
            print(f"✗ User '{args.username}' already exists")
            sys.exit(1)

    # Delete user
    elif args.command == 'delete':
        if args.username == 'admin':
            print("✗ Cannot delete admin user")
            sys.exit(1)

        confirm = input(f"Are you sure you want to delete user '{args.username}'? (y/N): ")
        if confirm.lower() != 'y':
            print("Cancelled.")
            return

        if user_manager.delete_user(args.username):
            print(f"✓ User '{args.username}' deleted successfully")
            print("  Note: User files were not deleted")
        else:
            print(f"✗ User '{args.username}' not found")
            sys.exit(1)

    # Change password
    elif args.command == 'password':
        if user_manager.update_password(args.username, args.new_password):
            print(f"✓ Password updated for '{args.username}'")
        else:
            print(f"✗ User '{args.username}' not found")
            sys.exit(1)


if __name__ == '__main__':
    main()
