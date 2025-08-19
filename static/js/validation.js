document.addEventListener('DOMContentLoaded', function () {
    const contactForm = document.getElementById('contactForm');
    const successMessage = document.getElementById('successMessage');

    contactForm.addEventListener('submit', function (event) {
        event.preventDefault();
        let isValid = true;

        // Clear previous error messages
        document.querySelectorAll('.error-message').forEach(function (el) {
            el.textContent = '';
        });

        // --- Name Validation ---
        const nameInput = document.getElementById('name');
        const nameError = nameInput.nextElementSibling;
        if (nameInput.value.trim().length < 2) {
            nameError.textContent = 'Full Name must be at least 2 characters.';
            isValid = false;
        }

        // --- Email Validation ---
        const emailInput = document.getElementById('email');
        const emailError = emailInput.nextElementSibling;
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(emailInput.value.trim())) {
            emailError.textContent = 'Please enter a valid email address.';
            isValid = false;
        }

        // --- Message Validation ---
        const messageInput = document.getElementById('message');
        const messageError = messageInput.nextElementSibling;
        if (messageInput.value.trim().length < 10) {
            messageError.textContent = 'Message must be at least 10 characters.';
            isValid = false;
        }

        if (isValid) {
            // Hide the form and show the success message
            contactForm.style.display = 'none';
            successMessage.style.display = 'block';
        }
    });
});
