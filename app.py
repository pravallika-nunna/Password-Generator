from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
from generate_password import PasswordGenerator
import sqlite3
import re
import hashlib
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for flash messages
password_gen = PasswordGenerator()

# Hashing function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Check if user exists
def user_exists(email):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    return user

# Register a new user
def register_user(username, email, password):
    hashed_password = hash_password(password)
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                   (username, email, hashed_password))
    conn.commit()
    conn.close()

# Validate email format
def is_valid_email(email):
    email_regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(email_regex, email) is not None

@app.route('/')
def index():
    if 'logged_in' in session and session['logged_in']:
        return render_template('index.html')  # Password generator page
    else:
        return redirect(url_for('login_page'))
    
# Check if user exists and return the hashed password if they do
def get_user_password(email):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE email = ?', (email,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not is_valid_email(email):
            flash("Invalid email format. Please enter a valid email.", 'error')
            return redirect(url_for('login_page'))

        stored_password_hash = get_user_password(email)
        if stored_password_hash:
            if hash_password(password) == stored_password_hash:
                session['logged_in'] = True
                session['username'] = email  # Set username in session
                flash("Logged in successfully.", 'success')
                return redirect(url_for('index'))
            else:
                flash("Invalid email or password. Please try again.", 'error')
                return redirect(url_for('login_page'))
        else:
            flash("User does not exist. Please register.", 'error')
            return redirect(url_for('register_page'))

    return render_template('login_page.html')


@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    if not is_valid_email(email):
        return jsonify({'success': False, 'message': 'Invalid email format. Please enter a valid email.'})

    if user_exists(email):
        return jsonify({'success': False, 'message': 'Email already registered. Please choose a different email.'})

    register_user(username, email, password)
    return jsonify({'success': True, 'message': 'Registration successful! Please log in.'})

@app.route('/generate-password', methods=['POST'])
def generate_password_route():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login_page'))

    data = request.json
    include_lower = data.get('includeLower', False)
    include_upper = data.get('includeUpper', False)
    include_numbers = data.get('includeNumbers', False)
    include_special = data.get('includeSpecial', False)
    keyword = data.get('keyword', '')
    exclude_char = data.get('excludeChar', '')
    length = data.get('length', 8)

    # Set options and keyword
    options = {
        'include_lower': include_lower,
        'include_upper': include_upper,
        'include_numbers': include_numbers,
        'include_special': include_special,
        'exclude_char': exclude_char,
        'length': length
    }
    password_gen.set_options(options)
    password_gen.set_keyword(keyword)

    # Generate password
    password_data = password_gen.generate_password()
    
    return jsonify(password_data)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True)