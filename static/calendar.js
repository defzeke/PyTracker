document.addEventListener('DOMContentLoaded', function() {
    const calendarIcon = document.getElementById('calendar-image');
    const calendarPopover = document.getElementById('calendar-popover');

    if (!calendarIcon || !calendarPopover) return;

    calendarIcon.addEventListener('click', function(e) {
        e.stopPropagation();
        // Toggle active state
        if (calendarIcon.classList.contains('active')) {
            calendarIcon.classList.remove('active');
            calendarIcon.src = calendarIcon.getAttribute('data-inactive');
            calendarPopover.style.display = 'none';
        } else {
            calendarIcon.classList.add('active');
            calendarIcon.src = calendarIcon.getAttribute('data-active');
            calendarPopover.style.display = 'block';
        }
    });

    // Hide calendar when clicking outside
    document.addEventListener('click', function(e) {
        if (calendarPopover.style.display === 'block' &&
            !calendarPopover.contains(e.target) &&
            e.target !== calendarIcon) {
            calendarPopover.style.display = 'none';
            calendarIcon.classList.remove('active');
            calendarIcon.src = calendarIcon.getAttribute('data-inactive');
        }
    });
});