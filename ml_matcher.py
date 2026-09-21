"""
Machine Learning Job Matching Engine (Phase 7)
==============================================
Implements TF-IDF Vectorization and Cosine Similarity to compute ranked
job recommendations for a candidate resume.
"""

from typing import List, Dict, Any
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def _clean_text_for_tfidf(text: str) -> str:
    """Preprocesses raw text by lowercasing and normalizing whitespace."""
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\+\#\.\s]", " ", text)
    return " ".join(text.split())


class JobMatcher:
    """TF-IDF and Cosine Similarity Matching Engine."""

    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            token_pattern=r"(?u)\b[\w\+\#\.]+\b",
            ngram_range=(1, 2),  # unigrams and bigrams (e.g. "machine learning")
            max_features=5000
        )

    def calculate_skill_overlap_score(self, candidate_skills: List[str], job_skills: List[Dict[str, Any]]) -> float:
        """
        Computes weighted skill overlap score between candidate skills and job requirements.
        Mandatory skills carry 1.0 weight, important skills carry 0.8 weight, etc.
        """
        if not job_skills:
            return 0.0

        candidate_set = {s.lower() for s in candidate_skills}
        total_weight = sum(js.get("weight", 1.0) for js in job_skills)
        matched_weight = 0.0

        for js in job_skills:
            skill_name = js.get("skill_name", "").lower()
            weight = js.get("weight", 1.0)
            if skill_name in candidate_set:
                matched_weight += weight

        if total_weight == 0:
            return 0.0
        return (matched_weight / total_weight) * 100.0

    def match_resume_to_jobs(
        self, 
        resume_text: str, 
        candidate_skills: List[str], 
        jobs_list: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Computes hybrid match score for all jobs using TF-IDF Cosine Similarity (50%)
        and Direct Weighted Skill Overlap (50%).
        """
        if not jobs_list:
            return []

        # 1. Prepare Document Corpus for TF-IDF
        clean_resume = _clean_text_for_tfidf(resume_text + " " + " ".join(candidate_skills))
        
        job_docs = []
        for job in jobs_list:
            skills_str = " ".join([js["skill_name"] for js in job.get("skills", [])])
            doc = f"{job['title']} {job['description']} {skills_str}"
            job_docs.append(_clean_text_for_tfidf(doc))

        # 2. Compute TF-IDF Matrix & Cosine Similarity
        corpus = [clean_resume] + job_docs
        try:
            tfidf_matrix = self.vectorizer.fit_transform(corpus)
            resume_vec = tfidf_matrix[0:1]
            job_vecs = tfidf_matrix[1:]
            
            # Compute cosine similarity array
            cosine_scores = cosine_similarity(resume_vec, job_vecs)[0]
        except Exception:
            cosine_scores = np.zeros(len(jobs_list))

        # 3. Combine with Skill Overlap for Hybrid Match Score
        candidate_skills_set = {s.lower() for s in candidate_skills}
        ranked_results = []

        for idx, job in enumerate(jobs_list):
            raw_cosine = float(cosine_scores[idx]) if idx < len(cosine_scores) else 0.0
            tfidf_score = min(raw_cosine * 100.0 * 1.5, 100.0)  # normalized scale
            
            skill_score = self.calculate_skill_overlap_score(candidate_skills, job.get("skills", []))
            
            # Hybrid Formula: 40% TF-IDF Text Similarity + 60% Skill Overlap
            hybrid_match = (0.40 * tfidf_score) + (0.60 * skill_score)
            final_match = round(min(max(hybrid_match, 5.0 if candidate_skills else 0.0), 100.0), 1)

            # Matched & Missing Skills
            matched_skills = []
            missing_skills = []
            for js in job.get("skills", []):
                s_name = js["skill_name"]
                if s_name.lower() in candidate_skills_set:
                    matched_skills.append(s_name)
                else:
                    missing_skills.append(s_name)

            ranked_results.append({
                "job_id": job["job_id"],
                "title": job["title"],
                "company": job["company"],
                "industry": job["industry"],
                "salary_range": job["salary_range"],
                "experience_level": job["experience_level"],
                "description": job["description"],
                "match_percentage": final_match,
                "tfidf_similarity": round(tfidf_score, 1),
                "skill_overlap_score": round(skill_score, 1),
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "total_required_skills": len(job.get("skills", [])),
                "matched_count": len(matched_skills),
                "missing_count": len(missing_skills),
                "explanation": self._generate_explanation(
                    job["title"], final_match, matched_skills, missing_skills
                )
            })

        # Sort by match percentage in descending order
        ranked_results.sort(key=lambda x: x["match_percentage"], reverse=True)
        
        for rank, item in enumerate(ranked_results, start=1):
            item["rank"] = rank

        return ranked_results

    def _generate_explanation(
        self, 
        job_title: str, 
        match_score: float, 
        matched: List[str], 
        missing: List[str]
    ) -> str:
        """Generates clear, academic justification for the match percentage."""
        if match_score >= 75.0:
            fit_type = "Strong Fit"
        elif match_score >= 50.0:
            fit_type = "Moderate Fit"
        else:
            fit_type = "Developing Fit"

        matched_str = ", ".join(matched[:3]) if matched else "None"
        missing_str = ", ".join(missing[:3]) if missing else "None"

        return (
            f"{fit_type} ({match_score}% match). You match core skills like {matched_str}. "
            f"Acquiring {missing_str} will increase your competitiveness for this role."
        )


# Singleton instance
job_matcher = JobMatcher()
