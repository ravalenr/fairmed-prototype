# FairMed - AI Bias Detection & Mitigation Tool

A web-based prototype for detecting and mitigating algorithmic bias in medical AI diagnostic systems.

---

## Academic Disclaimer

**This is a student project developed as part of the CCT College Dublin Higher Diploma in Computing coursework (Project Skills & Professionalism module).**

This prototype demonstrates core software development competencies including:
- Full-stack web development (React + Flask)
- RESTful API design and implementation
- Data structure optimization and algorithm complexity analysis
- Frontend data visualization with Chart.js
- Professional UI/UX design principles

---

## Table of Contents

1. [Technology Stack](#technology-stack)
2. [Project Description](#project-description)
3. [Folder Organization](#folder-organization)
4. [How to Run the Application](#how-to-run-the-application)
5. [Data Structure & Time Complexity Analysis](#data-structure--time-complexity-analysis)
6. [How FairMed Works](#how-fairmed-works)
7. [For Recruiters](#for-recruiters)

---

## Technology Stack

### Backend
- **Python 3.8+** - Core programming language
- **Flask 3.0+** - Lightweight WSGI web framework for REST API
- **Flask-CORS** - Cross-Origin Resource Sharing support

### Frontend
- **React 18.2** - JavaScript library for building user interfaces
- **Chart.js 4.4** - Data visualization library
- **react-chartjs-2 5.2** - React wrapper for Chart.js
- **Axios 1.6** - HTTP client for API communication

### Development Tools
- **Node.js 16+** - JavaScript runtime for frontend development
- **npm** - Package manager for JavaScript dependencies
- **Python venv** - Virtual environment for Python dependency isolation

---

## Project Description

FairMed is an interactive web application that addresses the critical issue of algorithmic bias in medical AI systems. Healthcare algorithms trained on non-representative datasets can perpetuate or amplify healthcare disparities across demographic groups.

### Core Functionality

1. **Bias Detection**: Analyzes AI model performance across different demographic groups (skin tone, gender, age) using established fairness metrics
2. **Visualization**: Presents performance disparities through interactive charts and comparison tables
3. **Mitigation Strategies**: Recommends evidence-based approaches to reduce bias (adversarial debiasing, data augmentation, threshold adjustment)
4. **Impact Demonstration**: Shows before/after comparison when mitigation techniques are applied

### Demo Scenarios

The prototype includes three pre-configured medical AI bias scenarios:

1. **Dermatology AI** - Melanoma detection showing 30% accuracy disparity across skin tones (Fitzpatrick I-III vs V-VI)
2. **Cardiovascular Predictor** - Heart disease diagnosis with 13% gender-based performance gap
3. **Pain Management Algorithm** - Age-biased pain assessment undertreating elderly patients by 14%

Each scenario demonstrates realistic bias patterns based on documented cases in medical AI literature.

---

## Folder Organization

```
fairmed-prototype/
│
├── backend/                    # Flask REST API server
│   ├── app.py                 # Main application with API endpoints
│   ├── requirements.txt       # Python dependencies
│   └── venv/                  # Python virtual environment (created during setup)
│
├── frontend/                   # React web application
│   ├── public/                # Static assets
│   │   └── index.html        # HTML template
│   ├── src/                   # Source code
│   │   ├── components/       # React components
│   │   │   └── Dashboard.js  # Results visualization component
│   │   ├── App.js            # Main React component
│   │   ├── App.css           # Application styles
│   │   └── index.js          # React entry point
│   ├── package.json          # Node.js dependencies
│   └── node_modules/         # Installed npm packages (created during setup)
│
├── README.md                   # This file
└── QUICKSTART.md              # Quick setup guide for demos
```

### Key Files

- **backend/app.py**: Core API with 3 endpoints (`/api/health`, `/api/analyze`, `/api/mitigate`) and 6 scenario data functions
- **frontend/src/App.js**: Main UI with scenario selection, API integration, and state management
- **frontend/src/components/Dashboard.js**: Data visualization with Chart.js integration
- **frontend/src/App.css**: Professional styling with responsive design

---

## How to Run the Application

### Prerequisites

Ensure you have installed:
- Python 3.8+ ([Download](https://www.python.org/downloads/))
- Node.js 16+ ([Download](https://nodejs.org/))

### Quick Start

#### Step 1: Start Backend Server

Open a terminal and run:

```bash
cd fairmed-prototype/backend
python3 -m venv venv
source venv/bin/activate          # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python3 app.py
```

You should see:
```
============================================================
FairMed API Server Starting...
============================================================
Server: http://localhost:5001
Health Check: http://localhost:5001/api/health
============================================================
```

**Keep this terminal running.**

#### Step 2: Start Frontend Server

Open a **new terminal** and run:

```bash
cd fairmed-prototype/frontend
npm install
npm start
```

The application will automatically open in your browser at **http://localhost:3000**

If it doesn't open automatically, manually visit: http://localhost:3000

#### Step 3: Demo the Application

1. Select a scenario (Dermatology AI is pre-selected)
2. Click "Run Bias Analysis"
3. Review the fairness score and performance disparities
4. Click "Apply This Fix (Demo)" to see the mitigation impact
5. Compare before/after results

### Troubleshooting

**Port Conflicts:**
- Backend uses port 5001 (macOS AirPlay uses 5000)
- Frontend uses port 3000
- If ports are occupied, check running processes: `lsof -i :5001` or `lsof -i :3000`

**API Connection Issues:**
- Ensure both servers are running
- Check browser console for CORS errors
- Verify backend health: `curl http://localhost:5001/api/health`

---

## Data Structure & Time Complexity Analysis

### Data Structures

#### 1. Scenario Results (Nested Dictionary)

**Structure:**
```python
{
    'scenario': str,                    # O(1) access
    'overall_score': float,            # O(1) access
    'groups': {                        # Dictionary of groups
        'group_name': {                # O(1) group lookup
            'accuracy': float,         # O(1) metric access
            'tpr': float,
            'precision': float,
            'confusion_matrix': {...}  # O(1) nested access
        }
    },
    'flags': [...],                    # Array of warning objects
    'recommendations': [...]           # Array of mitigation strategies
}
```

**Time Complexity:**
- **Group lookup**: O(1) average case (hash table)
- **Metric access**: O(1) (direct key access)
- **Iteration over all groups**: O(n) where n = number of demographic groups
- **Flag generation**: O(n) - one pass through groups to calculate disparities

**Space Complexity:** O(n × m) where n = number of groups, m = metrics per group

**Justification:** Dictionaries (hash maps) provide O(1) average-case lookup for group-specific metrics, critical for real-time dashboard rendering.

#### 2. Chart Data Arrays

**Structure:**
```javascript
const groupNames = Object.keys(results.groups);        // O(n) extraction
const accuracies = groupNames.map(g => ...);          // O(n) transformation
```

**Time Complexity:**
- **Data extraction**: O(n) where n = number of groups
- **Chart rendering**: O(n) for bar chart (Chart.js renders linearly)

**Space Complexity:** O(n) - separate arrays for each metric type

**Justification:** Arrays maintain group ordering for consistent chart visualization. Linear iteration is acceptable given small n (typically 2-3 groups).

#### 3. API Request/Response Flow

```
Client Request → Flask Router (O(1)) → Scenario Loader (O(1)) →
JSON Serialization (O(n)) → HTTP Response → Axios Parsing (O(n)) →
React State Update (O(1)) → Component Re-render (O(n))
```

**Total API Call Complexity**: O(n) where n = total JSON data size

**Optimization Considerations:**
- Hardcoded scenario data eliminates ML computation overhead (which would be O(n²) for pairwise fairness comparisons in production)
- Flask JSON response uses built-in serialization (C-optimized)
- React uses virtual DOM diffing to minimize actual DOM updates

### Algorithm Complexity

#### Bias Score Calculation (Simplified for Demo)

```python
# Actual fairness metric calculation (not implemented in demo):
# for group_a in groups:
#     for group_b in groups:
#         disparity = abs(metric[group_a] - metric[group_b])
#         if disparity > threshold:
#             flags.append(warning)
# Time Complexity: O(n²) for pairwise comparison
# Space Complexity: O(k) where k = number of flags
```

**Demo Implementation:**
- Pre-calculated metrics stored in dictionaries
- No runtime computation required
- O(1) lookup per scenario

#### Frontend Rendering

**React Component Updates:**
```javascript
// Worst-case rendering complexity:
// - Dashboard component: O(n) where n = number of groups
// - Chart.js bar chart: O(n × m) where m = metrics per group
// - Table rendering: O(n × m)
// Total: O(n × m)
```

**Optimization Techniques:**
- React.memo() could be applied to Dashboard component (not implemented due to small data size)
- Chart.js uses canvas rendering (faster than SVG for this data volume)
- No unnecessary re-renders due to proper state management

---

## How FairMed Works

### The Problem

Medical AI systems trained on non-diverse datasets can exhibit significant performance disparities across demographic groups. For example:

- Dermatology AI trained primarily on light skin performs poorly on darker skin tones
- Cardiovascular algorithms undertrained on female patients lead to misdiagnosis
- Pain management systems use age as a proxy for pain tolerance, undertreating elderly patients

These biases can perpetuate or worsen existing healthcare inequities.

### FairMed's Solution

FairMed implements a **three-layer bias mitigation framework**:

#### 1. Pre-Deployment Detection
- **Fairness Metrics**: Calculates statistical parity, equalized odds, and predictive parity across demographic groups
- **Disparity Thresholds**: Flags models exceeding 5% performance variance
- **Visualization**: Interactive charts highlight group-specific accuracy, TPR, and precision

#### 2. Active Mitigation
Three evidence-based strategies:
- **Adversarial Debiasing**: Retrain model with dual objectives (accuracy + fairness)
- **Data Augmentation**: Add synthetic samples for underrepresented groups
- **Threshold Adjustment**: Use group-specific decision thresholds

#### 3. Post-Deployment Monitoring
- **Before/After Comparison**: Quantifies mitigation impact
- **Continuous Metrics**: Tracks fairness score over time
- **Impact Measurement**: Shows disparity reduction and bias score improvement

### Workflow

1. **Select Scenario**: Choose from three pre-configured medical AI bias cases
2. **Run Analysis**: System calculates fairness metrics and generates warnings
3. **Review Disparities**: Interactive dashboard shows performance gaps across groups
4. **Apply Mitigation**: Select recommended strategy (e.g., adversarial debiasing)
5. **Verify Impact**: Compare before/after metrics to ensure equitable performance

### Example Results

**Dermatology AI - Before Mitigation:**
- Overall Fairness Score: 45.2 (Biased)
- Accuracy Gap: 30% (90% light skin vs 60% dark skin)

**After Applying Adversarial Debiasing:**
- Overall Fairness Score: 87.3 (Fair)
- Accuracy Gap: 3% (87% vs 84%)
- Bias Reduction: 90%

---

## For Recruiters

### Skills Demonstrated in This Project

If you're looking for a developer with **full-stack competency**, **algorithm optimization expertise**, and **professional software engineering practices**, this project showcases:

#### Technical Skills
- **Full-Stack Development**: React frontend + Flask backend with RESTful API design
- **Data Visualization**: Chart.js integration for interactive medical data dashboards
- **Algorithm Analysis**: Time complexity optimization and data structure selection
- **State Management**: React hooks (useState) for complex application state
- **API Integration**: Axios-based HTTP communication with error handling
- **Responsive Design**: Professional CSS with gradient themes and hover effects

#### Software Engineering Practices
- **Code Organization**: Modular component architecture with clear separation of concerns
- **Documentation**: Comprehensive README with complexity analysis
- **Version Control**: Clean commit history and project structure
- **Performance Optimization**: O(1) lookups using hash maps, efficient rendering strategies
- **Accessibility**: Professional UI following modern design principles

#### Domain Knowledge
- **Healthcare AI Ethics**: Understanding of algorithmic bias and fairness metrics
- **Machine Learning Concepts**: Statistical parity, equalized odds, adversarial debiasing
- **Data Analysis**: Confusion matrix interpretation, performance metric calculation

### Connect With Me

**Interested in discussing full-stack development, AI ethics, or software optimization?**

I'm actively seeking opportunities in **software engineering** or **AI/ML development** where I can apply my skills to build impactful, equitable systems.

**Contact:**
- **LinkedIn**: https://linkedin.com/in/raphahribs
- **GitHub**: ravalenr
- **Email**: raphahribs@icloud.com
- **Portfolio**: [Your Portfolio Website]

**Available for:**
- Full-time software engineering roles
- Software Engineering graduate roles
- Contract/freelance full-stack development
- Healthcare AI/ML projects
- Code reviews and technical consultations

---

**Built with ❤️ by a CCT College Dublin student | Higher Diploma in Computing | 2025-2026**

---

### License

This project is for educational purposes only. Not intended for production medical use.

