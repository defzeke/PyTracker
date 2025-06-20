document.addEventListener("DOMContentLoaded", function() {
    const classDropdown = document.getElementById('classes-dropdown');
    const sectionDropdown = document.getElementById('sections-dropdown');
    let profData = null;

    // Fetch all dropdown data at once
    fetch("/prof_dropdown_data")
        .then(res => res.json())
        .then(data => {
            profData = data;
            // Populate class dropdown
            classDropdown.innerHTML = '';
            const defaultOption = document.createElement("option");
            defaultOption.value = '';
            defaultOption.disabled = true;
            defaultOption.selected = true;
            defaultOption.textContent = "Select Class";
            classDropdown.appendChild(defaultOption);

            data.classes.forEach(cls => {
                const option = document.createElement("option");
                option.value = cls.class_ID;
                option.textContent = cls.class_ID;
                option.style.paddingLeft = "12px";
                classDropdown.appendChild(option);
            });
        });

    classDropdown.addEventListener("change", function() {
        const classId = this.value;

        // Find the selected class and get its subject
        const cls = profData.classes.find(c => c.class_ID === classId);
        const subjectNameSpan = document.getElementById("subject-name");
        if (cls && subjectNameSpan) {
            subjectNameSpan.textContent = cls.subject || "None";
        } else if (subjectNameSpan) {
            subjectNameSpan.textContent = "None";
        }

        // Populate section dropdown
        sectionDropdown.innerHTML = '';
        const defaultSectionOption = document.createElement("option");
        defaultSectionOption.value = '';
        defaultSectionOption.disabled = true;
        defaultSectionOption.selected = true;
        defaultSectionOption.textContent = "Select Section";
        sectionDropdown.appendChild(defaultSectionOption);

        // Only allow sections 1-1 to 1-5
        (profData.class_sections[classId] || []).forEach(sec => {
            // Extract section part after the space (e.g., "BSCPE 1-1" -> "1-1")
            let sectionPart = sec.split(" ").pop();
            if (["1-1", "1-2", "1-3", "1-4", "1-5"].includes(sectionPart)) {
                const option = document.createElement("option");
                option.value = sec;
                option.textContent = sec;
                sectionDropdown.appendChild(option);
            }
        });
    });

    classDropdown.addEventListener("blur", function() {
        if (!this.value) {
            const subjectNameSpan = document.getElementById("subject-name");
            if (subjectNameSpan) subjectNameSpan.textContent = "None";
        }
    });

    sectionDropdown.addEventListener("change", loadStudents);

    function loadStudents() {
        const class_id = classDropdown.value;
        const section = sectionDropdown.value;
        const container = document.getElementById("attendance-students");
        const pleaseWaitModal = document.getElementById("please-wait-modal");

        if (!class_id || !section) {
            container.innerHTML = `
                <div style="width:100%;text-align:center;font-size:1.3em;color:#444;padding:40px 0;">
                    No Option Selected
                </div>
            `;
            if (pleaseWaitModal) pleaseWaitModal.style.display = "none";
            return;
        }

        if (pleaseWaitModal) pleaseWaitModal.style.display = "flex";

        fetch(`/get_students?class_id=${class_id}&section=${section}`)
            .then(res => res.json())
            .then(grouped => {
                if (pleaseWaitModal) pleaseWaitModal.style.display = "none";
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

                    // Wrapper for header and row, for alignment
                    const groupInner = document.createElement("div");
                    groupInner.style.paddingTop = "5px";
                    groupInner.style.paddingLeft = "120px";

                    // Header for the group
                    const header = document.createElement("div");
                    header.textContent = initial;
                    header.style.fontWeight = "bold";
                    header.style.fontSize = "1.2em";
                    header.style.margin = "20px 0 5px 0";
                    groupInner.appendChild(header);

                    // Row for student cards (flex, but only for this group)
                    const row = document.createElement("div");
                    row.style.display = "flex";
                    row.style.gap = "10px";
                    row.style.marginLeft = "85px";
                    groupInner.appendChild(row);

                    groupBlock.appendChild(groupInner);

                    grouped[initial].forEach(stu => {
                        const card = document.createElement("div");
                        card.className = "student-card";
                        const profilePicUrl = stu.profile_pic
                            ? `/static/profile_pics/${stu.profile_pic}`
                            : '/static/images/profile.png'; // fallback image

                        card.innerHTML = `
                            <div class="student-pic" style="background: none; display: flex; justify-content: center; align-items: center;">
                                <img src="${profilePicUrl}" alt="Profile" style="width:80px;height:80px;border-radius:50%;object-fit:cover;">
                            </div>
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

    loadStudents();

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
            date: dateStr,
            section: section
        }));
        
        const pleaseWaitModal = document.getElementById("please-wait-modal");
        if (pleaseWaitModal) pleaseWaitModal.style.display = "flex";

        // Send all attendance records to backend
        fetch("/mark_attendance_bulk", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({records: attendanceData})
        }).then(res => res.json()).then(resp => {
            if (pleaseWaitModal) pleaseWaitModal.style.display = "none";
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

function updateLiveDateTime() {
    const dtSpan = document.getElementById("live-datetime");
    if (!dtSpan) return;
    const now = new Date();
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    const dateStr = now.toLocaleDateString(undefined, options);
    const timeStr = now.toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    dtSpan.textContent = `${dateStr} ${timeStr}`;
}
setInterval(updateLiveDateTime, 1000);
updateLiveDateTime();