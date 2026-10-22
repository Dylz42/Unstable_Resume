import os
from dotenv import load_dotenv
from openai import OpenAI
from flask import Flask, render_template, request, session, redirect, url_for

load_dotenv()
client = OpenAI(api_key = os.environ["API_KEY"])

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

@app.route("/", methods=["POST", "GET"])
def index():
    session.clear()
    if request.method == "POST":
        # Get the form submission for the job description
        
        # Validate the inputs

        # Load the master resume

        # Send the master resume and job description to chat gpt and get the response text

        # Make sure chatgpt output is valid and not incorrect

        # Render the resume shown
        print("POST REQUEST")
    
    else:
        # Render the index page for the application
        print("GET REQUEST")

if __name__ == "__main__":
    app.run()