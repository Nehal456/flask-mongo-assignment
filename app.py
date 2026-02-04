from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)

# --------------------------------------------------
# MongoDB Atlas Connection (PART 2 requirement)
# --------------------------------------------------
mongo_uri = os.getenv("MONGO_URI")


client = MongoClient(mongo_uri)
db = client.assignment_db
users_collection = db.users


# --------------------------------------------------
# PART 1: API Route (reads from backend file)
# --------------------------------------------------
@app.route("/api", methods=["GET"])
def api_data():
    """
    Reads data from backend JSON file and returns it as API response
    """
    with open("data.json", "r") as file:
        data = json.load(file)

    return jsonify(data)


# --------------------------------------------------
# Home Route – Form Page
# --------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")


# --------------------------------------------------
# Form Submission Route (PART 2)
# --------------------------------------------------
@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    email = request.form.get("email")

    if not name or not email:
        return render_template("index.html", error="All fields are required")

    try:
        users_collection.insert_one({
            "name": name,
            "email": email
        })
        return redirect(url_for("success"))

    except Exception as e:
        return render_template("index.html", error=str(e))


# --------------------------------------------------
# Success Route
# --------------------------------------------------
@app.route("/success")
def success():
    return render_template("success.html")


# --------------------------------------------------
# Run Application
# --------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
