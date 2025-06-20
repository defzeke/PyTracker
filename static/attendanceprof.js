// Example: static/attendance.js
// This script handles the attendance functionality for professors, including class selection, subject and section filtering, and student attendance marking.
// Ensure this script is loaded after the DOM is fully loaded

    document.addEventListener("DOMContentLoaded", function() {
    const classDropdown = document.getElementById('classes-dropdown');
    const subjectDropdown = document.getElementById('subjects-dropdown');
    const sectionDropdown = document.getElementById('sections-dropdown');

    // Populate class dropdown
    fetch("/get_classes")
        .then(res => res.json())
        .then(classes => {
            classDropdown.innerHTML = '';
            const defaultOption = document.createElement("option");
            defaultOption.value = '';
            defaultOption.disabled = true;
            defaultOption.selected = true;
            defaultOption.textContent = "Select Class";
            classDropdown.appendChild(defaultOption);

            classes.forEach(cls => {
                // Only show class_ID, no subject/parentheses
                const option = document.createElement("option");
                option.value = cls.class_ID;
                option.textContent = cls.class_ID;
                // Add a left padding for slight indent
                option.style.paddingLeft = "12px";
                classDropdown.appendChild(option);
            });
        });

    classDropdown.addEventListener("change", function() {
        const classId = this.value;

        // Populate subject dropdown
        fetch(`/get_subjects?class_id=${classId}`)
            .then(res => res.json())
            .then(subjects => {
                subjectDropdown.innerHTML = '';
                const defaultOption = document.createElement("option");
                defaultOption.value = '';
                defaultOption.disabled = true;
                defaultOption.selected = true;
                defaultOption.textContent = "Select Subject";
                subjectDropdown.appendChild(defaultOption);

                subjects.forEach(subj => {
                    const option = document.createElement("option");
                    option.value = subj;
                    option.textContent = subj;
                    subjectDropdown.appendChild(option);
                });
            });

        // Populate section dropdown
        fetch(`/get_sections?class_id=${classId}`)
            .then(res => res.json())
            .then(sections => {
                sectionDropdown.innerHTML = '';
                const defaultOption = document.createElement("option");
                defaultOption.value = '';
                defaultOption.disabled = true;
                defaultOption.selected = true;
                defaultOption.textContent = "Select Section";
                sectionDropdown.appendChild(defaultOption);

                sections.forEach(sec => {
                    const option = document.createElement("option");
                    option.value = sec;
                    option.textContent = sec;
                    sectionDropdown.appendChild(option);
                });
            });

        document.getElementById("attendance-students").innerHTML = "";
    });

    subjectDropdown.addEventListener("change", loadStudents);
    sectionDropdown.addEventListener("change", loadStudents);

    function loadStudents() {
        const class_id = classDropdown.value;
        const subject = subjectDropdown.value;
        const section = sectionDropdown.value;
        if (class_id && subject && section) {
            fetch(`/get_students?class_id=${class_id}&subject=${subject}&section=${section}`)
                .then(res => res.json())
                .then(grouped => {
                    const container = document.getElementById("attendance-students");
                    container.innerHTML = "";
                    if (!grouped || Object.keys(grouped).length === 0) {
                        container.innerHTML = `
                            <div class="student-card default-card">
                                <div class="student-pic"></div>
                                <div class="student-name">No Students Found</div>
                                <div class="pal-btns">
                                    <button>P</button>
                                    <button>A</button>
                                    <button>L</button>
                                </div>
                            </div>
                        `;
                        return;
                    }
                    Object.keys(grouped).forEach(initial => {
                        // Group wrapper (block)
                        const groupBlock = document.createElement("div");
                        groupBlock.style.display = "block";
                        groupBlock.style.marginBottom = "32px";

                        // Header for the group
                        const header = document.createElement("div");
                        header.textContent = initial;
                        header.style.fontWeight = "bold";
                        header.style.fontSize = "1.2em";
                        header.style.margin = "24px 0 8px 85px";
                        groupBlock.appendChild(header);

                        // Row for student cards (flex, but only for this group)
                        const row = document.createElement("div");
                        row.style.display = "flex";
                        row.style.gap = "32px";
                        row.style.marginLeft = "85px";

                        grouped[initial].forEach(stu => {
                            const card = document.createElement("div");
                            card.className = "student-card";
                            card.innerHTML = `
                                <div class="student-pic"></div>
                                <div class="student-name">${stu.name}</div>
                                <div class="pal-btns">
                                    <button data-id="${stu.id_number}" data-status="Present">P</button>
                                    <button data-id="${stu.id_number}" data-status="Absent">A</button>
                                    <button data-id="${stu.id_number}" data-status="Late">L</button>
                                </div>
                            `;
                            row.appendChild(card);
                        });
                        groupBlock.appendChild(row);
                        container.appendChild(groupBlock);
                    });
                });
        }
    }

    let attendanceSelections = {}; // { student_ID: status }

    document.getElementById("attendance-students").addEventListener("click", function(e) {
        if (e.target.tagName === "BUTTON" && e.target.dataset.id && e.target.dataset.status) {
            const student_id = e.target.dataset.id;
            const status = e.target.dataset.status;

            // Save selection
            attendanceSelections[student_id] = status;

            // Remove selected state from sibling buttons
            const btns = e.target.parentElement.querySelectorAll("button");
            btns.forEach(btn => {
                btn.classList.remove("selected-attendance");
                btn.style.background = "#e3e9ed";
                btn.style.color = "#272757";
            });

            // Set selected state
            e.target.classList.add("selected-attendance");
            if (status === "Present") {
                e.target.style.background = "#22bb33";
                e.target.style.color = "#fff";
            } else if (status === "Absent") {
                e.target.style.background = "#dc143c";
                e.target.style.color = "#fff";
            } else if (status === "Late") {
                e.target.style.background = "#ffb300";
                e.target.style.color = "#fff";
            }
        }
    });

    // Hover effect (only if not selected)
    document.getElementById("attendance-students").addEventListener("mouseover", function(e) {
        if (e.target.tagName === "BUTTON" && !e.target.classList.contains("selected-attendance")) {
            if (e.target.dataset.status === "Present") {
                e.target.style.background = "#22bb33";
                e.target.style.color = "#fff";
            } else if (e.target.dataset.status === "Absent") {
                e.target.style.background = "#dc143c";
                e.target.style.color = "#fff";
            } else if (e.target.dataset.status === "Late") {
                e.target.style.background = "#ffb300";
                e.target.style.color = "#fff";
            }
        }
    });
    document.getElementById("attendance-students").addEventListener("mouseout", function(e) {
        if (e.target.tagName === "BUTTON" && !e.target.classList.contains("selected-attendance")) {
            e.target.style.background = "#e3e9ed";
            e.target.style.color = "#272757";
        }
    });

    // Take Attendance button logic
    document.getElementById("take-attendance-btn").addEventListener("click", function() {
        // Get all student IDs
        const studentCards = document.querySelectorAll("#attendance-students .student-card");
        const studentIDs = Array.from(studentCards).map(card => {
            const btn = card.querySelector("button[data-id]");
            return btn ? btn.dataset.id : null;
        }).filter(Boolean);

        // Find students without attendance
        const missing = studentIDs.filter(id => !attendanceSelections[id]);
        if (missing.length > 0) {
            // Get names of missing students
            const names = missing.map(id => {
                const card = document.querySelector(`#attendance-students .student-card button[data-id="${id}"]`).closest('.student-card');
                return card.querySelector('.student-name').textContent;
            });
            showPopup(`The following students have not been marked for attendance:<br><b>${names.join(", ")}</b>`);
            return;
        }

        // Prepare data for submission
        const class_id = document.getElementById('classes-dropdown').value;
        const section = document.getElementById('sections-dropdown').value;
        // Format date as YYYY-MM-DD (MySQL standard)
        const date = new Date();
        const dateStr = `${date.getFullYear()}-${(date.getMonth()+1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`;
        const timeStr = date.toLocaleTimeString();

        const attendanceData = studentIDs.map(id => ({
            class_ID: class_id,
            student_ID: id,
            status: attendanceSelections[id],
            date: dateStr
        }));

        // Send all attendance records to backend
        fetch("/mark_attendance_bulk", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({records: attendanceData})
        }).then(res => res.json()).then(resp => {
            if (resp.success) {
                showPopup(`Attendance submitted!<br>
                    <b>Class ID:</b> ${class_id}<br>
                    <b>Section:</b> ${section}<br>
                    <b>Date & Time:</b> ${dateStr} ${timeStr}`);
                attendanceSelections = {}; // Reset for next session
                // Optionally, reset button states here
                document.querySelectorAll("#attendance-students .pal-btns button").forEach(btn => {
                    btn.classList.remove("selected-attendance");
                    btn.style.background = "#e3e9ed";
                    btn.style.color = "#272757";
                });
            }
        });
    });

    // Popup function
    function showPopup(message) {
        let popup = document.createElement("div");
        popup.innerHTML = message;
        popup.style.position = "fixed";
        popup.style.top = "50%";
        popup.style.left = "50%";
        popup.style.transform = "translate(-50%, -50%)";
        popup.style.background = "#fff";
        popup.style.color = "#222";
        popup.style.padding = "32px 48px";
        popup.style.border = "2px solid #272757";
        popup.style.borderRadius = "12px";
        popup.style.zIndex = "9999";
        popup.style.fontSize = "1.2em";
        popup.style.textAlign = "center";
        document.body.appendChild(popup);
        setTimeout(() => popup.remove(), 3500);
    }
});