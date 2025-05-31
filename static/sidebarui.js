document.querySelectorAll('.sidebar-icon').forEach(icon => {
        icon.addEventListener('click', function() {
            // Remove 'active' class from all icons and set to inactive image
            document.querySelectorAll('.sidebar-icon').forEach(i => {
                i.classList.remove('active');
                i.src = i.getAttribute('data-inactive');
            });
            // Set this icon to active
            this.classList.add('active');
            this.src = this.getAttribute('data-active');
        });
    });