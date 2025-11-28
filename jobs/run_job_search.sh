#!/bin/bash

# Job Search Automation Runner Script
# This script is designed to be run by cron

# Set up environment
export PATH=/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin

# Script directory
SCRIPT_DIR="/Users/bisikennadi/Projects/automations/jobs"
LOG_DIR="$SCRIPT_DIR/logs"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Load environment variables from .env file
if [ -f "$SCRIPT_DIR/.env" ]; then
    export $(cat "$SCRIPT_DIR/.env" | grep -v '^#' | xargs)
fi

# Create logs directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Change to script directory
cd "$SCRIPT_DIR" || exit 1

# Log file for this run
LOG_FILE="$LOG_DIR/job_search_$TIMESTAMP.log"

echo "========================================" >> "$LOG_FILE"
echo "Job Search Started: $(date)" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

# Check if virtual environment exists, activate if present
if [ -d "$SCRIPT_DIR/venv" ]; then
    echo "Activating virtual environment..." >> "$LOG_FILE"
    source "$SCRIPT_DIR/venv/bin/activate"
fi

# Run the Python script
python3 jobs.py >> "$LOG_FILE" 2>&1

# Capture exit status
EXIT_CODE=$?

echo "========================================" >> "$LOG_FILE"
echo "Job Search Completed: $(date)" >> "$LOG_FILE"
echo "Exit Code: $EXIT_CODE" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

# Keep only last 30 log files (cleanup)
cd "$LOG_DIR" && ls -t job_search_*.log | tail -n +31 | xargs -r rm

exit $EXIT_CODE

