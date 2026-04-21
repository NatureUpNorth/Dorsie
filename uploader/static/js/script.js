<!-- JS for Tabs-->

    <!-- TAB SWITCHING -->
        document.querySelectorAll(".tab").forEach(tab => {
            tab.addEventListener("click", () => {

                document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
                tab.classList.add("active");

                document.querySelectorAll(".section").forEach(sec => sec.classList.remove("active"));
                document.getElementById(tab.dataset.target).classList.add("active");
                map.invalidateSize() //necessary to ensure map tiles show up properly on location tab
            });
        });


    <!-- SUBMIT VALIDATION -->
            document.getElementById("submitAll").addEventListener("click", function (event) {
            event.preventDefault();      // prevents form from submitting immediately when submit button is clicked


            const habitatBoxes = document.querySelectorAll(".habitat-checkbox");
            let oneChecked = false;       // oneChecked is a flag that tracks if at least one habitat is selected

            habitatBoxes.forEach(box => {
                if (box.checked) oneChecked = true;    // if any checkbox is checked then oneChecked = true
            });

            // stops submission if no habitat is selected
            if (!oneChecked) {
                alert("Please select at least ONE habitat.");
                document.querySelector('.tab[data-target="habitat"]').click();
                return;
            }

            const tabs = document.querySelectorAll(".tab");
            const sections = document.querySelectorAll(".section");

            let firstInvalidTab = null;
            let formIsValid = true;

            tabs.forEach(tab => tab.classList.remove("error"));

            sections.forEach(section => {
                const requiredFields = section.querySelectorAll("[required]");
                let sectionValid = true;

                requiredFields.forEach(field => {
                    if (!field.value) {
                        sectionValid = false;
                        formIsValid = false;
                    }
                });

                if (!sectionValid) {
                    const tab = document.querySelector(`.tab[data-target="${section.id}"]`);
                    tab.classList.add("error");

                    if (!firstInvalidTab) firstInvalidTab = tab;
                }
            });

            if (!formIsValid) {
                firstInvalidTab.click();
                return;
            }

            event.target.closest("form").submit();
        });

    <!-- AFFILIATION DROPDOWN -->
        document.addEventListener("DOMContentLoaded", function () {

            const affiliationSelect = document.getElementById("affiliation_type");
            const subContainer = document.getElementById("subAffiliationContainer");

            const options = {
                "University": ["St. Lawrence", "Clarkson", "SUNY Canton"],
                "School": [
                    "Canton Central",
                    "Colton-Pierrepont Central School",
                    "Little River Community School",
                    "Massena Central School"
                ]
            };

            affiliationSelect.addEventListener("change", function () {
                const selected = this.value;

                if (options[selected]) {
                    subContainer.innerHTML = `
                <label class="form-label">Sub-Affiliation</label>
                <select class="form-select" id="sub_affiliation" name="sub_affiliation" required>
                    <option value="" disabled selected>Select sub-affiliation</option>
                </select>
            `;

                    const sel = document.getElementById("sub_affiliation");

                    options[selected].forEach(opt => {
                        const o = document.createElement("option");
                        o.value = opt;
                        o.textContent = opt;
                        sel.appendChild(o);
                    });
                }
                else {
                    subContainer.innerHTML = `
                <label class="form-label">Sub-Affiliation</label>
                <input type="text" class="form-control" id="sub_affiliation"
                       name="sub_affiliation" placeholder="Enter affiliation name" required>
            `;
                }
            });

        });


    <!-- HABITAT DROPDOWN -->
        const mainHabitat = document.getElementById("mainHabitat");
        const subHabitatSelect = document.getElementById("subHabitat");

        const subHabitats = [
            "Deciduous Forest",
            "Mixed Forest",
            "Evergreen Forest",
            "Plantation Forest",
            "Natural Field or Meadow (Old Field)",
            "Agricultural Field",
            "Public Park/School Grounds",
            "Home Lawn",
            "Garden",
            "Wetland Edge",
            "Edge Between Two Habitats",
            "Other"
        ];

        mainHabitat.addEventListener("change", function () {

            subHabitatSelect.innerHTML = "";

            const defaultOpt = document.createElement("option");
            defaultOpt.value = "";
            defaultOpt.textContent = "Select sub-habitat";
            defaultOpt.disabled = true;
            defaultOpt.selected = true;
            subHabitatSelect.appendChild(defaultOpt);

            subHabitats.forEach(hab => {
                const o = document.createElement("option");
                o.value = hab;
                o.textContent = hab;
                subHabitatSelect.appendChild(o);
            });
        });


    <!-- DATE VALIDATION -->
        const startDate = document.getElementById("start_date");
        const endDate = document.getElementById("end_date");
        const dateError = document.getElementById("dateError");

        function validateDates() {

            if (!startDate.value || !endDate.value) {
                dateError.style.display = "none";
                return;
            }

            if (endDate.value < startDate.value) {
                dateError.style.display = "block";
            } else {
                dateError.style.display = "none";
            }
        }

        startDate.addEventListener("change", validateDates);
        endDate.addEventListener("change", validateDates);


    <!-- UPLOAD SECTION -->

        const dropArea = document.getElementById('drop-area');
        const fileList = document.getElementById('file-list');
        const folderInput = document.getElementById('fileElemFolder');
        let filesToUpload = [];

        dropArea.addEventListener('dragover', e => {
            e.preventDefault();
            dropArea.classList.add('dragover');
        });

        dropArea.addEventListener('dragleave', e => {
            e.preventDefault();
            dropArea.classList.remove('dragover');
        });

        dropArea.addEventListener('drop', e => {
            e.preventDefault();
            dropArea.classList.remove('dragover');

            const items = e.dataTransfer.items;
            if (items) {
                for (const item of items) {
                    const entry = item.webkitGetAsEntry?.();
                    if (entry) traverseFileTree(entry);
                }
            }
        });

        folderInput.addEventListener('change', e => {
            handleFiles(e.target.files);
        });

        function traverseFileTree(entry, path = "") {
            if (entry.isFile) {
                entry.file(file => {
                    if (file.name.startsWith('.')) return;
                    file.relativePath = path + file.name;
                    filesToUpload.push(file);
                    renderFileList();
                    syncInputFiles();
                });
            } else if (entry.isDirectory) {
                const reader = entry.createReader();
                reader.readEntries(entries => {
                    for (const ent of entries) {
                        traverseFileTree(ent, path + entry.name + "/");
                    }
                });
            }
        }

        function renderFileList() {
            fileList.innerHTML = '';
            filesToUpload.forEach((f, idx) => {
                const row = document.createElement('div');
                const name = document.createElement('span');
                name.textContent = f.relativePath || f.webkitRelativePath || f.name;

                const removeBtn = document.createElement('button');
                removeBtn.type = 'button';
                removeBtn.textContent = 'Remove';
                removeBtn.className = 'btn btn-sm btn-outline-danger ms-2';
                removeBtn.onclick = () => {
                    filesToUpload.splice(idx, 1);
                    syncInputFiles();
                    renderFileList();
                };

                row.appendChild(name);
                row.appendChild(removeBtn);
                fileList.appendChild(row);
            });
        }

        function syncInputFiles() {
            const dt = new DataTransfer();
            filesToUpload.forEach(f => dt.items.add(f));
            folderInput.files = dt.files;
        }

        function handleFiles(files) {
            filesToUpload = Array.from(files).filter(f => !f.name.startsWith('.'));
            renderFileList();
            syncInputFiles();
        }
