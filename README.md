# HR Analytics Web Application

A comprehensive HR analytics platform powered by machine learning to optimize hiring processes.

## Features

### 🎯 Application Volume Prediction
- Predict expected job applications using ML models
- Input job parameters (title, skills, salary, etc.)
- Get categorized predictions (Low/Medium/High)
- Understand hiring difficulty

### 📊 Resume Matching & Filtering
- Upload resumes (PDF/DOCX) and job descriptions
- AI-powered matching scores (0-100%)
- Identify matched and missing skills
- Get hiring recommendations

### 📈 HR Dashboard
- View aggregated analytics
- Interactive charts and visualizations
- Track top candidates
- Monitor hiring metrics

## Technology Stack

**Backend:**
- Python 3.8+
- Flask (Web framework)
- scikit-learn (Machine Learning)
- PyPDF2 (PDF processing)
- python-docx (DOCX processing)

**Frontend:**
- HTML5
- CSS3 (Modern design with gradients and animations)
- Vanilla JavaScript
- Chart.js (Data visualization)

## Installation

1. **Install Python dependencies:**
```bash
cd "C:\Users\piyush madhukar\Downloads\colab"
pip install -r requirements.txt
```

2. **Start the Flask server:**
```bash
python app.py
```

3. **Open your browser:**
Navigate to `http://localhost:5000`

## Usage

### Predict Application Volume
1. Click "Predict Applications" from the homepage
2. Fill in job details (title, skills, salary, etc.)
3. Click "Predict Applications"
4. View predicted count and insights

### Match Resumes
1. Click "Match Resumes" from the homepage
2. Upload a resume (PDF or DOCX)
3. Enter or upload job description
4. Click "Analyze Match"
5. View matching score and skill analysis

### View Dashboard
1. Click "Dashboard" from the homepage
2. View summary statistics
3. Explore charts and candidate rankings
4. Click "Refresh Data" to update

## API Endpoints

### POST `/api/predict-applications`
Predict application volume for a job posting.

**Request Body:**
```json
{
  "jobTitle": "Senior Software Engineer",
  "skills": ["Python", "Machine Learning"],
  "experienceLevel": "Senior",
  "minSalary": 100000,
  "maxSalary": 150000,
  "jobType": "Full-time",
  "remoteOption": true,
  "companySize": "500-1000",
  "industry": "Technology"
}
```

**Response:**
```json
{
  "success": true,
  "prediction": {
    "count": 150,
    "category": "High",
    "difficulty": "Easy",
    "explanation": "..."
  }
}
```

### POST `/api/match-resume`
Match a resume to a job description.

**Request:** Multipart form data
- `resume`: PDF/DOCX file
- `jobDescriptionText`: Text (optional)
- `jobDescription`: PDF/DOCX file (optional)

**Response:**
```json
{
  "success": true,
  "result": {
    "score": 85.5,
    "category": "Excellent",
    "priority": "High",
    "matched_skills": ["Python", "Machine Learning"],
    "missing_skills": ["AWS"],
    "recommendation": "..."
  }
}
```

### GET `/api/dashboard-data`
Get aggregated dashboard statistics.

**Response:**
```json
{
  "success": true,
  "data": {
    "summary": {
      "totalJobs": 10,
      "avgPredictedApplications": 125.5,
      "totalResumes": 5,
      "topMatchScore": 92.0
    },
    "jobs": [...],
    "topCandidates": [...]
  }
}
```

## Project Structure

```
colab/
├── app.py                  # Flask backend server
├── ml_models.py            # ML model classes
├── utils.py                # Utility functions
├── requirements.txt        # Python dependencies
├── index.html              # Landing page
├── prediction.html         # Application prediction page
├── matching.html           # Resume matching page
├── dashboard.html          # Analytics dashboard
├── style.css               # Design system
└── README.md               # This file
```

## Design Features

- **Modern Dark Theme** with vibrant gradients
- **Glassmorphism** effects on cards
- **Smooth Animations** and transitions
- **Responsive Design** for all screen sizes
- **Interactive Charts** with Chart.js
- **Premium Typography** using Google Fonts (Inter, Outfit)

## Notes

- The ML models use simplified algorithms for demonstration
- For production use, train models on actual hiring data
- File uploads are limited to 5MB
- Dashboard data is stored in-memory (resets on server restart)

## Future Enhancements

- Persistent database (PostgreSQL/MongoDB)
- User authentication and authorization
- Advanced ML models with real training data
- Email notifications for top candidates
- Export reports to PDF/Excel
- Batch resume processing
- Integration with ATS systems

## License

This project is for educational and demonstration purposes.

---

**Built with ❤️ using Python, Flask, and Machine Learning**
