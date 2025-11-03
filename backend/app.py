from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Note: For demo purposes, we use pre-calculated metrics instead of live calculation
# This function would be used for real model analysis with uploaded data
# def calculate_fairness_metrics(y_true, y_pred, sensitive_features):
#     """Calculate comprehensive fairness metrics across demographic groups."""
#     # Implementation would go here for production version
#     pass


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'FairMed API is running'})


@app.route('/api/analyze', methods=['POST'])
def analyze_bias():
    """
    Analyze bias in uploaded model and dataset.
    Expects JSON with:
    - scenario: 'dermatology', 'cardiovascular', or 'pain'
    - use_sample: boolean (whether to use pre-loaded sample data)
    """
    try:
        data = request.get_json()
        scenario = data.get('scenario', 'dermatology')
        use_sample = data.get('use_sample', True)

        if use_sample:
            # Load pre-loaded sample scenario
            if scenario == 'dermatology':
                results = load_dermatology_scenario()
            elif scenario == 'cardiovascular':
                results = load_cardiovascular_scenario()
            elif scenario == 'pain':
                results = load_pain_scenario()
            else:
                return jsonify({'error': 'Invalid scenario'}), 400

            return jsonify(results)
        else:
            return jsonify({'error': 'File upload not yet implemented'}), 501

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def load_dermatology_scenario():
    """
    Load pre-calculated dermatology AI bias scenario.
    Shows bias against darker skin tones (Fitzpatrick V-VI).
    """
    # Simulated results for demo
    return {
        'scenario': 'dermatology',
        'title': 'Melanoma Detection AI - Skin Tone Bias',
        'description': 'AI model trained primarily on light skin (Fitzpatrick I-III) showing significant accuracy disparities',
        'overall_score': 45.2,  # Low score indicates bias
        'groups': {
            'Light Skin (I-III)': {
                'group': 'Light Skin (I-III)',
                'sample_size': 700,
                'accuracy': 0.90,
                'tpr': 0.92,
                'fpr': 0.08,
                'precision': 0.89,
                'confusion_matrix': {
                    'tn': 322,
                    'fp': 28,
                    'fn': 24,
                    'tp': 326
                }
            },
            'Medium Skin (IV)': {
                'group': 'Medium Skin (IV)',
                'sample_size': 200,
                'accuracy': 0.76,
                'tpr': 0.78,
                'fpr': 0.24,
                'precision': 0.74,
                'confusion_matrix': {
                    'tn': 76,
                    'fp': 24,
                    'fn': 22,
                    'tp': 78
                }
            },
            'Dark Skin (V-VI)': {
                'group': 'Dark Skin (V-VI)',
                'sample_size': 100,
                'accuracy': 0.60,
                'tpr': 0.62,
                'fpr': 0.38,
                'precision': 0.58,
                'confusion_matrix': {
                    'tn': 31,
                    'fp': 19,
                    'fn': 19,
                    'tp': 31
                }
            }
        },
        'metrics': {
            'statistical_parity': 0.30,  # 30% accuracy disparity
            'equalized_odds_tpr': 0.30,  # 30% TPR disparity
            'equalized_odds_fpr': 0.30,  # 30% FPR disparity
            'predictive_parity': 0.31   # 31% precision disparity
        },
        'flags': [
            {
                'type': 'accuracy_disparity',
                'severity': 'high',
                'message': 'Accuracy varies by 30.0% across skin tones (threshold: 5%)',
                'value': 0.30
            },
            {
                'type': 'tpr_disparity',
                'severity': 'high',
                'message': 'True Positive Rate varies by 30.0% across skin tones',
                'value': 0.30
            },
            {
                'type': 'precision_disparity',
                'severity': 'high',
                'message': 'Precision varies by 31.0% across skin tones',
                'value': 0.31
            }
        ],
        'recommendations': [
            {
                'priority': 'high',
                'title': 'Augment Training Data',
                'description': 'Add synthetic images of melanoma on darker skin tones (Fitzpatrick V-VI)',
                'expected_improvement': 35,
                'implementation_cost': '€15,000',
                'timeline': '2-3 weeks'
            },
            {
                'priority': 'high',
                'title': 'Apply Adversarial Debiasing',
                'description': 'Retrain model with dual objectives: accuracy + fairness across skin tones',
                'expected_improvement': 40,
                'implementation_cost': '€8,000',
                'timeline': '1-2 weeks'
            },
            {
                'priority': 'medium',
                'title': 'Adjust Decision Thresholds',
                'description': 'Use group-specific thresholds to equalize sensitivity across skin tones',
                'expected_improvement': 25,
                'implementation_cost': '€2,000',
                'timeline': '3-5 days'
            }
        ],
        'mitigated_results': None  # Will be populated after applying fix
    }


def load_cardiovascular_scenario():
    """Cardiovascular disease predictor showing gender bias"""
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
    """Pain management algorithm showing age bias"""
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
    Simulate applying bias mitigation and return improved results.
    """
    try:
        data = request.get_json()
        scenario = data.get('scenario', 'dermatology')

        if scenario == 'dermatology':
            return jsonify(get_mitigated_dermatology_results())
        elif scenario == 'cardiovascular':
            return jsonify(get_mitigated_cardiovascular_results())
        elif scenario == 'pain':
            return jsonify(get_mitigated_pain_results())
        else:
            return jsonify({'error': 'Invalid scenario'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def get_mitigated_dermatology_results():
    """Dermatology results after applying adversarial debiasing"""
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
    """Cardiovascular results after balancing dataset"""
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
    """Pain management results after removing age feature"""
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
    print("=" * 60)
    print("FairMed API Server Starting...")
    print("=" * 60)
    print("🏥 AI Bias Detection Tool for Medical Diagnostics")
    print("📍 Server: http://localhost:5001")
    print("💚 Health Check: http://localhost:5001/api/health")
    print("=" * 60)
    print("⚠️  Note: Using port 5001 (port 5000 is used by macOS AirPlay)")
    print("=" * 60)
    app.run(debug=True, port=5001)
