document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('generate-password').addEventListener('click', function() {
        generatePassword();
    });

    document.getElementById('copy-button').addEventListener('click', function() {
        copyPassword();
    });
});

function generatePassword() {
    const lengthInput = document.getElementById('length');
    const length = lengthInput.value;
    const errorMessageElement = document.getElementById('length-error');

    // Clear previous error message
    errorMessageElement.textContent = '';

    // Validate password length input
    if (!length || length <= 0) {
        errorMessageElement.textContent = 'This field cannot be empty and must be a positive number';
        lengthInput.classList.add('error');
        return;
    } else {
        lengthInput.classList.remove('error');
    }

    const keyword = document.getElementById('keyword').value;
    const includeUpper = document.getElementById('include-upper').checked ? 'y' : 'n';
    const includeLower = document.getElementById('include-lower').checked ? 'y' : 'n';
    const includeSpecial = document.getElementById('include-special').checked ? 'y' : 'n';
    const includeNumbers = document.getElementById('include-numbers').checked ? 'y' : 'n';
    const excludeChar = document.getElementById('exclude-char').value;

    fetch('/generate_password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            keyword: keyword,
            include_upper: includeUpper,
            include_lower: includeLower,
            include_special: includeSpecial,
            include_numbers: includeNumbers,
            length: length,
            exclude_char: excludeChar
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.password) {
            const generatedPassword = data.password;
            document.getElementById('generated-password').value = generatedPassword;
            checkPasswordStrength(generatedPassword);
        } else {
            console.error('Error: No password returned');
            document.getElementById('password-strength-value').textContent = 'Error generating password';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('password-strength-value').textContent = 'Error generating password';
    });
}

function copyPassword() {
    const copyText = document.getElementById('generated-password');
    copyText.select();
    document.execCommand('copy');
    // Optional: Provide feedback to the user
    alert('Password copied to clipboard!');
}

function checkPasswordStrength(password) {
    fetch('/check_password_strength', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ password: password }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.strength) {
            const strength = data.strength;
            document.getElementById('password-strength-value').textContent = strength;
            document.getElementById('feedback').textContent = data.feedback || 'No feedback available.';
            document.getElementById('crack-time-seconds').textContent = data.crack_time_seconds || 'N/A';
            document.getElementById('crack-time-display').textContent = data.crack_time_display || 'N/A';
        } else {
            console.error('Error: No strength returned');
            document.getElementById('password-strength-value').textContent = 'Error checking password strength';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('password-strength-value').textContent = 'Error checking password strength';
    });
}
