"""
FairMed API Server
==================
Flask REST API for medical AI bias detection and mitigation.

This prototype demonstrates bias analysis across three medical scenarios:
- Dermatology: Skin tone bias in melanoma detection
- Cardiovascular: Gender bias in heart disease prediction
- Pain Management: Age bias in pain assessment

Author: Rafael Ribeiro
Academic Project: AI Bias in Healthcare
"""

from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize Flask application
app = Flask(__name__)
# Enable CORS to allow frontend (React) to communicate with backend
CORS(app)


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify API is running
    Returns: JSON with status and message
    """
    return jsonify({'status': 'healthy', 'message': 'FairMed API is running'})


@app.route('/api/analyze', methods=['POST'])
def analyze_bias():
    """
    Analyze bias in medical AI model across demographic groups.

    Request Body (JSON):
        - scenario (str): One of 'dermatology', 'cardiovascular', or 'pain'
        - use_sample (bool): Whether to use pre-loaded demo data (default: True)

    Returns:
        JSON object containing:
        - overall_score: Fairness score (0-100, higher is better)
        - groups: Performance metrics per demographic group
        - metrics: Fairness metrics (statistical parity, equalized odds)
        - flags: List of detected bias warnings
        - recommendations: Suggested mitigation strategies

    HTTP Status Codes:
        200: Success
        400: Invalid scenario parameter
        501: File upload feature not implemented
        500: Server error
    """
    try:
        data = request.get_json()
        scenario = data.get('scenario', 'dermatology')
        use_sample = data.get('use_sample', True)

        if use_sample:
            # Load pre-calculated sample scenario data
            # Uses O(1) dictionary lookup for scenario selection
            scenario_loaders = {
                'dermatology': load_dermatology_scenario,
                'cardiovascular': load_cardiovascular_scenario,
                'pain': load_pain_scenario
            }

            if scenario in scenario_loaders:
                results = scenario_loaders[scenario]()
                return jsonify(results)
            else:
                return jsonify({'error': 'Invalid scenario'}), 400
        else:
            # Feature reserved for production implementation with actual model uploads
            return jsonify({'error': 'File upload not yet implemented'}), 501

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def load_dermatology_scenario():
    """
    Load pre-calculated dermatology AI bias scenario.

    Demonstrates real-world bias in melanoma detection AI systems.
    Problem: Training data predominantly features lighter skin tones (Fitzpatrick I-III),
    causing significantly worse performance on darker skin (Fitzpatrick V-VI).

    Returns:
        dict: Complete bias analysis with performance metrics, fairness metrics,
              bias flags, and mitigation recommendations

    Data Structure:
        - overall_score: 45.2/100 (indicates significant bias)
        - groups: Performance breakdown by Fitzpatrick skin tone scale
        - metrics: Fairness measurements (lower is better, 0 = perfectly fair)
        - flags: Detected bias violations exceeding 5% threshold
        - recommendations: Evidence-based mitigation strategies with costs
    """
    return {
        'scenario': 'dermatology',
        'title': 'Melanoma Detection AI - Skin Tone Bias',
        'description': 'AI model trained primarily on light skin (Fitzpatrick I-III) showing significant accuracy disparities',
        'overall_score': 45.2,  # Low score indicates significant bias (scale: 0-100)

        # Performance metrics segmented by skin tone (Fitzpatrick scale)
        'groups': {
            'Light Skin (I-III)': {
                'group': 'Light Skin (I-III)',
                'sample_size': 700,  # Largest sample, most training data representation
                'accuracy': 0.90,    # 90% correct predictions
                'tpr': 0.92,         # True Positive Rate (sensitivity)
                'fpr': 0.08,         # False Positive Rate (1 - specificity)
                'precision': 0.89,   # Positive Predictive Value
                'confusion_matrix': {
                    'tn': 322,  # True Negatives (correctly identified non-melanoma)
                    'fp': 28,   # False Positives (false alarms)
                    'fn': 24,   # False Negatives (missed melanomas - dangerous!)
                    'tp': 326   # True Positives (correctly detected melanomas)
                }
            },
            'Medium Skin (IV)': {
                'group': 'Medium Skin (IV)',
                'sample_size': 200,  # Moderate representation
                'accuracy': 0.76,    # 14% worse than light skin
                'tpr': 0.78,         # Lower sensitivity - more missed melanomas
                'fpr': 0.24,         # Higher false alarm rate
                'precision': 0.74,   # Lower confidence in positive predictions
                'confusion_matrix': {
                    'tn': 76,
                    'fp': 24,
                    'fn': 22,   # More missed melanomas than light skin
                    'tp': 78
                }
            },
            'Dark Skin (V-VI)': {
                'group': 'Dark Skin (V-VI)',
                'sample_size': 100,  # Smallest sample - underrepresentation
                'accuracy': 0.60,    # 30% worse than light skin - severe bias
                'tpr': 0.62,         # Only 62% sensitivity - misses 38% of melanomas
                'fpr': 0.38,         # Very high false positive rate
                'precision': 0.58,   # Low confidence in predictions
                'confusion_matrix': {
                    'tn': 31,
                    'fp': 19,
                    'fn': 19,   # Nearly 40% of melanomas missed - life-threatening
                    'tp': 31
                }
            }
        },

        # Fairness metrics quantifying disparity (0 = perfect fairness)
        'metrics': {
            'statistical_parity': 0.30,    # 30% accuracy disparity between groups
            'equalized_odds_tpr': 0.30,    # 30% difference in true positive rates
            'equalized_odds_fpr': 0.30,    # 30% difference in false positive rates
            'predictive_parity': 0.31      # 31% difference in precision
        },
        # Bias warnings flagged by system (exceeding 5% threshold)
        'flags': [
            {
                'type': 'accuracy_disparity',
                'severity': 'high',
                'message': 'Accuracy varies by 30.0% across skin tones (threshold: 5%)',
                'value': 0.30  # 6x above acceptable threshold
            },
            {
                'type': 'tpr_disparity',
                'severity': 'high',
                'message': 'True Positive Rate varies by 30.0% across skin tones',
                'value': 0.30  # Critical: darker skin patients have melanomas missed
            },
            {
                'type': 'precision_disparity',
                'severity': 'high',
                'message': 'Precision varies by 31.0% across skin tones',
                'value': 0.31  # Lower confidence in predictions for darker skin
            }
        ],

        # Evidence-based mitigation strategies (sorted by priority)
        'recommendations': [
            {
                'priority': 'high',
                'title': 'Augment Training Data',
                'description': 'Add synthetic images of melanoma on darker skin tones (Fitzpatrick V-VI)',
                'expected_improvement': 35,  # % improvement in fairness score
                'implementation_cost': '€15,000',  # Realistic cost estimate
                'timeline': '2-3 weeks'
            },
            {
                'priority': 'high',
                'title': 'Apply Adversarial Debiasing',
                'description': 'Retrain model with dual objectives: accuracy + fairness across skin tones',
                'expected_improvement': 40,  # Highest expected improvement
                'implementation_cost': '€8,000',
                'timeline': '1-2 weeks'
            },
            {
                'priority': 'medium',
                'title': 'Adjust Decision Thresholds',
                'description': 'Use group-specific thresholds to equalize sensitivity across skin tones',
                'expected_improvement': 25,  # Quick fix but lower improvement
                'implementation_cost': '€2,000',  # Lowest cost option
                'timeline': '3-5 days'
            }
        ],

        'mitigated_results': None  # Populated after /api/mitigate endpoint call
    }


def load_cardiovascular_scenario():
    """
    Load cardiovascular disease prediction scenario with gender bias.

    Demonstrates gender bias in heart disease AI diagnostics.
    Problem: Training data contains fewer female patients, and symptoms
    present differently in women (atypical presentations often missed).

    Real-world Impact: Women are 50% more likely to receive incorrect
    initial heart attack diagnosis, leading to delayed treatment.

    Returns:
        dict: Bias analysis showing 13% gender disparity in accuracy
    """
    return {
        'scenario': 'cardiovascular',
        'title': 'Cardiovascular Disease Predictor - Gender Bias',
        'description': 'AI model undertrained on female patients, leading to underdiagnosis',
        'overall_score': 62.0,
        'groups': {
            'Male': {
                'group': 'Male',
                'sample_size': 700,
                'accuracy': 0.85,
                'tpr': 0.87,
                'fpr': 0.13,
                'precision': 0.84,
                'confusion_matrix': {'tn': 305, 'fp': 45, 'fn': 45, 'tp': 305}
            },
            'Female': {
                'group': 'Female',
                'sample_size': 300,
                'accuracy': 0.72,
                'tpr': 0.70,
                'fpr': 0.28,
                'precision': 0.68,
                'confusion_matrix': {'tn': 108, 'fp': 42, 'fn': 42, 'tp': 108}
            }
        },
        'metrics': {
            'statistical_parity': 0.13,
            'equalized_odds_tpr': 0.17,
            'equalized_odds_fpr': 0.15,
            'predictive_parity': 0.16
        },
        'flags': [
            {
                'type': 'accuracy_disparity',
                'severity': 'high',
                'message': 'Accuracy varies by 13.0% between genders (threshold: 5%)',
                'value': 0.13
            }
        ],
        'recommendations': [
            {
                'priority': 'high',
                'title': 'Balance Training Dataset',
                'description': 'Increase female patient representation to 50%',
                'expected_improvement': 30,
                'implementation_cost': '€12,000',
                'timeline': '3-4 weeks'
            }
        ],
        'mitigated_results': None
    }


def load_pain_scenario():
    """
    Load pain management scenario with age bias.

    Demonstrates age discrimination in pain assessment algorithms.
    Problem: AI uses age as a proxy for pain tolerance, systematically
    underestimating pain in elderly patients (65+).

    Real-world Impact: Elderly patients receive inadequate pain management,
    leading to unnecessary suffering and complications.

    Returns:
        dict: Bias analysis showing 14% disparity across age groups
    """
    return {
        'scenario': 'pain',
        'title': 'Pain Management Algorithm - Age Bias',
        'description': 'AI uses age as proxy for pain tolerance, undertreating elderly patients',
        'overall_score': 58.5,
        'groups': {
            'Age 18-40': {
                'group': 'Age 18-40',
                'sample_size': 400,
                'accuracy': 0.82,
                'tpr': 0.84,
                'fpr': 0.16,
                'precision': 0.81,
                'confusion_matrix': {'tn': 168, 'fp': 32, 'fn': 32, 'tp': 168}
            },
            'Age 41-64': {
                'group': 'Age 41-64',
                'sample_size': 350,
                'accuracy': 0.78,
                'tpr': 0.76,
                'fpr': 0.22,
                'precision': 0.74,
                'confusion_matrix': {'tn': 137, 'fp': 38, 'fn': 42, 'tp': 133}
            },
            'Age 65+': {
                'group': 'Age 65+',
                'sample_size': 250,
                'accuracy': 0.68,
                'tpr': 0.65,
                'fpr': 0.32,
                'precision': 0.67,
                'confusion_matrix': {'tn': 85, 'fp': 40, 'fn': 44, 'tp': 81}
            }
        },
        'metrics': {
            'statistical_parity': 0.14,
            'equalized_odds_tpr': 0.19,
            'equalized_odds_fpr': 0.16,
            'predictive_parity': 0.14
        },
        'flags': [
            {
                'type': 'accuracy_disparity',
                'severity': 'high',
                'message': 'Accuracy varies by 14.0% across age groups (threshold: 5%)',
                'value': 0.14
            }
        ],
        'recommendations': [
            {
                'priority': 'high',
                'title': 'Remove Age as Direct Feature',
                'description': 'Eliminate age-based assumptions about pain tolerance',
                'expected_improvement': 35,
                'implementation_cost': '€5,000',
                'timeline': '1-2 weeks'
            }
        ],
        'mitigated_results': None
    }


@app.route('/api/mitigate', methods=['POST'])
def apply_mitigation():
    """
    Apply bias mitigation and return improved results.

    Simulates applying recommended mitigation strategies (adversarial debiasing,
    data augmentation, threshold adjustment) and returns post-mitigation metrics.

    Request Body (JSON):
        - scenario (str): Scenario to apply mitigation to
        - mitigation (str): Mitigation strategy (currently uses adversarial debiasing)

    Returns:
        JSON object with improved metrics and comparison data

    HTTP Status Codes:
        200: Success
        400: Invalid scenario
        500: Server error
    """
    try:
        data = request.get_json()
        scenario = data.get('scenario', 'dermatology')

        # O(1) lookup for mitigation result functions
        mitigation_results = {
            'dermatology': get_mitigated_dermatology_results,
            'cardiovascular': get_mitigated_cardiovascular_results,
            'pain': get_mitigated_pain_results
        }

        if scenario in mitigation_results:
            return jsonify(mitigation_results[scenario]())
        else:
            return jsonify({'error': 'Invalid scenario'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def get_mitigated_dermatology_results():
    """
    Return dermatology results after applying adversarial debiasing.

    Mitigation Applied: Adversarial debiasing + data augmentation
    - Added 500 synthetic melanoma images for darker skin tones
    - Retrained with dual loss function (accuracy + fairness)
    - Result: Bias reduced by 90%, disparity drops from 30% to 3%

    Returns:
        dict: Post-mitigation metrics showing improved fairness
    """
    return {
        'scenario': 'dermatology',
        'title': 'Melanoma Detection AI - After Mitigation',
        'description': 'After applying adversarial debiasing and data augmentation',
        'overall_score': 87.3,  # Much improved
        'groups': {
            'Light Skin (I-III)': {
                'group': 'Light Skin (I-III)',
                'sample_size': 700,
                'accuracy': 0.87,
                'tpr': 0.88,
                'fpr': 0.12,
                'precision': 0.86,
                'confusion_matrix': {'tn': 308, 'fp': 42, 'fn': 42, 'tp': 308}
            },
            'Medium Skin (IV)': {
                'group': 'Medium Skin (IV)',
                'sample_size': 200,
                'accuracy': 0.85,
                'tpr': 0.86,
                'fpr': 0.14,
                'precision': 0.84,
                'confusion_matrix': {'tn': 86, 'fp': 14, 'fn': 14, 'tp': 86}
            },
            'Dark Skin (V-VI)': {
                'group': 'Dark Skin (V-VI)',
                'sample_size': 100,
                'accuracy': 0.84,
                'tpr': 0.85,
                'fpr': 0.15,
                'precision': 0.83,
                'confusion_matrix': {'tn': 43, 'fp': 7, 'fn': 8, 'tp': 42}
            }
        },
        'metrics': {
            'statistical_parity': 0.03,  # Down from 30%!
            'equalized_odds_tpr': 0.03,
            'equalized_odds_fpr': 0.03,
            'predictive_parity': 0.03
        },
        'flags': [],  # No flags - within threshold!
        'improvement': {
            'bias_score_change': 42.1,
            'accuracy_disparity_reduction': 0.27,
            'message': 'Bias reduced by 90% - now within acceptable thresholds'
        }
    }


def get_mitigated_cardiovascular_results():
    """
    Return cardiovascular results after dataset balancing.

    Mitigation Applied: Dataset balancing + retraining
    - Increased female patient representation to 50%
    - Added atypical symptom features for women
    - Result: Gender disparity reduced from 13% to 2%

    Returns:
        dict: Post-mitigation metrics with equitable performance
    """
    return {
        'scenario': 'cardiovascular',
        'title': 'Cardiovascular Disease Predictor - After Mitigation',
        'overall_score': 92.0,
        'groups': {
            'Male': {
                'group': 'Male',
                'sample_size': 700,
                'accuracy': 0.83,
                'tpr': 0.84,
                'fpr': 0.16,
                'precision': 0.82,
                'confusion_matrix': {'tn': 294, 'fp': 56, 'fn': 56, 'tp': 294}
            },
            'Female': {
                'group': 'Female',
                'sample_size': 300,
                'accuracy': 0.81,
                'tpr': 0.82,
                'fpr': 0.18,
                'precision': 0.80,
                'confusion_matrix': {'tn': 123, 'fp': 27, 'fn': 27, 'tp': 123}
            }
        },
        'metrics': {
            'statistical_parity': 0.02,
            'equalized_odds_tpr': 0.02,
            'equalized_odds_fpr': 0.02,
            'predictive_parity': 0.02
        },
        'flags': [],
        'improvement': {
            'bias_score_change': 30.0,
            'accuracy_disparity_reduction': 0.11,
            'message': 'Gender bias eliminated - equitable performance achieved'
        }
    }


def get_mitigated_pain_results():
    """
    Return pain assessment results after removing age bias.

    Mitigation Applied: Feature engineering + retraining
    - Removed age as direct feature from model
    - Added objective pain indicators (vital signs, patient self-report)
    - Result: Age disparity reduced from 14% to 2%

    Returns:
        dict: Post-mitigation metrics with fair pain assessment
    """
    return {
        'scenario': 'pain',
        'title': 'Pain Management Algorithm - After Mitigation',
        'overall_score': 88.7,
        'groups': {
            'Age 18-40': {
                'group': 'Age 18-40',
                'sample_size': 400,
                'accuracy': 0.80,
                'tpr': 0.81,
                'fpr': 0.19,
                'precision': 0.79,
                'confusion_matrix': {'tn': 162, 'fp': 38, 'fn': 38, 'tp': 162}
            },
            'Age 41-64': {
                'group': 'Age 41-64',
                'sample_size': 350,
                'accuracy': 0.79,
                'tpr': 0.80,
                'fpr': 0.20,
                'precision': 0.78,
                'confusion_matrix': {'tn': 140, 'fp': 35, 'fn': 35, 'tp': 140}
            },
            'Age 65+': {
                'group': 'Age 65+',
                'sample_size': 250,
                'accuracy': 0.78,
                'tpr': 0.79,
                'fpr': 0.21,
                'precision': 0.77,
                'confusion_matrix': {'tn': 99, 'fp': 26, 'fn': 26, 'tp': 99}
            }
        },
        'metrics': {
            'statistical_parity': 0.02,
            'equalized_odds_tpr': 0.02,
            'equalized_odds_fpr': 0.02,
            'predictive_parity': 0.02
        },
        'flags': [],
        'improvement': {
            'bias_score_change': 30.2,
            'accuracy_disparity_reduction': 0.12,
            'message': 'Age bias eliminated - fair pain assessment across all ages'
        }
    }


if __name__ == '__main__':
    # Startup banner for development debugging
    print("=" * 60)
    print("FairMed API Server Starting...")
    print("=" * 60)
    print("AI Bias Detection Tool for Medical Diagnostics")
    print("Server: http://localhost:5001")
    print("Health Check: http://localhost:5001/api/health")
    print("=" * 60)
    print("Note: Using port 5001 to avoid conflicts with other services.")
    print("=" * 60)

    # Run Flask development server
    # WARNING: debug=True should be disabled in production for security
    app.run(debug=True, port=5001)
