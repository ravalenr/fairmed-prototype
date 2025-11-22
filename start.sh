#!/bin/bash
# FairMed Application Startup Script
# This script ensures smooth startup of both backend and frontend services

set -e  # Exit on error

echo "=========================================="
echo "  FairMed Application Startup"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        echo -e "${YELLOW}Warning: Port $1 is already in use${NC}"
        echo "Killing process on port $1..."
        lsof -ti:$1 | xargs kill -9 2>/dev/null || true
        sleep 1
    fi
}

# Check and clear ports
echo "Checking ports..."
check_port 5001  # Backend
check_port 3000  # Frontend

# Start Backend
echo ""
echo -e "${GREEN}Starting Backend (Flask API)...${NC}"
cd backend

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv and install dependencies
source venv/bin/activate
pip install -q -r requirements.txt

# Start Flask server in background
python3 app.py &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

# Wait for backend to start
echo "Waiting for backend to be ready..."
sleep 3

# Verify backend is running
if curl -s http://localhost:5001/api/health > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Backend is running on http://localhost:5001${NC}"
else
    echo "Error: Backend failed to start"
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi

# Start Frontend
echo ""
echo -e "${GREEN}Starting Frontend (React)...${NC}"
cd ../frontend

# Check if node_modules exists, install if not
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

# Start React development server
echo "Starting React development server..."
BROWSER=none PORT=3000 npm start &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

# Wait for frontend to compile
echo "Waiting for webpack to compile..."
sleep 15

echo ""
echo "=========================================="
echo -e "${GREEN}  Application Started Successfully!${NC}"
echo "=========================================="
echo ""
echo "Backend:  http://localhost:5001"
echo "Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Save PIDs for cleanup
echo $BACKEND_PID > /tmp/fairmed_backend.pid
echo $FRONTEND_PID > /tmp/fairmed_frontend.pid

# Wait for Ctrl+C
trap "echo ''; echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; rm -f /tmp/fairmed_*.pid; echo 'Services stopped.'; exit 0" INT

# Keep script running
wait
