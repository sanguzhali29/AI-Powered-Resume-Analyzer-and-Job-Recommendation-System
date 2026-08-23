-- ==============================================================================
-- PROJECT   : AI-Powered Resume Analyzer and Job Recommendation System
-- FILE      : database/schema.sql
-- TARGET DB : MySQL 8.0+
-- TABLES    : users, resumes, skills, jobs, job_skills, recommendations, learning_resources
-- ==============================================================================

-- 1. DATABASE CREATION & SETUP
DROP DATABASE IF EXISTS resume_analyzer_db;
CREATE DATABASE resume_analyzer_db 
    CHARACTER SET utf8mb4 
    COLLATE utf8mb4_unicode_ci;

USE resume_analyzer_db;

-- ------------------------------------------------------------------------------
-- 2. USERS TABLE
-- Stores student/candidate profiles and system administrators.
-- ------------------------------------------------------------------------------
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('student', 'admin') NOT NULL DEFAULT 'student',
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_email (email)
) ENGINE=InnoDB;

-- ------------------------------------------------------------------------------
-- 3. RESUMES TABLE
-- Stores uploaded resume files, extracted plain text, and analysis metadata.
-- ------------------------------------------------------------------------------
CREATE TABLE resumes (
    resume_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    resume_title VARCHAR(150) NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    file_type VARCHAR(10) NOT NULL,
    extracted_text MEDIUMTEXT,
    extracted_skills TEXT,
    completeness_score DECIMAL(5,2) DEFAULT 0.00,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_resume_user (user_id),
    CONSTRAINT fk_resumes_user 
        FOREIGN KEY (user_id) REFERENCES users(user_id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------------------------------
-- 4. SKILLS TABLE (Master Catalog)
-- Master taxonomy of recognized technical, tool, domain, and soft skills.
-- ------------------------------------------------------------------------------
CREATE TABLE skills (
    skill_id INT AUTO_INCREMENT PRIMARY KEY,
    skill_name VARCHAR(100) NOT NULL UNIQUE,
    skill_category ENUM('programming_languages', 'frameworks', 'databases', 'tools', 'domain', 'soft_skills') NOT NULL DEFAULT 'programming_languages',
    INDEX idx_skill_name (skill_name)
) ENGINE=InnoDB;

-- ------------------------------------------------------------------------------
-- 5. JOBS TABLE
-- Stored job postings with target industry, experience level, and description.
-- ------------------------------------------------------------------------------
CREATE TABLE jobs (
    job_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(150) NOT NULL,
    company VARCHAR(100) NOT NULL DEFAULT 'TechCorp Innovations',
    industry VARCHAR(100) NOT NULL DEFAULT 'Information Technology',
    experience_level VARCHAR(50) NOT NULL DEFAULT 'Entry to Mid Level',
    salary_range VARCHAR(50) DEFAULT '6 - 12 LPA',
    description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_job_title (title)
) ENGINE=InnoDB;

-- ------------------------------------------------------------------------------
-- 6. JOB_SKILLS TABLE (Junction Table M:N)
-- Links required skills to job postings with importance weights.
-- ------------------------------------------------------------------------------
CREATE TABLE job_skills (
    job_skill_id INT AUTO_INCREMENT PRIMARY KEY,
    job_id INT NOT NULL,
    skill_id INT NOT NULL,
    importance_level ENUM('mandatory', 'important', 'good_to_have') NOT NULL DEFAULT 'mandatory',
    weight DECIMAL(3,2) NOT NULL DEFAULT 1.00,
    UNIQUE KEY uq_job_skill (job_id, skill_id),
    INDEX idx_js_job (job_id),
    INDEX idx_js_skill (skill_id),
    CONSTRAINT fk_js_job 
        FOREIGN KEY (job_id) REFERENCES jobs(job_id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    CONSTRAINT fk_js_skill 
        FOREIGN KEY (skill_id) REFERENCES skills(skill_id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------------------------------
-- 7. RECOMMENDATIONS TABLE
-- Stores AI match results, similarity percentages, and identified skill gaps.
-- ------------------------------------------------------------------------------
CREATE TABLE recommendations (
    recommendation_id INT AUTO_INCREMENT PRIMARY KEY,
    resume_id INT NOT NULL,
    job_id INT NOT NULL,
    match_percentage DECIMAL(5,2) NOT NULL,
    matched_skills TEXT,
    missing_skills TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_rec_resume (resume_id),
    INDEX idx_rec_job (job_id),
    CONSTRAINT fk_rec_resume 
        FOREIGN KEY (resume_id) REFERENCES resumes(resume_id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    CONSTRAINT fk_rec_job 
        FOREIGN KEY (job_id) REFERENCES jobs(job_id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ------------------------------------------------------------------------------
-- 8. LEARNING_RESOURCES TABLE
-- Free learning courses (YouTube, freeCodeCamp, Coursera Free, W3Schools).
-- ------------------------------------------------------------------------------
CREATE TABLE learning_resources (
    resource_id INT AUTO_INCREMENT PRIMARY KEY,
    skill_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    url VARCHAR(500) NOT NULL,
    platform ENUM('YouTube', 'freeCodeCamp', 'Coursera Free', 'W3Schools', 'Official Docs', 'GeeksforGeeks') NOT NULL,
    resource_type ENUM('Video Course', 'Interactive Tutorial', 'Documentation', 'Article') NOT NULL DEFAULT 'Video Course',
    duration_hours VARCHAR(30) DEFAULT '5-10 Hours',
    is_free BOOLEAN NOT NULL DEFAULT TRUE,
    INDEX idx_lr_skill (skill_id),
    CONSTRAINT fk_lr_skill 
        FOREIGN KEY (skill_id) REFERENCES skills(skill_id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE
) ENGINE=InnoDB;

-- ==============================================================================
-- 9. SAMPLE SEED DATA
-- ==============================================================================

-- 9.1 Seed Users (Password is 'password123' hashed with pbkdf2:sha256)
INSERT INTO users (full_name, email, password_hash, role, phone) VALUES
('Demo Student', 'student@demo.com', 'scrypt:32768:8:1$K3GgE1H7g8vX$a4b64a4d6f8c7b8d1e2f3a4b5c6d7e8f90123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef', 'student', '9876543210'),
('Admin Recruiter', 'admin@demo.com', 'scrypt:32768:8:1$K3GgE1H7g8vX$a4b64a4d6f8c7b8d1e2f3a4b5c6d7e8f90123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef', 'admin', '9988776655');

-- 9.2 Seed Skills Catalog
INSERT INTO skills (skill_name, skill_category) VALUES
-- Programming Languages
('Python', 'programming_languages'),
('Java', 'programming_languages'),
('JavaScript', 'programming_languages'),
('TypeScript', 'programming_languages'),
('C++', 'programming_languages'),
('C#', 'programming_languages'),
('Go', 'programming_languages'),
('SQL', 'programming_languages'),
-- Frameworks
('Flask', 'frameworks'),
('Django', 'frameworks'),
('FastAPI', 'frameworks'),
('React', 'frameworks'),
('Node.js', 'frameworks'),
('Express', 'frameworks'),
('Angular', 'frameworks'),
('Spring Boot', 'frameworks'),
-- Databases
('MySQL', 'databases'),
('PostgreSQL', 'databases'),
('MongoDB', 'databases'),
('Redis', 'databases'),
-- Tools & Cloud
('Git', 'tools'),
('Docker', 'tools'),
('Kubernetes', 'tools'),
('AWS', 'tools'),
('Linux', 'tools'),
('Postman', 'tools'),
-- Domain & ML
('Machine Learning', 'domain'),
('Deep Learning', 'domain'),
('Natural Language Processing', 'domain'),
('Data Analysis', 'domain'),
('REST API', 'domain'),
('Data Structures', 'domain'),
-- Soft Skills
('Communication', 'soft_skills'),
('Problem Solving', 'soft_skills'),
('Teamwork', 'soft_skills'),
('Agile', 'soft_skills');

-- 9.3 Seed Jobs
INSERT INTO jobs (title, company, industry, experience_level, salary_range, description) VALUES
('Python Backend Developer', 'CloudScale Technologies', 'Software Development', '0-2 Years (Junior/Entry)', '6.5 - 9.0 LPA', 'Responsible for designing, building, and maintaining high-performance REST APIs and backend microservices using Python, Flask/Django, MySQL, Redis, and Docker. Good knowledge of Git version control and relational database design required.'),
('Full Stack Web Developer', 'WebMatrix Solutions', 'IT Services', '1-3 Years', '7.0 - 11.0 LPA', 'Looking for a passionate Full Stack Developer skilled in React on frontend and Node.js / Flask on backend. Must have solid knowledge of JavaScript, HTML/CSS, REST APIs, MySQL/MongoDB, and Git.'),
('Data Scientist & ML Engineer', 'NeuralAI Analytics', 'Artificial Intelligence', '0-3 Years', '8.0 - 14.0 LPA', 'Exciting role for training and deploying Machine Learning and Natural Language Processing models using Python, scikit-learn, Pandas, and SQL. Hands-on experience with Data Analysis, Deep Learning, and API deployment is highly desirable.'),
('Frontend React Developer', 'PixelCraft Digital', 'Product Development', '0-2 Years', '6.0 - 8.5 LPA', 'Create responsive, interactive, and high-performance user interfaces using React, JavaScript, TypeScript, HTML/CSS, and REST API integration with modern Git workflows.'),
('DevOps & Cloud Engineer', 'InfraScale Systems', 'Cloud Infrastructure', '1-4 Years', '8.5 - 15.0 LPA', 'Manage CI/CD pipelines, container orchestration with Docker and Kubernetes, cloud architecture on AWS, and Linux infrastructure automation.'),
('Java Enterprise Developer', 'Global FinTech Corp', 'Financial Technology', '1-3 Years', '7.5 - 12.0 LPA', 'Build robust, scalable enterprise banking solutions using Java, Spring Boot, Microservices, MySQL, REST API, and Git.');

-- 9.4 Seed Job Skills Mappings
INSERT INTO job_skills (job_id, skill_id, importance_level, weight) VALUES
-- Python Backend Developer (Job 1)
(1, 1, 'mandatory', 1.00), -- Python
(1, 9, 'mandatory', 1.00), -- Flask
(1, 17, 'mandatory', 0.90), -- MySQL
(1, 21, 'important', 0.80), -- Git
(1, 22, 'important', 0.70), -- Docker
(1, 29, 'important', 0.80), -- REST API
-- Full Stack Developer (Job 2)
(2, 3, 'mandatory', 1.00), -- JavaScript
(2, 12, 'mandatory', 1.00), -- React
(2, 13, 'mandatory', 0.90), -- Node.js
(2, 17, 'important', 0.80), -- MySQL
(2, 21, 'important', 0.70), -- Git
(2, 29, 'important', 0.80), -- REST API
-- Data Scientist (Job 3)
(3, 1, 'mandatory', 1.00), -- Python
(3, 25, 'mandatory', 1.00), -- Machine Learning
(3, 27, 'mandatory', 0.90), -- NLP
(3, 28, 'important', 0.80), -- Data Analysis
(3, 8, 'important', 0.70), -- SQL
(3, 26, 'good_to_have', 0.60), -- Deep Learning
-- Frontend React Developer (Job 4)
(4, 3, 'mandatory', 1.00), -- JavaScript
(4, 12, 'mandatory', 1.00), -- React
(4, 4, 'important', 0.80), -- TypeScript
(4, 21, 'important', 0.70), -- Git
(4, 29, 'important', 0.80), -- REST API
-- DevOps Engineer (Job 5)
(5, 22, 'mandatory', 1.00), -- Docker
(5, 23, 'mandatory', 1.00), -- Kubernetes
(5, 24, 'mandatory', 1.00), -- AWS
(5, 25, 'important', 0.80), -- Linux
(5, 21, 'important', 0.80), -- Git
-- Java Developer (Job 6)
(6, 2, 'mandatory', 1.00), -- Java
(6, 16, 'mandatory', 1.00), -- Spring Boot
(6, 17, 'mandatory', 0.90), -- MySQL
(6, 29, 'important', 0.80), -- REST API
(6, 21, 'important', 0.70); -- Git

-- 9.5 Seed Free Learning Resources
INSERT INTO learning_resources (skill_id, title, url, platform, resource_type, duration_hours, is_free) VALUES
(1, 'Python for Beginners Full Course', 'https://www.youtube.com/watch?v=_uQrJ0TkZlc', 'YouTube', 'Video Course', '6 Hours', TRUE),
(1, 'Scientific Computing with Python Certification', 'https://www.freecodecamp.org/learn/scientific-computing-with-python/', 'freeCodeCamp', 'Interactive Tutorial', '30 Hours', TRUE),
(1, 'Python Tutorial - W3Schools', 'https://www.w3schools.com/python/', 'W3Schools', 'Interactive Tutorial', '10 Hours', TRUE),
(9, 'Flask Web Development Crash Course', 'https://www.youtube.com/watch?v=Z1RJmh_OwhA', 'YouTube', 'Video Course', '4 Hours', TRUE),
(9, 'Flask Official Quickstart Documentation', 'https://flask.palletsprojects.com/en/latest/quickstart/', 'Official Docs', 'Documentation', '3 Hours', TRUE),
(12, 'React.js Complete Course 2026', 'https://www.youtube.com/watch?v=bMknfKXIFA8', 'YouTube', 'Video Course', '12 Hours', TRUE),
(12, 'Front End Development Libraries (React)', 'https://www.freecodecamp.org/learn/front-end-development-libraries/', 'freeCodeCamp', 'Interactive Tutorial', '25 Hours', TRUE),
(17, 'MySQL Database Full Course for Beginners', 'https://www.youtube.com/watch?v=HXV3zeQKqGY', 'YouTube', 'Video Course', '4 Hours', TRUE),
(17, 'MySQL Tutorial by W3Schools', 'https://www.w3schools.com/mysql/', 'W3Schools', 'Interactive Tutorial', '8 Hours', TRUE),
(21, 'Git and GitHub Crash Course for Beginners', 'https://www.youtube.com/watch?v=RGOj5yH7evk', 'YouTube', 'Video Course', '2 Hours', TRUE),
(22, 'Docker Tutorial for Beginners Full Course', 'https://www.youtube.com/watch?v=3c-iBn73dDE', 'YouTube', 'Video Course', '3 Hours', TRUE),
(23, 'Kubernetes for Beginners Course', 'https://www.youtube.com/watch?v=d6WC5n9G_sM', 'YouTube', 'Video Course', '4 Hours', TRUE),
(24, 'AWS Certified Cloud Practitioner Free Training', 'https://www.freecodecamp.org/news/aws-certified-cloud-practitioner-study-course/', 'freeCodeCamp', 'Video Course', '14 Hours', TRUE),
(25, 'Machine Learning for Everybody', 'https://www.freecodecamp.org/news/machine-learning-course/', 'freeCodeCamp', 'Video Course', '4 Hours', TRUE),
(25, 'Machine Learning Introduction Specialization (Free Audit)', 'https://www.coursera.org/specializations/machine-learning-introduction', 'Coursera Free', 'Video Course', '20 Hours', TRUE),
(27, 'NLP Tutorial for Deep Learning and Text Processing', 'https://www.youtube.com/watch?v=vyOgWhwUmec', 'YouTube', 'Video Course', '5 Hours', TRUE);
