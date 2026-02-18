import random
import re

# Note: Numpy, Pandas, and Scikit-learn removed to prevent MemoryError on this environment.
# Using pure Python implementation instead.

class ApplicationPredictor:
    """
    Predicts the number of applications for a job posting.
    Uses a simplified model based on job characteristics.
    """
    
    def __init__(self):
        # Feature weights based on typical hiring patterns
        self.base_applications = 100
        
        self.experience_multipliers = {
            'Entry': 1.5,
            'Mid': 1.0,
            'Senior': 0.7
        }
        
        self.job_type_multipliers = {
            'Full-time': 1.2,
            'Part-time': 0.8,
            'Contract': 0.9
        }
        
        self.company_size_multipliers = {
            '1-10': 0.6,
            '11-50': 0.8,
            '51-200': 1.0,
            '201-500': 1.2,
            '501-1000': 1.3,
            '1001-5000': 1.4,
            '5000+': 1.5
        }
        
    def predict(self, features):
        """
        Predict application volume based on job features.
        
        Args:
            features (dict): Job characteristics
            
        Returns:
            dict: Prediction with count and category
        """
        # Start with base
        predicted_count = self.base_applications
        
        # Apply experience level multiplier
        exp_level = features.get('experience_level', 'Mid')
        predicted_count *= self.experience_multipliers.get(exp_level, 1.0)
        
        # Apply job type multiplier
        job_type = features.get('job_type', 'Full-time')
        predicted_count *= self.job_type_multipliers.get(job_type, 1.0)
        
        # Apply company size multiplier
        company_size = features.get('company_size', '100-500')
        predicted_count *= self.company_size_multipliers.get(company_size, 1.0)
        
        # Remote option boost
        if features.get('remote_option', False):
            predicted_count *= 1.3
        
        # Salary attractiveness
        max_salary = features.get('max_salary', 0)
        if max_salary > 150000:
            predicted_count *= 1.2
        elif max_salary > 100000:
            predicted_count *= 1.1
        elif max_salary < 50000:
            predicted_count *= 0.8
        
        # Skills count factor
        skills = features.get('skills', [])
        if len(skills) > 5:
            predicted_count *= 0.9  # Too many requirements
        elif len(skills) < 2:
            predicted_count *= 1.1  # Fewer barriers
        
        # Add some randomness for realism (using random instead of numpy)
        predicted_count *= random.uniform(0.9, 1.1)
        
        # Round to integer
        predicted_count = int(round(predicted_count))
        
        # Categorize
        if predicted_count < 100:
            category = 'Low'
            difficulty = 'Hard'
        elif predicted_count < 200:
            category = 'Medium'
            difficulty = 'Medium'
        else:
            category = 'High'
            difficulty = 'Easy'
        
        return {
            'count': predicted_count,
            'category': category,
            'difficulty': difficulty,
            'explanation': self._generate_explanation(predicted_count, category, features)
        }
    
    def _generate_explanation(self, count, category, features):
        """Generate human-readable explanation."""
        exp_level = features.get('experience_level', 'Mid')
        remote = features.get('remote_option', False)
        
        explanations = {
            'Low': f"This position may receive fewer applications due to specific requirements. Consider broadening criteria or increasing visibility.",
            'Medium': f"Expected moderate interest. This is typical for {exp_level}-level positions in this industry.",
            'High': f"High application volume expected! {'Remote work option' if remote else 'Competitive salary'} makes this position attractive."
        }
        
        return explanations.get(category, "Application volume prediction based on job characteristics.")


class ResumeMatcherModel:
    """
    Matches resumes to job descriptions using simple keyword matching suitable for low-memory environments.
    """
    
    def __init__(self):
        # Common tech skills for extraction
        self.common_skills = [
            'python', 'java', 'javascript', 'c++', 'sql', 'html', 'css',
            'react', 'angular', 'vue', 'node', 'django', 'flask', 'spring',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'git',
            'machine learning', 'deep learning', 'nlp', 'computer vision',
            'data analysis', 'statistics', 'excel', 'tableau', 'power bi',
            'agile', 'scrum', 'project management', 'leadership',
            'communication', 'teamwork', 'problem solving'
        ]
    
    def match(self, resume_text, jd_text):
        """
        Calculate match score between resume and job description.
        
        Args:
            resume_text (str): Resume content
            jd_text (str): Job description content
            
        Returns:
            dict: Match results with score, category, and skills
        """
        # Use simple keyword matching
        score = self._simple_match(resume_text, jd_text)
        
        # Extract skills
        matched_skills, missing_skills = self._extract_skills(resume_text, jd_text)
        
        # Categorize match
        if score >= 80:
            category = 'Excellent'
            priority = 'High'
        elif score >= 60:
            category = 'Good'
            priority = 'Medium'
        elif score >= 40:
            category = 'Average'
            priority = 'Low'
        else:
            category = 'Poor'
            priority = 'Very Low'
        
        return {
            'score': score,
            'category': category,
            'priority': priority,
            'matched_skills': matched_skills,
            'missing_skills': missing_skills,
            'recommendation': self._generate_recommendation(score, category)
        }
    
    def _simple_match(self, resume_text, jd_text):
        """Simple keyword-based matching."""
        resume_words = set(resume_text.lower().split())
        jd_words = set(jd_text.lower().split())
        
        if not jd_words:
            return 0
        
        # Calculate intersection of words (Jaccard similarity approximation)
        common_words = resume_words.intersection(jd_words)
        
        # Simple ratio
        if len(jd_words) == 0:
            return 0
            
        score = (len(common_words) / len(jd_words)) * 100
        
        # Normalize/Boost score for better UX (raw word intersection is usually low)
        # Assuming finding 20% of words is a "good" match in this simple model
        adjusted_score = min(score * 4, 95) 
        
        return round(adjusted_score, 1)
    
    def _extract_skills(self, resume_text, jd_text):
        """Extract matched and missing skills."""
        resume_lower = resume_text.lower()
        jd_lower = jd_text.lower()
        
        matched = []
        missing = []
        
        for skill in self.common_skills:
            in_jd = skill in jd_lower
            in_resume = skill in resume_lower
            
            if in_jd and in_resume:
                matched.append(skill.title())
            elif in_jd and not in_resume:
                missing.append(skill.title())
        
        return matched[:10], missing[:10]  # Limit to top 10
    
    def _generate_recommendation(self, score, category):
        """Generate hiring recommendation."""
        recommendations = {
            'Excellent': 'Strong candidate! Recommend immediate interview. Skills and experience align very well with requirements.',
            'Good': 'Qualified candidate. Schedule interview to assess cultural fit and specific expertise.',
            'Average': 'Potential candidate. May require additional training or development in key areas.',
            'Poor': 'Skills gap identified. Consider only if candidate shows strong potential in other areas.'
        }
        
        return recommendations.get(category, 'Review candidate profile for detailed assessment.')
