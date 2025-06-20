document.addEventListener("DOMContentLoaded", function() {
    fetch("/weather")
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                document.getElementById("weather-today").innerHTML = "<div style='color:#a00;text-align:center;'>Weather unavailable.</div>";
                return;
            }
            // Show Manila, Philippines
            document.getElementById("weather-location").textContent = "Manila, Philippines";

            // Weather icon
            const iconUrl = `https://openweathermap.org/img/wn/${data.icon}@2x.png`;

            // Weather display
            document.getElementById("weather-today").innerHTML = `
                <div style="text-align:center;">
                    <img src="${iconUrl}" alt="${data.description}" style="width:64px;height:64px;background:#272757;border-radius:50%;padding:8px;">
                    <div style="font-weight:bold;font-size:1.2em;margin-top:8px;">${data.city}</div>
                    <div style="font-size:1.1em;">${data.description}</div>
                    <div style="margin-top:8px;">
                        <span style="font-size:2em;font-weight:bold;">${data.temp}°C</span>
                        <div style="font-size:0.95em;color:#888;">
                            Min: ${data.temp_min}°C &nbsp;|&nbsp; Max: ${data.temp_max}°C
                        </div>
                    </div>
                </div>
            `;
            // Optionally, hide tomorrow's card if you only want current weather
            document.getElementById("weather-tomorrow").style.display = "none";
        })
        .catch(() => {
            document.getElementById("weather-today").innerHTML = "<div style='color:#a00;text-align:center;'>Weather unavailable.</div>";
        });
});