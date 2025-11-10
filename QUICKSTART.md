# FairMed Quick Start Guide

## First Time Setup

### 1. Backend Setup (Terminal 1)

```bash
cd fairmed-prototype/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

Keep this terminal running!

### 2. Frontend Setup (Terminal 2)

```bash
cd fairmed-prototype/frontend
npm install
npm start
```

Your browser will open automatically at http://localhost:3000

---

## Subsequent Runs

### Backend (Terminal 1)
```bash
cd fairmed-prototype/backend
source venv/bin/activate
python3 app.py
```

### Frontend (Terminal 2)
```bash
cd fairmed-prototype/frontend
npm start
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

## Need Help?

See the full README.md for detailed troubleshooting.
