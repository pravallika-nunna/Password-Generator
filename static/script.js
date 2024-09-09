document.addEventListener('DOMContentLoaded', function() {
    // Attach event listener for generating password
    document.getElementById('generate-password').addEventListener('click', function() {
        generatePassword();
    });

    // Attach event listener for copying password
    document.getElementById('copy-button').addEventListener('click', function() {
        copyPassword();
    });

    // Attach event listener for password feedback button
    document.getElementById('password-feedback-button').addEventListener('click', function() {
        togglePasswordFeedback(true);
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

    // Show loading indicator
    document.getElementById('password-strength-value').textContent = 'Generating...';

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

            // Show the password feedback button
            document.getElementById('password-feedback-button').style.display = 'block';
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

function togglePasswordFeedback(show) {
    const modal = document.getElementById('feedback-modal');
    if (show) {
        modal.style.display = 'block';  // Show modal
    } else {
        modal.style.display = 'none';   // Hide modal
    }
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
        if (data.password_strength_value) {  // Adjusted to match the backend response key
            const strength = data.password_strength_value;  // Use 'password_strength_value'
            document.getElementById('password-strength-value').textContent = strength;  // Adjusted ID
            document.getElementById('password-feedback').textContent = data.feedback || 'No feedback available.';  // Adjusted ID
            document.getElementById('crack-time-seconds').textContent = data.crack_time_seconds || 'N/A';  // Adjusted ID
            document.getElementById('crack-time-display').textContent = data.crack_time_display || 'N/A';  // Adjusted ID
        } else {
            console.error('Error: No strength returned');
            document.getElementById('password-strength-value').textContent = 'Error checking password strength';  // Adjusted ID
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('password-strength-value').textContent = 'Error checking password strength';  // Adjusted ID
    });
}

function copyPassword() {
    const copyText = document.getElementById('generated-password');
    
    if (!copyText.value) {
        alert('No password to copy!');
        return;
    }

    // Use Clipboard API to copy text
    navigator.clipboard.writeText(copyText.value)
    .then(() => {
        // Show success message
        document.getElementById('copy-message').textContent = 'Password copied to clipboard!';
        
        // Clear the message after a few seconds
        setTimeout(() => {
            document.getElementById('copy-message').textContent = '';
        }, 2000);
    })
    .catch(err => {
        console.error('Error copying password with Clipboard API:', err);
        alert('Failed to copy password. Please try manually.');
    });
}