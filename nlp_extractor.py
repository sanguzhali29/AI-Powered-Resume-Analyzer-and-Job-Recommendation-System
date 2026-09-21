"""
NLP Skill & Entity Extraction Module (Phase 5)
==============================================
Extracts structured entities, skills by category, contact information,
education, and work experience from raw resume text using NLP and regex boundaries.
"""

import re
from typing import Dict, List, Any

# Section Header Keywords for Section Splitting
SECTION_HEADERS = {
    "skills": ["skills", "technical skills", "core competencies", "skills & tools", "technologies", "expertise", "proficiencies", "technical expertise"],
    "education": ["education", "academic background", "qualifications", "academics", "educational qualification", "degrees", "educational history"],
    "experience": ["experience", "work experience", "employment history", "professional experience", "internships", "work history"],
    "projects": ["projects", "academic projects", "key projects", "personal projects", "notable projects"],
    "certifications": ["certifications", "certificates", "courses & certifications", "accreditations", "licenses"],
}

# Master Skill Dictionary with canonical name -> search aliases
SKILL_TAXONOMY = {
    "programming_languages": {
        "Python": ["python", "python3", "python 3"],
        "Java": ["java", "core java", "j2se", "jdk"],
        "JavaScript": ["javascript", "js", "ecmascript", "es6"],
        "TypeScript": ["typescript", "ts"],
        "C++": ["c++", "cpp"],
        "C#": ["c#", "csharp", "c sharp"],
        "C": ["c programming", "c language"],
        "Go": ["golang", "go language"],
        "Rust": ["rust"],
        "SQL": ["sql", "t-sql", "pl/sql"],
        "HTML": ["html", "html5"],
        "CSS": ["css", "css3"],
        "PHP": ["php"],
        "R": ["r programming", "r language"],
        "Ruby": ["ruby"],
        "Kotlin": ["kotlin"],
        "Swift": ["swift"],
    },
    "frameworks": {
        "Flask": ["flask"],
        "Django": ["django"],
        "FastAPI": ["fastapi"],
        "React": ["react", "react.js", "reactjs"],
        "Node.js": ["node.js", "nodejs", "node"],
        "Express": ["express.js", "expressjs", "express"],
        "Angular": ["angular", "angularjs"],
        "Vue.js": ["vue", "vue.js", "vuejs"],
        "Spring Boot": ["spring boot", "springboot", "spring framework"],
        "ASP.NET": ["asp.net", ".net", "dotnet", ".net core"],
        "Bootstrap": ["bootstrap", "bootstrap 5"],
        "Tailwind CSS": ["tailwind", "tailwindcss", "tailwind css"],
        "Next.js": ["next.js", "nextjs"],
        "jQuery": ["jquery"],
    },
    "databases": {
        "MySQL": ["mysql"],
        "PostgreSQL": ["postgresql", "postgres"],
        "MongoDB": ["mongodb", "mongo"],
        "SQLite": ["sqlite", "sqlite3"],
        "Redis": ["redis"],
        "Oracle": ["oracle", "oracle db"],
        "Cassandra": ["cassandra"],
        "Firebase": ["firebase", "firestore"],
    },
    "tools": {
        "Git": ["git", "version control"],
        "GitHub": ["github"],
        "GitLab": ["gitlab"],
        "Docker": ["docker", "containerization"],
        "Kubernetes": ["kubernetes", "k8s"],
        "AWS": ["aws", "amazon web services", "ec2", "s3"],
        "Azure": ["azure", "microsoft azure"],
        "GCP": ["gcp", "google cloud"],
        "Linux": ["linux", "ubuntu", "centos", "bash", "shell scripting"],
        "Postman": ["postman"],
        "Jira": ["jira"],
        "CI/CD": ["ci/cd", "continuous integration", "cicd"],
        "Jenkins": ["jenkins"],
    },
    "domain": {
        "Machine Learning": ["machine learning", "ml", "supervised learning", "unsupervised learning"],
        "Deep Learning": ["deep learning", "neural networks", "cnn", "rnn", "lstm"],
        "Natural Language Processing": ["nlp", "natural language processing", "text mining", "spacy", "nltk", "tf-idf"],
        "Computer Vision": ["computer vision", "opencv"],
        "Data Analysis": ["data analysis", "exploratory data analysis", "eda"],
        "Data Visualization": ["data visualization", "matplotlib", "seaborn", "tableau", "power bi"],
        "Pandas": ["pandas"],
        "NumPy": ["numpy"],
        "Scikit-learn": ["scikit-learn", "sklearn"],
        "TensorFlow": ["tensorflow", "tf"],
        "PyTorch": ["pytorch"],
        "REST API": ["rest api", "restful api", "rest apis", "rest endpoints"],
        "Microservices": ["microservices", "microservice architecture"],
        "Data Structures": ["data structures", "dsa", "arrays", "linked lists", "trees", "graphs"],
        "Algorithms": ["algorithms", "algorithmic problem solving"],
        "Object-Oriented Programming": ["oop", "oops", "object oriented programming"],
    },
    "soft_skills": {
        "Communication": ["communication", "verbal communication", "written communication"],
        "Problem Solving": ["problem solving", "analytical thinking", "troubleshooting"],
        "Teamwork": ["teamwork", "team collaboration", "cross-functional"],
        "Agile": ["agile", "scrum", "kanban", "sprint planning"],
        "Leadership": ["leadership", "mentoring", "team lead"],
        "Time Management": ["time management", "prioritization", "multitasking"],
        "Critical Thinking": ["critical thinking"],
    }
}

EDUCATION_KEYWORDS = [
    "b.e", "b.tech", "btech", "m.tech", "mtech", "b.sc", "bsc", "m.sc", "msc",
    "bca", "mca", "bachelor of engineering", "bachelor of technology",
    "master of computer applications", "computer science", "information technology",
    "electronics", "data science", "university", "institute", "college", "cgpa", "gpa"
]


def _build_regex_pattern(term: str) -> re.Pattern:
    """Builds safe word-boundary regular expression for exact skill matching."""
    escaped = re.escape(term.strip().lower())
    pattern = r"(?<![a-zA-Z0-9])" + escaped + r"(?![a-zA-Z0-9])"
    return re.compile(pattern, re.IGNORECASE)


class NLPExtractor:
    """NLP Entity & Skill Extraction Engine."""

    def __init__(self):
        # Pre-compile regexes for fast matching
        self.compiled_skills = {}
        for category, skill_dict in SKILL_TAXONOMY.items():
            self.compiled_skills[category] = {}
            for canonical, aliases in skill_dict.items():
                all_terms = set([canonical.lower()] + [a.lower().strip() for a in aliases])
                self.compiled_skills[category][canonical] = [
                    _build_regex_pattern(term) for term in all_terms
                ]

    def split_sections(self, text: str) -> Dict[str, str]:
        """Splits resume text into functional sections."""
        lines = text.split("\n")
        sections = {"header": []}
        current_section = "header"

        for line in lines:
            stripped = line.strip().lower().strip(":").strip()
            matched = None
            if 0 < len(stripped) <= 45:
                for section_name, keywords in SECTION_HEADERS.items():
                    if any(stripped == kw or stripped.startswith(kw + " ") for kw in keywords):
                        matched = section_name
                        break
            if matched:
                current_section = matched
                sections.setdefault(current_section, [])
                continue

            sections.setdefault(current_section, [])
            sections[current_section].append(line)

        return {k: "\n".join(v).strip() for k, v in sections.items()}

    def extract_skills(self, text: str) -> Dict[str, List[str]]:
        """Matches resume text against master taxonomy across 6 categories."""
        sections = self.split_sections(text)
        # Search skills section + entire document for complete coverage
        search_scope = sections.get("skills", "") + "\n" + text
        
        extracted = {}
        for category, canonical_dict in self.compiled_skills.items():
            found_in_category = []
            for canonical, patterns in canonical_dict.items():
                for pattern in patterns:
                    if pattern.search(search_scope):
                        found_in_category.append(canonical)
                        break
            extracted[category] = sorted(found_in_category)
            
        return extracted

    def extract_contact_info(self, text: str) -> Dict[str, Any]:
        """Extracts email, phone number, LinkedIn, and GitHub links."""
        email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
        phone_match = re.search(r"(?:\+?\d{1,3}[\s-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}", text)
        linkedin_match = re.search(r"(?:https?://)?(?:www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+", text, re.IGNORECASE)
        github_match = re.search(r"(?:https?://)?(?:www\.)?github\.com/[a-zA-Z0-9_-]+", text, re.IGNORECASE)

        return {
            "email": email_match.group(0) if email_match else None,
            "phone": phone_match.group(0) if phone_match else None,
            "linkedin": linkedin_match.group(0) if linkedin_match else None,
            "github": github_match.group(0) if github_match else None,
        }

    def extract_education(self, text: str) -> List[str]:
        """Extracts degrees, university names, and education entries."""
        sections = self.split_sections(text)
        edu_text = sections.get("education", "") or text
        results = []
        
        for line in edu_text.split("\n"):
            clean = line.strip()
            if not clean or len(clean) < 4:
                continue
            lower = clean.lower()
            if any(_build_regex_pattern(kw).search(lower) for kw in EDUCATION_KEYWORDS):
                results.append(clean)
                
        # Deduplicate preserving order
        unique_results = []
        seen = set()
        for r in results:
            if r.lower() not in seen:
                seen.add(r.lower())
                unique_results.append(r)
        return unique_results[:8]

    def extract_experience_summary(self, text: str) -> Dict[str, Any]:
        """Estimates total years of experience and parses work experience lines."""
        sections = self.split_sections(text)
        exp_text = sections.get("experience", "")
        
        # Look for explicit experience mentions
        matches = re.findall(
            r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years|yrs|year)\s*(?:of)?\s*experience",
            text.lower()
        )
        years = max([float(y) for y in matches], default=None)

        entries = []
        if exp_text:
            for line in exp_text.split("\n"):
                clean = line.strip(" \t-•*")
                if clean and len(clean) > 8:
                    entries.append(clean)

        return {
            "years_mentioned": years,
            "has_experience_section": bool(exp_text),
            "entries": entries[:10]
        }

    def extract_projects(self, text: str) -> List[str]:
        """Extracts notable project titles and descriptions."""
        sections = self.split_sections(text)
        proj_text = sections.get("projects", "")
        if not proj_text:
            return []

        entries = []
        for line in proj_text.split("\n"):
            clean = line.strip(" \t-•*")
            if clean and len(clean) > 8:
                entries.append(clean)
        return entries[:10]

    def full_parse(self, text: str) -> Dict[str, Any]:
        """Executes full NLP extraction pipeline on resume text."""
        skills = self.extract_skills(text)
        flat_skills = []
        for cat, sk_list in skills.items():
            flat_skills.extend(sk_list)
        flat_skills = sorted(list(set(flat_skills)))

        return {
            "skills": skills,
            "flat_skills": flat_skills,
            "total_skills_count": len(flat_skills),
            "contact": self.extract_contact_info(text),
            "education": self.extract_education(text),
            "experience": self.extract_experience_summary(text),
            "projects": self.extract_projects(text),
            "sections_found": list(self.split_sections(text).keys())
        }


# Singleton instance for efficient reuse across the app
nlp_extractor = NLPExtractor()
