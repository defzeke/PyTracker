// Example: Place in static/heatmapprof.js and include in your HTML
document.addEventListener("DOMContentLoaded", function() {
    fetch("/attendance_heatmap_data")
        .then(res => res.json())
        .then(data => {
            // Cal-Heatmap expects {date: value} where value > 0 is colored
            const cal = new CalHeatmap();
            cal.paint({
                itemSelector: "#attendance-heatmap",
                domain: "month",
                subDomain: "day",
                data: { source: data, x: "date", y: "value" },
                start: new Date(new Date().getFullYear(), new Date().getMonth() - 2, 1),
                range: 7, // Show 7 months (2 before, current, 4 after)
                legend: [0, 1],
                legendColors: {
                    min: "#e3e9ed",
                    max: "#22bb33"
                },
                tooltip: true,
                domainGutter: 8,
                subDomainTextFormat: (date, value) => value > 0 ? "●" : "",
                onClick: function(date, value) {
                    // Optional: handle click
                }
            });
        });
});

// Place this after Cal-Heatmap is loaded and after the DOM is ready
document.addEventListener("DOMContentLoaded", function() {
    const cal = new CalHeatmap();
    cal.paint({
        itemSelector: "#attendance-heatmap",
        domain: "month",
        subDomain: "day",
        data: {
            source: [
                { date: "2025-06-01", value: 1 },
                { date: "2025-06-02", value: 2 },
                { date: "2025-06-03", value: 3 }
            ],
            x: "date",
            y: "value"
        },
        start: new Date(2025, 5, 1), // June 2025
        range: 1,
        legend: [0, 1, 2, 3],
        legendColors: {
            min: "#e3e9ed",
            max: "#22bb33"
        }
    });
});