"""
Resume Scoring & ATS Analytics Module (Phase 10)
================================================
Evaluates resume quality, structural completeness, skill depth, and ATS readiness.
Generates comprehensive diagnostic scores and actionable improvement tips.
"""

from typing import Dict, Any, List

def calculate_resume_completeness(parsed_data: Dict[str, Any], raw_text: str) -> Dict[str, Any]:
    """
    Evaluates resume against 5 essential academic and industry criteria (total 100 points):
    1. Contact Information (20%)
    2. Skills Breadth & Diversity (30%)
    3. Education Section (15%)
    4. Work Experience / Internships (20%)
    5. Projects & Practical Portfolio (15%)
    """
    score_breakdown = {}
    improvement_tips = []
    
    # -------------------------------------------------------------
    # 1. Contact Information Score (Max 20 pts)
    # -------------------------------------------------------------
    contact = parsed_data.get("contact", {})
    contact_score = 0
    if contact.get("email"):
        contact_score += 7
    else:
        improvement_tips.append("Add a professional email address at the top.")

    if contact.get("phone"):
        contact_score += 7
    else:
        improvement_tips.append("Include an active phone number for recruiter outreach.")

    if contact.get("linkedin") or contact.get("github"):
        contact_score += 6
    else:
        improvement_tips.append("Add links to your LinkedIn profile or GitHub portfolio.")

    score_breakdown["contact_score"] = contact_score  # out of 20

    # -------------------------------------------------------------
    # 2. Skills Diversity Score (Max 30 pts)
    # -------------------------------------------------------------
    skills = parsed_data.get("skills", {})
    total_skills = parsed_data.get("total_skills_count", 0)
    
    # Categories present
    categories_present = sum(1 for cat, sk_list in skills.items() if len(sk_list) > 0)
    
    skills_score = 0
    # Volume score (up to 15 pts)
    if total_skills >= 10:
        skills_score += 15
    elif total_skills >= 5:
        skills_score += 10
    elif total_skills >= 1:
        skills_score += 5
    else:
        improvement_tips.append("Include a dedicated Technical Skills section with at least 8-10 key competencies.")

    # Diversity score (up to 15 pts)
    skills_score += min(categories_present * 3, 15)
    
    if not skills.get("tools") or len(skills.get("tools", [])) == 0:
        improvement_tips.append("Mention essential developer tools like Git, Docker, or Postman.")
    if not skills.get("soft_skills") or len(skills.get("soft_skills", [])) == 0:
        improvement_tips.append("Highlight transferable soft skills such as Problem Solving or Agile Collaboration.")

    score_breakdown["skills_score"] = min(skills_score, 30)

    # -------------------------------------------------------------
    # 3. Education Score (Max 15 pts)
    # -------------------------------------------------------------
    education = parsed_data.get("education", [])
    edu_score = 0
    if len(education) >= 2:
        edu_score = 15
    elif len(education) == 1:
        edu_score = 10
    else:
        improvement_tips.append("Clearly detail your degree (e.g. B.E. / B.Tech Computer Science) and institution.")

    score_breakdown["education_score"] = edu_score

    # -------------------------------------------------------------
    # 4. Experience / Internships Score (Max 20 pts)
    # -------------------------------------------------------------
    exp = parsed_data.get("experience", {})
    exp_score = 0
    if exp.get("has_experience_section") and len(exp.get("entries", [])) > 0:
        exp_score = 20
    elif exp.get("years_mentioned"):
        exp_score = 15
    else:
        exp_score = 8  # Entry level baseline
        improvement_tips.append("Add an Experience/Internships section detailing past roles or academic training.")

    score_breakdown["experience_score"] = exp_score

    # -------------------------------------------------------------
    # 5. Projects & Practical Work Score (Max 15 pts)
    # -------------------------------------------------------------
    projects = parsed_data.get("projects", [])
    proj_score = 0
    if len(projects) >= 2:
        proj_score = 15
    elif len(projects) == 1:
        proj_score = 10
    else:
        improvement_tips.append("Include 2-3 technical projects highlighting technologies used and outcomes achieved.")

    score_breakdown["projects_score"] = proj_score

    # -------------------------------------------------------------
    # Total Calculation
    # -------------------------------------------------------------
    total_score = (
        contact_score + 
        score_breakdown["skills_score"] + 
        edu_score + 
        exp_score + 
        proj_score
    )
    total_score = min(max(total_score, 10), 100)

    # ATS Quality Level
    if total_score >= 80:
        quality_level = "Excellent (Ready for Job Applications)"
        badge_class = "success"
    elif total_score >= 60:
        quality_level = "Good (Needs Minor Optimizations)"
        badge_class = "info"
    elif total_score >= 40:
        quality_level = "Average (Recommended to Add Missing Sections)"
        badge_class = "warning"
    else:
        quality_level = "Needs Significant Improvement"
        badge_class = "danger"

    # Text Metrics
    words = raw_text.split()
    word_count = len(words)
    estimated_read_time_seconds = round((word_count / 200) * 60)

    return {
        "overall_score": total_score,
        "quality_level": quality_level,
        "badge_class": badge_class,
        "breakdown": score_breakdown,
        "word_count": word_count,
        "estimated_read_time_seconds": estimated_read_time_seconds,
        "improvement_tips": improvement_tips[:5]
    }
