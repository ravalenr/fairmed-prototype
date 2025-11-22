#!/bin/bash
# FairMed Application Stop Script
# Gracefully stops both backend and frontend services

echo "Stopping FairMed services..."

# Kill processes by PID files if they exist
if [ -f /tmp/fairmed_backend.pid ]; then
    BACKEND_PID=$(cat /tmp/fairmed_backend.pid)
    kill $BACKEND_PID 2>/dev/null && echo "Backend stopped (PID: $BACKEND_PID)"
    rm -f /tmp/fairmed_backend.pid
fi

if [ -f /tmp/fairmed_frontend.pid ]; then
    FRONTEND_PID=$(cat /tmp/fairmed_frontend.pid)
    kill $FRONTEND_PID 2>/dev/null && echo "Frontend stopped (PID: $FRONTEND_PID)"
    rm -f /tmp/fairmed_frontend.pid
fi

# Also kill any remaining processes on the ports
lsof -ti:5001 | xargs kill -9 2>/dev/null || true
lsof -ti:3000 | xargs kill -9 2>/dev/null || true

# Kill any lingering react-scripts processes
pkill -f "react-scripts" 2>/dev/null || true

echo "All services stopped."
