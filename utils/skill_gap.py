"""
Skill Gap Analysis Module (Phase 8)
===================================
Performs detailed gap analysis between a candidate's detected skills and
a selected target job profile. Prioritizes missing skills based on market demand.
"""

from typing import List, Dict, Any
from collections import Counter
from models.job import Job

def calculate_global_skill_demand() -> Dict[str, int]:
    """
    Counts how many job postings require each skill across the entire database.
    Used to prioritize which missing skills the candidate should learn first.
    """
    try:
        all_jobs = Job.query.all()
        skill_counter = Counter()
        for job in all_jobs:
            for s_name in job.get_required_skills():
                skill_counter[s_name] += 1
        return dict(skill_counter)
    except Exception:
        return {}


def analyze_skill_gap_for_job(
    candidate_skills: List[str], 
    target_job: Job, 
    skill_demand: Dict[str, int] = None
) -> Dict[str, Any]:
    """
    Calculates matched vs missing skills, gap percentage, and priority learning list.
    """
    if skill_demand is None:
        skill_demand = calculate_global_skill_demand()

    candidate_set = {s.lower(): s for s in candidate_skills}
    job_required_skills = target_job.get_required_skills()
    
    matched_skills = []
    missing_skills = []

    for req_skill in job_required_skills:
        if req_skill.lower() in candidate_set:
            matched_skills.append(req_skill)
        else:
            missing_skills.append(req_skill)

    total_required = len(job_required_skills)
    matched_count = len(matched_skills)
    missing_count = len(missing_skills)

    readiness_percentage = round((matched_count / total_required) * 100, 1) if total_required > 0 else 100.0
    gap_percentage = round(100.0 - readiness_percentage, 1)

    # Prioritize missing skills by global market demand count
    priority_missing = []
    for skill in missing_skills:
        demand = skill_demand.get(skill, 1)
        priority_missing.append({
            "skill_name": skill,
            "demand_count": demand,
            "importance": "High" if demand >= 3 else "Medium"
        })

    # Sort priority skills by demand descending
    priority_missing.sort(key=lambda x: x["demand_count"], reverse=True)

    return {
        "job_id": target_job.job_id,
        "job_title": target_job.title,
        "company": target_job.company,
        "industry": target_job.industry,
        "total_required": total_required,
        "matched_count": matched_count,
        "missing_count": missing_count,
        "readiness_percentage": readiness_percentage,
        "gap_percentage": gap_percentage,
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills),
        "priority_learning_list": priority_missing
    }
