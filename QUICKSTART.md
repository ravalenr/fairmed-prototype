# FairMed Quick Start Guide

## Easiest Method: One-Command Startup

```bash
cd fairmed-prototype
./start.sh
```

This script automatically:
- Checks and clears ports 3000 and 5001
- Starts the Flask backend on http://localhost:5001
- Starts the React frontend on http://localhost:3000
- Handles all dependencies

To stop all services:
```bash
./stop.sh
```

---

## Manual Setup (Alternative)

### First Time Setup

#### 1. Backend Setup (Terminal 1)

```bash
cd fairmed-prototype/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

Keep this terminal running!

#### 2. Frontend Setup (Terminal 2)

```bash
cd fairmed-prototype/frontend
npm install
BROWSER=none npm start
```

---

## Subsequent Runs (Manual Method)

### Backend (Terminal 1)
```bash
cd fairmed-prototype/backend
source venv/bin/activate
python3 app.py
```

### Frontend (Terminal 2)
```bash
cd fairmed-prototype/frontend
BROWSER=none npm start
```

---

## Quick Health Check

Backend is running:
```bash
curl http://localhost:5001/api/health
```

Should return: `{"message": "FairMed API is running", "status": "healthy"}`

---

## Stop the Servers

Press `Ctrl+C` in each terminal window.

---

## Troubleshooting

### Frontend won't start or hangs during compilation

If `npm start` hangs without showing "Compiled successfully!", try:

```bash
cd fairmed-prototype/frontend
rm -rf node_modules package-lock.json
npm install
BROWSER=none npm start
```

This clears corrupted cache and reinstalls dependencies.

### Port already in use

If you see "Port 3000 is already in use":
```bash
lsof -ti:3000 | xargs kill -9
```

If you see "Port 5001 is already in use":
```bash
lsof -ti:5001 | xargs kill -9
```

Or simply use the `stop.sh` script to kill all services.

---

## Need Help?

See the full README.md for detailed troubleshooting.
