#!/bin/bash
echo "Starting ThanuRaksha Email Service..."
echo "PORT: $PORT"
echo "GMAIL_USER: $GMAIL_USER"
echo "Python version: $(python --version)"
echo "Gunicorn version: $(gunicorn --version)"

# Start the application
exec gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 120 --log-level info
