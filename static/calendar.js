document.addEventListener("DOMContentLoaded", function() {
    const calendarImg = document.getElementById("calendar-image");
    const calendarPopover = document.getElementById("calendar-popover");

    calendarImg.addEventListener("click", function() {
        calendarPopover.style.display = (calendarPopover.style.display === "block") ? "none" : "block";
    });

    // Only close if click is outside BOTH the popover and the image
    document.addEventListener("click", function(e) {
        if (
            calendarPopover.style.display === "block" &&
            !calendarPopover.contains(e.target) &&
            e.target !== calendarImg
        ) {
            calendarPopover.style.display = "none";
        }
    });

    // Remove any previous calendar
    document.getElementById('calendar-container').innerHTML = "";

    // Initialize Pikaday
    if (window.Pikaday) {
        new Pikaday({
            field: document.createElement('input'),
            container: document.getElementById('calendar-container'),
            bound: false,
            defaultDate: new Date(),
            setDefaultDate: true,
            firstDay: 1,
            format: 'YYYY-MM-DD'
        });
    } else {
        document.getElementById('calendar-container').innerHTML =
            `<div style="font-size:1.5em; font-weight:bold; text-align:center; margin:24px 0;">
                ${new Date().toLocaleDateString()}
            </div>`;
    }
});