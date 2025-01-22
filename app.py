from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os 

app = Flask(__name__)

@app.route('/home' ,  methods=["GET", "POST"])
def home():
    return render_template('index.html')

if __name__ == '_main_':
    app.run(debug=True)

#app = Flask(__name__)  #initializing flask
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
@app.route('/landing')
def landing():
    return render_template('landingpage.html')

# rendered login page, checking user id and password
@app.route('/signin', methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        user_id = request.form["user_id"]  # Get user ID from the form
        password = request.form["password"]  # Get password from the form
        users = load_users()  # Load existing users

        if any(user["user_id"] == user_id and user["password"] == password for user in users):
            return redirect("/landing")  # ✅ Redirect to home page
        else:
            #flash("Invalid User ID or Password.")  # Show error message
            return "Invalid Password or User name"

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

# notepad
@app.route('/notepad', methods=['GET'])
def show_notepad():
    return render_template('notepad.html')

@app.route('/save_note', methods=['POST'])
def write_to_file():
    text = request.form['notes']
    with open("note.txt", "a") as file:
        file.write(text + "\n\n")  
    
    # return render_template('viewnotes.html')
    
    # return "Text has been written to the file! <a href='/notepad'>Go Back</a>"
    return "Text has been written to the file! <a href='/viewnotes'>Go Back</a>"

#View notes code

@app.route('/viewnotes', methods=['GET'])
def show_notes():
    notes = []
    if os.path.exists("note.txt"):
        with open("note.txt", "r") as file:
            notes = [note.strip() for note in file.readlines() if note.strip()]  # Remove empty lines and strip whitespace

    return render_template('viewnotes.html', notes=enumerate(notes))  # Pass enumerated notes (index + note)

@app.route('/edit_note/<int:note_index>', methods=['GET', 'POST'])
def edit_note(note_index):
    notes = []
    if os.path.exists("note.txt"):
        with open("note.txt", "r") as file:
            notes = [note.strip() for note in file.readlines() if note.strip()]  # Remove empty lines

    if request.method == 'POST':
        updated_note = request.form['updated_note']
        if 0 <= note_index < len(notes):  # Ensure valid index
            notes[note_index] = updated_note  # Update the note
            with open("note.txt", "w") as file:
                file.write("\n".join(notes) + "\n")  # Write updated notes back
        return redirect('/viewnotes')  # Redirect to the notes page

    # Render edit form for the selected note
    return render_template('editnote.html', note=notes[note_index], note_index=note_index)

#event calander
@app.route('/event')
def event():
    return render_template('event.html')



import uuid

EVENTS_DATA_FILE = "events.json"

def load_events():
    if not os.path.exists(EVENTS_DATA_FILE):
        return []
    try:
        with open(EVENTS_DATA_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []

def save_events(events):
    with open(EVENTS_DATA_FILE, "w") as file:
        json.dump(events, file, indent=4, ensure_ascii=False)

@app.route('/add_event', methods=['POST'])
def add_event():
    event_data = request.get_json()
    events = load_events()

    new_event = {
        "id": str(uuid.uuid4()),  # Generate a unique ID for each event
        "date": event_data["eventDate"],
        "title": event_data["eventTitle"],
        "description": event_data["eventDescription"]
    }

    events.append(new_event)
    save_events(events)

    return {"success": True, "event": new_event}


@app.route('/get_events', methods=['GET'])
def get_events():
    events = load_events()  # Load events from file
    return {"events": events}

@app.route('/delete_event/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    events = load_events()
    updated_events = [event for event in events if event["id"] != event_id]
    
    if len(events) == len(updated_events):
        return {"success": False}  # Event not found
    
    save_events(updated_events)
    return {"success": True}


    
if __name__ == '__main__':
    app.run(debug=True)