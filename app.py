from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)

# MongoDB Atlas connection
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["flask_mongodb_db"]
collection = db["users"]


# Home page and form submission
@app.route("/", methods=["GET", "POST"])
def home():

    error = None

    if request.method == "POST":

        try:
            name = request.form.get("name")
            email = request.form.get("email")
            course = request.form.get("course")

            # Check that all fields are filled
            if not name or not email or not course:
                raise ValueError("All fields are required.")

            # Insert data into MongoDB
            collection.insert_one({
                "name": name,
                "email": email,
                "course": course
            })

            # Redirect to success page
            return redirect(url_for("success"))

        except Exception as e:
            # Display error on the same page
            error = str(e)

    return render_template("index.html", error=error)


# Success page
@app.route("/success")
def success():
    return render_template("success.html")


# JSON API route
@app.route("/api")
def api():

    try:
        with open("data.json", "r") as file:
            data = json.load(file)

        return jsonify(data)

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

# To-Do item submission API
@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():

    try:
        item_name = request.form.get("itemName")
        item_description = request.form.get("itemDescription")

        if not item_name or not item_description:
            return "Item Name and Item Description are required.", 400

        collection.insert_one({
            "itemName": item_name,
            "itemDescription": item_description
        })

        return redirect(url_for("success"))

    except Exception as e:
        return f"Error: {str(e)}", 500
# Start Flask server
if __name__ == "__main__":
    app.run(debug=True)