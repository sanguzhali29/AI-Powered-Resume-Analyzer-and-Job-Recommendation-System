# AI-Based Resume Analyzer & Job Recommendation System
## PHASE 1 — Planning & Design Documentation

---

## 1. Project Overview

This project is a web application that reads a person's resume, understands what skills and experience it contains, and then suggests suitable job roles for that person. It also tells the user how well their resume matches a particular job description, and gives tips to improve it.

In simple words: **you upload your resume → the system reads it like a human recruiter would → it tells you which jobs suit you and what to improve.**

The system uses Natural Language Processing (NLP) and Machine Learning to "understand" text, instead of just searching for keywords blindly.

---

## 2. Problem Statement

- Students and job seekers often don't know which jobs match their skill set.
- Writing a resume that passes automated screening (used by real companies) is hard for beginners.
- Manually comparing a resume against every job description is slow and tiring.
- Career guidance from a real counselor is not available to everyone.

**There is a need for an automated system that can read a resume, understand it, and recommend the right jobs — instantly and for free.**

---

## 3. Existing System

Most current tools fall into one of these categories:

| Type | Limitation |
|---|---|
| Manual resume review by placement cells | Slow, limited to few people, subjective |
| Simple keyword-matching resume checkers | Don't understand context or meaning, easily fooled |
| Generic job portals (Naukri, LinkedIn, Indeed) | Recommend jobs based on filters, not resume content |
| Paid resume-scoring tools | Expensive, closed-source, not customizable for a student project |

**Common problem:** none of these truly "read and understand" a resume the way a human would, and none combine resume analysis + job recommendation in one simple system.

---

## 4. Proposed System

We propose a web-based system where:

1. The user uploads a resume (PDF/DOCX).
2. The system extracts the text and important sections (skills, education, experience).
3. NLP techniques clean and process this text.
4. Using **TF-IDF** and **Cosine Similarity**, the system compares the resume against a database of job descriptions.
5. The system returns a **ranked list of matching jobs** with a **match percentage**.
6. The system also gives resume improvement suggestions (missing skills, formatting tips).
7. An Admin can manage the job listings and monitor system usage.

---

## 5. Objectives

1. To automatically extract and understand content from a resume.
2. To use NLP and ML to measure similarity between a resume and job descriptions.
3. To recommend the most relevant jobs to the user, ranked by match score.
4. To identify missing/weak skills in a resume compared to a target job.
5. To provide a simple, clean web interface usable by any student without technical knowledge.
6. To give the Admin control over job data and platform monitoring.

---

## 6. Features

**User-side features**
- User registration and login
- Upload resume (PDF/DOCX)
- Automatic resume parsing (name, skills, education, experience extraction)
- Resume vs Job Description match score (%)
- Top job recommendations based on resume content
- Missing skills / improvement suggestions
- Resume history (previously uploaded resumes and results)
- Downloadable analysis report

**Admin-side features**
- Admin login (secure, separate from user login)
- Add / edit / delete job listings
- View all registered users
- View all uploaded resumes and analysis results
- Basic usage statistics/dashboard (e.g., total users, total resumes analyzed)

---

## 7. Modules

1. **User Authentication Module** – Registration, login, session/password management.
2. **Resume Upload & Parsing Module** – Accepts PDF/DOCX, extracts raw text, extracts structured fields (skills, education, experience).
3. **NLP Preprocessing Module** – Cleans text: lowercasing, removing stopwords, tokenization, lemmatization.
4. **AI/ML Matching Module** – Converts resume + job descriptions into TF-IDF vectors, computes Cosine Similarity, ranks jobs.
5. **Job Recommendation Module** – Displays top-N matching jobs with scores.
6. **Resume Feedback Module** – Compares resume skills vs job-required skills, lists missing skills.
7. **Admin Management Module** – Manage job postings, view users/resumes, dashboard stats.
8. **Database Module** – Stores users, resumes, parsed data, jobs, and results in MySQL.
9. **Report Module** – Generates a downloadable summary of the analysis.

---

## 8. User Workflow

1. User visits the website and registers/logs in.
2. User uploads their resume (PDF/DOCX).
3. System parses the resume and extracts text + skills.
4. System preprocesses the text using NLP.
5. System runs TF-IDF + Cosine Similarity against stored job descriptions.
6. System displays:
   - Match percentage for each relevant job
   - Top recommended jobs (ranked)
   - Missing skills / suggestions
7. User can view past results in "My History."
8. User can download the analysis as a report.

---

## 9. Admin Workflow

1. Admin logs in through a separate secure admin login.
2. Admin lands on a dashboard showing overall statistics (total users, total resumes analyzed, total jobs posted).
3. Admin can add a new job listing (title, description, required skills).
4. Admin can edit or delete existing job listings.
5. Admin can view the list of registered users.
6. Admin can view resumes uploaded and their analysis results (for monitoring/moderation).
7. Admin logs out.

---

## 10. System Architecture

A simple 3-layer (client–server–database) architecture:

```
 ┌───────────────────────────┐
 │        CLIENT SIDE         │
 │  HTML, CSS, JavaScript,    │
 │  Bootstrap (Browser UI)    │
 └─────────────┬──────────────┘
               │  HTTP Requests (Forms, AJAX)
 ┌─────────────▼──────────────┐
 │        SERVER SIDE          │
 │       Python Flask          │
 │  - Routes / Controllers     │
 │  - Resume Parsing Logic     │
 │  - NLP + ML Engine          │
 │    (Scikit-learn, TF-IDF,   │
 │     Cosine Similarity)      │
 └─────────────┬──────────────┘
               │  SQL Queries
 ┌─────────────▼──────────────┐
 │        DATABASE             │
 │           MySQL             │
 │  Users | Resumes | Jobs |   │
 │  Results | Admin            │
 └──────────────────────────────┘
```

**Flow:** Browser (client) sends requests → Flask server handles logic and talks to the ML engine → MySQL stores/retrieves data → Flask sends the result back → Browser displays it.

---

## 11. AI/ML Workflow

This is the "brain" of the project — how the system understands resumes and matches jobs.

```
Step 1: Text Extraction
   Resume (PDF/DOCX) ---> Extract raw text (using PyPDF2 / python-docx)

Step 2: Text Preprocessing (NLP)
   Raw text ---> Lowercase ---> Remove punctuation/stopwords
        ---> Tokenization ---> Lemmatization ---> Clean text

Step 3: Feature Extraction (Vectorization)
   Clean resume text + Clean job description texts
        ---> Converted into numeric vectors using TF-IDF

Step 4: Similarity Calculation
   Resume vector  vs  Each Job vector
        ---> Cosine Similarity Score (0 to 1) calculated for each job

Step 5: Ranking
   All jobs sorted by similarity score (highest first)
        ---> Top-N jobs selected as recommendations

Step 6: Skill Gap Analysis
   Job's required skills  −  Resume's extracted skills
        ---> List of missing skills shown to user

Step 7: Output
   Match %, Ranked Job List, Missing Skills ---> Displayed to user
```

**Why TF-IDF + Cosine Similarity?**
- TF-IDF (Term Frequency–Inverse Document Frequency) converts text into numbers based on how important each word is.
- Cosine Similarity then measures how "close" two pieces of text are in meaning/direction — perfect for comparing a resume to a job description.
- Both are beginner-friendly, well-documented in Scikit-learn, and ideal for a final-year project (no heavy deep learning setup needed).

---

## 12. Database Architecture

**Database:** MySQL

### Tables

**1. users**
| Column | Type | Description |
|---|---|---|
| user_id | INT (PK, AUTO_INCREMENT) | Unique user ID |
| name | VARCHAR(100) | Full name |
| email | VARCHAR(100), UNIQUE | Login email |
| password | VARCHAR(255) | Hashed password |
| created_at | DATETIME | Registration date |

**2. admin**
| Column | Type | Description |
|---|---|---|
| admin_id | INT (PK, AUTO_INCREMENT) | Unique admin ID |
| username | VARCHAR(50), UNIQUE | Admin username |
| password | VARCHAR(255) | Hashed password |

**3. resumes**
| Column | Type | Description |
|---|---|---|
| resume_id | INT (PK, AUTO_INCREMENT) | Unique resume ID |
| user_id | INT (FK → users.user_id) | Owner of resume |
| file_path | VARCHAR(255) | Path to uploaded file |
| extracted_text | TEXT | Raw parsed text |
| skills_extracted | TEXT | Extracted skills (comma-separated / JSON) |
| uploaded_at | DATETIME | Upload timestamp |

**4. jobs**
| Column | Type | Description |
|---|---|---|
| job_id | INT (PK, AUTO_INCREMENT) | Unique job ID |
| title | VARCHAR(150) | Job title |
| description | TEXT | Full job description |
| required_skills | TEXT | Required skills (comma-separated) |
| posted_by | INT (FK → admin.admin_id) | Admin who added it |
| created_at | DATETIME | Date added |

**5. results**
| Column | Type | Description |
|---|---|---|
| result_id | INT (PK, AUTO_INCREMENT) | Unique result ID |
| resume_id | INT (FK → resumes.resume_id) | Related resume |
| job_id | INT (FK → jobs.job_id) | Related job |
| match_score | FLOAT | Cosine similarity score (%) |
| missing_skills | TEXT | Skills missing for this job |
| generated_at | DATETIME | When the analysis was done |

### Relationships
- One **user** → many **resumes**
- One **resume** → many **results** (one per job compared)
- One **job** → many **results**
- One **admin** → many **jobs** posted

---

## 13. Complete Folder Structure

```
resume-analyzer/
│
├── app.py                        # Main Flask application entry point
├── config.py                     # Configuration (DB credentials, secret key)
├── requirements.txt              # Python dependencies list
├── README.md                     # Project documentation
│
├── static/
│   ├── css/
│   │   └── style.css             # Custom styling
│   ├── js/
│   │   └── script.js             # Custom JS (form validation, AJAX calls)
│   ├── images/
│   └── uploads/                  # Uploaded resume files stored here
│
├── templates/
│   ├── base.html                 # Common layout (navbar, footer)
│   ├── index.html                # Landing page
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html            # User dashboard
│   ├── upload_resume.html
│   ├── results.html              # Match results & recommendations
│   ├── history.html
│   ├── admin/
│   │   ├── admin_login.html
│   │   ├── admin_dashboard.html
│   │   ├── manage_jobs.html
│   │   ├── view_users.html
│   │   └── view_resumes.html
│
├── routes/
│   ├── auth_routes.py            # Register/login/logout routes
│   ├── user_routes.py            # Upload, results, history routes
│   └── admin_routes.py           # Admin management routes
│
├── models/
│   └── db_models.py              # Table definitions / DB helper functions
│
├── ml/
│   ├── resume_parser.py          # Extract text from PDF/DOCX
│   ├── preprocessing.py          # NLP cleaning (stopwords, lemmatization)
│   ├── tfidf_matcher.py          # TF-IDF + Cosine Similarity logic
│   └── skill_extractor.py        # Skill keyword extraction logic
│
├── database/
│   └── schema.sql                # MySQL table creation script
│
└── docs/
    ├── project_report.docx
    ├── ppt_presentation.pptx
    └── er_diagram.png
```

---

## 14. Technologies and Libraries

**Frontend**
- HTML5, CSS3, JavaScript
- Bootstrap 5 (responsive UI)

**Backend**
- Python 3.x
- Flask (web framework)
- Flask-Login / Flask-Session (authentication)
- Werkzeug (password hashing)

**Database**
- MySQL
- mysql-connector-python or PyMySQL (Python–MySQL connectivity)

**AI / NLP / ML**
- Scikit-learn (TF-IDF Vectorizer, Cosine Similarity)
- NLTK or spaCy (stopword removal, tokenization, lemmatization)
- PyPDF2 / pdfplumber (PDF text extraction)
- python-docx (DOCX text extraction)
- Pandas, NumPy (data handling)

**Other tools**
- Git & GitHub (version control)
- VS Code (IDE)
- Postman (API testing, optional)

---

## 15. Software Requirements

| Requirement | Details |
|---|---|
| Operating System | Windows 10/11, Linux, or macOS |
| Programming Language | Python 3.9+ |
| Web Framework | Flask |
| Database | MySQL 8.0+ |
| IDE/Editor | VS Code / PyCharm |
| Browser | Chrome / Edge / Firefox (latest version) |
| Version Control | Git + GitHub |
| Package Manager | pip |

---

## 16. Hardware Requirements

| Component | Minimum Requirement |
|---|---|
| Processor | Intel i3 / AMD equivalent or higher |
| RAM | 4 GB minimum (8 GB recommended) |
| Storage | 500 MB free space (for project + libraries) |
| Internet | Required for installing libraries and testing |
| Display | Standard monitor (1366x768 or higher) |

*(No GPU is needed — TF-IDF and Cosine Similarity are lightweight, CPU-friendly algorithms, unlike deep learning models.)*

---

## 17. Complete Development Roadmap

**Phase 1 — Planning & Design** ✅ *(this document)*
- Requirement gathering, system design, database design, folder structure

**Phase 2 — Environment Setup**
- Install Python, Flask, MySQL, required libraries
- Set up project folder structure and Git repository
- Create MySQL database and tables

**Phase 3 — Frontend Development**
- Build static pages: landing, login, register, dashboard (HTML/CSS/Bootstrap)
- Make pages responsive

**Phase 4 — Backend & Authentication**
- Build Flask routes for registration, login, logout
- Connect Flask to MySQL
- Implement session handling and password hashing

**Phase 5 — Resume Upload & Parsing**
- Build file upload functionality
- Extract text from PDF/DOCX using PyPDF2/python-docx
- Extract basic fields (skills, education) using rule-based/regex + NLP

**Phase 6 — NLP Preprocessing**
- Clean extracted text (stopword removal, lemmatization, tokenization)
- Prepare a sample job description dataset

**Phase 7 — AI/ML Matching Engine**
- Implement TF-IDF vectorization
- Implement Cosine Similarity comparison
- Rank jobs by match score
- Implement missing-skills logic

**Phase 8 — Results & Recommendation UI**
- Display match %, top jobs, missing skills on results page
- Build resume history page

**Phase 9 — Admin Panel**
- Admin login
- Manage job listings (CRUD)
- View users and resumes
- Dashboard statistics

**Phase 10 — Testing & Debugging**
- Test all user/admin flows
- Fix bugs, edge cases (bad file formats, empty resumes, etc.)

**Phase 11 — Report Generation Feature**
- Add downloadable PDF/summary report of analysis

**Phase 12 — Final Documentation & Presentation**
- Prepare README, project report, ER diagram, PPT, and viva Q&A

---

**PHASE 1 COMPLETED**
