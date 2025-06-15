// Example: Place in static/heatmapprof.js and include in your HTML
document.addEventListener("DOMContentLoaded", function() {
    // Example static data for 2 weeks (Sun-Sat)
    const days = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
    const weeks = ['Week 1','Week 2'];
    const data = [
        [1,0,1,1,0,1,0], // Week 1
        [0,1,1,0,1,0,1]  // Week 2
    ];

    const series = weeks.map((w, wi) => ({
        name: w,
        points: days.map((d, di) => ({
            x: d,
            y: w,
            value: data[wi][di]
        }))
    }));

    JSC.Chart('attendance-heatmap', {
        type: 'heatmap solid',
        legend_visible: false,
        yAxis: { categories: weeks, orientation: 'opposite' },
        xAxis: { categories: days },
        palette: [
            { value: 0, color: '#cccccc', label: 'No Attendance' },
            { value: 1, color: '#2ecc40', label: 'Attended' }
        ],
        defaultTooltip: {
            template: '%yValue %xValue: <b>%value</b>'
        },
        series: series
    });
});