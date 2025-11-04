/**
 * FairMed - Main Application Component
 * =====================================
 * Entry point for the FairMed bias detection interface.
 * Manages state for scenario selection, API communication, and results display.
 *
 * @author Rafael Ribeiro
 */

import React, { useState } from 'react';
import './App.css';
import Dashboard from './components/Dashboard';
import axios from 'axios';

// Backend API endpoint - Flask server running on port 5001
const API_URL = 'http://localhost:5001/api';

/**
 * Main App component managing the entire FairMed interface
 * @returns {JSX.Element} The complete FairMed application
 */
function App() {
  // State management for application
  const [selectedScenario, setSelectedScenario] = useState('dermatology'); // Current scenario selection
  const [loading, setLoading] = useState(false); // Loading state during API calls
  const [results, setResults] = useState(null); // Original bias analysis results
  const [mitigatedResults, setMitigatedResults] = useState(null); // Results after applying mitigation
  const [showComparison, setShowComparison] = useState(false); // Toggle before/after view

  /**
   * Pre-configured medical AI scenarios demonstrating different types of bias
   * Each scenario represents a real-world bias pattern found in medical AI systems
   */
  const scenarios = [
    {
      id: 'dermatology',
      title: 'Dermatology AI',
      description: 'Melanoma detection showing bias against darker skin tones (Fitzpatrick V-VI)',
      category: 'Skin Analysis'
    },
    {
      id: 'cardiovascular',
      title: 'Cardiovascular Predictor',
      description: 'Heart disease diagnosis with gender bias - women underdiagnosed',
      category: 'Cardiac Health'
    },
    {
      id: 'pain',
      title: 'Pain Management',
      description: 'Algorithm showing age bias - elderly patients undertreated',
      category: 'Pain Assessment'
    }
  ];

  /**
   * Initiates bias analysis for the selected scenario
   * Makes POST request to /api/analyze endpoint with scenario parameters
   * @async
   */
  const handleAnalyze = async () => {
    // Reset state for new analysis
    setLoading(true);
    setResults(null);
    setMitigatedResults(null);
    setShowComparison(false);

    try {
      // Simulate processing time for realistic demo experience (1.5 seconds)
      await new Promise(resolve => setTimeout(resolve, 1500));

      // Request bias analysis from Flask backend
      const response = await axios.post(`${API_URL}/analyze`, {
        scenario: selectedScenario,
        use_sample: true // Use pre-loaded demo data
      });

      setResults(response.data);
    } catch (error) {
      console.error('Error analyzing bias:', error);
      alert('Error connecting to backend. Make sure Flask server is running on port 5001.');
    } finally {
      setLoading(false);
    }
  };

  /**
   * Applies bias mitigation techniques and retrieves improved results
   * Makes POST request to /api/mitigate endpoint
   * @async
   */
  const handleApplyMitigation = async () => {
    setLoading(true);

    try {
      // Simulate model retraining time for realistic demo (2 seconds)
      await new Promise(resolve => setTimeout(resolve, 2000));

      // Request mitigated results from Flask backend
      const response = await axios.post(`${API_URL}/mitigate`, {
        scenario: selectedScenario,
        mitigation: 'adversarial_debiasing' // Mitigation strategy
      });

      setMitigatedResults(response.data);
      setShowComparison(true); // Show before/after comparison
    } catch (error) {
      console.error('Error applying mitigation:', error);
      alert('Error applying mitigation. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="container">
        {/* Header */}
        <header className="header">
          <div className="header-content">
            <div className="logo-section">
              <div className="logo-icon">
                <svg width="50" height="50" viewBox="0 0 50 50" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <rect width="50" height="50" rx="10" fill="#2563eb"/>
                  <path d="M25 10L25 40M10 25L40 25" stroke="white" strokeWidth="4" strokeLinecap="round"/>
                  <circle cx="25" cy="25" r="8" stroke="white" strokeWidth="2" fill="none"/>
                </svg>
              </div>
              <div className="title-section">
                <h1>FairMed</h1>
                <p className="subtitle">AI Bias Detection & Mitigation Tool for Medical Diagnostics</p>
              </div>
            </div>
            <div className="header-image">
              <svg width="200" height="120" viewBox="0 0 200 120" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="20" y="20" width="35" height="80" rx="5" fill="#e0f2fe" stroke="#2563eb" strokeWidth="2"/>
                <rect x="65" y="40" width="35" height="60" rx="5" fill="#ddd6fe" stroke="#7c3aed" strokeWidth="2"/>
                <rect x="110" y="30" width="35" height="70" rx="5" fill="#dbeafe" stroke="#3b82f6" strokeWidth="2"/>
                <rect x="155" y="35" width="35" height="65" rx="5" fill="#e0e7ff" stroke="#6366f1" strokeWidth="2"/>
                <line x1="0" y1="100" x2="200" y2="100" stroke="#cbd5e1" strokeWidth="2"/>
              </svg>
            </div>
          </div>
        </header>

        {/* How It Works Section */}
        <div className="how-it-works">
          <h2>How FairMed Works</h2>
          <div className="workflow-steps">
            <div className="step">
              <div className="step-number">1</div>
              <h3>Upload & Analyze</h3>
              <p>Select a medical AI scenario and run automated bias detection using established fairness metrics</p>
            </div>
            <div className="step-arrow">→</div>
            <div className="step">
              <div className="step-number">2</div>
              <h3>Detect Disparities</h3>
              <p>Calculate statistical parity, equalized odds, and predictive parity across demographic groups</p>
            </div>
            <div className="step-arrow">→</div>
            <div className="step">
              <div className="step-number">3</div>
              <h3>Apply Mitigation</h3>
              <p>Use adversarial debiasing and data augmentation to reduce bias while maintaining accuracy</p>
            </div>
            <div className="step-arrow">→</div>
            <div className="step">
              <div className="step-number">4</div>
              <h3>Verify Results</h3>
              <p>Compare before and after metrics to ensure equitable performance across all patient groups</p>
            </div>
          </div>
        </div>

        {/* Scenario Selection */}
        <div className="scenario-selector">
          <h2>Select Medical AI Scenario</h2>
          <div className="scenario-buttons">
            {scenarios.map(scenario => (
              <button
                key={scenario.id}
                className={`scenario-btn ${selectedScenario === scenario.id ? 'active' : ''}`}
                onClick={() => {
                  setSelectedScenario(scenario.id);
                  setResults(null);
                  setMitigatedResults(null);
                  setShowComparison(false);
                }}
              >
                <div className="scenario-category">{scenario.category}</div>
                <h3>{scenario.title}</h3>
                <p>{scenario.description}</p>
              </button>
            ))}
          </div>
        </div>

        {/* Analyze Button */}
        <div className="analyze-section">
          <button
            className="analyze-btn"
            onClick={handleAnalyze}
            disabled={loading}
          >
            {loading ? 'Analyzing...' : 'Run Bias Analysis'}
          </button>
        </div>

        {/* Loading State */}
        {loading && !results && (
          <div className="loading">
            <div className="spinner"></div>
            <h3>Analyzing AI Model for Bias...</h3>
            <p>Calculating fairness metrics across demographic groups</p>
          </div>
        )}

        {/* Results Dashboard */}
        {results && !showComparison && (
          <Dashboard
            results={results}
            onApplyMitigation={handleApplyMitigation}
            loading={loading}
          />
        )}

        {/* Comparison View (Before/After) */}
        {showComparison && mitigatedResults && (
          <div className="comparison-view">
            <div className="comparison-header">
              <h2>Before & After Mitigation</h2>
              <div className="improvement-badge">
                ↑ {mitigatedResults.improvement?.bias_score_change.toFixed(1)} Point Improvement
              </div>
            </div>

            <div className="comparison-cards">
              <div className="before-after before">
                <h3>Before Mitigation</h3>
                <Dashboard results={results} compact={true} />
              </div>

              <div className="before-after after">
                <h3>After Mitigation</h3>
                <Dashboard results={mitigatedResults} compact={true} />
                <div style={{ marginTop: '20px', padding: '15px', background: 'white', borderRadius: '8px' }}>
                  <strong>Success:</strong> {mitigatedResults.improvement?.message}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
