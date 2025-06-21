document.addEventListener('DOMContentLoaded', function() {
    // List all topbar features and their popovers by id
    const features = [
        { icon: 'notification-logo', popover: 'notification-popover' },
        { icon: 'extender-logo', popover: null } // Add extender logo (no popover)
    ];

    // Helper to close all popovers and deactivate all icons
    function closeAllPopovers() {
        features.forEach(f => {
            const icon = document.getElementById(f.icon);
            const popover = f.popover ? document.getElementById(f.popover) : null;
            // Do NOT deactivate extender-logo here
            if (icon && f.icon !== 'extender-logo') {
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
        const popover = f.popover ? document.getElementById(f.popover) : null;
        if (!icon) return;

        icon.addEventListener('click', function(e) {
            e.stopPropagation();
            // Extender logo: always toggle active/inactive on click and do NOT call closeAllPopovers
            if (f.icon === 'extender-logo') {
                icon.classList.toggle('active');
                if (icon.classList.contains('active')) {
                    if (icon.hasAttribute('data-active')) {
                        icon.src = icon.getAttribute('data-active');
                    }
                } else {
                    if (icon.hasAttribute('data-inactive')) {
                        icon.src = icon.getAttribute('data-inactive');
                    }
                }
                return; // Prevent any other logic from running
            }
            // Other icons: popover logic
            if (icon.classList.contains('active')) {
                closeAllPopovers();
            } else {
                closeAllPopovers();
                icon.classList.add('active');
                if (icon.hasAttribute('data-active')) {
                    icon.src = icon.getAttribute('data-active');
                }
                if (popover) popover.style.display = 'block';
            }
        });
    });

    // Hide popovers when clicking outside
    document.addEventListener('click', function(e) {
        let clickedInside = false;
        features.forEach(f => {
            const icon = document.getElementById(f.icon);
            const popover = f.popover ? document.getElementById(f.popover) : null;
            if (popover && (popover.contains(e.target) || e.target === icon)) {
                clickedInside = true;
            }
            // Extender logo: don't close on outside click
            if (f.icon === 'extender-logo' && e.target === icon) {
                clickedInside = true;
            }
        }); 
        if (!clickedInside) {
            closeAllPopovers();
        }
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const topbarIcons = document.querySelectorAll('.topbar-icon');
    const tooltip = document.getElementById('topbar-tooltip');
    let tooltipTimer = null;

    topbarIcons.forEach(icon => {
        icon.addEventListener('mouseenter', function(e) {
            tooltipTimer = setTimeout(() => {
                const tooltipText = icon.getAttribute('data-tooltip');
                if (tooltipText) {
                    tooltip.textContent = tooltipText;
                    tooltip.style.opacity = 1;
                    // Position tooltip below the icon
                    const rect = icon.getBoundingClientRect();
                    tooltip.style.left = rect.left + window.scrollX + rect.width / 2 - tooltip.offsetWidth / 2 + 'px';
                    tooltip.style.top = rect.bottom + window.scrollY + 8 + 'px';
                }
            }, 500); 
        });
        icon.addEventListener('mouseleave', function() {
            clearTimeout(tooltipTimer);
            tooltip.style.opacity = 0;
        });
    });
});

function showNotificationModal() {
    const bell = document.getElementById('notification-logo');
    const modal = document.getElementById('notification-modal');
    const content = document.getElementById('notification-modal-content');
    // Position the modal just below the bell
    const rect = bell.getBoundingClientRect();
    modal.style.left = (rect.left + window.scrollX - 180) + 'px'; 
    modal.style.top = (rect.bottom + window.scrollY + 10) + 'px'; 
    modal.style.display = 'block';

    // Load notifications
    fetch('/get_notifications')
        .then(res => res.json())
        .then(notifs => {
            if (!notifs.length) {
                content.innerHTML = "<p style='margin:12px 0;'>No new notifications</p>";
            } else {
                content.innerHTML = notifs.map(n =>
                    `<div class="notif-item">
                        <div class="notif-message">${n.message}</div>
                        <div class="notif-date">${n.created_at}</div>
                    </div>`
                ).join('');
            }
        });
}

// Show/hide modal on bell click
document.getElementById('notification-logo').addEventListener('click', function(e) {
    e.stopPropagation();
    const modal = document.getElementById('notification-modal');
    if (modal.style.display === 'block') {
        modal.style.display = 'none';
    } else {
        showNotificationModal();
    }
});

// Hide modal when clicking outside
document.addEventListener('click', function(e) {
    const modal = document.getElementById('notification-modal');
    const bell = document.getElementById('notification-logo');
    if (!modal.contains(e.target) && e.target !== bell) {
        modal.style.display = 'none';
    }
});