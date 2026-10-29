import os
import json
import copy
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
from flask import Flask, render_template, request, redirect, url_for, flash

load_dotenv()
client = OpenAI(api_key = os.environ["API_KEY"])

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

class TailoredEducation(BaseModel):
    """A structure for the education elements for the AI model"""
    education_index: int
    coursework: list[str]

class SkillCategory(BaseModel):
    """A structure for the skill elements for the AI model"""
    category: str
    skills: list[str]

class TailoredResume(BaseModel):
    """A structure for the resume for the AI model"""
    about_me: list[str]
    education: list[TailoredEducation]
    skills: list[SkillCategory]


@app.route("/", methods=["POST", "GET"])
def index():
    """Index route for the web application"""
    if request.method == "POST":
        # Get the form submission for the job description
        job_description = request.form.get("description", "").strip()

        # Validate the inputs
        if not job_description:
            flash("Please enter a job description", "error")
            return redirect(url_for("index"))

        # Load the master resume json file
        resume_path = Path(__file__).resolve().parent / "data" / "resume_data.json"

        with open(resume_path, "r", encoding="utf-8") as file:
            master_resume = json.load(file)

        # Structure the master resume for AI Processing

        # header_data is a dictionary full of personal details [No AI processing here]
        header_data = master_resume["personal"]

        # about_me is a list of strings [Ai Processing based on description]
        about_me = master_resume["about"]["paragraphs"]

        # experience is a list of dictionaries [No Ai Processing here yet]
        experience = master_resume["experience"]

        # projects is a list of dictionaries [No Ai processing here yet]
        projects = master_resume["projects"]

        # education is a list of dictionaries [Ai Process the coursework]
        education = master_resume["education"]

        # skills is a list of strings [Ai Processing here]
        skills = master_resume["skills"]

        # references is a string [No Ai processing]
        references = master_resume["references"]

        # Send the master resume and job description to chat gpt and get the response text
        tailored_data = ai_call(
            job_description, about_me, education, skills
        )
        
        # Make sure chatgpt output is valid and not incorrect with its structure
        tailored_education = copy.deepcopy(education)

        returned_indices = [
            entry.education_index
            for entry in tailored_data.education
        ]

        expected_indices = list(range(len(education)))

        if sorted(returned_indices) != expected_indices:
            flash("OpenAI returned coursework listed duplicate entries, try again")
            return redirect(url_for("index"))

        for entry in tailored_data.education:
            index = entry.education_index

            if not 0 <= index < len(tailored_education):
                raise ValueError(f"Invalid education index: {index}")
            
            original_coursework = education[index].get("coursework",[])

            invalid_coursework = [
                subject
                for subject in entry.coursework
                if subject not in original_coursework
            ]

            if invalid_coursework:
                flash("OpenAI returned coursework not listed in master resume, try again")
                return redirect(url_for("index"))

            tailored_education[index]["coursework"] = entry.coursework
    
        tailored_resume = {
        "personal": header_data,
        "about": {
            "paragraphs": tailored_data.about_me
        },
        "experience": experience,
        "projects": projects,
        "education": tailored_education,
        "skills": tailored_data.skills,
        "references": references
    }

        # Render the resume shown
        print("POST REQUEST COMPLETED")
        return render_template("resume.html", resume=tailored_resume)
    
    else:
        # Render the index page for the application
        return render_template("index.html")


def ai_call(job_description, about_me, education, skills):
    """Uses pydantic and openai to return a structured call for the open ai model"""

    instructions = """
    You are a professional resume tailoring assistant.

    Tailor the candidate's resume information to the supplied
    job description.

    Rules:
    1. Only use information contained in the master resume.
    2. Never invent skills, qualifications, achievements or experience.
    3. Prioritise information relevant to the job description.
    4. Rewrite descriptions to emphasise relevant experience.
    5. Maintain a professional, concise and ATS-friendly tone.
    6. Do not exaggerate the candidate's experience.
    7. Preserve factual details such as dates, qualifications
    and employment history.
    8. Return the tailored resume as valid JSON.

    Select relevant skills from the master resume and group them
    into professional categories such as Programming Languages,
    Artificial Intelligence, Data Analytics, Database Management,
    Software Development, Web Development, Development Tools
    and Technical Support.

    Only include categories relevant to the job description.
    Use only skills present in the master resume.
    Do not duplicate skills unnecessarily.

        ABOUT ME SECTION:
    - Rewrite the About Me section to be relevant to the job description,
    while maintaining a general professional tone.
    - Avoid making the summary overly specific to the advertised position.
    It should describe the candidate's overall qualifications, experience,
    technical abilities and professional qualities.
    - Emphasise transferable skills and relevant strengths rather than
    directly mirroring the job description.
    - Maintain approximately the same total word count as the original
    About Me section (within 3%).
    - Preserve the original number of paragraphs and their general structure.
    - Use clear, natural and professional language.
    - Do not invent qualifications, experience, achievements or skills.
    - Avoid mentioning the employer's name or the specific job title just say the general title as advertised.

        EDUCATION AND COURSEWORK:
    - Process every education entry in the master resume.
    - Use education_index to identify each entry by its
    zero-based position in the education array.
    - Return exactly one result for each education entry.
    - Rank subjects from most relevant to least relevant.
    - Select up to 10 most relevant coursework subjects per entry.
    - Only select subjects from that entry's original coursework.
    - Preserve the exact original subject names.
    - Do not invent qualifications or coursework.
    """

    resume_input = {
        "about_me": about_me,
        "education": education,
        "skills": skills
    }

    response = client.responses.parse(
        model="gpt-6-luna",
        instructions=instructions,
        input=[
            {
                "role": "user",
                "content": (
                    "MASTER RESUME INFORMATION:\n"
                    + json.dumps(resume_input, ensure_ascii=False)
                    + "\n\nJOB DESCRIPTION:\n"
                    + job_description
                )
            }
        ],
        text_format=TailoredResume

    )

    if response.output_parsed is None:
        raise ValueError("AI did not return a valid resume")
    
    return response.output_parsed

if __name__ == "__main__":
    app.run()