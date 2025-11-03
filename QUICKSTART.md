# FairMed - Quick Start Guide

## ⚡ Fast Setup (5 minutes)

### Step 1: Start Backend (Terminal 1)

```bash
cd fairmed-prototype/backend
source venv/bin/activate
python app.py
```

You should see:
```
🏥 AI Bias Detection Tool for Medical Diagnostics
📍 Server: http://localhost:5000
```

**Keep this terminal running!**

### Step 2: Start Frontend (Terminal 2)

Open a **new terminal**, then:

```bash
cd fairmed-prototype/frontend
npm start
```

The app will automatically open in your browser at **http://localhost:3000**

If it doesn't open, manually visit: http://localhost:3000

### Step 3: Demo the Application

1. **Select Dermatology AI scenario** (pre-selected by default)
2. Click **"Run Bias Analysis"**
3. Review the results:
   - Bias Score: 45.2 (red - biased)
   - Accuracy gap: 90% (light skin) vs 60% (dark skin)
4. Click **"Apply This Fix (Demo)"** button
5. See the improvement: Score increases to 87.3 (green - fair)

## 🎯 Demo Flow for Presentation

**Total Time: 2-3 minutes**

1. **Opening** (15 sec): "This is FairMed - it detects bias in medical AI"
2. **Show Problem** (30 sec): Run analysis, point out 30% accuracy disparity
3. **Apply Fix** (45 sec): Click mitigation, show before/after comparison
4. **Results** (30 sec): "Bias reduced by 90% - now fair across all skin tones"

## 🔍 Testing the API Directly

Test backend health:
```bash
curl http://localhost:5000/api/health
```

Test dermatology scenario:
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"scenario": "dermatology", "use_sample": true}'
```

## 🚨 Troubleshooting

### Backend won't start

**Problem**: `ModuleNotFoundError: No module named 'flask'`
**Solution**:
```bash
cd fairmed-prototype/backend
source venv/bin/activate
pip install flask flask-cors
```

### Frontend won't start

**Problem**: `npm: command not found`
**Solution**: Install Node.js from https://nodejs.org/

**Problem**: Compilation errors
**Solution**:
```bash
cd fairmed-prototype/frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

### Can't connect frontend to backend

**Problem**: "Error connecting to backend" in browser console
**Solution**:
1. Check Flask is running on port 5000
2. Check browser console for CORS errors
3. Verify both servers are running

### Port already in use

**Problem**: `Address already in use` for port 5000 or 3000
**Solution**:
```bash
# Find process on port 5000
lsof -i :5000

# Kill it (replace PID with actual number)
kill -9 <PID>
```

## 📱 What You Should See

### Backend Terminal:
```
============================================================
FairMed API Server Starting...
============================================================
🏥 AI Bias Detection Tool for Medical Diagnostics
📍 Server: http://localhost:5000
💚 Health Check: http://localhost:5000/api/health
============================================================
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Frontend Terminal:
```
Compiled successfully!

You can now view fairmed-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.X.X:3000
```

### Browser:
A purple/blue gradient interface with:
- FairMed header with hospital icon
- Three scenario buttons
- "Run Bias Analysis" button
- Results dashboard with charts

## 🎬 Recording the Demo

For your presentation video:

1. **Screen Recording**:
   - macOS: Cmd + Shift + 5
   - Windows: Windows + G
   - Record browser window only

2. **What to Show**:
   - Full demo flow (2-3 minutes)
   - Emphasize the visual impact (red → green scores)
   - Show the before/after comparison

3. **Backup Plan**:
   - Take screenshots of each step
   - If live demo fails, show screenshots

## 💡 Demo Tips

1. **Practice 3 times** before presenting
2. **Have backup**: Keep screenshots ready
3. **Test 30 minutes before**: Ensure everything runs
4. **Clear browser cache**: For clean demo
5. **Close unnecessary tabs**: Better performance

## 🎓 Key Numbers to Mention

- **Before**: 30% accuracy gap (90% vs 60%)
- **After**: 3% accuracy gap (87% vs 84%)
- **Improvement**: 90% reduction in bias
- **Score**: 45.2 → 87.3 (42 point increase)

## 📊 All Three Scenarios

Try each one to see different bias patterns:

1. **Dermatology AI** - Skin tone bias (most visual)
2. **Cardiovascular** - Gender bias
3. **Pain Management** - Age bias

## ⏱️ Next Time You Run It

Just open two terminals and:

**Terminal 1:**
```bash
cd fairmed-prototype/backend
source venv/bin/activate
python app.py
```

**Terminal 2:**
```bash
cd fairmed-prototype/frontend
npm start
```

That's it! Both servers will start and you're ready to demo.

---

**Need Help?** Check the full README.md for detailed documentation.

**Good luck with your presentation! 🚀**
