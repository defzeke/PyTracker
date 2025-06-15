document.addEventListener("DOMContentLoaded", function() {
    fetch("/histogram_data")
        .then(res => res.json())
        .then(data => {
            if (data.error) throw new Error(data.error);

            // Remove any existing canvas (for hot reloads)
            const histogramDiv = document.getElementById('histogram');
            histogramDiv.innerHTML = '<canvas id="histogram-canvas"></canvas>';

            const ctx = document.getElementById('histogram-canvas').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: [
                        "Absent", 
                        "Late", 
                        "No Classes/Excused", 
                        "Attended", 
                        "Days Remaining"
                    ],
                    datasets: [{
                        label: "Count",
                        data: [
                            data["Absent"], 
                            data["Late"], 
                            data["No Classes/Excused"], 
                            data["Attended"], 
                            data["Days Remaining"]
                        ],
                        backgroundColor: [
                            "#e74c3c",    // Absent - red
                            "#f1c40f",    // Late - yellow
                            "#3498db",    // No Classes/Excused - blue
                            "#2ecc40",    // Attended - green
                            "#888888"     // Days Remaining - gray
                        ],
                        borderRadius: 8,
                        borderSkipped: false,
                        maxBarThickness: 48
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            enabled: true,
                            callbacks: {
                                label: function(context) {
                                    // Show the value in a clear format
                                    return `${context.label}: ${context.parsed.y} days`;
                                }
                            },
                            backgroundColor: '#222',
                            titleColor: '#fff',
                            bodyColor: '#fff',
                            borderColor: '#fff',
                            borderWidth: 1,
                            cornerRadius: 6,
                            padding: 10
                        }
                    },
                    scales: {
                        x: {
                            ticks: { color: "#222", font: { weight: "bold" } }
                        },
                        y: {
                            beginAtZero: true,
                            ticks: { stepSize: 1 }
                        }
                    }
                }
            });
        })
        .catch(() => {
            document.getElementById("histogram").innerHTML = "<div style='color:#a00;text-align:center;padding:24px;'>Histogram unavailable.</div>";
        });
});