// Track if the captcha has been successfully verified
let captchaVerified = false;

// Callback for when the captcha is solved
function onCaptchaSuccess() {
    captchaVerified = true;
    const captchaSection = document.getElementById('captcha-section');
    const otpSection = document.getElementById('otp-section');
    const otpContainer = document.querySelector('.otp-container');

    // Fade out the captcha section
    captchaSection.style.transition = "opacity 0.5s";
    captchaSection.style.opacity = 0;

    setTimeout(() => {
        // Hide captcha, show OTP section and container
        captchaSection.style.display = "none";
        otpSection.style.display = "block";
        if (otpContainer) otpContainer.style.display = "flex"; // Show the OTP container if it exists
        setTimeout(() => {
            otpSection.style.opacity = 1;
        }, 10);
    }, 500);

    checkEnableSignup();
}

// Enable the signup button only if captcha is verified and OTP is complete
function checkEnableSignup() {
    const otpDigits = document.querySelectorAll('.otp-digit');
    const signupBtn = document.getElementById('signup-btn');
    let otpValue = '';

    // Combine all OTP digit inputs into one value
    otpDigits.forEach(input => otpValue += input.value);
    document.getElementById('otp-input').value = otpValue;

    // Enable button if captcha is verified and all OTP digits are filled with numbers
    if (captchaVerified && otpValue.length === otpDigits.length && /^[0-9]+$/.test(otpValue)) {
        signupBtn.disabled = false;
    } else {
        signupBtn.disabled = true;
    }
}

// Set up OTP input behavior on page load
document.addEventListener('DOMContentLoaded', function() {
    const otpDigits = document.querySelectorAll('.otp-digit');
    otpDigits.forEach((input, idx) => {
        // Only allow digits and auto-focus next input
        input.addEventListener('input', function(e) {
            input.value = input.value.replace(/[^0-9]/g, ''); // Only allow digits
            if (input.value.length === 1 && idx < otpDigits.length - 1) {
                otpDigits[idx + 1].focus();
            }
            checkEnableSignup();
        });
        // Move focus to previous input on backspace if empty
        input.addEventListener('keydown', function(e) {
            if (e.key === "Backspace" && input.value === "" && idx > 0) {
                otpDigits[idx - 1].focus();
            }
        });
    });
});