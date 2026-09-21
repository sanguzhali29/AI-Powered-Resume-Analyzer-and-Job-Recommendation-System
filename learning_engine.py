"""
Learning Recommendation Engine (Phase 11)
=========================================
Maps identified missing skills to curated free learning courses,
interactive tutorials, and documentation stored in the database.
"""

from typing import List, Dict, Any
from models.skill import Skill
from models.learning_resource import LearningResource

def get_fallback_resources_for_skill(skill_name: str) -> List[Dict[str, Any]]:
    """Generates direct search links for skills without pre-seeded database resources."""
    query = skill_name.replace(" ", "+")
    return [
        {
            "resource_id": 0,
            "title": f"{skill_name} Tutorial for Beginners",
            "url": f"https://www.youtube.com/results?search_query={query}+tutorial+for+beginners",
            "platform": "YouTube",
            "resource_type": "Video Course",
            "duration_hours": "3-5 Hours",
            "is_free": True
        },
        {
            "resource_id": 0,
            "title": f"{skill_name} Guide & Articles",
            "url": f"https://www.freecodecamp.org/news/search/?query={query}",
            "platform": "freeCodeCamp",
            "resource_type": "Interactive Tutorial",
            "duration_hours": "Self-paced",
            "is_free": True
        },
        {
            "resource_id": 0,
            "title": f"Search Official {skill_name} Documentation",
            "url": f"https://www.google.com/search?q={query}+official+documentation",
            "platform": "Official Docs",
            "resource_type": "Documentation",
            "duration_hours": "Reference",
            "is_free": True
        }
    ]


def get_learning_recommendations_for_skills(missing_skills: List[str]) -> List[Dict[str, Any]]:
    """
    Retrieves free learning courses for each missing skill in the list.
    """
    results = []

    for skill_name in missing_skills:
        skill_obj = Skill.query.filter(Skill.skill_name.ilike(skill_name.strip())).first()
        
        resources = []
        if skill_obj and skill_obj.learning_resources:
            for lr in skill_obj.learning_resources:
                resources.append(lr.to_dict())
        else:
            # Fallback direct search links
            resources = get_fallback_resources_for_skill(skill_name)

        results.append({
            "skill_name": skill_name,
            "category": skill_obj.skill_category if skill_obj else "general",
            "total_resources": len(resources),
            "resources": resources
        })

    return results
