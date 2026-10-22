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
        print("POST REQUEST")
    
    else:
        # Render the index page for the application
        print("GET REQUEST")

if __name__ == "__main__":
    app.run()