document.addEventListener('DOMContentLoaded', function () {
    const contactForm = document.getElementById('contactForm');
    const successMessage = document.getElementById('successMessage');

    const iconHTML = '<i class="fas fa-exclamation-circle" aria-hidden="true"></i>';

    function setError(input, message) {
        const errorEl = input.nextElementSibling;
        if (!errorEl) return;
        input.classList.add('invalid');
        errorEl.innerHTML = `${iconHTML}<span>${message}</span>`;
    }

    function clearError(input) {
        const errorEl = input.nextElementSibling;
        if (!errorEl) return;
        input.classList.remove('invalid');
        errorEl.innerHTML = '';
    }

    function validateName() {
        const nameInput = document.getElementById('name');
        const value = nameInput.value.trim();
        if (!value) {
            setError(nameInput, 'Please enter your name.');
            return false;
        }
        if (value.length < 2) {
            setError(nameInput, 'Full Name must be at least 2 characters.');
            return false;
        }
        clearError(nameInput);
        return true;
    }

    function validateEmail() {
        const emailInput = document.getElementById('email');
        const value = emailInput.value.trim();
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!value) {
            setError(emailInput, 'Please enter your email address.');
            return false;
        }
        if (!emailPattern.test(value)) {
            setError(emailInput, 'Please enter a valid email address.');
            return false;
        }
        clearError(emailInput);
        return true;
    }

    function validateMessage() {
        const messageInput = document.getElementById('message');
        const value = messageInput.value.trim();
        if (!value) {
            setError(messageInput, 'Please enter your message.');
            return false;
        }
        if (value.length < 10) {
            setError(messageInput, 'Message must be at least 10 characters.');
            return false;
        }
        clearError(messageInput);
        return true;
    }

    // Live validation
    ['input', 'blur'].forEach(evt => {
        document.getElementById('name').addEventListener(evt, validateName);
        document.getElementById('email').addEventListener(evt, validateEmail);
        document.getElementById('message').addEventListener(evt, validateMessage);
    });

    contactForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const ok = [validateName(), validateEmail(), validateMessage()].every(Boolean);
        if (ok) {
            // Clear any previous errors
            ['name','email','message'].forEach(id => clearError(document.getElementById(id)));

            // Reset form but keep it visible
            contactForm.reset();

            // Announce success at the top
            if (successMessage) {
                successMessage.innerHTML = `
                    <span class="success-icon" aria-hidden="true"><i class="fas fa-check"></i></span>
                    <span class="success-text">Your message has been sent successfully!</span>
                    <button type="button" class="success-close" aria-label="Dismiss notification">&times;</button>
                `;
                successMessage.style.display = 'flex';
                successMessage.setAttribute('role', 'status');
                successMessage.setAttribute('aria-live', 'polite');

                // Dismiss on click of close button
                const closeBtn = successMessage.querySelector('.success-close');
                if (closeBtn) {
                    closeBtn.addEventListener('click', () => {
                        successMessage.style.display = 'none';
                        successMessage.innerHTML = '';
                    }, { once: true });
                }

                // No auto-hide; user dismisses via the close button only
            }
        }
    });
});
