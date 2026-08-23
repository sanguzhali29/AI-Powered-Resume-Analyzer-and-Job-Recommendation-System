"""
Database Seeder Script
======================
Populates the database with initial master skills, standard job postings,
free learning resources, and default accounts (Demo Student & Demo Admin).
Can be run standalone via `python database/seed_data.py` or triggered automatically on app startup.
"""

from database.connection import db
from models.user import User
from models.skill import Skill
from models.job import Job, JobSkill
from models.learning_resource import LearningResource

# Master Skill Taxonomies
INITIAL_SKILLS = [
    # Programming Languages
    ("Python", "programming_languages"),
    ("Java", "programming_languages"),
    ("JavaScript", "programming_languages"),
    ("TypeScript", "programming_languages"),
    ("C++", "programming_languages"),
    ("C#", "programming_languages"),
    ("Go", "programming_languages"),
    ("Rust", "programming_languages"),
    ("SQL", "programming_languages"),
    ("HTML", "programming_languages"),
    ("CSS", "programming_languages"),
    ("PHP", "programming_languages"),
    ("R", "programming_languages"),
    
    # Frameworks & Libraries
    ("Flask", "frameworks"),
    ("Django", "frameworks"),
    ("FastAPI", "frameworks"),
    ("React", "frameworks"),
    ("Node.js", "frameworks"),
    ("Express", "frameworks"),
    ("Angular", "frameworks"),
    ("Vue.js", "frameworks"),
    ("Spring Boot", "frameworks"),
    ("ASP.NET", "frameworks"),
    ("Bootstrap", "frameworks"),
    ("Tailwind CSS", "frameworks"),
    ("Next.js", "frameworks"),
    
    # Databases
    ("MySQL", "databases"),
    ("PostgreSQL", "databases"),
    ("MongoDB", "databases"),
    ("SQLite", "databases"),
    ("Redis", "databases"),
    ("Oracle", "databases"),
    
    # Tools, Cloud & DevOps
    ("Git", "tools"),
    ("GitHub", "tools"),
    ("Docker", "tools"),
    ("Kubernetes", "tools"),
    ("AWS", "tools"),
    ("Azure", "tools"),
    ("GCP", "tools"),
    ("Linux", "tools"),
    ("Postman", "tools"),
    ("Jira", "tools"),
    ("CI/CD", "tools"),
    ("Jenkins", "tools"),
    
    # AI, ML & Domain
    ("Machine Learning", "domain"),
    ("Deep Learning", "domain"),
    ("Natural Language Processing", "domain"),
    ("Computer Vision", "domain"),
    ("Data Analysis", "domain"),
    ("Data Visualization", "domain"),
    ("Pandas", "domain"),
    ("NumPy", "domain"),
    ("Scikit-learn", "domain"),
    ("TensorFlow", "domain"),
    ("PyTorch", "domain"),
    ("REST API", "domain"),
    ("Microservices", "domain"),
    ("Data Structures", "domain"),
    ("Algorithms", "domain"),
    ("Object-Oriented Programming", "domain"),
    
    # Soft Skills
    ("Communication", "soft_skills"),
    ("Problem Solving", "soft_skills"),
    ("Teamwork", "soft_skills"),
    ("Agile", "soft_skills"),
    ("Leadership", "soft_skills"),
    ("Time Management", "soft_skills"),
    ("Critical Thinking", "soft_skills"),
]

# Standard Job Descriptions & Skill Requirements
INITIAL_JOBS = [
    {
        "title": "Python Backend Developer",
        "company": "CloudScale Technologies",
        "industry": "Software Development",
        "experience_level": "0-2 Years (Entry/Junior)",
        "salary_range": "6.5 - 9.5 LPA",
        "description": "Responsible for designing, building, and maintaining high-performance REST APIs and backend microservices using Python, Flask/Django, MySQL, Redis, and Docker. Strong understanding of Object-Oriented Programming, Git version control, and database optimization required.",
        "skills": [
            ("Python", "mandatory", 1.0),
            ("Flask", "mandatory", 1.0),
            ("MySQL", "mandatory", 0.9),
            ("REST API", "mandatory", 0.9),
            ("Git", "important", 0.8),
            ("Docker", "important", 0.7),
            ("Data Structures", "important", 0.7),
            ("Problem Solving", "good_to_have", 0.5),
        ]
    },
    {
        "title": "Full Stack Web Developer",
        "company": "WebMatrix Solutions",
        "industry": "IT Services & Consulting",
        "experience_level": "1-3 Years",
        "salary_range": "7.0 - 12.0 LPA",
        "description": "Looking for a proactive Full Stack Developer skilled in React for client UI and Node.js or Python Flask for server logic. Must have hands-on experience with JavaScript, HTML, CSS, REST APIs, MySQL/MongoDB, and version control using Git.",
        "skills": [
            ("JavaScript", "mandatory", 1.0),
            ("React", "mandatory", 1.0),
            ("Node.js", "mandatory", 0.9),
            ("HTML", "mandatory", 0.8),
            ("CSS", "mandatory", 0.8),
            ("MySQL", "important", 0.8),
            ("REST API", "important", 0.8),
            ("Git", "important", 0.7),
            ("Bootstrap", "good_to_have", 0.5),
        ]
    },
    {
        "title": "Data Scientist & ML Engineer",
        "company": "NeuralAI Analytics",
        "industry": "Artificial Intelligence & Analytics",
        "experience_level": "0-3 Years",
        "salary_range": "8.5 - 15.0 LPA",
        "description": "Develop and deploy Machine Learning and Natural Language Processing pipelines. Requires proficiency in Python, Pandas, NumPy, Scikit-learn, SQL, and data analysis. Experience with Deep Learning (TensorFlow/PyTorch) and REST API model deployment is a strong plus.",
        "skills": [
            ("Python", "mandatory", 1.0),
            ("Machine Learning", "mandatory", 1.0),
            ("Natural Language Processing", "mandatory", 0.9),
            ("Data Analysis", "mandatory", 0.9),
            ("Pandas", "important", 0.8),
            ("NumPy", "important", 0.8),
            ("Scikit-learn", "important", 0.8),
            ("SQL", "important", 0.7),
            ("Deep Learning", "good_to_have", 0.6),
        ]
    },
    {
        "title": "Frontend React Developer",
        "company": "PixelCraft Interactive",
        "industry": "Product Engineering",
        "experience_level": "0-2 Years",
        "salary_range": "6.0 - 9.0 LPA",
        "description": "Design and build fast, responsive, modern web interfaces using React, JavaScript, TypeScript, HTML5, and CSS3/Tailwind. Integrate with backend REST APIs and collaborate with UI/UX designers using Agile methodologies.",
        "skills": [
            ("JavaScript", "mandatory", 1.0),
            ("React", "mandatory", 1.0),
            ("HTML", "mandatory", 0.9),
            ("CSS", "mandatory", 0.9),
            ("TypeScript", "important", 0.8),
            ("REST API", "important", 0.8),
            ("Git", "important", 0.7),
            ("Tailwind CSS", "good_to_have", 0.6),
        ]
    },
    {
        "title": "DevOps & Cloud Engineer",
        "company": "InfraScale Networks",
        "industry": "Cloud Infrastructure",
        "experience_level": "1-4 Years",
        "salary_range": "9.0 - 16.0 LPA",
        "description": "Automate build and deployment pipelines with CI/CD, manage containerized microservices using Docker and Kubernetes, and orchestrate cloud infrastructure on AWS. Strong Linux scripting and Git workflow proficiency required.",
        "skills": [
            ("Docker", "mandatory", 1.0),
            ("Kubernetes", "mandatory", 1.0),
            ("AWS", "mandatory", 1.0),
            ("Linux", "mandatory", 0.9),
            ("Git", "important", 0.8),
            ("CI/CD", "important", 0.8),
            ("Python", "good_to_have", 0.6),
        ]
    },
    {
        "title": "Java Enterprise Developer",
        "company": "Global FinTech Systems",
        "industry": "Banking & Financial Technology",
        "experience_level": "1-3 Years",
        "salary_range": "7.5 - 12.5 LPA",
        "description": "Design high-throughput banking and transaction services using Java, Spring Boot, Microservices architecture, MySQL/PostgreSQL, and Docker. Strong background in OOP, Data Structures, and secure REST APIs.",
        "skills": [
            ("Java", "mandatory", 1.0),
            ("Spring Boot", "mandatory", 1.0),
            ("MySQL", "mandatory", 0.9),
            ("REST API", "mandatory", 0.9),
            ("Microservices", "important", 0.8),
            ("Git", "important", 0.7),
            ("Data Structures", "important", 0.8),
        ]
    },
    {
        "title": "Data Analyst",
        "company": "Insightful Data Labs",
        "industry": "Business Intelligence & Analytics",
        "experience_level": "0-2 Years",
        "salary_range": "5.5 - 8.5 LPA",
        "description": "Transform raw datasets into actionable executive insights. Requires strong SQL querying, Data Analysis, Python (Pandas/NumPy), Data Visualization, and statistical problem-solving capabilities.",
        "skills": [
            ("SQL", "mandatory", 1.0),
            ("Python", "mandatory", 0.9),
            ("Data Analysis", "mandatory", 1.0),
            ("Data Visualization", "mandatory", 0.9),
            ("Pandas", "important", 0.8),
            ("MySQL", "important", 0.7),
            ("Communication", "important", 0.7),
        ]
    },
    {
        "title": "Mobile App Developer (React Native / Flutter)",
        "company": "AppNova Studios",
        "industry": "Mobile Software",
        "experience_level": "0-2 Years",
        "salary_range": "6.0 - 10.0 LPA",
        "description": "Build cross-platform mobile apps for iOS and Android. Requires strong JavaScript/TypeScript skills, REST API consumption, state management, and Git collaboration.",
        "skills": [
            ("JavaScript", "mandatory", 1.0),
            ("React", "mandatory", 1.0),
            ("TypeScript", "important", 0.8),
            ("REST API", "mandatory", 0.9),
            ("Git", "important", 0.7),
            ("Problem Solving", "good_to_have", 0.6),
        ]
    }
]

# Curated Free Learning Resources (YouTube, freeCodeCamp, Coursera Free, W3Schools, Official Docs)
INITIAL_RESOURCES = [
    # Python
    ("Python", "Python for Beginners Full 6-Hour Course", "https://www.youtube.com/watch?v=_uQrJ0TkZlc", "YouTube", "Video Course", "6 Hours"),
    ("Python", "Scientific Computing with Python Certification", "https://www.freecodecamp.org/learn/scientific-computing-with-python/", "freeCodeCamp", "Interactive Tutorial", "30 Hours"),
    ("Python", "Python Tutorial & Reference Guide", "https://www.w3schools.com/python/", "W3Schools", "Interactive Tutorial", "10 Hours"),
    
    # Flask
    ("Flask", "Flask Web Development Crash Course 2026", "https://www.youtube.com/watch?v=Z1RJmh_OwhA", "YouTube", "Video Course", "4 Hours"),
    ("Flask", "Flask Official Quickstart & Application Factory Guide", "https://flask.palletsprojects.com/en/latest/quickstart/", "Official Docs", "Documentation", "3 Hours"),
    
    # Django
    ("Django", "Django Full Course for Beginners", "https://www.youtube.com/watch?v=F5mRW0jo-U4", "YouTube", "Video Course", "8 Hours"),
    
    # React
    ("React", "React.js Full Tutorial for Beginners", "https://www.youtube.com/watch?v=bMknfKXIFA8", "YouTube", "Video Course", "12 Hours"),
    ("React", "Front End Development Libraries with React", "https://www.freecodecamp.org/learn/front-end-development-libraries/", "freeCodeCamp", "Interactive Tutorial", "25 Hours"),
    ("React", "React Tutorial & Hands-on Examples", "https://www.w3schools.com/react/", "W3Schools", "Interactive Tutorial", "8 Hours"),
    
    # JavaScript & TypeScript
    ("JavaScript", "JavaScript Full Course for Beginners", "https://www.youtube.com/watch?v=PkZNo7MFNFg", "YouTube", "Video Course", "8 Hours"),
    ("JavaScript", "JavaScript Algorithms and Data Structures Certification", "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures-v8/", "freeCodeCamp", "Interactive Tutorial", "40 Hours"),
    ("TypeScript", "TypeScript Course for Beginners 2026", "https://www.youtube.com/watch?v=d56mG7DezGs", "YouTube", "Video Course", "3 Hours"),
    
    # MySQL & SQL
    ("MySQL", "MySQL Database Full Course for Beginners", "https://www.youtube.com/watch?v=HXV3zeQKqGY", "YouTube", "Video Course", "4 Hours"),
    ("MySQL", "MySQL Tutorial - SQL Queries and Relational Design", "https://www.w3schools.com/mysql/", "W3Schools", "Interactive Tutorial", "10 Hours"),
    ("SQL", "Relational Database Certification", "https://www.freecodecamp.org/learn/relational-database/", "freeCodeCamp", "Interactive Tutorial", "30 Hours"),
    
    # Git
    ("Git", "Git and GitHub Crash Course for Beginners", "https://www.youtube.com/watch?v=RGOj5yH7evk", "YouTube", "Video Course", "2 Hours"),
    ("Git", "Git Handbook and Command Guide", "https://www.freecodecamp.org/news/git-and-github-handbook/", "freeCodeCamp", "Article", "2 Hours"),
    
    # Docker & Kubernetes
    ("Docker", "Docker Tutorial for Beginners Full Course", "https://www.youtube.com/watch?v=3c-iBn73dDE", "YouTube", "Video Course", "3 Hours"),
    ("Docker", "Docker Official Getting Started Documentation", "https://docs.docker.com/get-started/", "Official Docs", "Documentation", "4 Hours"),
    ("Kubernetes", "Kubernetes for Beginners Crash Course", "https://www.youtube.com/watch?v=d6WC5n9G_sM", "YouTube", "Video Course", "4 Hours"),
    
    # AWS & Cloud
    ("AWS", "AWS Certified Cloud Practitioner Free Study Course", "https://www.freecodecamp.org/news/aws-certified-cloud-practitioner-study-course/", "freeCodeCamp", "Video Course", "14 Hours"),
    ("Linux", "Linux Command Line Basics for Beginners", "https://www.youtube.com/watch?v=ZtqBQ68cfJc", "YouTube", "Video Course", "5 Hours"),
    
    # Machine Learning, NLP & AI
    ("Machine Learning", "Machine Learning for Everybody Full Course", "https://www.freecodecamp.org/news/machine-learning-course/", "freeCodeCamp", "Video Course", "4 Hours"),
    ("Machine Learning", "Machine Learning Introduction Specialization (Free Audit)", "https://www.coursera.org/specializations/machine-learning-introduction", "Coursera Free", "Video Course", "20 Hours"),
    ("Natural Language Processing", "NLP and Text Preprocessing Tutorial in Python", "https://www.youtube.com/watch?v=vyOgWhwUmec", "YouTube", "Video Course", "5 Hours"),
    ("Data Analysis", "Data Analysis with Python Certification", "https://www.freecodecamp.org/learn/data-analysis-with-python/", "freeCodeCamp", "Interactive Tutorial", "30 Hours"),
    ("Pandas", "Pandas and NumPy for Data Science Full Tutorial", "https://www.youtube.com/watch?v=vmEHCJofslg", "YouTube", "Video Course", "6 Hours"),
    
    # Java & Spring Boot
    ("Java", "Java Programming Full Course for Beginners", "https://www.youtube.com/watch?v=eIrMbAQSU34", "YouTube", "Video Course", "9 Hours"),
    ("Spring Boot", "Spring Boot Full Course - Build RESTful APIs", "https://www.youtube.com/watch?v=9SGDpanrc8U", "YouTube", "Video Course", "7 Hours"),
    
    # Data Structures & Soft Skills
    ("Data Structures", "Data Structures and Algorithms Full Course", "https://www.youtube.com/watch?v=8hly31xKli0", "YouTube", "Video Course", "8 Hours"),
    ("Communication", "Professional Technical Communication and Presentation Skills", "https://www.youtube.com/watch?v=HAnw168huqA", "YouTube", "Video Course", "2 Hours"),
]


def seed_database():
    """Seeds the database with master skills, jobs, resources, and demo users."""
    print("[Seed] Seeding database started...")

    # 1. Seed Users (Demo student & demo admin)
    if User.query.count() == 0:
        student = User(
            full_name="Alex Johnson",
            email="student@demo.com",
            role="student",
            phone="9876543210"
        )
        student.set_password("password123")
        db.session.add(student)

        admin = User(
            full_name="Admin Recruiter",
            email="admin@demo.com",
            role="admin",
            phone="9988776655"
        )
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        print("[Seed] Created demo student (student@demo.com) and admin (admin@demo.com).")

    # 2. Seed Skills
    skill_map = {}
    for name, category in INITIAL_SKILLS:
        existing = Skill.query.filter_by(skill_name=name).first()
        if not existing:
            new_skill = Skill(skill_name=name, skill_category=category)
            db.session.add(new_skill)
            db.session.flush()
            skill_map[name] = new_skill
        else:
            skill_map[name] = existing
    db.session.commit()
    print(f"[Seed] Processed {len(INITIAL_SKILLS)} master skills.")

    # 3. Seed Jobs & JobSkills
    for job_info in INITIAL_JOBS:
        existing_job = Job.query.filter_by(title=job_info["title"]).first()
        if not existing_job:
            job = Job(
                title=job_info["title"],
                company=job_info["company"],
                industry=job_info["industry"],
                experience_level=job_info["experience_level"],
                salary_range=job_info["salary_range"],
                description=job_info["description"]
            )
            db.session.add(job)
            db.session.flush()

            # Attach skills
            for s_name, importance, weight in job_info["skills"]:
                skill_obj = Skill.query.filter_by(skill_name=s_name).first()
                if skill_obj:
                    js = JobSkill(
                        job_id=job.job_id,
                        skill_id=skill_obj.skill_id,
                        importance_level=importance,
                        weight=weight
                    )
                    db.session.add(js)
    db.session.commit()
    print(f"[Seed] Processed {len(INITIAL_JOBS)} standard job postings.")

    # 4. Seed Learning Resources
    for s_name, title, url, platform, r_type, duration in INITIAL_RESOURCES:
        skill_obj = Skill.query.filter_by(skill_name=s_name).first()
        if skill_obj:
            existing_res = LearningResource.query.filter_by(
                skill_id=skill_obj.skill_id, title=title
            ).first()
            if not existing_res:
                res = LearningResource(
                    skill_id=skill_obj.skill_id,
                    title=title,
                    url=url,
                    platform=platform,
                    resource_type=r_type,
                    duration_hours=duration,
                    is_free=True
                )
                db.session.add(res)
    db.session.commit()
    print(f"[Seed] Processed {len(INITIAL_RESOURCES)} free learning resources.")
    print("[Seed] Database seeding completed successfully!")
