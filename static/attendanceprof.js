// Example: static/attendance.js
document.addEventListener("DOMContentLoaded", function() {
    // Helper for custom dropdowns
    function setupCustomDropdown(dropdownId, onSelect) {
        const dropdown = document.getElementById(dropdownId);
        const selected = dropdown.querySelector('.selected');
        const optionsDiv = dropdown.querySelector('.dropdown-options');
        dropdown.addEventListener('click', function(e) {
            if (e.target.classList.contains('selected')) {
                // Toggle open
                dropdown.classList.toggle('open');
                // Close others
                document.querySelectorAll('#attendance-dropdowns .custom-dropdown').forEach(dd => {
                    if (dd !== dropdown) dd.classList.remove('open');
                });
            } else if (e.target.parentElement === optionsDiv) {
                // Option clicked
                const value = e.target.getAttribute('data-value');
                selected.textContent = e.target.textContent;
                selected.setAttribute('data-value', value);
                dropdown.classList.remove('open');
                // Mark selected
                optionsDiv.querySelectorAll('div').forEach(opt => opt.classList.remove('selected'));
                e.target.classList.add('selected');
                if (onSelect) onSelect(value, e.target.textContent);   
            }
        });
        // Close on outside click
        document.addEventListener('click', function(e) {
            if (!dropdown.contains(e.target)) dropdown.classList.remove('open');
        });
        return {
            setOptions: function(options, placeholder) {
                optionsDiv.innerHTML = '';
                selected.textContent = placeholder;
                selected.setAttribute('data-value', '');
                options.forEach(opt => {
                    const div = document.createElement('div');
                    div.textContent = opt;
                    div.setAttribute('data-value', opt);
                    optionsDiv.appendChild(div);
                });
            },
            getValue: function() {
                return selected.getAttribute('data-value');
            },
            setValue: function(value, label) {
                selected.textContent = label;
                selected.setAttribute('data-value', value);
                optionsDiv.querySelectorAll('div').forEach(opt => {
                    opt.classList.toggle('selected', opt.getAttribute('data-value') === value);
                });
            }
        };
    }

    // Setup dropdowns
    const classDropdown = setupCustomDropdown('classes-dropdown', onClassSelect);
    const subjectDropdown = setupCustomDropdown('subjects-dropdown', onSubjectSelect);
    const sectionDropdown = setupCustomDropdown('sections-dropdown', onSectionSelect);

    // Populate class dropdown
    fetch("/get_classes")
        .then(res => res.json())
        .then(classes => {
            // If you want to show class_ID + subject:
            classDropdown.setOptions(
                classes.map(c => `${c.class_ID} (${c.subject})`),
                "Select Class"
            );
            subjectDropdown.setOptions([], "Select Subject");
            sectionDropdown.setOptions([], "Select Section");
        });

    function onClassSelect(class_id) {
        if (!class_id) {
            subjectDropdown.setOptions([], "Select Subject");
            sectionDropdown.setOptions([], "Select Section");
            return;
        }
        // Subjects
        fetch(`/get_subjects?class_id=${class_id}`)
            .then(res => res.json())
            .then(subjects => {
                subjectDropdown.setOptions(subjects, "Select Subject");
                sectionDropdown.setOptions([], "Select Section");
            });
        // Sections
        fetch(`/get_sections?class_id=${class_id}`)
            .then(res => res.json())
            .then(sections => {
                sectionDropdown.setOptions(sections, "Select Section");
            });
        // Clear students
        document.getElementById("attendance-students").innerHTML = "";
    }

    function onSubjectSelect() {
        loadStudents();
    }
    function onSectionSelect() {
        loadStudents();
    }

    function loadStudents() {
        const class_id = classDropdown.getValue();
        const subject = subjectDropdown.getValue();
        const section = sectionDropdown.getValue();
        if (class_id && subject && section) {
            fetch(`/get_students?class_id=${class_id}&subject=${subject}&section=${section}`)
                .then(res => res.json())
                .then(grouped => {
                    const container = document.getElementById("attendance-students");
                    container.innerHTML = "";
                    // If no students, show a message
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
                    // For each group (A, B, ...)
                    Object.keys(grouped).forEach(initial => {
                        // Header for the group
                        const header = document.createElement("div");
                        header.textContent = initial;
                        header.style.fontWeight = "bold";
                        header.style.fontSize = "1.2em";
                        header.style.margin = "24px 0 8px 0";
                        container.appendChild(header);

                        // Row for student cards
                        const row = document.createElement("div");
                        row.style.display = "flex";
                        row.style.gap = "32px";
                        row.style.marginBottom = "24px";
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
                        container.appendChild(row);
                    });
                });
        }
    }

    document.getElementById("attendance-students").addEventListener("click", function(e) {
        if (e.target.tagName === "BUTTON" && e.target.dataset.id && e.target.dataset.status) {
            const student_id = e.target.dataset.id;
            const status = e.target.dataset.status;
            const class_id = classDropdown.getValue();
            const date = new Date().toISOString().slice(0, 10); // YYYY-MM-DD
            fetch("/mark_attendance", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({class_ID: class_id, student_ID: student_id, status: status, date: date})
            }).then(res => res.json()).then(resp => {
                if (resp.success) {
                    e.target.style.background = "#22bb33";
                    setTimeout(() => { e.target.style.background = "#e3e9ed"; }, 800);
                }
            });
        }
    });
});