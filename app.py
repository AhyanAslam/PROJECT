from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os 

app = Flask(__name__)  #initializing flask
app.secret_key = "supersecretkey"  #requirement for using flash

USER_DATA_FILE="users.json"  # file for storing users id password 

# Load users from file
def load_users():
    if not os.path.exists(USER_DATA_FILE):
        return []  # Return empty list if file doesn't exist
    try:
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)  # Load data as list
    except json.JSONDecodeError:
        return []  # If file is empty or corrupted, return empty list

# Save users to file
def save_users(users):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(users, file, indent=4, ensure_ascii=False)  # Save as list

# rendered home page
@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

# rendered login page, checking user id and password
@app.route('/signin', methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        user_id = request.form["user_id"]  # Get user ID from the form
        password = request.form["password"]  # Get password from the form
        users = load_users()  # Load existing users

        if any(user["user_id"] == user_id and user["password"] == password for user in users):
            return redirect("/home")  # ✅ Redirect to home page
        else:
            flash("Invalid User ID or Password.")  # Show error message

    return render_template("signin.html")  # Render signin page again if failed


# rendered register page,
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user_id = request.form["user_id"]
        password = request.form["password"]
        users = load_users()  # Load existing users (as list)

        # Check if user already exists
        if any(user["user_id"] == user_id for user in users):
            flash("User ID already exists.", "error")
        else:
            users.append({"user_id": user_id, "password": password})  # Append new user
            save_users(users)  # Save updated list
            flash("Registration successful! You can now log in.", "success")
            return redirect("/") 

    return render_template("register.html")

    
if __name__ == '__main__':
    app.run(debug=True)