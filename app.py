from flask import Flask, render_template, request, jsonify
from generate_password import Password
from password_strength import PasswordStrengthChecker

app = Flask(__name__)

# Initialize the strength checker
strength_checker = PasswordStrengthChecker()

@app.route('/')
def index():
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

    # Check the strength of the password using zxcvbn
    strength = strength_checker.check_strength(password)

    return jsonify(password=password, strength=strength)

if __name__ == '__main__':
    app.run(debug=True)