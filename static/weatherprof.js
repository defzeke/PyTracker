document.addEventListener("DOMContentLoaded", function() {
    function getWeatherIcon(code) {
        if ([0, 1].includes(code)) return "/static/images/Sunny_Weather.png";
        if ([2, 3].includes(code)) return "/static/images/Cloudy_Weather.png";
        if ([45, 48].includes(code)) return "/static/images/Foggy_Weather.png";
        if ((code >= 51 && code <= 67)) return "/static/images/Drizzle_Weather.png";
        if ((code >= 71 && code <= 77)) return "/static/images/weather_snow.png";
        if ((code >= 80 && code <= 82)) return "/static/images/Rainy_Weather.png";
        if ((code >= 95 && code <= 99)) return "/static/images/Storm_Weather.png";
        return "/static/images/weather_unknown.png";
    }
    function getWeatherDesc(code) {
        if ([0, 1].includes(code)) return "Clear";
        if ([2, 3].includes(code)) return "Cloudy";
        if ([45, 48].includes(code)) return "Foggy";
        if ((code >= 51 && code <= 67)) return "Drizzle";
        if ((code >= 71 && code <= 77)) return "Snow";
        if ((code >= 80 && code <= 82)) return "Rainy";
        if ((code >= 95 && code <= 99)) return "Thunderstorm";
        return "Unknown";
    }
    fetch("/weather")
        .then(res => res.json())
        .then(data => {
            if (data.error) throw new Error(data.error);
            const today = data.today;
            const tomorrow = data.tomorrow;
            document.getElementById("weather-today").innerHTML = `
                <div style="display:flex;flex-direction:column;align-items:center;gap:8px;">
                    <img src="${getWeatherIcon(today.weathercode)}" alt="Weather" style="width:48px;height:48px;">
                    <div style="font-weight:bold;">Today</div>
                    <div>${getWeatherDesc(today.weathercode)}</div>
                    <div>${today.temp_min}&deg;C - ${today.temp_max}&deg;C</div>
                </div>
            `;
            document.getElementById("weather-tomorrow").innerHTML = `
                <div style="display:flex;flex-direction:column;align-items:center;gap:8px;">
                    <img src="${getWeatherIcon(tomorrow.weathercode)}" alt="Weather" style="width:48px;height:48px;">
                    <div style="font-weight:bold;">Tomorrow</div>
                    <div>${getWeatherDesc(tomorrow.weathercode)}</div>
                    <div>${tomorrow.temp_min}&deg;C - ${tomorrow.temp_max}&deg;C</div>
                </div>
            `;
        })
        .catch(() => {
            document.getElementById("weather-content").innerHTML = "<div style='color:#a00;text-align:center;'>Weather unavailable.</div>";
        });
});