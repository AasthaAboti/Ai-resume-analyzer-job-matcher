import os
import pdfplumber
import json
from colorama import Fore, Back, Style, init
init(autoreset=True)

print("=="*30)
print(Fore.MAGENTA+"🤖AI RESUME ANALYZER AND JOB MATCHER")
print("=="*30)


resume_path=input("enter your resume pdf path: ").strip().strip('"')
#case1 check if path exists
if os.path.isfile(resume_path):
    print("path found successfully")
    if resume_path.lower().endswith(".pdf"):
        print("resume uploaded successfully ") 

        with pdfplumber.open(resume_path) as pdf:
            total_pages=len(pdf.pages)
            print("total pages:",total_pages)
            resume_text = ""
            for page in pdf.pages:
                resume_text += page.extract_text() + "\n"
            #print(resume_text)
    else:
        print("only pdf files allowed") 
else:          
    print("not found")      

    print("="*30)
    print(Fore.MAGENTA+"✅SKILLS FOUND")
    print("="*30) 

with open("data/skills.json", "r",encoding="utf-8") as file:
    master_skill = json.load(file)

    skill_found=[]
    for skill in master_skill:
        if skill.lower() in resume_text.lower():
            skill_found.append(skill)
    for skill in skill_found:
        print(skill)         


with open("data/roles.json", "r", encoding="utf-8") as file:
    roles = json.load(file)
role_match = {}
for role, required_skills in roles.items():
    matched_skills = 0
    for required_skill in required_skills:
        if required_skill in skill_found:
            matched_skills += 1

    total_required = len(required_skills)
    percentage = (matched_skills / total_required) * 100
    role_match[role] = round(percentage, 2)


print("\n" + "=" * 40)
print(Fore.MAGENTA+"🎯 Top 5 ROLE RECOMMENDATIONS")
print("=" * 40)


for role, percentage in role_match.items():
    #print(f"{role} : {percentage}%")     
    sorted_roles = sorted(role_match.items(), key=lambda x: x[1], reverse=True)
print(Fore.MAGENTA+"Top 5 Roles")

for role, percentage in sorted_roles[:5]:
    print(Fore.CYAN+role,"-----", percentage,"%")
best_role, best_percentage = sorted_roles[0]
required_skills = roles[best_role]


print("="*30)
print(Fore.MAGENTA+"📌MISSING SKILLS")
print("="*30)


missing_skills = []
for required_skill in required_skills:
    if required_skill not in skill_found:
        missing_skills.append(required_skill)
for skill in missing_skills:
    print(Fore.RED+skill) 


print("="*30)
print(Fore.MAGENTA+"\n💡 PERSONALIZED SUGGESTIONS")
print("="*30)


with open("data/suggestions.json", "r", encoding="utf-8") as file:
    suggestions = json.load(file)
    choice = input(Fore.YELLOW+"Do you want skill improvement suggestions? (yes/no): ").strip().lower()
if choice == "yes" or choice == "y":
    for skill in missing_skills:
        if skill in suggestions:
            details = suggestions[skill]
            print("📌 Skill:", skill)
            print("📚 Course:", details["course"])
            print("💻 Project:", details["project"])
            print("⭐ Difficulty:", details["difficulty"])
            print()
elif choice =="no" or choice =="n":
    print(Fore.BLUE+"Suggestions skipped.")
else:
    print("Please enter yes or no.")


print("="*30)
print("📊 ATS SCORE")
print("="*30)


print("ATS SCORE:" ,best_percentage) 
if best_percentage > 90:
    print("🏆 Excellent Resume!") 
elif 80 <= best_percentage < 90:
    print("⭐ Strong Resume!")  
elif 60 <= best_percentage < 80:
    print("Good,but can be improved")
else:
    print("⚠️ Needs Improvement.")  

jd_path = input("Enter Job Description (.txt) file path: ").strip().strip('"')
with open(jd_path, "r", encoding="utf-8") as file:
    job_description = file.read()

jd_skills = []
for skill in master_skill:
    if skill.lower() in job_description.lower():
        jd_skills.append(skill)

matched_jd_skills = []
for skill in jd_skills:
    if skill in skill_found:
        matched_jd_skills.append(skill)


print("=" * 30)
print("📄 JOB DESCRIPTION ATS SCORE")
print("=" * 30)
jd_percentage=(len(matched_jd_skills)/len(jd_skills)) *100 
round(jd_percentage, 2)
if len(jd_skills) > 0:
    print(f"🎯 JD ATS Score: {jd_percentage:.2f}%")
else:
    print("No recognizable skills found in the job description.") 
if jd_percentage>90:
    print("⭐ Strong Resume! matches job description")
elif 80 <= jd_percentage< 90:
    print("your resume matches the job description")  
elif 60 <= jd_percentage < 80:
    print(" Your resume partially matches this job description.")
else:
    print("⚠️ Needs to add more skills to increase your job chances.")    



print("=" * 30)
print(" COMPANIES RECOMMENDATION")
print("=" * 30)


with open("data/companies.json", "r", encoding="utf-8") as file:
    companies = json.load(file)
    recommended_companies = companies[best_role]
medals = ["🥇", "🥈", "🥉", "🏅", "🏅"]
for i, company in enumerate(recommended_companies):
    print(medals[i], company)
sections = [
    "Contact",
    "Summary",
    "Education",
    "Skills",
    "Projects",
    "Experience",
    "Internships",
    "Certifications",
    "Achievements",
    "Languages"
]
section_found = []
for section in sections:
    if section.lower() in resume_text.lower():
        section_found.append(section)    
completeness_score = (len(section_found) / len(sections)) * 100
print(f"📊 Resume Completeness: {completeness_score:.2f}%")
for section in sections:
    if section in sections:
        print("✅", section)
    else:
        print("❌", section)
