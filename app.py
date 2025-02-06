from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import config

app = Flask(__name__)
app.config.from_object(config.Config)

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html', title='Blood Donation App')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cur.fetchone()
        if existing_user:
            cur.close()
            return render_template('partials/signup_form.html', error='Username already exists.')
        
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        cur.close()
        
        return render_template('partials/signup_form.html', success='Signup successful! Please login.')
    return render_template('signup.html', title='Sign Up')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[2], password):
            session['username'] = user[1]
            return jsonify({'redirect': url_for('index')})
        return render_template('partials/login_form.html', error='Invalid username or password')
    return render_template('login.html', title='Login')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# This is an exmaple, will be removed later.
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
    app.run(host='0.0.0.0', port=5000)
