let captchaVerified = false;

function onCaptchaSuccess() {
    captchaVerified = true;
    const captchaSection = document.getElementById('captcha-section');
    const otpSection = document.getElementById('otp-section');
    const otpContainer = document.querySelector('.otp-container');
    captchaSection.style.transition = "opacity 0.5s";
    captchaSection.style.opacity = 0;
    setTimeout(() => {
        captchaSection.style.display = "none";
        otpSection.style.display = "block";
        if (otpContainer) otpContainer.style.display = "flex"; // Show the OTP container
        setTimeout(() => {
            otpSection.style.opacity = 1;
        }, 10);
    }, 500);
    checkEnableSignup();
}

function checkEnableSignup() {
    const otpDigits = document.querySelectorAll('.otp-digit');
    const signupBtn = document.getElementById('signup-btn');
    let otpValue = '';
    otpDigits.forEach(input => otpValue += input.value);
    document.getElementById('otp-input').value = otpValue;
    if (captchaVerified && otpValue.length === otpDigits.length && /^[0-9]+$/.test(otpValue)) {
        signupBtn.disabled = false;
    } else {
        signupBtn.disabled = true;
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const otpDigits = document.querySelectorAll('.otp-digit');
    otpDigits.forEach((input, idx) => {
        input.addEventListener('input', function(e) {
            // Only allow digits
            input.value = input.value.replace(/[^0-9]/g, '');
            if (input.value.length === 1 && idx < otpDigits.length - 1) {
                otpDigits[idx + 1].focus();
            }
            checkEnableSignup();
        });
        input.addEventListener('keydown', function(e) {
            if (e.key === "Backspace" && input.value === "" && idx > 0) {
                otpDigits[idx - 1].focus();
            }
        });
    });
});