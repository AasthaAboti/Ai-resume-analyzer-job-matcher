from flask import Flask, render_template, request
import pdfplumber
import json

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    # Get uploaded PDF
    resume = request.files["resume"]
    resume_path = "uploaded_resume.pdf"
    resume.save(resume_path)

    # Extract resume text
    with pdfplumber.open(resume_path) as pdf:
        resume_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                resume_text += text + "\n"

    # Skills
    with open("data/skills.json", "r", encoding="utf-8") as file:
        master_skill = json.load(file)

    skill_found = []

    for skill in master_skill:
        if skill.lower() in resume_text.lower():
            skill_found.append(skill)

    # Roles
    with open("data/roles.json", "r", encoding="utf-8") as file:
        roles = json.load(file)

    role_match = {}

    for role, required_skills in roles.items():
        matched_skills = 0

        for required_skill in required_skills:
            if required_skill in skill_found:
                matched_skills += 1

        percentage = (matched_skills / len(required_skills)) * 100
        role_match[role] = round(percentage, 2)

    sorted_roles = sorted(
        role_match.items(),
        key=lambda x: x[1],
        reverse=True
    )

    top_roles = sorted_roles[:5]

    # Best role + missing skills
    best_role, best_percentage = sorted_roles[0]
    required_skills = roles[best_role]

    missing_skills = []

    for skill in required_skills:
        if skill not in skill_found:
            missing_skills.append(skill)

    # Companies
    with open("data/companies.json", "r", encoding="utf-8") as file:
        companies = json.load(file)

    recommended_companies = companies[best_role]

    # Resume completeness
    sections = [
        "Contact", "Summary", "Education", "Skills",
        "Projects", "Experience", "Internships",
        "Certifications", "Achievements", "Languages"
    ]
    section_found = []
    for section in sections:
        if section.lower() in resume_text.lower():
            section_found.append(section)
    completeness_score = (
        len(section_found) / len(sections)
    ) * 100
    return f"""
    <h1>Resume Analysis Results</h1>
    <h2>Skills Found</h2>
    <p>{", ".join(skill_found)}</p>
    <h2>Top 5 Role Recommendations</h2>
    <p>{"<br>".join([role + " - " + str(score) + "%" for role, score in top_roles])}</p>
    <h2>Missing Skills</h2>
    <p>{", ".join(missing_skills)}</p>
    <h2>ATS Score</h2>
    <p>{best_percentage}%</p>
    <h2>Recommended Companies</h2>
    <p>{"<br>".join(recommended_companies)}</p>
    <h2>Resume Completeness</h2>
    <p>{completeness_score:.2f}%</p>
    <br>
    <a href="/">Analyze another resume</a>
    """
if __name__ == "__main__":
    app.run(debug=True)