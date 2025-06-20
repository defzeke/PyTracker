let histogramChart = null;

const chartBackgroundPlugin = {
    id: 'custom_canvas_background_color',
    beforeDraw: (chart) => {
        const ctx = chart.canvas.getContext('2d');
        ctx.save();
        ctx.globalCompositeOperation = 'destination-over';
        ctx.fillStyle = document.body.classList.contains('dark-mode') ? '#23234a' : '#fff';
        ctx.fillRect(0, 0, chart.width, chart.height);
        ctx.restore();
    }
};

function getHistogramColors() {
    const isDark = document.body.classList.contains('dark-mode');
    return {
        axisColor: isDark ? "#fff" : "#222",
        gridColor: isDark ? "rgba(255,255,255,0.15)" : "#ddd",
        tooltipBg: isDark ? "#23234a" : "#fff",
        tooltipText: isDark ? "#fff" : "#222",
        legendColor: isDark ? "#fff" : "#222",
        borderColor: isDark ? "#fff" : "#222"
    };
}

function updateHistogramColors() {
    if (!histogramChart) return;
    const colors = getHistogramColors();
    histogramChart.options.scales.x.ticks.color = colors.axisColor;
    histogramChart.options.scales.x.grid.color = colors.gridColor;
    histogramChart.options.scales.y.ticks.color = colors.axisColor;
    histogramChart.options.scales.y.grid.color = colors.gridColor;
    if (histogramChart.options.plugins.tooltip) {
        histogramChart.options.plugins.tooltip.backgroundColor = colors.tooltipBg;
        histogramChart.options.plugins.tooltip.titleColor = colors.tooltipText;
        histogramChart.options.plugins.tooltip.bodyColor = colors.tooltipText;
        histogramChart.options.plugins.tooltip.borderColor = colors.borderColor;
    }
    if (histogramChart.options.plugins.legend && histogramChart.options.plugins.legend.labels) {
        histogramChart.options.plugins.legend.labels.color = colors.legendColor;
    }
    histogramChart.update();
}

document.addEventListener("DOMContentLoaded", function() {
    fetch("/histogram_data_student")
        .then(res => res.json())
        .then(data => {
            if (data.error) throw new Error(data.error);

            const histogramDiv = document.getElementById('histogram');
            histogramDiv.innerHTML = '<canvas id="histogram-canvas"></canvas>';

            const ctx = document.getElementById('histogram-canvas').getContext('2d');
            const colors = getHistogramColors();

            histogramChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: [
                        "Absent", 
                        "Late", 
                        "Attended", 
                        "Days Remaining"
                    ],
                    datasets: [{
                        label: "Count",
                        data: [
                            data["Absent"], 
                            data["Late"], 
                            data["Attended"], 
                            data["Days Remaining"]
                        ],
                        backgroundColor: [
                            "#e74c3c",    // Absent - red
                            "#f1c40f",    // Late - yellow
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
                        legend: { 
                            display: false,
                            labels: {
                                color: colors.legendColor
                            }
                        },
                        tooltip: {
                            enabled: true,
                            backgroundColor: colors.tooltipBg,
                            titleColor: colors.tooltipText,
                            bodyColor: colors.tooltipText,
                            borderColor: colors.borderColor,
                            borderWidth: 1,
                            cornerRadius: 6,
                            padding: 10,
                            callbacks: {
                                label: function(context) {
                                    return `${context.label}: ${context.parsed.y} days`;
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            ticks: { color: colors.axisColor, font: { weight: "bold" } },
                            grid: { color: colors.gridColor }
                        },
                        y: {
                            beginAtZero: true,
                            ticks: { color: colors.axisColor, stepSize: 1 },
                            grid: { color: colors.gridColor }
                        }
                    }
                },
                plugins: [chartBackgroundPlugin]
            });

            // Listen for dark mode toggle and update chart colors
            const darkModeBtn = document.getElementById('dark-mode-btn');
            if (darkModeBtn) {
                darkModeBtn.addEventListener('click', function() {
                    setTimeout(updateHistogramColors, 10);
                });
            }
        })
        .catch(() => {
            document.getElementById("histogram").innerHTML = "<div style='color:#a00;text-align:center;padding:24px;'>Histogram unavailable.</div>";
        });
});