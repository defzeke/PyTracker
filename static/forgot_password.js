function showWaitModal() {
    document.getElementById('wait-modal').style.display = 'block';
}
function hideWaitModal() {
    document.getElementById('wait-modal').style.display = 'none';
}

document.getElementById('otp-form').addEventListener('submit', function(e) {
    let otpValue = '';
    document.querySelectorAll('.otp-digit').forEach(input => otpValue += input.value);
    document.getElementById('otp-input').value = otpValue;
});

document.getElementById('check-id-btn').addEventListener('click', function() {
    const idInput = document.getElementById('reset-id-number');
    const idNumber = idInput.value.trim();
    showWaitModal();

    fetch('/check_id', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({id_number: idNumber})
    })
    .then(response => response.json())
    .then(data => {
        hideWaitModal();
        if (data.exists) {
            document.getElementById('reset-otp-section').style.display = 'block';
            document.getElementById('reset-resend-container').style.display = 'block';
            idInput.readOnly = true;
            document.getElementById('check-id-btn').style.display = 'none';
            document.getElementById('user-email').textContent = data.email;
        } else {
            alert('No such ID number is registered.');
            document.getElementById('reset-otp-section').style.display = 'none';
            document.getElementById('reset-resend-container').style.display = 'none';
        }
    })
    .catch(() => {
        hideWaitModal();
        alert('An error occurred. Please try again.');
    });
});

document.getElementById('reset-resend-code').addEventListener('click', function() {
    const btn = this;
    const status = document.getElementById('reset-resend-status');
    let countdown = 180; 

    btn.disabled = true;
    status.textContent = `Available in ${countdown}s`;

    const timer = setInterval(() => {
        countdown--;
        if (countdown > 0) {
            status.textContent = `Available in ${countdown}s`;
        } else {
            clearInterval(timer);
            btn.disabled = false;
            status.textContent = "";
        }
    }, 1000);
    fetch('/resend_otp', {method: 'POST'})
        .catch(() => {
        });
});

document.getElementById('otp-form').addEventListener('submit', function(e) {
e.preventDefault();
    let otpValue = '';
    document.querySelectorAll('.otp-digit').forEach(input => otpValue += input.value);

    fetch('/check_otp', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({otp: otpValue})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = "/change-password";
        } else {
            alert(data.error || "Incorrect OTP. Please try again.");
        }
    })
    .catch(() => {
        alert('An error occurred. Please try again.');
    });
});

document.getElementById('resend-code').addEventListener('click', function() {
    const btn = this;
    const status = document.getElementById('resend-status');
    let countdown = 180

    btn.disabled = true;
    status.textContent = `Available in ${countdown}s`;

    const timer = setInterval(() => {
        countdown--;
        if (countdown > 0) {
            status.textContent = `Available in ${countdown}s`;
        } else {
            clearInterval(timer);
            btn.disabled = false;
            status.textContent = "";
        }
    }, 1000);

    fetch('/resend_otp', {method: 'POST'})
        .catch(() => {
        });
});