import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement
} from 'chart.js';
import { Bar, Doughnut } from 'react-chartjs-2';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement
);

const Dashboard = ({ results, onApplyMitigation, loading, compact = false }) => {
  if (!results) return null;

  const getScoreColor = (score) => {
    if (score >= 80) return '#16a34a';
    if (score >= 60) return '#f59e0b';
    return '#dc2626';
  };

  const getScoreStatus = (score) => {
    if (score >= 80) return { label: 'Fair', className: 'fair' };
    if (score >= 60) return { label: 'Borderline', className: 'borderline' };
    return { label: 'Biased', className: 'biased' };
  };

  const getMetricBadge = (value) => {
    if (value >= 0.80) return 'good';
    if (value >= 0.65) return 'medium';
    return 'poor';
  };

  // Prepare data for group comparison chart
  const groupNames = Object.keys(results.groups);
  const accuracies = groupNames.map(g => results.groups[g].accuracy * 100);
  const tprs = groupNames.map(g => results.groups[g].tpr * 100);
  const precisions = groupNames.map(g => results.groups[g].precision * 100);

  const barChartData = {
    labels: groupNames,
    datasets: [
      {
        label: 'Accuracy %',
        data: accuracies,
        backgroundColor: 'rgba(37, 99, 235, 0.7)',
        borderColor: 'rgba(37, 99, 235, 1)',
        borderWidth: 2
      },
      {
        label: 'True Positive Rate %',
        data: tprs,
        backgroundColor: 'rgba(16, 185, 129, 0.7)',
        borderColor: 'rgba(16, 185, 129, 1)',
        borderWidth: 2
      },
      {
        label: 'Precision %',
        data: precisions,
        backgroundColor: 'rgba(245, 158, 11, 0.7)',
        borderColor: 'rgba(245, 158, 11, 1)',
        borderWidth: 2
      }
    ]
  };

  const barChartOptions = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Performance Metrics by Demographic Group',
        font: {
          size: 16,
          weight: 'bold'
        }
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            return `${context.dataset.label}: ${context.parsed.y.toFixed(1)}%`;
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        ticks: {
          callback: function(value) {
            return value + '%';
          }
        }
      }
    }
  };

  // Bias score doughnut chart
  const scoreStatus = getScoreStatus(results.overall_score);
  const doughnutData = {
    labels: ['Bias Score', 'Remaining'],
    datasets: [
      {
        data: [results.overall_score, 100 - results.overall_score],
        backgroundColor: [
          getScoreColor(results.overall_score),
          '#e2e8f0'
        ],
        borderWidth: 0
      }
    ]
  };

  const doughnutOptions = {
    responsive: true,
    maintainAspectRatio: true,
    cutout: '70%',
    plugins: {
      legend: {
        display: false
      },
      tooltip: {
        enabled: false
      }
    }
  };

  return (
    <div className="dashboard">
      {/* Bias Score Card */}
      <div className="bias-score-card">
        <h2>{results.title}</h2>
        <p style={{ color: '#64748b', marginTop: '10px' }}>{results.description}</p>

        <div className="score-circle">
          <Doughnut data={doughnutData} options={doughnutOptions} />
          <div style={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            textAlign: 'center'
          }}>
            <div className={`score-value ${scoreStatus.className}`}>
              {results.overall_score.toFixed(0)}
            </div>
            <div style={{ color: '#64748b', fontSize: '0.9rem' }}>/ 100</div>
          </div>
        </div>

        <div className="score-label">Overall Fairness Score</div>
        <div className={`score-status ${scoreStatus.className}`}>
          {scoreStatus.label}
        </div>

        {results.improvement && (
          <div className="improvement-badge" style={{ marginTop: '15px' }}>
            ↑ +{results.improvement.bias_score_change.toFixed(1)} points
          </div>
        )}
      </div>

      {/* Flags Section */}
      {results.flags && results.flags.length > 0 && (
        <div className="flags-section">
          <h2>Bias Warnings</h2>
          {results.flags.map((flag, index) => (
            <div key={index} className={`flag-item ${flag.severity}`}>
              <strong>{flag.type.replace(/_/g, ' ').toUpperCase()}</strong>
              <p>{flag.message}</p>
            </div>
          ))}
        </div>
      )}

      {results.flags && results.flags.length === 0 && (
        <div className="flags-section" style={{ background: '#dcfce7', border: '2px solid #bbf7d0' }}>
          <h2>No Bias Detected</h2>
          <p style={{ color: '#16a34a', marginTop: '10px' }}>
            All fairness metrics are within acceptable thresholds. This model performs equitably across all demographic groups.
          </p>
        </div>
      )}

      {/* Group Comparison Chart */}
      {!compact && (
        <div className="groups-comparison">
          <h2>Performance Comparison Across Groups</h2>
          <div className="chart-container">
            <Bar data={barChartData} options={barChartOptions} />
          </div>
        </div>
      )}

      {/* Detailed Metrics Table */}
      <div className="groups-comparison">
        <h2>Detailed Metrics by Group</h2>
        <table className="groups-table">
          <thead>
            <tr>
              <th>Group</th>
              <th>Sample Size</th>
              <th>Accuracy</th>
              <th>True Positive Rate</th>
              <th>Precision</th>
            </tr>
          </thead>
          <tbody>
            {groupNames.map(groupName => {
              const group = results.groups[groupName];
              return (
                <tr key={groupName}>
                  <td><strong>{groupName}</strong></td>
                  <td>{group.sample_size}</td>
                  <td>
                    <span className={`metric-badge ${getMetricBadge(group.accuracy)}`}>
                      {(group.accuracy * 100).toFixed(1)}%
                    </span>
                  </td>
                  <td>
                    <span className={`metric-badge ${getMetricBadge(group.tpr)}`}>
                      {(group.tpr * 100).toFixed(1)}%
                    </span>
                  </td>
                  <td>
                    <span className={`metric-badge ${getMetricBadge(group.precision)}`}>
                      {(group.precision * 100).toFixed(1)}%
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Recommendations */}
      {results.recommendations && results.recommendations.length > 0 && !compact && (
        <div className="recommendations">
          <h2>Recommended Mitigation Strategies</h2>
          {results.recommendations.map((rec, index) => (
            <div key={index} className="recommendation-card">
              <div className="rec-header">
                <h3>{rec.title}</h3>
                <span className={`priority-badge ${rec.priority}`}>
                  {rec.priority.toUpperCase()} PRIORITY
                </span>
              </div>
              <p className="rec-description">{rec.description}</p>
              <div className="rec-metrics">
                <div className="rec-metric">
                  <div className="rec-metric-value">+{rec.expected_improvement}%</div>
                  <div className="rec-metric-label">Expected Improvement</div>
                </div>
                <div className="rec-metric">
                  <div className="rec-metric-value">{rec.implementation_cost}</div>
                  <div className="rec-metric-label">Implementation Cost</div>
                </div>
                <div className="rec-metric">
                  <div className="rec-metric-value">{rec.timeline}</div>
                  <div className="rec-metric-label">Timeline</div>
                </div>
              </div>
              {index === 0 && onApplyMitigation && (
                <button
                  className="apply-btn"
                  onClick={onApplyMitigation}
                  disabled={loading}
                >
                  {loading ? 'Applying Mitigation...' : 'Apply This Fix (Demo)'}
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Dashboard;
