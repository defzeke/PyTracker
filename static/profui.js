// Sidebar toggle
document.getElementById("extender-logo").addEventListener("click", () => {
  const sidebar = document.getElementById("sidebar");
  sidebar.classList.toggle("sidebar-hidden");
});

// Popover toggles
const togglePopover = (triggerId, popoverId) => {
  const trigger = document.getElementById(triggerId);
  const popover = document.getElementById(popoverId);

  trigger.addEventListener("click", (e) => {
    e.stopPropagation();
    document.querySelectorAll('.popover-panel').forEach(p => {
      if (p !== popover) p.style.display = "none";
    });
    popover.style.display = (popover.style.display === "none" || popover.style.display === "") ? "block" : "none";
  });
};

togglePopover("status-logo", "status-popover");
togglePopover("message-logo", "message-popover");
togglePopover("recitation-logo", "recitation-popover");
togglePopover("notification-logo", "notification-popover");
togglePopover("calendar-image", "calendar-popover");
togglePopover("profile-logo", "profile-popover");

// Account Settings Popover
document.getElementById("account-btn").addEventListener("click", () => {
  document.getElementById("profile-popover").style.display = "none";
  document.getElementById("account-settings-popover").style.display = "block";
});

document.getElementById("back-to-profile-btn").addEventListener("click", () => {
  document.getElementById("account-settings-popover").style.display = "none";
  document.getElementById("profile-popover").style.display = "block";
});

// Hide all popovers when clicking outside
document.addEventListener("click", () => {  
  document.querySelectorAll('.popover-panel').forEach(p => {
    p.style.display = "none";
  });
});

function showSection(section) {
    document.getElementById('main-content').style.display = (section === 'dashboard') ? 'block' : 'none';
    document.getElementById('attendance-content').style.display = (section === 'attendance') ? 'block' : 'none';
    document.getElementById('addclass-content').style.display = (section === 'addclass') ? 'block' : 'none';
}

// Sidebar click handlers
document.getElementById('dashboard-logo').addEventListener('click', () => showSection('dashboard'));
document.getElementById('attendance-logo').addEventListener('click', () => showSection('attendance'));
document.getElementById('addclass-logo').addEventListener('click', () => showSection('addclass'));

// On load, show dashboard only
showSection('dashboard');


