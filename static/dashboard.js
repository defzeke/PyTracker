document.addEventListener("DOMContentLoaded", function() {
    // Elements
    const clsBtn = document.getElementById('student-class-btn');
    const clsDropdown = document.getElementById('class-dropdown-content');
    const secBtn = document.getElementById('student-section-btn');
    const secDropdown = document.getElementById('section-dropdown-content');

    let profData = null;
    let selectedClass = null;

    // Fetch classes and sections for the logged-in professor
    fetch("/prof_dropdown_data")
        .then(res => res.json())
        .then(data => {
            profData = data;
            // Populate CLS dropdown
            clsDropdown.innerHTML = '';
            data.classes.forEach(cls => {
                const a = document.createElement("a");
                a.textContent = cls.class_ID;
                a.href = "#";
                a.style.display = "block";
                a.style.padding = "8px";
                a.onclick = function(e) {
                    e.preventDefault();
                    clsBtn.textContent = cls.class_ID;
                    selectedClass = cls.class_ID;
                    secBtn.textContent = "SEC";
                    secBtn.disabled = false;
                    secDropdown.innerHTML = '';
                    (profData.class_sections[cls.class_ID] || []).forEach(sec => {
                        const aSec = document.createElement("a");
                        aSec.textContent = sec;
                        aSec.href = "#";
                        aSec.style.display = "block";
                        aSec.style.padding = "8px";
                        aSec.onclick = function(e) {
                            e.preventDefault();
                            secBtn.textContent = sec;
                            secDropdown.style.display = "none";
                        };
                        secDropdown.appendChild(aSec);
                    });
                    clsDropdown.style.display = "none";
                };
                clsDropdown.appendChild(a);
            });
            clsBtn.disabled = false;
        });

    // Show/hide class dropdown
    clsBtn.addEventListener("click", function(e) {
        e.stopPropagation();
        clsDropdown.style.display = clsDropdown.style.display === "block" ? "none" : "block";
        secDropdown.style.display = "none";
    });

    // Show/hide section dropdown
    secBtn.addEventListener("click", function(e) {
        if (secBtn.disabled) return;
        e.stopPropagation();
        secDropdown.style.display = secDropdown.style.display === "block" ? "none" : "block";
        clsDropdown.style.display = "none";
    });

    // Hide dropdowns when clicking outside
    document.addEventListener("click", function() {
        clsDropdown.style.display = "none";
        secDropdown.style.display = "none";
    });
});

function getSelectedClassAndSection() {
    const clsBtn = document.getElementById('student-class-btn');
    const secBtn = document.getElementById('student-section-btn');
    return {
        classId: clsBtn ? clsBtn.textContent.trim() : null,
        section: secBtn ? secBtn.textContent.trim() : null
    };
}

function getSelectedClassAndSection() {
    const clsBtn = document.getElementById('student-class-btn');
    const secBtn = document.getElementById('student-section-btn');
    const classId = clsBtn ? clsBtn.textContent.trim() : null;
    const section = secBtn ? secBtn.textContent.trim() : null;
    return { classId, section };
}

function viewAttendance() {
    // Get class
    let classId = null;
    const classDropdown = document.getElementById('student-class-dropdown');
    const classBtn = document.getElementById('student-class-btn');
    if (classDropdown) {
        classId = classDropdown.value;
    } else if (classBtn) {
        classId = classBtn.textContent.trim();
    }

    // Get section (CYS)
    const sectionBtn = document.getElementById('student-section-btn');
    let section = sectionBtn ? sectionBtn.textContent.trim() : null;

    // Show modal
    document.getElementById('attendance-modal').style.display = 'flex';
    const modalContent = document.getElementById('attendance-modal-content');
    modalContent.innerHTML = '<div style="text-align:center; color:#888;">Loading...</div>';

    if (!classId || classId === "CLS" || !section || section === "SEC") {
        modalContent.innerHTML = '<div style="color:#d32f2f; text-align:center;">Please select a class first.</div>';
        return;
    }

    fetch(`/get_students?class_id=${encodeURIComponent(classId)}&section=${encodeURIComponent(section)}`)
        .then(res => res.json())
        .then(grouped => {
            // Flatten grouped students
            let students = [];
            Object.values(grouped).forEach(arr => students = students.concat(arr));
            if (students.length === 0) {
                modalContent.innerHTML = '<div style="color:#d32f2f; text-align:center;">No students found for this class and section.</div>';
                return;
            }
            // Fetch attendance records for these students
            fetch(`/get_attendance_summary?class_id=${encodeURIComponent(classId)}&section=${encodeURIComponent(section)}`)
                .then(res => res.json())
                .then(attendanceData => {
                    let html = `
                    <div style="max-height: 400px; overflow-y: auto;">
                    <table style="width:100%; border-collapse:collapse; min-width: 700px;">
                        <thead>
                            <tr style="background:#f5f7fa;">
                                <th style="padding:8px; border-bottom:1px solid #e3e9ed;">Name</th>
                                <th style="padding:8px; border-bottom:1px solid #e3e9ed;">Present</th>
                                <th style="padding:8px; border-bottom:1px solid #e3e9ed;">Absent</th>
                                <th style="padding:8px; border-bottom:1px solid #e3e9ed;">Late</th>
                                <th style="padding:8px; border-bottom:1px solid #e3e9ed;">Dates</th>
                            </tr>
                        </thead>
                        <tbody>`;
                    students.forEach(stu => {
                        const att = attendanceData[stu.id_number] || {present:0, absent:0, late:0, dates:[]};
                        html += `<tr>
                            <td style="padding:8px; border-bottom:1px solid #f0f0f0;">${stu.name}</td>
                            <td style="padding:8px; text-align:center; color:#219653; font-weight:600; background:#eafaf1;">${att.present}</td>
                            <td style="padding:8px; text-align:center; color:#d32f2f; font-weight:600; background:#fdeaea;">${att.absent}</td>
                            <td style="padding:8px; text-align:center; color:#b8860b; font-weight:600; background:#fffbe6;">${att.late}</td>
                            <td style="padding:8px; font-size:0.95em;">${
                                att.dates.map(d => {
                                    let color = d.status === "Present" || d.status === "Attended" ? "#219653"
                                            : d.status === "Absent" ? "#d32f2f"
                                            : d.status === "Late" ? "#b8860b"
                                            : "#333";
                                    let dateStr = d.date || '';
                                    return `<span style="color:${color}; font-weight:500;">${d.status}</span>: ${dateStr}`;
                                }).join('<br>')
                            }</td>
                        </tr>`;
                    });
                    html += `</tbody></table></div>`;
                    modalContent.innerHTML = html;
                });
        });
}

document.addEventListener("DOMContentLoaded", function() {
    // Close modal on X button
    document.getElementById("close-attendance-modal").onclick = function() {
        document.getElementById("attendance-modal").style.display = "none";
    };
    // Close modal when clicking outside the modal content
    document.getElementById("attendance-modal").onclick = function(e) {
        if (e.target === this) {
            this.style.display = "none";
        }
    };
});