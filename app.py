import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
from flask import Flask, render_template, request, session, redirect, url_for, flash

load_dotenv()
client = OpenAI(api_key = os.environ["API_KEY"])

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

class TailoredCoursework(BaseModel):
    uts: list[str]
    cs50: list[str]

class TailoredResume(BaseModel):
    about_me: list[str]
    coursework: TailoredCoursework
    skills: list[str]


@app.route("/", methods=["POST", "GET"])
def index():
    session.clear()
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
            client, job_description, about_me, education, skills
        )
        
        # Make sure chatgpt output is valid and not incorrect with its structure
        invalid_skills = [
            skill for skill in tailored_data.skills
            if skill not in skills
        ]

        if invalid_skills:
            raise ValueError(f"Invalid skills: {invalid_skills}")

        uts_coursework = education[0]["coursework"]
        cs50_coursework = education[1]["coursework"]

        for subject in tailored_data.coursework.uts:
            if subject not in uts_coursework:
                raise ValueError(f"Invalid UTS subject: {subject}")

        for subject in tailored_data.coursework.cs50:
            if subject not in cs50_coursework:
                raise ValueError(f"Invalid CS50 subject: {subject}")
        
        tailored_resume = {
        "personal": header_data,
        "about": {
            "paragraphs": tailored_data.about_me
        },
        "experience": experience,
        "projects": projects,
        "education": education,
        "skills": tailored_data.skills,
        "references": references
    }

        # Render the resume shown
        print("POST REQUEST COMPLETED")
        return render_template("resume.html", resume=tailored_resume)
    
    else:
        # Render the index page for the application
        return render_template("index.html")


def ai_call(client, job_description, about_me, education, skills):

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
    """

    resume_input = {
        "about_me": about_me,
        "education": education,
        "skills": skills
    }

    response = client.responses.parse(
        model="gpt-5-mini",
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