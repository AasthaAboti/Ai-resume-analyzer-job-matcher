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
    
with open("data/skills.json", "r",encoding="utf-8") as file:
    master_skill = json.load(file)
    skill_found=[]
    print("="*30)
    print(Fore.MAGENTA+"✅SKILLS FOUND")
    print("="*30) 
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
elif 60 <= best_percentage < 80::
    print("Good,but can be improved")
else:
    print("⚠️ Needs Improvement.")            