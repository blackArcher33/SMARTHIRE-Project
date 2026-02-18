from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from ml_models import ApplicationPredictor, ResumeMatcherModel
from utils import extract_text_from_pdf, extract_text_from_docx, clean_text
import json
from datetime import datetime

app = Flask(__name__, static_folder='.')
CORS(app)

# Initialize ML models
app_predictor = ApplicationPredictor()
resume_matcher = ResumeMatcherModel()

# In-memory storage for dashboard data
dashboard_data = {
    'jobs': [],
    'resumes': [],
    'predictions': []
}

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/api/predict-applications', methods=['POST'])
def predict_applications():
    try:
        data = request.json
        
        # Extract features from request
        features = {
            'job_title': data.get('jobTitle', ''),
            'skills': data.get('skills', []),
            'experience_level': data.get('experienceLevel', 'Mid'),
            'min_salary': float(data.get('minSalary', 0)),
            'max_salary': float(data.get('maxSalary', 0)),
            'job_type': data.get('jobType', 'Full-time'),
            'remote_option': data.get('remoteOption', False),
            'company_size': data.get('companySize', '100-500'),
            'industry': data.get('industry', 'Technology')
        }
        
        # Make prediction
        prediction = app_predictor.predict(features)
        
        # Store for dashboard
        dashboard_data['jobs'].append({
            'title': features['job_title'],
            'predicted_applications': prediction['count'],
            'category': prediction['category'],
            'timestamp': datetime.now().isoformat()
        })
        
        return jsonify({
            'success': True,
            'prediction': prediction
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/match-resume', methods=['POST'])
def match_resume():
    try:
        # Handle file uploads
        resume_file = request.files.get('resume')
        jd_file = request.files.get('jobDescription')
        jd_text = request.form.get('jobDescriptionText', '')
        
        # Extract resume text
        if resume_file:
            filename = resume_file.filename.lower()
            if filename.endswith('.pdf'):
                resume_text = extract_text_from_pdf(resume_file)
            elif filename.endswith('.docx') or filename.endswith('.doc'):
                resume_text = extract_text_from_docx(resume_file)
            else:
                return jsonify({
                    'success': False,
                    'error': 'Unsupported resume format. Please upload PDF or DOC/DOCX.'
                }), 400
        else:
            return jsonify({
                'success': False,
                'error': 'Resume file is required.'
            }), 400
        
        # Extract job description text
        if jd_file:
            filename = jd_file.filename.lower()
            if filename.endswith('.pdf'):
                jd_text = extract_text_from_pdf(jd_file)
            elif filename.endswith('.docx') or filename.endswith('.doc'):
                jd_text = extract_text_from_docx(jd_file)
        
        if not jd_text:
            return jsonify({
                'success': False,
                'error': 'Job description is required.'
            }), 400
        
        # Clean texts
        resume_text = clean_text(resume_text)
        jd_text = clean_text(jd_text)
        
        # Perform matching
        match_result = resume_matcher.match(resume_text, jd_text)
        
        # Store for dashboard
        dashboard_data['resumes'].append({
            'score': match_result['score'],
            'category': match_result['category'],
            'matched_skills': match_result['matched_skills'],
            'timestamp': datetime.now().isoformat()
        })
        
        return jsonify({
            'success': True,
            'result': match_result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/dashboard-data', methods=['GET'])
def get_dashboard_data():
    try:
        # Calculate summary statistics
        total_jobs = len(dashboard_data['jobs'])
        total_resumes = len(dashboard_data['resumes'])
        
        avg_applications = 0
        if dashboard_data['jobs']:
            avg_applications = sum(j['predicted_applications'] for j in dashboard_data['jobs']) / total_jobs
        
        top_match_score = 0
        if dashboard_data['resumes']:
            top_match_score = max(r['score'] for r in dashboard_data['resumes'])
        
        # Get top candidates
        top_candidates = sorted(
            dashboard_data['resumes'],
            key=lambda x: x['score'],
            reverse=True
        )[:10]
        
        return jsonify({
            'success': True,
            'data': {
                'summary': {
                    'totalJobs': total_jobs,
                    'avgPredictedApplications': round(avg_applications, 1),
                    'totalResumes': total_resumes,
                    'topMatchScore': round(top_match_score, 1)
                },
                'jobs': dashboard_data['jobs'][-20:],  # Last 20 jobs
                'topCandidates': top_candidates
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    print("Starting HR Analytics Server...")
    print("Server running at http://localhost:5000")
    print("Open your browser and navigate to http://localhost:5000")
    app.run(debug=True, port=5000)
