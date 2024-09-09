from flask import Flask, request, jsonify, send_from_directory
from generate_password import PasswordGenerator

app = Flask(__name__)
password_gen = PasswordGenerator()

@app.route('/')
def home():
    return send_from_directory('.', 'home.html')

@app.route('/generate-password', methods=['POST'])
def generate_password_route():
    data = request.json
    include_lower = data.get('includeLower', False)
    include_upper = data.get('includeUpper', False)
    include_numbers = data.get('includeNumbers', False)
    include_special = data.get('includeSpecial', False)
    keyword = data.get('keyword', '')
    exclude_char = data.get('excludeChar', '')
    length = data.get('length', 8)  # Add this if you want to pass length as well

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

if __name__ == '__main__':
    app.run(debug=True)