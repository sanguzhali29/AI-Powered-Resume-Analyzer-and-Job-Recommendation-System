# AI-Based Resume Analyzer & Job Recommendation System
### Final Year Project Documentation (BE-CSE)

---

## 1. Abstract

Finding the right job and the right candidate is a difficult task in today's competitive world. Recruiters receive hundreds of resumes for a single job post, and manually checking each resume takes a lot of time. On the other side, job seekers often do not know which skills they are missing for their dream job.

This project, "AI-Based Resume Analyzer & Job Recommendation System," solves this problem using Artificial Intelligence and Natural Language Processing (NLP). The system reads a resume (PDF/DOCX), extracts important information such as skills, education, and experience, and compares it with job descriptions using text similarity techniques like TF-IDF and Cosine Similarity. Based on this comparison, the system recommends the most suitable jobs to the candidate and also shows the skill gap between the candidate's resume and the required job skills.

This system helps job seekers improve their resumes and choose the right job, and it helps recruiters shortlist candidates faster and more accurately.

---

## 2. Introduction

Every year, millions of students and professionals apply for jobs. The traditional method of resume screening is manual, slow, and prone to human error. Recruiters may miss good candidates simply because they do not have time to read every resume carefully.

Artificial Intelligence and Machine Learning have made it possible to automate this process. By using Natural Language Processing (NLP), a computer can "read" and "understand" a resume just like a human, extract meaningful data from it, and match it with the requirements of a job.

This project builds a web-based system where a user uploads their resume, and the system automatically:
- Extracts skills, education, and experience from the resume
- Compares the resume with a set of job descriptions
- Recommends the best-matching jobs
- Shows which skills are missing for a particular job

This makes the job search process smarter, faster, and more personalized.

---

## 3. Problem Statement

- Job seekers do not know how well their resume matches a job posting.
- Candidates are unaware of the skills they need to learn to become eligible for a job.
- Recruiters spend a large amount of time manually screening resumes.
- Manual screening can be biased and inconsistent.
- There is no easy tool that connects resume analysis with automatic job recommendation.

There is a need for an intelligent system that can analyze a resume, match it with suitable jobs, and highlight the skill gap — all automatically.

---

## 4. Existing System

In the current/traditional system:
- Recruiters manually read and shortlist resumes, which is time-consuming.
- Job portals show jobs based only on keyword search entered by the user, not based on actual resume content.
- There is no automatic skill gap analysis for candidates.
- Existing Applicant Tracking Systems (ATS) mostly perform simple keyword matching without understanding meaning or context.
- Job recommendations are generic and not personalized to the candidate's actual profile.

**Drawbacks of Existing System:**
- Time-consuming and manual effort
- Less accurate matching
- No skill gap feedback for candidates
- No ranking of jobs based on resume-job similarity

---

## 5. Proposed System

The proposed system automates resume analysis and job recommendation using AI/NLP techniques.

**Key Features:**
- Upload resume (PDF/DOCX) and extract text automatically
- Extract skills, education, experience using NLP techniques
- Compare resume with job descriptions using TF-IDF and Cosine Similarity
- Recommend top matching jobs with a similarity/match score
- Show skill gap report (skills present vs skills required)
- Simple and user-friendly web interface

This system saves time for both job seekers and recruiters and gives personalized, data-driven recommendations instead of simple keyword search.

---

## 6. Objectives

1. To design a system that can automatically extract information from resumes.
2. To apply NLP techniques (TF-IDF, Cosine Similarity) for resume-job matching.
3. To recommend the most suitable jobs based on resume content.
4. To identify and display the skill gap for each recommended job.
5. To build a simple and easy-to-use web application for both job seekers and recruiters.
6. To reduce the manual effort involved in resume screening.

---

## 7. Scope

- The system works for resumes in PDF and DOCX formats.
- It focuses on technical/IT job roles (can be extended to other domains).
- It matches resumes with a stored dataset of job descriptions.
- It provides skill gap analysis only for the skills mentioned in the job description.
- The system can be extended in the future to support real-time job portal APIs, multiple languages, and more advanced deep learning models.

---

## 8. System Requirements

The system requires a computer with internet browser access, a backend server to run the AI/NLP model, and a database to store resumes, job data, and results.

---

## 9. Software Requirements

| Component | Requirement |
|---|---|
| Operating System | Windows 10/11 or Linux |
| Programming Language | Python 3.x |
| Web Framework | Flask / Django |
| Frontend | HTML, CSS, JavaScript, Bootstrap |
| NLP Libraries | NLTK, spaCy, Scikit-learn |
| Resume Parsing | PyPDF2 / pdfplumber, python-docx |
| Database | MySQL / SQLite |
| IDE | VS Code / PyCharm |
| Version Control | Git, GitHub |

---

## 10. Hardware Requirements

| Component | Minimum Requirement |
|---|---|
| Processor | Intel i3 or above |
| RAM | 4 GB (8 GB recommended) |
| Hard Disk | 100 GB or more |
| Display | Standard monitor |
| Internet | Required for setup and deployment |

---

## 11. System Architecture

The system follows a layered architecture:

```
 ┌───────────────────────┐
 │   User Interface       │  (Web Browser - Upload Resume)
 └──────────┬─────────────┘
            │
 ┌──────────▼─────────────┐
 │   Application Layer     │  (Flask/Django Server)
 │  - Resume Upload Handler│
 │  - Text Extraction      │
 │  - NLP Processing Engine│
 │  - Matching Engine      │
 └──────────┬─────────────┘
            │
 ┌──────────▼─────────────┐
 │   AI/ML Module           │
 │  - TF-IDF Vectorizer     │
 │  - Cosine Similarity     │
 │  - Skill Gap Analyzer    │
 └──────────┬─────────────┘
            │
 ┌──────────▼─────────────┐
 │   Database               │
 │  - Resume Data           │
 │  - Job Data               │
 │  - Results/Reports        │
 └───────────────────────┘
```

The user uploads a resume through the interface. The application layer extracts text and sends it to the AI/ML module, which processes the text, compares it with job data, and returns recommendations and skill gap reports, which are then stored and displayed to the user.

---

## 12. Module Description

**1. Resume Upload Module**
Allows the user to upload a resume file (PDF/DOCX) through the web interface.

**2. Text Extraction Module**
Extracts raw text from the uploaded resume using libraries like PyPDF2/pdfplumber and python-docx.

**3. Information Extraction Module (NLP)**
Extracts specific details such as name, email, phone number, skills, education, and experience using NLP techniques (tokenization, keyword matching, Named Entity Recognition).

**4. Job Matching Module**
Converts resume text and job descriptions into numeric vectors using TF-IDF, then calculates Cosine Similarity to rank jobs by match score.

**5. Skill Gap Analysis Module**
Compares the skills present in the resume with the skills required for a job and lists the missing skills.

**6. Recommendation Module**
Displays the top matching jobs sorted by similarity score, along with the skill gap report.

**7. Admin Module**
Allows the admin to add/update/delete job descriptions in the database.

**8. User Dashboard Module**
Displays results, resume history, and recommended jobs to the logged-in user.

---

## 13. Database Design

**Main Tables:**

**Users Table**
| Field | Type |
|---|---|
| user_id (PK) | INT |
| name | VARCHAR |
| email | VARCHAR |
| password | VARCHAR |

**Resume Table**
| Field | Type |
|---|---|
| resume_id (PK) | INT |
| user_id (FK) | INT |
| resume_text | TEXT |
| skills | TEXT |
| education | TEXT |
| experience | TEXT |
| upload_date | DATETIME |

**Job Table**
| Field | Type |
|---|---|
| job_id (PK) | INT |
| job_title | VARCHAR |
| job_description | TEXT |
| required_skills | TEXT |
| company_name | VARCHAR |

**Match Result Table**
| Field | Type |
|---|---|
| result_id (PK) | INT |
| resume_id (FK) | INT |
| job_id (FK) | INT |
| match_score | FLOAT |
| missing_skills | TEXT |

---

## 14. ER Diagram Explanation

The Entity-Relationship (ER) diagram shows the relationship between entities:

- **User** (1) — (Many) **Resume**: One user can upload multiple resumes.
- **Resume** (1) — (Many) **Match Result**: One resume can be matched with many jobs.
- **Job** (1) — (Many) **Match Result**: One job can be matched with many resumes.

So, **Match Result** acts as a bridge table connecting **Resume** and **Job** with attributes like match_score and missing_skills. This is a many-to-many relationship between Resume and Job, resolved using the Match Result table.

---

## 15. Data Flow Diagram (DFD) Explanation

**DFD Level 0 (Context Diagram):**
User → [Resume Analyzer System] → Job Recommendations + Skill Gap Report

**DFD Level 1:**
1. User uploads resume → Text Extraction process → Extracted Text
2. Extracted Text → NLP Processing → Skills, Education, Experience
3. Extracted Skills + Job Database → Matching Engine (TF-IDF + Cosine Similarity) → Match Scores
4. Match Scores → Ranking → Top Job Recommendations
5. Extracted Skills vs Job Required Skills → Skill Gap Analysis → Missing Skills Report
6. Final Output → Displayed on User Dashboard

Each process takes input, transforms it, and passes the output to the next process, finally giving the user a personalized job recommendation and skill gap report.

---

## 16. AI/ML Methodology

The core AI methodology used in this project is **Natural Language Processing (NLP)** combined with **Information Retrieval techniques**:

1. **Text Preprocessing**: Cleaning resume and job text (lowercasing, removing stopwords, punctuation, tokenization, lemmatization).
2. **Feature Extraction**: Using TF-IDF to convert text into numeric vectors.
3. **Similarity Calculation**: Using Cosine Similarity to measure how close a resume is to a job description.
4. **Ranking**: Jobs are ranked based on similarity score (highest first).
5. **Skill Gap Detection**: Comparing skill sets using set difference (required skills − candidate skills).

This methodology does not require deep learning or huge datasets, making it lightweight, fast, and suitable for a final-year project, while still giving accurate and meaningful results.

---

## 17. TF-IDF Explanation

**TF-IDF** stands for **Term Frequency – Inverse Document Frequency**. It is a technique to convert text into numbers so that a computer can process it.

- **Term Frequency (TF)**: How many times a word appears in a document.
  TF = (Number of times word appears in document) / (Total words in document)

- **Inverse Document Frequency (IDF)**: How rare or common a word is across all documents. Common words like "the," "and" get a low score; rare, important words like "Python," "Machine Learning" get a high score.
  IDF = log(Total number of documents / Number of documents containing the word)

- **TF-IDF = TF × IDF**

In this project, both the resume text and job description text are converted into TF-IDF vectors. Important skill-related words get higher weight, while common words get lower weight, making the comparison meaningful.

---

## 18. Cosine Similarity Explanation

**Cosine Similarity** measures how similar two text documents are, by calculating the angle between their TF-IDF vectors.

Formula:
```
Cosine Similarity = (A · B) / (||A|| × ||B||)
```
Where A and B are the TF-IDF vectors of the resume and the job description.

- The similarity score ranges from **0 to 1**.
- A score close to **1** means the resume and job are very similar (good match).
- A score close to **0** means they are very different (poor match).

In this project, the resume vector is compared with every job vector in the database, and jobs are sorted in descending order of similarity score to recommend the best matches first.

---

## 19. Skill Gap Methodology

Skill gap analysis identifies which skills the candidate is missing for a particular job.

**Steps:**
1. Extract the list of skills from the resume (Resume_Skills).
2. Extract the list of required skills from the job description (Job_Skills).
3. Calculate missing skills using set difference:
   ```
   Missing_Skills = Job_Skills − Resume_Skills
   ```
4. Display the missing skills to the user as a "Skill Gap Report."
5. Optionally, suggest online courses or resources for each missing skill.

This helps the candidate understand exactly what to learn to become eligible for their desired job.

---

## 20. Implementation

**Implementation Steps:**
1. Set up the Flask/Django project and configure the database.
2. Build the resume upload interface (HTML/CSS/Bootstrap form).
3. Implement text extraction using PyPDF2/pdfplumber for PDF and python-docx for Word files.
4. Implement NLP-based information extraction (skills, education, experience) using regex and spaCy/NLTK.
5. Build a job dataset (CSV or database table) with job titles, descriptions, and required skills.
6. Implement TF-IDF vectorization using Scikit-learn's `TfidfVectorizer`.
7. Implement Cosine Similarity calculation using `cosine_similarity` from Scikit-learn.
8. Rank jobs by similarity score and display the top N recommendations.
9. Implement skill gap logic using set operations.
10. Design the results dashboard to display recommended jobs and missing skills.
11. Test the complete system with sample resumes and job data.

**Sample Code Snippet (Matching Logic):**
```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

documents = [resume_text] + job_descriptions
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(documents)

similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
ranked_jobs = similarity_scores.argsort()[0][::-1]
```

---

## 21. Testing

| Test Case | Input | Expected Output | Result |
|---|---|---|---|
| Upload valid PDF resume | resume.pdf | Text extracted successfully | Pass |
| Upload unsupported file | resume.txt | Error message shown | Pass |
| Resume with no skills section | Blank skills | System shows "No skills found" | Pass |
| Match resume with jobs | Sample resume | Ranked job list with scores | Pass |
| Skill gap calculation | Resume vs job skills | Correct missing skills shown | Pass |
| Login with wrong password | Invalid credentials | Access denied message | Pass |
| Multiple resume uploads | 2 resumes, same user | Both stored separately | Pass |

**Types of Testing Used:**
- Unit Testing (each module tested individually)
- Integration Testing (modules tested together)
- System Testing (complete workflow tested end-to-end)
- User Acceptance Testing (tested with sample users)

---

## 22. Results

- The system successfully extracts text and skills from resumes with high accuracy for well-formatted resumes.
- Job recommendations are shown ranked by match score (e.g., Job A – 82%, Job B – 75%, Job C – 68%).
- The skill gap report correctly lists missing skills for each recommended job.
- The system significantly reduces the manual effort of comparing resumes with job requirements.
- Average processing time per resume is a few seconds, showing the system is efficient for practical use.

*(Screenshots of the upload page, results dashboard, and skill gap report should be added here in the final report.)*

---

## 23. Advantages

- Saves time for both recruiters and job seekers.
- Provides personalized and accurate job recommendations.
- Helps candidates identify and fill skill gaps.
- Reduces human bias in resume screening.
- Simple, lightweight, and easy to deploy.
- Can be scaled to handle a large number of resumes and jobs.

---

## 24. Limitations

- Accuracy depends on how well-structured and clearly written the resume is.
- Works best for text-based PDFs; scanned/image resumes need OCR (not included by default).
- Currently supports mainly technical/IT job roles.
- TF-IDF is a keyword/statistics-based method; it does not fully understand context or synonyms (e.g., "ML" vs "Machine Learning") unless handled separately.
- Requires a good, updated job dataset to give accurate recommendations.

---

## 25. Future Enhancement

- Use advanced NLP models like BERT or Word2Vec for better semantic understanding.
- Add OCR support for scanned/image-based resumes.
- Integrate with real job portals (LinkedIn, Naukri, Indeed) using APIs for live job data.
- Add a course/certification recommendation system for missing skills.
- Build a recruiter-side dashboard for bulk resume screening.
- Add multi-language resume support.
- Deploy the system on cloud platforms (AWS/Azure) for public use.

---

## 26. Conclusion

The "AI-Based Resume Analyzer & Job Recommendation System" successfully demonstrates how Artificial Intelligence and NLP techniques like TF-IDF and Cosine Similarity can be used to automate resume screening and job matching. The system helps job seekers find suitable jobs and understand their skill gaps, while helping recruiters save time in the shortlisting process. This project can be further improved using advanced deep learning techniques and can be extended into a full-scale job portal solution.

---

## 27. References

1. Scikit-learn Documentation – https://scikit-learn.org
2. NLTK Documentation – https://www.nltk.org
3. spaCy Documentation – https://spacy.io
4. Flask Documentation – https://flask.palletsprojects.com
5. "Introduction to Information Retrieval" – Manning, Raghavan, Schütze
6. Research papers on Resume Parsing and NLP-based Job Matching (IEEE/Google Scholar)
7. Python official documentation – https://docs.python.org

*(Note: I don't have access to live search or a database, so please verify these reference links and any external citations before including them in your final submission, as they may need updating or correction.)*

---

# PPT Structure (15 Slides)

1. **Title Slide** – Project title, student name, guide name, college, department
2. **Introduction** – Brief overview of the project
3. **Problem Statement** – Why this project is needed
4. **Existing System** – Current methods and their drawbacks
5. **Proposed System** – What this project offers
6. **Objectives** – Goals of the project
7. **Scope** – What the project covers
8. **System Architecture** – Architecture diagram
9. **Module Description** – Overview of each module
10. **AI/ML Methodology** – TF-IDF and Cosine Similarity explained simply
11. **Database Design / ER Diagram** – Table structure and relationships
12. **Implementation Screenshots** – Upload page, results, skill gap report
13. **Testing & Results** – Test cases and outcomes
14. **Advantages, Limitations & Future Scope**
15. **Conclusion & Thank You / Q&A Slide**

---

# Demo Explanation (What to Show During Demo)

1. Open the web application home page.
2. Register/Login as a user.
3. Upload a sample resume (PDF/DOCX).
4. Show the extracted information — skills, education, experience.
5. Click "Find Matching Jobs" and show the ranked list of recommended jobs with match scores.
6. Click on a job to show the Skill Gap Report (skills present vs skills missing).
7. Show the admin panel where job descriptions can be added/updated.
8. Summarize by explaining how TF-IDF and Cosine Similarity worked behind the scenes to produce these results.

---

# Project Viva Questions and Answers

**Q1. What is the main aim of your project?**
A: To automatically analyze a resume and recommend the most suitable jobs using AI/NLP techniques, and to show the skill gap for each recommended job.

**Q2. What algorithms did you use?**
A: TF-IDF (Term Frequency-Inverse Document Frequency) for converting text to numeric vectors, and Cosine Similarity for measuring the similarity between the resume and job descriptions.

**Q3. Why did you choose TF-IDF instead of deep learning models?**
A: TF-IDF is simple, fast, does not require large training data or GPUs, and gives good results for keyword/skill-based matching, which is suitable for a final-year project.

**Q4. What is Cosine Similarity?**
A: It measures the similarity between two text vectors by calculating the cosine of the angle between them. A value close to 1 means high similarity, and close to 0 means low similarity.

**Q5. How does your system extract text from a resume?**
A: Using libraries like PyPDF2/pdfplumber for PDF files and python-docx for Word files, which read the file and extract raw text.

**Q6. How do you calculate skill gap?**
A: By comparing the skills required for a job with the skills present in the resume and finding the skills that are in the job requirement but not in the resume (set difference).

**Q7. What is the difference between TF and IDF?**
A: TF measures how frequently a word appears in a document. IDF measures how rare or important a word is across all documents. Multiplying them gives more weight to important, less common words.

**Q8. What database did you use and why?**
A: MySQL/SQLite, because it is reliable, easy to use, and suitable for storing structured data like users, resumes, and job listings.

**Q9. Can your system handle scanned/image resumes?**
A: Not currently — it works with text-based PDFs and DOCX files. OCR support can be added as a future enhancement for scanned resumes.

**Q10. What are the limitations of TF-IDF?**
A: It is a keyword-based, statistical method and does not understand meaning or context. For example, it may not recognize that "ML" and "Machine Learning" mean the same thing unless handled separately.

**Q11. How is this project useful in real life?**
A: It saves time for recruiters screening resumes, and it helps job seekers understand which jobs suit them and what skills they need to improve.

**Q12. What is the future scope of this project?**
A: Using advanced models like BERT for better context understanding, adding OCR, integrating live job portal APIs, and adding a course recommendation feature.

---

# 2-Minute Project Explanation

"My project is called the AI-Based Resume Analyzer and Job Recommendation System. Its goal is to help job seekers by automatically analyzing their resume and recommending the best-matching jobs, using Artificial Intelligence.

In today's world, recruiters get hundreds of resumes for one job, and manually checking each one takes a lot of time. On the other hand, job seekers often don't know which jobs suit their skills or what skills they are missing.

My system solves both problems. The user uploads their resume in PDF or Word format. The system extracts the text and identifies important details like skills, education, and experience using Natural Language Processing. Then, using a technique called TF-IDF, both the resume and a set of job descriptions are converted into numeric vectors. I use Cosine Similarity to compare these vectors and calculate a match score between the resume and each job. The jobs are then ranked and shown to the user, with the best match on top.

The system also performs skill gap analysis — it compares the skills required for a job with the skills already in the resume, and shows the candidate exactly which skills they are missing.

This project makes the job search process faster, smarter, and more personalized, and it can also help recruiters shortlist candidates more efficiently."

---

# 5-Minute Project Explanation

"Good [morning/afternoon], my project is titled 'AI-Based Resume Analyzer and Job Recommendation System.'

**Problem:** Today, job seekers apply to many jobs without knowing how well their resume actually matches the job requirements. At the same time, recruiters receive a huge number of resumes for every job opening, and manually going through each one is slow, tiring, and often inconsistent. Existing job portals mostly rely on simple keyword search, which does not truly understand the content of a resume.

**Solution — My Proposed System:** I built a system that uses Artificial Intelligence, specifically Natural Language Processing, to automatically read a resume and match it intelligently with available job descriptions.

**How it works:**
First, the user uploads their resume in PDF or DOCX format. My system extracts the raw text using libraries like PyPDF2 and python-docx, and then uses NLP techniques to pull out important information — the candidate's skills, education, and work experience.

Next comes the core AI part. I use a technique called TF-IDF, which stands for Term Frequency-Inverse Document Frequency. This method converts text into numbers by giving higher importance to meaningful and rare words — like specific technical skills — and lower importance to common words like 'the' or 'and.' Both the resume and every job description in my database are converted into these TF-IDF vectors.

Then, I use Cosine Similarity to compare the resume vector with each job vector. This gives a similarity score between 0 and 1 for every job — the higher the score, the better the match. The system then ranks all the jobs and displays the top matches to the user, along with their match percentage.

In addition to job recommendation, my system also performs Skill Gap Analysis. It compares the skills required for a specific job with the skills already present in the resume, and clearly shows which skills the candidate is missing. This is very useful because it tells the candidate exactly what they need to learn to become eligible for that job.

**Architecture:** The system has a simple layered architecture — a user interface built with HTML, CSS and Bootstrap; an application layer built using Flask, which handles resume upload and processing; an AI/ML module that does the TF-IDF and Cosine Similarity calculations; and a database that stores user data, resumes, jobs, and results.

**Testing and Results:** I tested the system with multiple sample resumes and job descriptions. It successfully extracted relevant information, produced ranked job recommendations with meaningful match scores, and generated accurate skill gap reports.

**Advantages:** This system saves significant time for both job seekers and recruiters, gives personalized recommendations instead of generic keyword search results, and helps reduce human bias in resume screening.

**Limitations:** Since I used TF-IDF, which is a statistical, keyword-based method, it doesn't fully understand context or synonyms. Also, it currently works only with text-based resumes, not scanned images.

**Future Scope:** In the future, this project can be improved by using advanced deep learning models like BERT for better semantic understanding, adding OCR for scanned resumes, integrating with real job portals through APIs, and adding a course recommendation feature for the missing skills.

**Conclusion:** Overall, this project shows how AI and NLP can make the job search and recruitment process faster, smarter, and more effective for everyone involved. Thank you."

---

**PROJECT COMPLETED**
