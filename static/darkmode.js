curr_mode = 'light';

document.getElementById("dark-mode-btn").addEventListener("click", function(){
    const light_mode_colors = {background: "#E3E9ED", sidebar: "#272757", topbar: "#fff",
                               text: "#272757",  dashboard_content: "#F5F7FA", pop_over: "#fff",
                               btns:"#fff", dropdown:"#fff", std_card: "#fff"
    };
    const dark_mode_colors = {background: "#2b324f", sidebar: "#060639", topbar: "#54536f",
                               text: "#c2cdd5",  dashboard_content: "#646385", pop_over: "#646385",
                               btns:"#646385", dropdown:"#646385", std_card: "#646385"
    };

    switch (curr_mode){
        case 'light':
            curr_mode = 'dark';

            change_color(dark_mode_colors)

            break;
        case 'dark':
            curr_mode = 'light';

            change_color(light_mode_colors)

            break;
    }


    function change_color(color_mode){
            document.body.style.backgroundColor = color_mode.background;
            document.getElementById('sidebar').style.backgroundColor = color_mode.sidebar;
            document.getElementById('topbar').style.backgroundColor = color_mode.topbar;
            document.getElementById('weather-greeting').style.color = color_mode.text;
            document.getElementById('weather-today').style.color = color_mode.text;
            document.getElementById('weather-tomorrow').style.color = color_mode.text;

            Array.from(document.getElementsByClassName('header-text')).forEach(element => {
                element.style.color = color_mode.text;
            });

            Array.from(document.getElementsByClassName('dashboard-element')).forEach(element => {
                element.style.backgroundColor = color_mode.dashboard_content;
            });

            Array.from(document.getElementsByClassName('popover-panel')).forEach(element => {
                element.style.color = color_mode.text;
                element.style.backgroundColor = color_mode.pop_over;
                element.style.borderColor = color_mode.pop_over;
                
                if (element.id === 'profile-popover' || element.id === 'account-settings-popover'){
                    element.style.setProperty('--triangle', `16px solid ${color_mode.pop_over}`);
                }
                else{
                    element.style.setProperty('--triangle', `16px solid ${color_mode.pop_over}`);
                }
                    
            });

            Array.from(document.getElementsByClassName('btns')).forEach(element => {
                if (element.id === 'take-attendance-btn' && curr_mode === 'dark'){
                    element.style.color = '#c2cdd5';
                }
                else if (element.id === 'take-attendance-btn' && curr_mode === 'light'){
                    element.style.color = '#fff';
                }
                else{
                    element.style.color = color_mode.text;
                }
            });
            document.getElementById('back-to-profile-btn').style.color = color_mode.text;


            Array.from(document.getElementsByClassName('custom-dropdown')).forEach(element => {
                element.style.color = color_mode.text;
                element.style.backgroundColor = color_mode.dropdown;
                element.style.borderColor = color_mode.dropdown
            });

            Array.from(document.getElementsByClassName('student-card')).forEach(element => {
                element.style.backgroundColor = color_mode.std_card;
            });

            Array.from(document.getElementsByClassName('student-name')).forEach(element => {
                element.style.color = color_mode.text;
            });

    };

    console.log(curr_mode)
});
