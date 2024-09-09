document.addEventListener('DOMContentLoaded', () => {
    const wrapper = document.querySelector('.wrapper');
    const btnPopup = document.querySelector('.btnLogin-popup');
    const loginLink = document.querySelector('.login-link');
    const registerLink = document.querySelector('.register-link');
    const iconCloseButtons = document.querySelectorAll('.icon-close'); 

    // Open the popup
    btnPopup.addEventListener('click', () => {
        wrapper.classList.add('active-popup');
    });

    // Switch to the login form
    loginLink.addEventListener('click', () => {
        wrapper.classList.remove('active');
        //wrapper.classList.add('active-login');
    });

    // Switch to the registration form
    registerLink.addEventListener('click', () => {
        console.log('Register link clicked');
        console.log('Adding active-register class');
        wrapper.classList.add('active');
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
});
