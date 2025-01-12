from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os 

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '_main_':
    app.run(debug=True)

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
            #localStorage.set
            # todo, python m localStorage ks trh use krte, wo dekho phrle
            # yhn pr localStorage m data save krdo, mtlb us user ko
            # aur phr navbar m dekho k localStorage m agar user hai to navbar m signup , signin ko remove krke logut button show krdo, phr agar s logout pr click kre to logut api cll krwado, usme localStorage s data remove krdo
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

<<<<<<< HEAD
# notepad
@app.route('/notepad', methods=['GET'])
def show_notepad():
    return render_template('notepad.html')

@app.route('/save_note', methods=['POST'])
def write_to_file():
    text = request.form['notes']
    with open("note.txt", "a") as file:
        file.write(text + "\n\n")  

    return "Text has been written to the file! <a href='/notepad'>Go Back</a>"

#View notes code
@app.route('/viewnotes', methods=['GET'])
def show_notes():
    return render_template('viewnotes.html')
=======

>>>>>>> 2a0940da082c7cdf23e2fda08eb6445eb1b8dc94


    
if __name__ == '__main__':
    app.run(debug=True)