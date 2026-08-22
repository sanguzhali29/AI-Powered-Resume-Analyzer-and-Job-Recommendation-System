# AI-Powered Resume Analyzer and Job Recommendation System
### Final Year B.E. Computer Science & Engineering Academic Project

---

## 1. Project Abstract

Recruiters spend countless hours manually screening resumes, while students and job seekers struggle to understand why their applications fail Applicant Tracking Systems (ATS) or which specific skills they need to master for target roles.

This project delivers a complete, full-stack, open-source **"AI-Powered Resume Analyzer and Job Recommendation System"**. The application extracts textual content from resumes (PDF, DOCX, TXT), performs Natural Language Processing (NLP) to categorize candidate proficiencies, measures mathematical similarity against target industry benchmarks using **TF-IDF Vectorization and Cosine Similarity**, diagnoses skill gaps, computes ATS completeness scores, and generates tailored learning roadmaps with free educational resources (YouTube, freeCodeCamp, Coursera Free, W3Schools).

---

## 2. Technology Stack & Open-Source Tools

| Layer | Technologies Used | Description |
|---|---|---|
| **Backend** | Python 3.9+, Flask 3.1, Jinja2 | REST routing, MVC structure, session management, decorators |
| **Database** | MySQL 8.0+ / SQLAlchemy ORM | Relational schema with auto-fallback to SQLite |
| **NLP** | spaCy / NLTK, Regex Word-Boundaries | Section splitting, entity parsing, contact extraction |
| **Machine Learning** | Scikit-Learn (`TfidfVectorizer`, `cosine_similarity`) | Text vectorization and angular similarity matching |
| **File Parsing** | PyPDF2, python-docx | Text extraction across PDF, Word, and text documents |
| **Frontend** | HTML5, CSS3, Bootstrap 5, Chart.js, Bootstrap Icons | Responsive UI, gauges, radar/bar charts, dark/light theme |

---

## 3. System Architecture & Workflow

```
┌────────────────────────────────────────────────────────────────────────┐
│                        CANDIDATE / RECRUITER UI                        │
│   Bootstrap 5 + Jinja2 + Chart.js (Upload, Dashboard, Skill Gap, Hub)  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTP Multipart Form / JSON API
┌───────────────────────────────────▼────────────────────────────────────┐
│                       FLASK WEB SERVER (app.py)                        │
│   ├── routes/auth_routes.py       -> User/Admin Auth & Session Guard   │
│   ├── routes/resume_routes.py     -> Upload, Parse, Result Dispatch    │
│   ├── routes/job_routes.py        -> Job Catalog & Admin Management    │
│   ├── routes/dashboard_routes.py  -> Candidate & Admin Portals         │
│   └── routes/learning_routes.py   -> Free Course Recommendations       │
└──────────────────┬─────────────────────────────────┬───────────────────┘
                   │                                 │
┌──────────────────▼──────────────┐   ┌──────────────▼───────────────────┐
│     AI / NLP / ML UTILITIES     │   │      DATABASE LAYER (SQLAlchemy) │
│ - file_parser.py (PDF/DOCX)     │   │ - MySQL Database                 │
│ - nlp_extractor.py (Taxonomy)   │   │ - users, resumes, skills, jobs,  │
│ - ml_matcher.py (TF-IDF Cosine) │   │   job_skills, recommendations,   │
│ - skill_gap.py (Set Difference) │   │   learning_resources             │
│ - scoring.py (ATS Readiness)    │   └──────────────────────────────────┘
│ - learning_engine.py (Roadmap)  │
└─────────────────────────────────┘
```

---

## 4. Database Schema Structure (`database/schema.sql`)

The database consists of 7 normalized relational tables:
1. **`users`**: Stores user credentials, hashed passwords (`werkzeug.security`), and roles (`student`, `admin`).
2. **`resumes`**: Stores uploaded resume paths, extracted plain text, and ATS completeness scores.
3. **`skills`**: Master taxonomy across 6 categories (`programming_languages`, `frameworks`, `databases`, `tools`, `domain`, `soft_skills`).
4. **`jobs`**: Target job roles with company, industry, experience level, and descriptions.
5. **`job_skills`**: Junction table mapping required skills to jobs with importance levels (`mandatory`, `important`, `good_to_have`) and weights.
6. **`recommendations`**: AI match results, similarity percentages, and matched/missing skill JSON arrays.
7. **`learning_resources`**: Curated free courses with direct URLs, platform tags, and estimated duration.

---

## 5. Core Algorithms & Mathematical Formulations

### 5.1 TF-IDF (Term Frequency – Inverse Document Frequency)
Converts text documents into numerical vectors by evaluating word significance:
- **Term Frequency (TF)**: 
  $$\text{TF}(t, d) = \frac{\text{Count of term } t \text{ in document } d}{\text{Total terms in document } d}$$
- **Inverse Document Frequency (IDF)**:
  $$\text{IDF}(t, D) = \log\left(\frac{|D|}{1 + |\{d \in D : t \in d\}|}\right)$$
- **TF-IDF Weight**:
  $$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \text{IDF}(t, D)$$

### 5.2 Cosine Similarity
Measures the cosine of the angle between the resume TF-IDF vector ($\vec{A}$) and each job description vector ($\vec{B}$):
$$\text{Cosine Similarity} = \frac{\vec{A} \cdot \vec{B}}{\|\vec{A}\| \|\vec{B}\|} = \frac{\sum_{i=1}^{n} A_i B_i}{\sqrt{\sum_{i=1}^{n} A_i^2} \sqrt{\sum_{i=1}^{n} B_i^2}}$$

### 5.3 Skill Gap Analysis
Calculates the exact set difference between job requirements and candidate skills:
$$\text{Matched Skills} = \text{Candidate Skills} \cap \text{Required Job Skills}$$
$$\text{Missing Skills} = \text{Required Job Skills} \setminus \text{Candidate Skills}$$
$$\text{Readiness \%} = \left(\frac{|\text{Matched Skills}|}{|\text{Required Job Skills}|}\right) \times 100$$

---

## 6. How to Run the Application Locally

### Step 1: Clone or Navigate to Project Directory
```bash
cd "resume scanning project"
```

### Step 2: Activate Virtual Environment
```bash
# On Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# On Windows (Command Prompt)
.\venv\Scripts\activate.bat
```

### Step 3: (Optional) Setup MySQL Database
If using MySQL, create the database and import `database/schema.sql`:
```bash
mysql -u root -p < database/schema.sql
```
*(Note: If MySQL is not running, the application **automatically uses SQLite fallback**, allowing seamless zero-setup execution!)*

### Step 4: Run the Application
```bash
python app.py
```

### Step 5: Open in Web Browser
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

### Demo Accounts for Viva / Testing:
- **Student Account**: `student@demo.com` | Password: `password123`
- **Admin Account**: `admin@demo.com` | Password: `admin123`

---

## 7. Project Viva & Defense Questions and Answers

**Q1: What is the main objective of this project?**
> **Answer**: To build an automated system that extracts skills and experience from resumes using NLP, matches candidates to target jobs using TF-IDF and Cosine Similarity, highlights missing skills through skill gap analysis, and recommends free learning resources.

**Q2: Why did you choose TF-IDF and Cosine Similarity over Deep Learning?**
> **Answer**: TF-IDF and Cosine Similarity are computationally lightweight, deterministic, explainable, and run in real-time on standard CPU hardware without needing massive labeled training datasets or expensive GPU infrastructure.

**Q3: How do you prevent false positive skill matches (e.g. 'C' matching 'CSS')?**
> **Answer**: We use regex lookaround word boundaries (`(?<![a-zA-Z0-9])term(?![a-zA-Z0-9])`) along with canonical taxonomy lookup to ensure only isolated, exact skill occurrences match.

**Q4: How does the system calculate the ATS Completeness Score?**
> **Answer**: It evaluates 5 structural dimensions: Contact info (20 pts), Skills volume & diversity (30 pts), Education (15 pts), Experience (20 pts), and Projects (15 pts), totaling 100 points.

**Q5: How are missing skills prioritized in the learning roadmap?**
> **Answer**: By calculating global market demand frequency across all jobs in the database. Missing skills requested by multiple job roles are given higher study priority.
