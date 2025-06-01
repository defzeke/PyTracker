document.addEventListener('DOMContentLoaded', function() {
    // Get the clear button and all dropdown elements
    const clearBtn = document.getElementById('clear-btn');
    const dropdowns = [
        document.getElementById('course-dropdown'),
        document.getElementById('section-dropdown'),
        document.getElementById('subject-dropdown')
    ];

    // When the clear button is clicked, reset all dropdowns to their first option
    clearBtn.addEventListener('click', function() {
        dropdowns.forEach(select => {
            if (select) select.selectedIndex = 0;
        });
    });
});