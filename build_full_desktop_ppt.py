"""
Advanced Visual PowerPoint Presentation Generator
=================================================
Generates high-resolution architecture diagrams, charts, and flowcharts,
and embeds them into a 16:9 widescreen presentation saved directly to the Desktop.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

os.makedirs("ppt_assets", exist_ok=True)

# -----------------------------------------------------------------------------
# 1. GENERATE VISUAL DIAGRAM IMAGES USING MATPLOTLIB
# -----------------------------------------------------------------------------

# Diagram 1: System Architecture Flowchart
def generate_architecture_diagram():
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis('off')
    fig.patch.set_facecolor('#0f172a')

    # Layer 1: Client
    rect1 = patches.FancyBboxPatch((0.5, 3.2), 2.4, 1.4, boxstyle="round,pad=0.2", fc='#1e293b', ec='#3b82f6', lw=2)
    ax.add_patch(rect1)
    ax.text(1.7, 4.1, "1. USER INTERFACE", color='#60a5fa', fontsize=11, fontweight='bold', ha='center')
    ax.text(1.7, 3.6, "• PDF/DOCX Resume Upload\n• Responsive Dashboard\n• Bootstrap 5 / Jinja2", color='#e2e8f0', fontsize=9, ha='center')

    # Arrow 1 -> 2
    ax.annotate('', xy=(3.5, 3.9), xytext=(2.9, 3.9), arrowprops=dict(arrowstyle="->", color='#3b82f6', lw=2.5))

    # Layer 2: NLP Parsing
    rect2 = patches.FancyBboxPatch((3.7, 3.2), 2.6, 1.4, boxstyle="round,pad=0.2", fc='#1e293b', ec='#10b981', lw=2)
    ax.add_patch(rect2)
    ax.text(5.0, 4.1, "2. NLP PARSER & NER", color='#34d399', fontsize=11, fontweight='bold', ha='center')
    ax.text(5.0, 3.6, "• PyPDF2 / python-docx\n• 6-Category Skill Extraction\n• ATS Completeness Score", color='#e2e8f0', fontsize=9, ha='center')

    # Arrow 2 -> 3
    ax.annotate('', xy=(6.9, 3.9), xytext=(6.3, 3.9), arrowprops=dict(arrowstyle="->", color='#10b981', lw=2.5))

    # Layer 3: ML Matching
    rect3 = patches.FancyBboxPatch((7.1, 3.2), 2.4, 1.4, boxstyle="round,pad=0.2", fc='#1e293b', ec='#8b5cf6', lw=2)
    ax.add_patch(rect3)
    ax.text(8.3, 4.1, "3. ML MATCH ENGINE", color='#c084fc', fontsize=11, fontweight='bold', ha='center')
    ax.text(8.3, 3.6, "• TF-IDF Vectorizer\n• Cosine Similarity (0-100%)\n• Ranked Job Recommender", color='#e2e8f0', fontsize=9, ha='center')

    # Bottom Arrow down from 3 to 4 & 5
    ax.annotate('', xy=(8.3, 2.3), xytext=(8.3, 3.2), arrowprops=dict(arrowstyle="->", color='#8b5cf6', lw=2.5))

    # Layer 4: Skill Gap & Free Courses
    rect4 = patches.FancyBboxPatch((5.5, 0.5), 4.0, 1.4, boxstyle="round,pad=0.2", fc='#1e293b', ec='#f59e0b', lw=2)
    ax.add_patch(rect4)
    ax.text(7.5, 1.4, "4. SKILL GAP & FREE LEARNING HUB", color='#fbbf24', fontsize=11, fontweight='bold', ha='center')
    ax.text(7.5, 0.9, "• Missing Skills = Required - Candidate\n• Market Demand Prioritization\n• YouTube / freeCodeCamp / W3Schools", color='#e2e8f0', fontsize=9, ha='center')

    # Layer 5: Database
    rect5 = patches.FancyBboxPatch((0.5, 0.5), 4.2, 1.4, boxstyle="round,pad=0.2", fc='#1e293b', ec='#06b6d4', lw=2)
    ax.add_patch(rect5)
    ax.text(2.6, 1.4, "5. DATABASE LAYER (MySQL 8.0+)", color='#22d3ee', fontsize=11, fontweight='bold', ha='center')
    ax.text(2.6, 0.9, "• SQLAlchemy ORM (SQLite Fallback)\n• Users, Resumes, Skills, Jobs,\n  Recommendations, Learning Resources", color='#e2e8f0', fontsize=9, ha='center')

    # Arrow 5 <-> 4
    ax.annotate('', xy=(4.7, 1.2), xytext=(5.5, 1.2), arrowprops=dict(arrowstyle="<->", color='#06b6d4', lw=2.5))

    plt.tight_layout()
    img_path = "ppt_assets/architecture_diagram.png"
    plt.savefig(img_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    return img_path

# Diagram 2: TF-IDF & Cosine Similarity Concept Graphic
def generate_tfidf_diagram():
    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis('off')
    fig.patch.set_facecolor('#0f172a')

    # Title Banner
    ax.text(5.0, 4.6, "TF-IDF Vector Space & Cosine Similarity Angle (Theta)", color='#60a5fa', fontsize=12, fontweight='bold', ha='center')

    # Vector A (Resume)
    ax.annotate('', xy=(7.0, 3.8), xytext=(2.0, 1.5), arrowprops=dict(arrowstyle="-|>", color='#10b981', lw=3.5))
    ax.text(7.2, 3.9, "Vector A: Candidate Resume (TF-IDF)", color='#34d399', fontsize=10, fontweight='bold')

    # Vector B (Job Description)
    ax.annotate('', xy=(7.8, 2.3), xytext=(2.0, 1.5), arrowprops=dict(arrowstyle="-|>", color='#3b82f6', lw=3.5))
    ax.text(8.0, 2.3, "Vector B: Job Description (TF-IDF)", color='#60a5fa', fontsize=10, fontweight='bold')

    # Angle Arc
    arc = patches.Arc((2.0, 1.5), 3.0, 3.0, angle=0, theta1=10, theta2=25, color='#f59e0b', lw=2.5)
    ax.add_patch(arc)
    ax.text(3.7, 2.0, "Small Angle θ -> Cos(θ) ≈ 1.0 (High Match %)", color='#fbbf24', fontsize=9, fontweight='bold')

    # Formula Box
    formula_box = patches.FancyBboxPatch((1.0, 0.3), 8.0, 0.9, boxstyle="round,pad=0.2", fc='#1e293b', ec='#8b5cf6', lw=1.5)
    ax.add_patch(formula_box)
    ax.text(5.0, 0.75, "Cosine Similarity = (A · B) / (||A|| × ||B||)  =  Sum(Ai * Bi) / (Sqrt(Sum(Ai^2)) * Sqrt(Sum(Bi^2)))", color='#f8fafc', fontsize=10, fontweight='bold', ha='center')

    plt.tight_layout()
    img_path = "ppt_assets/tfidf_diagram.png"
    plt.savefig(img_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    return img_path

# Diagram 3: ATS Completeness Scoring Breakdown
def generate_ats_chart():
    fig, ax = plt.subplots(figsize=(6, 4.5), dpi=300)
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#0f172a')

    categories = ['Contact Info\n(Email/Phone)', 'Skills Diversity\n(6 Categories)', 'Education\n(Degrees/CGPA)', 'Experience\n(Work/Intern)', 'Projects &\nPortfolio']
    weights = [20, 30, 15, 20, 15]
    colors = ['#3b82f6', '#10b981', '#06b6d4', '#f59e0b', '#8b5cf6']

    bars = ax.barh(categories, weights, color=colors, height=0.55, edgecolor='none')
    ax.set_xlim(0, 35)
    ax.set_xlabel('Maximum Weightage (Points / 100%)', color='#94a3b8', fontsize=9, fontweight='bold')
    ax.tick_params(colors='#e2e8f0', labelsize=8)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.grid(axis='x', color='#334155', linestyle='--', alpha=0.7)

    for bar in bars:
        w = bar.get_width()
        ax.text(w + 0.8, bar.get_y() + bar.get_height()/2, f"{int(w)}%", color='#ffffff', va='center', fontsize=9, fontweight='bold')

    ax.set_title("5-Dimension ATS Completeness Score (100 Points)", color='#60a5fa', fontsize=11, fontweight='bold', pad=12)
    plt.tight_layout()
    img_path = "ppt_assets/ats_chart.png"
    plt.savefig(img_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    return img_path


# -----------------------------------------------------------------------------
# 2. BUILD THE PRESENTATION DECK (.PPTX)
# -----------------------------------------------------------------------------
def build_deck():
    arch_img = generate_architecture_diagram()
    tfidf_img = generate_tfidf_diagram()
    ats_img = generate_ats_chart()

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    DARK_BLUE = RGBColor(15, 23, 42)     # #0f172a
    ACCENT_BLUE = RGBColor(59, 130, 246) # #3b82f6
    TEXT_WHITE = RGBColor(255, 255, 255)
    TEXT_MUTED = RGBColor(148, 163, 184) # #94a3b8
    TEXT_DARK = RGBColor(30, 41, 59)     # #1e293b
    BG_LIGHT = RGBColor(248, 250, 252)   # #f8fafc
    GREEN = RGBColor(16, 185, 129)
    CARD_BG = RGBColor(255, 255, 255)

    blank_layout = prs.slide_layouts[6]

    def set_bg(slide, color):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = color

    def add_header(slide, title, category="FINAL YEAR B.E. CSE PROJECT"):
        set_bg(slide, BG_LIGHT)
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_cat = tf.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_BLUE

        p_title = tf.add_paragraph()
        p_title.text = title
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = DARK_BLUE

    # -------------------------------------------------------------
    # SLIDE 1: Title Slide (Dark Theme)
    # -------------------------------------------------------------
    slide1 = prs.slides.add_slide(blank_layout)
    set_bg(slide1, DARK_BLUE)

    tbox1 = slide1.shapes.add_textbox(Inches(1.0), Inches(1.3), Inches(11.333), Inches(4.8))
    tf1 = tbox1.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "FINAL YEAR ACADEMIC PROJECT (B.E. COMPUTER SCIENCE & ENGINEERING)"
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = ACCENT_BLUE
    p0.alignment = PP_ALIGN.CENTER

    p1 = tf1.add_paragraph()
    p1.text = "AI-Powered Resume Analyzer and\nJob Recommendation System"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE
    p1.alignment = PP_ALIGN.CENTER

    p2 = tf1.add_paragraph()
    p2.text = "Automated NLP Parsing, TF-IDF Job Matching, Skill Gap Analysis & Free Learning Roadmaps"
    p2.font.size = Pt(15)
    p2.font.color.rgb = TEXT_MUTED
    p2.alignment = PP_ALIGN.CENTER

    p3 = tf1.add_paragraph()
    p3.text = "\nPresented by: Final Year CSE Students   |   Guided by: Project Guide / Dept. of CSE"
    p3.font.size = Pt(14)
    p3.font.bold = True
    p3.font.color.rgb = GREEN
    p3.alignment = PP_ALIGN.CENTER

    # -------------------------------------------------------------
    # SLIDE 2: Project Overview & Abstract
    # -------------------------------------------------------------
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "1. Project Overview & Abstract")

    tb2 = slide2.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    tf2 = tb2.text_frame
    tf2.word_wrap = True

    points2 = [
        "• The Challenge in Recruitment: Recruiters receive hundreds of resumes per job posting. Manual screening is slow, inconsistent, and highly labor-intensive.",
        "• The Applicant Dilemma: Job seekers face automated Applicant Tracking System (ATS) rejections without understanding why their profile failed or which skills they lack.",
        "• Proposed Solution: An intelligent, full-stack open-source web platform built with Python Flask, MySQL, and Scikit-Learn that automates end-to-end resume screening and career recommendation.",
        "• Explainable AI Engine: Uses Natural Language Processing (NLP) for entity parsing and TF-IDF Vectorization + Cosine Similarity for mathematical job matching.",
        "• Closing the Skill Gap: Identifies missing skills for target roles and delivers curated free learning roadmaps from YouTube, freeCodeCamp, Coursera Free, and W3Schools."
    ]
    for pt in points2:
        p = tf2.add_paragraph()
        p.text = pt
        p.font.size = Pt(15)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(12)

    # -------------------------------------------------------------
    # SLIDE 3: Problem Statement & Industry Need
    # -------------------------------------------------------------
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "2. Problem Statement & Industry Challenges")

    tb3 = slide3.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    tf3 = tb3.text_frame
    tf3.word_wrap = True

    points3 = [
        "1. Inefficiency of Manual Screening: Manual resume checks take hours, cause recruiter burnout, and lead to human bias in hiring decisions.",
        "2. Flaws in Traditional ATS Tools: Outdated systems rely on exact keyword counting, failing to recognize skill synonyms or understand semantic relevance.",
        "3. Zero Guidance for Students: When an application is rejected, candidates are not told which technical competencies they need to improve.",
        "4. High Cost of Enterprise Software: Commercial ATS products (Workday, Greenhouse) are expensive, proprietary, and inaccessible to students and colleges.",
        "5. Need for an Open-Source Alternative: An automated, transparent, explainable, and 100% free solution is needed for academia and job seekers."
    ]
    for pt in points3:
        p = tf3.add_paragraph()
        p.text = pt
        p.font.size = Pt(15)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(12)

    # -------------------------------------------------------------
    # SLIDE 4: Existing System vs Proposed System (Table)
    # -------------------------------------------------------------
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "3. Existing System vs Proposed System")

    rows, cols = 5, 3
    table_shape = slide4.shapes.add_table(rows, cols, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.0))
    table = table_shape.table
    table.columns[0].width = Inches(2.7)
    table.columns[1].width = Inches(4.5)
    table.columns[2].width = Inches(4.5)

    headers = ["Evaluation Parameter", "Existing / Traditional System", "Proposed AI-Powered System"]
    for i, h in enumerate(headers):
        cell = table.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = DARK_BLUE
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(14)
        p.font.color.rgb = TEXT_WHITE

    row_data = [
        ("Resume Screening", "Manual, slow, prone to human error", "Automated NLP extraction in under 2 seconds"),
        ("Matching Technique", "Naive keyword counting / boolean search", "TF-IDF Vectorization & Cosine Similarity ranking"),
        ("Candidate Feedback", "No feedback / generic rejection email", "ATS Completeness Score (0-100%) + Actionable Tips"),
        ("Skill Gap & Learning", "None; candidate must search on their own", "Automated Gap Analysis + Direct Free Course Links")
    ]
    for row_idx, data in enumerate(row_data, start=1):
        for col_idx, text in enumerate(data):
            cell = table.cell(row_idx, col_idx)
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.size = Pt(13)
            p.font.color.rgb = TEXT_DARK

    # -------------------------------------------------------------
    # SLIDE 5: System Architecture Diagram Slide (WITH IMAGE)
    # -------------------------------------------------------------
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "4. End-to-End System Architecture")

    # Insert generated Architecture Diagram Image
    slide5.shapes.add_picture(arch_img, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))

    # -------------------------------------------------------------
    # SLIDE 6: Multi-Format Resume Parsing Module
    # -------------------------------------------------------------
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "5. Multi-Format Resume Parsing Module")

    tb6 = slide6.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    tf6 = tb6.text_frame
    tf6.word_wrap = True

    points6 = [
        "• PDF Parsing Engine (PyPDF2):",
        "   - Extracts text streams across multiple pages, handling standard digital PDF layouts and multi-column formatting.",
        "• Microsoft Word Parsing Engine (python-docx):",
        "   - Reads paragraph text and iterates through document tables where candidate skills and education are structured.",
        "• Plain Text Parser (.txt):",
        "   - Implements multi-encoding fallbacks (UTF-8, Latin-1, CP1252) for cross-platform resilience.",
        "• Security & Validation Layer:",
        "   - Strict extension checks (.pdf, .docx, .txt), secure filename hashing, and 16 MB maximum payload protection."
    ]
    for pt in points6:
        p = tf6.add_paragraph()
        p.text = pt
        p.font.size = Pt(15)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(10)

    # -------------------------------------------------------------
    # SLIDE 7: NLP Skill & Entity Extraction Module
    # -------------------------------------------------------------
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "6. NLP Skill & Entity Extraction Taxonomy")

    tb7 = slide7.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    tf7 = tb7.text_frame
    tf7.word_wrap = True

    points7 = [
        "• 6 Taxonomy Categories Extracted from Resumes:",
        "   1. Programming Languages: Python, Java, JavaScript, TypeScript, C++, C#, SQL, Go, Rust...",
        "   2. Frameworks & Web: React, Flask, Django, Node.js, Spring Boot, Express, Angular, Next.js...",
        "   3. Databases: MySQL, PostgreSQL, MongoDB, Redis, SQLite, Oracle...",
        "   4. Developer Tools & Cloud: Git, Docker, Kubernetes, AWS, Linux, Postman, CI/CD...",
        "   5. Domain & AI/ML: Machine Learning, Deep Learning, NLP, Data Analysis, Pandas, REST APIs...",
        "   6. Soft Skills: Problem Solving, Teamwork, Communication, Agile Methodologies...",
        "• Word-Boundary Regex Protection: Lookarounds `(?<![a-zA-Z0-9])term(?![a-zA-Z0-9])` prevent false positives (e.g. 'Java' vs 'JavaScript', 'C' vs 'CSS').",
        "• Contact & Education Parsing: Automatically detects Email, Phone, LinkedIn, GitHub, Degrees, and Years of Experience."
    ]
    for pt in points7:
        p = tf7.add_paragraph()
        p.text = pt
        p.font.size = Pt(14)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 8: AI/ML Matching Engine (WITH TF-IDF GRAPHIC)
    # -------------------------------------------------------------
    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "7. AI/ML Matching Engine (TF-IDF + Cosine Similarity)")

    # Left: Explanation text
    tb8 = slide8.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(5.5), Inches(5.2))
    tf8 = tb8.text_frame
    tf8.word_wrap = True

    points8 = [
        "• Step 1: TF-IDF Vectorization:",
        "   - Converts resume and job texts into numerical term-frequency vectors.",
        "   - Down-weights common words ('the', 'and') while prioritizing technical competencies.",
        "• Step 2: Cosine Similarity:",
        "   - Calculates cosine angle between resume vector (A) and job vector (B).",
        "   - Measures semantic similarity from 0.0 (No overlap) to 1.0 (Exact match).",
        "• Step 3: Hybrid Scoring:",
        "   - Formula: 40% TF-IDF Similarity + 60% Weighted Skill Overlap.",
        "   - Ranks all available tech jobs in descending order."
    ]
    for pt in points8:
        p = tf8.add_paragraph()
        p.text = pt
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(6)

    # Right: TF-IDF Diagram Image
    slide8.shapes.add_picture(tfidf_img, Inches(6.5), Inches(1.8), Inches(6.0), Inches(4.5))

    # -------------------------------------------------------------
    # SLIDE 9: Skill Gap Analysis & Market Demand Priority
    # -------------------------------------------------------------
    slide9 = prs.slides.add_slide(blank_layout)
    add_header(slide9, "8. Skill Gap Analysis & Market Demand Prioritization")

    tb9 = slide9.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    tf9 = tb9.text_frame
    tf9.word_wrap = True

    points9 = [
        "• Mathematical Formulation of Skill Gap:",
        "   - Matched Skills = Candidate Skills ∩ Job Required Skills",
        "   - Missing Skills = Job Required Skills \\ Candidate Skills  (Set Difference)",
        "   - Role Readiness % = (|Matched Skills| / |Total Required Skills|) × 100",
        "   - Skill Gap Index = 100% − Readiness %",
        "• Market Demand Priority Engine:",
        "   - Computes global skill frequency across all active job postings in the database.",
        "   - High-demand skills required by multiple job roles (e.g. Git, Docker, SQL) are given top study priority.",
        "   - Ensures students invest their learning time where it yields maximum career payoff."
    ]
    for pt in points9:
        p = tf9.add_paragraph()
        p.text = pt
        p.font.size = Pt(15)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(12)

    # -------------------------------------------------------------
    # SLIDE 10: ATS Resume Completeness Scoring (WITH CHART)
    # -------------------------------------------------------------
    slide10 = prs.slides.add_slide(blank_layout)
    add_header(slide10, "9. ATS Resume Completeness & Diagnostic Scoring")

    # Left: Explanation text
    tb10 = slide10.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(5.5), Inches(5.2))
    tf10 = tb10.text_frame
    tf10.word_wrap = True

    points10 = [
        "• Objective: Help candidates optimize their resume to pass automated company ATS screeners.",
        "• 5 Structural Dimensions Evaluated:",
        "   1. Contact Metadata (Email, Phone, LinkedIn): 20 pts",
        "   2. Technical Skills Diversity & Volume: 30 pts",
        "   3. Education & Degree Credentials: 15 pts",
        "   4. Work Experience & Internships: 20 pts",
        "   5. Technical Projects & Portfolio: 15 pts",
        "• Actionable Improvement Feedback:",
        "   - Generates specific tips (e.g. 'Add a GitHub portfolio link', 'Detail your B.E. Computer Science degree')."
    ]
    for pt in points10:
        p = tf10.add_paragraph()
        p.text = pt
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(6)

    # Right: ATS Chart Image
    slide10.shapes.add_picture(ats_img, Inches(6.6), Inches(1.8), Inches(5.8), Inches(4.5))

    # -------------------------------------------------------------
    # SLIDE 11: Free Learning Recommendation Module
    # -------------------------------------------------------------
    slide11 = prs.slides.add_slide(blank_layout)
    add_header(slide11, "10. Free Learning Recommendation Module")

    tb11 = slide11.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    tf11 = tb11.text_frame
    tf11.word_wrap = True

    points11 = [
        "• 100% Free & Open Educational Resources:",
        "   - Maps every detected missing skill to curated, high-quality free video tutorials, interactive courses, and documentation.",
        "• Curated Learning Platforms:",
        "   - YouTube: Full-length courses from freeCodeCamp, Traversy Media, CS Dojo, TechWithTim.",
        "   - freeCodeCamp: Interactive certifications in Python, JavaScript, Data Structures, and Machine Learning.",
        "   - Coursera Free Audit: DeepLearning.AI and university machine learning foundational specializations.",
        "   - W3Schools & Official Documentation: Interactive playgrounds and reference guides.",
        "• Tailored Learning Roadmaps: Organizes missing skills with estimated study hours and direct clickable URLs."
    ]
    for pt in points11:
        p = tf11.add_paragraph()
        p.text = pt
        p.font.size = Pt(15)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(12)

    # -------------------------------------------------------------
    # SLIDE 12: Database Design & Relational Schema
    # -------------------------------------------------------------
    slide12 = prs.slides.add_slide(blank_layout)
    add_header(slide12, "11. Database Design & Relational Schema")

    tb12 = slide12.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    tf12 = tb12.text_frame
    tf12.word_wrap = True

    points12 = [
        "• Database Engine: MySQL 8.0+ managed via SQLAlchemy ORM (with zero-setup SQLite fallback).",
        "• 7 Normalized Relational Tables:",
        "   1. users: user_id (PK), full_name, email (UQ), password_hash, role (student/admin), phone",
        "   2. resumes: resume_id (PK), user_id (FK), resume_title, file_path, extracted_text, completeness_score",
        "   3. skills: skill_id (PK), skill_name (UQ), skill_category",
        "   4. jobs: job_id (PK), title, company, industry, experience_level, salary_range, description",
        "   5. job_skills: job_skill_id (PK), job_id (FK), skill_id (FK), importance_level, weight",
        "   6. recommendations: recommendation_id (PK), resume_id (FK), job_id (FK), match_percentage, skills JSON",
        "   7. learning_resources: resource_id (PK), skill_id (FK), title, url, platform, duration_hours, is_free"
    ]
    for pt in points12:
        p = tf12.add_paragraph()
        p.text = pt
        p.font.size = Pt(14)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(8)

    # -------------------------------------------------------------
    # SLIDE 13: UI Design & User/Admin Dashboards
    # -------------------------------------------------------------
    slide13 = prs.slides.add_slide(blank_layout)
    add_header(slide13, "12. UI Design & User/Admin Dashboards")

    tb13 = slide13.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    tf13 = tb13.text_frame
    tf13.word_wrap = True

    points13 = [
        "• Modern Responsive UI: Built with HTML5, CSS3, Bootstrap 5, and Jinja2 templates.",
        "• Drag-and-Drop Upload Zone: Animated file drop area with instant file size and format validation.",
        "• Candidate Dashboard: Displays latest scan progress, ATS score meters, top recommendations, and history.",
        "• Recruiter / Admin Analytics Portal: Interactive Chart.js visualization of top in-demand skills in the talent pool.",
        "• Job Management CRUD: Admin capability to add/edit job descriptions and assign mandatory skill weights.",
        "• 1-Click Desktop Launcher: Windows batch shortcut (`START_PROJECT.bat`) to launch and open browser automatically."
    ]
    for pt in points13:
        p = tf13.add_paragraph()
        p.text = pt
        p.font.size = Pt(15)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(11)

    # -------------------------------------------------------------
    # SLIDE 14: Testing, Performance & Results
    # -------------------------------------------------------------
    slide14 = prs.slides.add_slide(blank_layout)
    add_header(slide14, "13. Testing, Performance & Validation Results")

    tb14 = slide14.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    tf14 = tb14.text_frame
    tf14.word_wrap = True

    points14 = [
        "• Automated Test Suite (test_app.py):",
        "   - Executed 9 unit tests verifying all 11 phases in 3.74 seconds with 100% PASS rate (OK).",
        "• Validated Test Scenarios:",
        "   1. Multi-format file ingestion (PDF, DOCX, TXT parsing).",
        "   2. NLP taxonomy extraction without false positives (e.g. C vs CSS, Java vs JavaScript).",
        "   3. TF-IDF Cosine Similarity ranking accuracy against real resume samples.",
        "   4. Skill gap set operations and ATS scoring diagnostic accuracy.",
        "   5. User authentication, password hashing (Werkzeug PBKDF2/scrypt), and session guards.",
        "• Performance Benchmark: Average processing time per resume is under 2.0 seconds on standard CPU hardware."
    ]
    for pt in points14:
        p = tf14.add_paragraph()
        p.text = pt
        p.font.size = Pt(14)
        p.font.color.rgb = TEXT_DARK
        p.space_after = Pt(9)

    # -------------------------------------------------------------
    # SLIDE 15: Conclusion & Future Scope (Dark Theme)
    # -------------------------------------------------------------
    slide15 = prs.slides.add_slide(blank_layout)
    set_bg(slide15, DARK_BLUE)

    tbox15 = slide15.shapes.add_textbox(Inches(1.0), Inches(0.9), Inches(11.333), Inches(5.6))
    tf15 = tbox15.text_frame
    tf15.word_wrap = True

    p0 = tf15.paragraphs[0]
    p0.text = "14. ADVANTAGES, FUTURE SCOPE & CONCLUSION"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = ACCENT_BLUE

    p1 = tf15.add_paragraph()
    p1.text = "Conclusion:"
    p1.font.size = Pt(18)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE

    p2 = tf15.add_paragraph()
    p2.text = "The AI-Powered Resume Analyzer and Job Recommendation System demonstrates how open-source NLP and Machine Learning techniques (TF-IDF + Cosine Similarity) can automate recruitment screening, evaluate ATS readiness, and guide candidates with personalized upskilling roadmaps without expensive cloud APIs."
    p2.font.size = Pt(13)
    p2.font.color.rgb = TEXT_MUTED

    p3 = tf15.add_paragraph()
    p3.text = "\nFuture Enhancements:"
    p3.font.size = Pt(16)
    p3.font.bold = True
    p3.font.color.rgb = GREEN

    p4 = tf15.add_paragraph()
    p4.text = "• Integration with Transformer-based Semantic Models (BERT / RoBERTa / Sentence-Transformers).\n• Optical Character Recognition (OCR) for scanned image resumes (Tesseract OCR).\n• Live Job Portal API Integration (LinkedIn, Indeed, Naukri API synchronization)."
    p4.font.size = Pt(12)
    p4.font.color.rgb = TEXT_WHITE

    p5 = tf15.add_paragraph()
    p5.text = "\nThank You! Any Questions?"
    p5.font.size = Pt(22)
    p5.font.bold = True
    p5.font.color.rgb = ACCENT_BLUE
    p5.alignment = PP_ALIGN.CENTER

    # Save to project folder
    local_path = "AI_Resume_Analyzer_Presentation.pptx"
    prs.save(local_path)
    print(f"[SUCCESS] Saved local presentation: {local_path}")

    # Also save directly to Desktop
    desktop_paths = [
        os.path.join(os.environ.get("USERPROFILE", ""), "Desktop"),
        os.path.join(os.environ.get("USERPROFILE", ""), "OneDrive", "Desktop")
    ]
    for dp in desktop_paths:
        if os.path.exists(dp):
            dest = os.path.join(dp, "AI_Resume_Analyzer_Presentation.pptx")
            prs.save(dest)
            print(f"[SUCCESS] Saved presentation directly to Desktop: {dest}")

if __name__ == "__main__":
    build_deck()
