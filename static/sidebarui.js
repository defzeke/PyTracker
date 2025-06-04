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

    // --- Tooltip logic starts here ---
    let tooltipTimeout;
    let tooltipEl = document.createElement('div');
    tooltipEl.className = 'sidebar-tooltip';
    document.body.appendChild(tooltipEl);

    document.querySelectorAll('.sidebar-icon').forEach(icon => {
        icon.addEventListener('mouseenter', function(e) {
            tooltipTimeout = setTimeout(() => {
                tooltipEl.textContent = icon.getAttribute('data-tooltip');
                const rect = icon.getBoundingClientRect();
                tooltipEl.style.top = (rect.top + rect.height / 2 - 20) + 'px';
                tooltipEl.style.left = (rect.right + 12) + 'px';
                tooltipEl.style.opacity = 1;
            }, 500); // 2 seconds
        });
        icon.addEventListener('mouseleave', function() {
            clearTimeout(tooltipTimeout);
            tooltipEl.style.opacity = 0;
        });
    });
});
