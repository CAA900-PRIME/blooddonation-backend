from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import config

app = Flask(__name__)
app.config.from_object(config.Config)

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define your User model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    def __init__(self, username,password):
      self.username = username
      self.password = password
    def __repr__(self):
        return f'<User {self.username}>'

@app.route('/')
def index():
    return render_template('index.html', title='Blood Donation App')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Retrieve form data safely
        username = request.form.get('username')
        password = request.form.get('password')

        # Validate form inputs
        if not username or not password:
            return render_template('partials/signup_form.html', error='Both username and password are required.')

        # Hash the password
        password_hash = generate_password_hash(password)

        # Check if the username already exists
        existing_user = Users.query.filter_by(username=username).first()
        if existing_user:
            return render_template('partials/signup_form.html', error='Username already exists.')

        try:
            # Create and add new user
            new_user = Users(username=username, password=password_hash)
            db.session.add(new_user)
            db.session.commit()

            return render_template('partials/signup_form.html', success='Signup successful! Please login.')
        
        except Exception as e:
            # Rollback the session in case of an error and log it
            db.session.rollback()
            print(f"Error creating user: {e}")
            return render_template('partials/signup_form.html', error='An error occurred. Please try again.')

    # Render the signup form for GET requests
    return render_template('signup.html', title='Sign Up')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = Users.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['username'] = user.username
            return """<p>Login Successful! click <a href="/">Home</a> to check up coming events!</p>"""
        return render_template('partials/login_form.html', error='Invalid username or password')
    return render_template('login.html', title='Login')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# This is an example, will be removed later.
@app.route('/load-events')
def load_events():
    # For demo purposes, let's assume these are the events.
    events = [
        {'name': 'City Hospital Blood Drive', 'date': '2025-02-10'},
        {'name': 'Community Center Donation Day', 'date': '2025-02-15'},
        {'name': 'University Blood Donation Camp', 'date': '2025-02-20'}
    ]
    return render_template('partials/event_list.html', events=events)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
