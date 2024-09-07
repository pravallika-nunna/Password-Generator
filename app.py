from flask import Flask, render_template, request, jsonify, redirect, url_for, session

# Import your password generation and strength checker classes
from generate_password import Password
from password_strength import PasswordStrengthChecker

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set this to a secure key in production

# Initialize the strength checker
strength_checker = PasswordStrengthChecker()

# Dummy user data (replace with your user storage logic)
users = {'test@example.com': 'password'}  # Example user dictionary (email: password)

@app.route('/')
def index():
    # Ensure that only logged-in users can access the index page
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/generate_password', methods=['POST'])
def generate_password():
    data = request.json
    options = {
        'include_upper': data.get('include_upper', 'n').lower() == 'y',
        'include_lower': data.get('include_lower', 'n').lower() == 'y',
        'include_numbers': data.get('include_numbers', 'n').lower() == 'y',
        'include_special': data.get('include_special', 'n').lower() == 'y',
        'length': int(data.get('length', 8)),
        'exclude_char': data.get('exclude_char', "")
    }
    keyword = data.get('keyword', "")

    password_generator = Password(options)
    generated_password = password_generator.password_generator(keyword) if keyword else password_generator.password_generator()

    return jsonify(password=generated_password)

@app.route('/check_password_strength', methods=['POST'])
def check_password_strength():
    data = request.json
    password = data.get('password', '')

    if not password:
        return jsonify(error='Password is required'), 400

    # Check the strength of the password using the strength_checker
    strength_info = strength_checker.check_strength(password)

    return jsonify(strength_info)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the user exists and the password matches
        if email in users and users[email] == password:
            session['user'] = email  # Store the user's email in the session
            return redirect(url_for('index'))
        else:
            return render_template('login_page.html', error="Invalid email or password")
    
    return render_template('login_page.html')

@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']

    # Check if the user already exists
    if email in users:
        return render_template('login_page.html', error="User already exists. Please login.")

    # Register the user
    users[email] = password
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove user from session
    return redirect(url_for('login'))

@app.route('/generate_and_store', methods=['GET', 'POST'])
def generate_and_store():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Handle password generation and storage
        data = request.form
        options = {
            'include_upper': data.get('include_upper', 'n').lower() == 'y',
            'include_lower': data.get('include_lower', 'n').lower() == 'y',
            'include_numbers': data.get('include_numbers', 'n').lower() == 'y',
            'include_special': data.get('include_special', 'n').lower() == 'y',
            'length': int(data.get('length', 8)),
            'exclude_char': data.get('exclude_char', "")
        }
        keyword = data.get('keyword', "")
        
        password_generator = Password(options)
        generated_password = password_generator.password_generator(keyword) if keyword else password_generator.password_generator()
        
        # Store the password logic here
        # For example, you might save it to a database or session (just an example)
        # session['generated_password'] = generated_password

        return render_template('index.html', password=generated_password)
    
    return render_template('index.html')

@app.route('/routes')
def list_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': list(rule.methods - set(['HEAD', 'OPTIONS'])),
            'url': str(rule)
        })
    return jsonify(routes)

if __name__ == '__main__':
    app.run(debug=True)