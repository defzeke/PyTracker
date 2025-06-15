const termsRadio = document.getElementById('terms-radio');
const termsLabel = document.getElementById('terms-label');
const termsModal = document.getElementById('terms-modal');
const acceptTerms = document.getElementById('accept-terms');
const closeTerms = document.getElementById('close-terms');
const termsContent = document.getElementById('terms-content');

// Open modal when label is clicked
termsLabel.addEventListener('click', function(e) {
    e.preventDefault();
    termsModal.style.display = 'block';
    acceptTerms.disabled = true;
});

// Also prevent radio from being checked directly
termsRadio.addEventListener('click', function(e) {
    e.preventDefault();
    termsModal.style.display = 'block';
    acceptTerms.disabled = true;
});

// Enable accept button only when scrolled to bottom
termsContent.addEventListener('scroll', function() {
    if (termsContent.scrollTop + termsContent.clientHeight >= termsContent.scrollHeight - 5) {
        acceptTerms.disabled = false;
        acceptTerms.classList.add('active-accept');
    } else {
        acceptTerms.disabled = true;
        acceptTerms.classList.remove('active-accept');
    }
});

// Close modal when clicking outside the modal content
termsModal.addEventListener('click', function(e) {
    if (e.target === termsModal) {
        termsModal.style.display = 'none';
    }
});

// Accept terms: check radio and close modal
acceptTerms.addEventListener('click', function() {
    termsRadio.checked = true;
    termsModal.style.display = 'none';
});

// Close modal without accepting
closeTerms.addEventListener('click', function() {
    termsModal.style.display = 'none';
});

// Prevent form submission if terms are not accepted
document.querySelector('form').addEventListener('submit', function(e) {
    if (!termsRadio.checked) {
        e.preventDefault();
        alert("You must accept the Terms and Conditions before continuing.");
    }
});