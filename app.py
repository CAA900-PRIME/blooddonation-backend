from flask import Flask, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import config

## Moved database and models
from models import db, Users  # Import db and Users model from models

app = Flask(__name__)
app.config.from_object(config.Config)

db.init_app(app)  # Initialize the db with the app

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
            return render_template('partials/alert.html', error='Both username and password are required.')

        # Hash the password
        password_hash = generate_password_hash(password)

        # Check if the username already exists
        existing_user = Users.query.filter_by(username=username).first()
        if existing_user:
            return render_template('partials/alert.html', error='Username already exists.')

        try:
            # Create and add new user
            new_user = Users(username=username, password=password_hash)
            db.session.add(new_user)
            db.session.commit()

            return render_template('partials/alert.html', success='Signup successful! Please <a href="/login">login</a>.')
        
        except Exception as e:
            # Rollback the session in case of an error and log it
            db.session.rollback()
            print(f"Error creating user: {e}")
            return render_template('partials/alert.html', error='An error occurred. Please try again.')

    return render_template('signup.html', title='Sign Up')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = Users.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['username'] = user.username
            
            return render_template('partials/alert.html', success="Logged In Successfully! <a href='/'>Home</a>")
        return render_template('partials/alert.html', error='Invalid username or password')
    return render_template('login.html', title='Login')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# This is an example, will be removed later.
@app.route('/load-events')
def load_events():
    # let's assume these are the events. Only going to be shown for loggin users
    events = [
        {'name': 'City Hospital Blood Drive', 'date': '2025-02-10'},
        {'name': 'Community Center Donation Day', 'date': '2025-02-15'},
        {'name': 'University Blood Donation Camp', 'date': '2025-02-20'}
    ]
    return render_template('partials/event_list.html', events=events)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
