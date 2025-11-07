#!/bin/bash
# Setup script for multi-user and conversation threads

echo "========================================="
echo "Multi-User & Threads Setup"
echo "========================================="
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"
echo ""

# Run migration
echo "Running database migration..."
python3 migrate_database.py
echo ""

# Create tam user
echo "Creating tam user..."
python3 manage_users.py add tam tam123 --folder users/tam 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ User 'tam' created"
else
    echo "Note: User 'tam' may already exist"
fi
echo ""

# List users
echo "Current users:"
python3 manage_users.py list
echo ""

echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "You can now:"
echo "  1. Start the server: ./start.sh"
echo "  2. Login as admin: admin / changeme123"
echo "  3. Login as tam: tam / tam123"
echo ""
echo "Features enabled:"
echo "  ✓ Multi-user support with roles"
echo "  ✓ Conversation threads (reply to jobs)"
echo "  ✓ User-specific workspaces"
echo "  ✓ Full thread context for Claude Code"
echo ""
echo "See MULTI_USER_THREADS_GUIDE.md for usage instructions"
echo ""
