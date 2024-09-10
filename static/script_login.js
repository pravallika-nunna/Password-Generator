document.addEventListener('DOMContentLoaded', () => {
    const wrapper = document.querySelector('.wrapper');
    const btnPopup = document.querySelector('.btnLogin-popup');
    const loginLink = document.querySelector('.login-link');
    const registerLink = document.querySelector('.register-link');
    const iconCloseButtons = document.querySelectorAll('.icon-close'); 
    const loginForm = document.querySelector('#loginForm');
    const registerForm = document.querySelector('#registerForm');

    // Open the popup
    btnPopup.addEventListener('click', () => {
        wrapper.classList.add('active-popup');
    });

    // Switch to the login form
    loginLink.addEventListener('click', () => {
        wrapper.classList.remove('active');
        wrapper.classList.add('active-login');
    });

    // Switch to the registration form
    registerLink.addEventListener('click', () => {
        console.log('Register link clicked');
        console.log('Adding active-register class');
        wrapper.classList.add('active');
        wrapper.classList.remove('active-login');
    });
    
    // Close the popup when the close button is clicked
    iconCloseButtons.forEach(button => {
        button.addEventListener('click', () => {
            wrapper.classList.remove('active-popup');
        });
    });

    // Close the popup by clicking outside the modal
    window.addEventListener('click', (event) => {
        if (!wrapper.contains(event.target) && event.target !== btnPopup) {
            wrapper.classList.remove('active-popup');
        }
    });

    // Handle login form submission
    if (loginForm) {
        loginForm.addEventListener('submit', (event) => {
            event.preventDefault();
            const email = document.querySelector('#loginEmail').value;
            const password = document.querySelector('#loginPassword').value;

            fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    email: email,
                    password: password
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = '/generate-password-page';  // Redirect to password generation page on successful login
                } else {
                    alert('Login failed: ' + data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }

    // Handle registration form submission
    if (registerForm) {
        registerForm.addEventListener('submit', (event) => {
            event.preventDefault();
            const username = document.querySelector('#registerUsername').value;
            const email = document.querySelector('#registerEmail').value;
            const password = document.querySelector('#registerPassword').value;

            fetch('/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    username: username,
                    email: email,
                    password: password
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Registration successful! Please log in.');
                    loginLink.click();  // Switch to login form after successful registration
                } else {
                    alert('Registration failed: ' + data.message);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }
});