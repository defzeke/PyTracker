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

        // Show only the matching content section
        const contentIds = ['dashboard-content', 'attendance-content', 'addclass-content'];
        contentIds.forEach(id => {
            const el = document.getElementById(id);
            if (el) el.style.display = 'none';
        });
        if (this.id === 'dashboard-logo') {
            document.getElementById('dashboard-content').style.display = 'block';
        } else if (this.id === 'attendance-logo') {
            document.getElementById('attendance-content').style.display = 'block';
        } else if (this.id === 'addclass-logo') {
            document.getElementById('addclass-content').style.display = 'block';
        }
    });
});

// Show dashboard by default on page load
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('dashboard-content').style.display = 'block';
    document.getElementById('attendance-content').style.display = 'none';
    document.getElementById('addclass-content').style.display = 'none';
});