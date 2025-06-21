curr_mode = 'light';

document.getElementById("dark-mode-btn").addEventListener("click", function(){
    const light_mode_colors = {
        background: "#E3E9ED", sidebar: "#272757", topbar: "#fff",
        text: "#272757",  dashboard_content: "#F5F7FA", pop_over: "#fff",
        btns:"#fff", dropdown:"#fff", std_card: "#fff"
    };
    const dark_mode_colors = {
        background: "#18192a", sidebar: "#060639", topbar: "#23234a",
        text: "#e0e0e0",  dashboard_content: "#23234a", pop_over: "#23234a",
        btns:"#23234a", dropdown:"#23234a", std_card: "#23234a"
    };

    switch (curr_mode){
        case 'light':
            curr_mode = 'dark';
            change_color(dark_mode_colors);
            break;
        case 'dark':
            curr_mode = 'light';
            change_color(light_mode_colors);
            break;
    }

    function change_color(color_mode){
        // Main backgrounds
        document.body.style.backgroundColor = color_mode.background;
        document.documentElement.style.backgroundColor = color_mode.background;
        let mainContent = document.getElementById('main-content');
        if (mainContent) mainContent.style.backgroundColor = color_mode.background;

        // Sidebar and topbar
        document.getElementById('sidebar').style.backgroundColor = color_mode.sidebar;
        document.getElementById('topbar').style.backgroundColor = color_mode.topbar;

        // Weather text
        if (document.getElementById('weather-greeting')) document.getElementById('weather-greeting').style.color = color_mode.text;
        if (document.getElementById('weather-today')) document.getElementById('weather-today').style.color = color_mode.text;
        if (document.getElementById('weather-tomorrow')) document.getElementById('weather-tomorrow').style.color = color_mode.text;

        // Header text
        Array.from(document.getElementsByClassName('header-text')).forEach(element => {
            element.style.color = color_mode.text;
        });

        // Dashboard rectangles/cards
        Array.from(document.getElementsByClassName('dashboard-element')).forEach(element => {
            element.style.backgroundColor = color_mode.dashboard_content;
            element.style.boxShadow = 'none';
            element.style.borderColor = color_mode.dashboard_content;
        });

        const notifModal = document.getElementById('notification-modal');
            if (notifModal) {
                notifModal.style.backgroundColor = color_mode.pop_over;
                notifModal.style.borderColor     = color_mode.pop_over;
            }
        
        Array.from(document.querySelectorAll('.notif-item')).forEach(el => {
            el.style.backgroundColor   = color_mode.dashboard_content;
            el.style.borderBottomColor = color_mode.dashboard_content;
        });

        Array.from(document.getElementsByClassName('notif-message')).forEach(el => el.style.color = color_mode.text);
        Array.from(document.getElementsByClassName('notif-date')).forEach(el => el.style.color    = color_mode.text);

        // Popovers
        Array.from(document.getElementsByClassName('popover-panel')).forEach(el => {
            el.style.backgroundColor = color_mode.pop_over;
            el.style.borderColor     = color_mode.pop_over;
            el.style.color           = color_mode.text;
        });

        Array.from(document.getElementsByClassName('info-box')).forEach(el => {
            el.style.backgroundColor = color_mode.dashboard_content;
            el.style.borderColor     = color_mode.dashboard_content;
            el.style.color           = color_mode.text;
        });

        // Dashboard rectangles/cards
        Array.from(document.getElementsByClassName('dashboard-element')).forEach(el => {
            el.style.backgroundColor = color_mode.dashboard_content;
            el.style.boxShadow       = 'none';
            el.style.borderColor     = color_mode.dashboard_content;
        });
    

        // Buttons
        Array.from(document.getElementsByClassName('btns')).forEach(element => {
            if (element.id === 'take-attendance-btn' && curr_mode === 'dark'){
                element.style.color = '#e0e0e0';
            }
            else if (element.id === 'take-attendance-btn' && curr_mode === 'light'){
                element.style.color = '#fff';
            }
            else{
                element.style.color = color_mode.text;
            }
        });
        if (document.getElementById('back-to-profile-btn')) {
            document.getElementById('back-to-profile-btn').style.color = color_mode.text;
        }

        // Dropdowns
        Array.from(document.getElementsByClassName('custom-dropdown')).forEach(element => {
            element.style.color = color_mode.text;
            element.style.backgroundColor = color_mode.dropdown;
            element.style.borderColor = color_mode.dropdown;
        });

        // Student cards
        Array.from(document.getElementsByClassName('student-card')).forEach(element => {
            element.style.backgroundColor = color_mode.std_card;
            element.style.boxShadow = 'none';
            element.style.borderColor = color_mode.std_card;
        });

        // Student names
        Array.from(document.getElementsByClassName('student-name')).forEach(element => {
            element.style.color = color_mode.text;
        });
    }

    console.log(curr_mode)
});