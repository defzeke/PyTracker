document.querySelector('form').addEventListener('submit', function(e) {
    // Get the role from the hidden input and make it lowercase
    const role = document.querySelector('input[name="role"]').value.trim().toLowerCase();
    const email = document.getElementById('email').value.trim();
    let errorMsg = "";

    if ((role === "teacher" || role === "professor") && !email.endsWith("@gmail.com")) {
        errorMsg = "Professors email must end with @gmail.com";
    }
    if (role === "student" && !email.endsWith("@iskolarngbayan.pup.edu.ph")) {
        errorMsg = "Student email must end with @iskolarngbayan.pup.edu.ph";
    }

    if (errorMsg) {
        alert(errorMsg);
        e.preventDefault();
    }
});

document.querySelectorAll('.dropdown-row select').forEach(function(select) {
    select.addEventListener('change', function() {
        if (this.value === "") {
            this.style.color = "#b3b3b3";
        } else {
            this.style.color = "#fff";
        }
    });
    // Set initial color on page load
    if (select.value === "") {
        select.style.color = "#b3b3b3";
    } else {
        select.style.color = "#fff";
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const role = document.querySelector('input[name="role"]').value.trim().toLowerCase();
    const courseSelect = document.getElementById('course');
    const yearSectionSelect = document.getElementById('year-section');

    if (role === "professor") {
        courseSelect.disabled = true;
        yearSectionSelect.disabled = true;
        courseSelect.classList.add('disabled-dropdown');
        yearSectionSelect.classList.add('disabled-dropdown');
    } else {
        courseSelect.disabled = false;
        yearSectionSelect.disabled = false;
        courseSelect.classList.remove('disabled-dropdown');
        yearSectionSelect.classList.remove('disabled-dropdown');
    }
});

// Password strength indicator
const passwordInput = document.getElementById('password');
const strengthDiv = document.getElementById('password-strength');

passwordInput.addEventListener('input', function() {
    const val = passwordInput.value;
    let strength = '';
    let color = '';

    if (val.length < 6) {
        strength = 'Weak';
        color = '#ff4d4d';
    } else if (val.match(/[A-Z]/) && val.match(/[0-9]/) && val.match(/[^A-Za-z0-9]/) && val.length >= 8) {
        strength = 'Strong';
        color = '#4dff4d';
    } else if (val.length >= 6) {
        strength = 'Good';
        color = '#ffd700';
    }

    strengthDiv.textContent = strength ? `Password strength: ${strength}` : '';
    strengthDiv.style.color = color;
});

document.querySelector('form').addEventListener('submit', function(e) {
    // Password match check
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm-password').value;

    if (password.length < 6) {
        alert("Password must be at least 6 characters long");
        e.preventDefault();
        return;
    }

    if (password !== confirmPassword) {
        alert("Passwords do not match");
        e.preventDefault();
        return;
    }
});

document.addEventListener("DOMContentLoaded", function() {
    // Get the role from the hidden input
    var role = document.querySelector('input[name="role"]').value.toLowerCase();
    if (role === "teacher" || role === "professor") {
        document.getElementById("course").disabled = true;
        document.getElementById("year-section").disabled = true;
    }
});
