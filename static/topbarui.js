document.addEventListener('DOMContentLoaded', function() {
    // List all topbar features and their popovers by id
    const features = [
        { icon: 'notification-logo', popover: 'notification-popover' },
        { icon: 'status-logo', popover: 'status-popover' },
        { icon: 'message-logo', popover: 'message-popover' },
        { icon: 'recitation-logo', popover: 'recitation-popover' }
    ];

    // Helper to close all popovers and deactivate all icons
    function closeAllPopovers() {
        features.forEach(f => {
            const icon = document.getElementById(f.icon);
            const popover = document.getElementById(f.popover);
            if (icon) {
                icon.classList.remove('active');
                if (icon.hasAttribute('data-inactive')) {
                    icon.src = icon.getAttribute('data-inactive');
                }
            }
            if (popover) popover.style.display = 'none';
        });
    }

    features.forEach(f => {
        const icon = document.getElementById(f.icon);
        const popover = document.getElementById(f.popover);
        if (!icon || !popover) return;

        icon.addEventListener('click', function(e) {
            e.stopPropagation();
            // If already active, close all
            if (icon.classList.contains('active')) {
                closeAllPopovers();
            } else {
                closeAllPopovers();
                icon.classList.add('active');
                if (icon.hasAttribute('data-active')) {
                    icon.src = icon.getAttribute('data-active');
                }
                popover.style.display = 'block';
            }
        });
    });

    // Hide popovers when clicking outside
    document.addEventListener('click', function(e) {
        let clickedInside = false;
        features.forEach(f => {
            const icon = document.getElementById(f.icon);
            const popover = document.getElementById(f.popover);
            if (popover && (popover.contains(e.target) || e.target === icon)) {
                clickedInside = true;
            }
        });
        if (!clickedInside) {
            closeAllPopovers();
        }
    });
});


// --- Topbar tooltip logic ---
document.addEventListener('DOMContentLoaded', function() {
    let tooltipTimeout;
    let tooltipEl = document.createElement('div');
    tooltipEl.className = 'topbar-tooltip';
    document.body.appendChild(tooltipEl);

    document.querySelectorAll('.topbar-icon').forEach(icon => {
        icon.addEventListener('mouseenter', function(e) {
            tooltipTimeout = setTimeout(() => {
                tooltipEl.textContent = icon.getAttribute('data-tooltip');
                const rect = icon.getBoundingClientRect();
                tooltipEl.style.top = (rect.bottom + 8) + 'px'; // show below icon
                tooltipEl.style.left = (rect.left + rect.width / 2 - tooltipEl.offsetWidth / 2) + 'px';
                tooltipEl.style.opacity = 1;
            }, 500); // 1 second delay
        });
        icon.addEventListener('mouseleave', function() {
            clearTimeout(tooltipTimeout);
            tooltipEl.style.opacity = 0;
        });
    });
});