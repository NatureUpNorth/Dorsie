// TAB SWITCHING
let mapInitialized = false;

document.querySelectorAll(".tab").forEach(tab => {
    tab.addEventListener("click", () => {
        document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
        tab.classList.add("active");

        document.querySelectorAll(".section").forEach(sec => sec.classList.remove("active"));
        document.getElementById(tab.dataset.target).classList.add("active");
        
        if (typeof map !== 'undefined') {
            map.invalidateSize(); //necessary to ensure map tiles show up properly on location tab
        }
    });
});

// SUBMIT VALIDATION
document.getElementById("submitAll").addEventListener("click", function (event) {
    event.preventDefault(); // prevents form from submitting immediately when submit button is clicked

    const habitatBoxes = document.querySelectorAll(".habitat-checkbox");
    let oneChecked = false; // oneChecked is a flag that tracks if at least one habitat is selected

    habitatBoxes.forEach(box => {
        if (box.checked) oneChecked = true; // if any checkbox is checked then oneChecked = true
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

    tabs.forEach(tab => tab.classList.remove("error")); // removes red highlighting from tabs before re-checking

    sections.forEach(section => { 
        const requiredFields = section.querySelectorAll("[required]");
        let sectionValid = true;
        const radioGroups = new Set();

        requiredFields.forEach(field => {
            // radio buttons automatically have values assigned to them,
            //so I'm grouping them to validate entry and then cheking if one is selected

            if (field.type === "radio") {

                // Skip if already checked this group
                if (radioGroups.has(field.name)) return;
                radioGroups.add(field.name);
                const group = document.querySelectorAll(`input[name="${field.name}"]`);
                const oneChecked = Array.from(group).some(r => r.checked);
                if (!oneChecked) {
                    sectionValid = false;
                }
            } else if (!field.value) {
                sectionValid = false;
                formIsValid = false;
            }
        });

        // highlights the tab with an error red
        if (!sectionValid) {
            const tab = document.querySelector(`.tab[data-target="${section.id}"]`);
            if (tab) {
                tab.classList.add("error"); 
                if (!firstInvalidTab) firstInvalidTab = tab;
            }
        }
    });

    if (!formIsValid) {
        firstInvalidTab.click(); // automatically opens the first tab with errors
        return;
    }

    document.getElementById("mainForm").submit();
});

// AFFILIATION RADIO BUTTONS
document.addEventListener("DOMContentLoaded", function () {
    const radios = document.querySelectorAll('input[name="affiliation_type"]');
    const subBox = document.getElementById("subAffiliationBox");
    const subInput = document.getElementById("sub_affiliation");

    function hideSub() {
        subBox.classList.add("d-none");
        subInput.value = "";
        subInput.required = false;
    }

    radios.forEach(radio => {
        radio.addEventListener("change", function () {

            // Individual volunteer = no extra input
            if (this.value === "Individual Volunteer") {
                hideSub();
            } else {
                subBox.classList.remove("d-none");
                subInput.required = true;
            }
        });
    });
});

// DATE VALIDATION
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

// UPLOAD SECTION
const dropArea = document.getElementById('drop-area');
const fileList = document.getElementById('file-list');
const folderInput = document.getElementById('fileElemFolder');
let filesToUpload = [];

dropArea.addEventListener('dragover', e => { e.preventDefault(); dropArea.classList.add('dragover'); });
dropArea.addEventListener('dragleave', e => { e.preventDefault(); dropArea.classList.remove('dragover'); });
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

folderInput.addEventListener('change', e => handleFiles(e.target.files));

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
            for (const ent of entries) traverseFileTree(ent, path + entry.name + "/");
        });
    }
}

function renderFileList() {
    fileList.innerHTML = '';
    filesToUpload.forEach((f, idx) => {
        const row = document.createElement('div');
        row.className = "mb-1";
        const name = document.createElement('span');
        name.textContent = f.relativePath || f.webkitRelativePath || f.name;

        // Preview button for images (first 5)
        let previewBtn = null;
        if (f.type.startsWith("image/") && idx < 5) {
            previewBtn = document.createElement('button');
            previewBtn.type = 'button';
            previewBtn.textContent = 'Preview';
            previewBtn.className = 'btn btn-sm btn-outline-secondary ms-2';
            previewBtn.onclick = () => previewImage(f);
        }

        const removeBtn = document.createElement('button');
        removeBtn.type = 'button';
        removeBtn.textContent = 'Remove';
        removeBtn.className = 'btn btn-sm btn-outline-danger ms-2';
        removeBtn.onclick = () => {
            filesToUpload.splice(idx, 1);
            syncInputFiles();
            renderFileList();
        };

        const buttonGroup = document.createElement('div');
        buttonGroup.className = "file-buttons d-flex align-items-center";
        if (previewBtn) buttonGroup.appendChild(previewBtn);
        buttonGroup.appendChild(removeBtn);
        
        row.appendChild(name);
        row.appendChild(buttonGroup);
        fileList.appendChild(row);
    });
}

// Sync files to the hidden submit input so they travel with the form
function syncInputFiles() {
    const dt = new DataTransfer();
    filesToUpload.forEach(f => dt.items.add(f));
    folderInput.files = dt.files;
    document.getElementById("fileSubmit").files = dt.files; // fix for form submission
}

function handleFiles(files) {
    filesToUpload = Array.from(files).filter(f => !f.name.startsWith('.'));
    renderFileList();
    syncInputFiles();
}

// Image preview modal functions
function previewImage(file) {
    const modal = document.getElementById("imagePreviewModal");
    const img = document.getElementById("previewImage");
    const imageURL = URL.createObjectURL(file);
    img.src = imageURL;
    modal.style.display = "flex";
    modal.dataset.imageUrl = imageURL;
}

function closePreview() {
    const modal = document.getElementById("imagePreviewModal");
    const img = document.getElementById("previewImage");
    if (modal.dataset.imageUrl) URL.revokeObjectURL(modal.dataset.imageUrl);
    img.src = "";
    modal.style.display = "none";
}

document.querySelector(".close-preview").onclick = closePreview;
document.getElementById("imagePreviewModal").onclick = e => {
    if (e.target === document.getElementById("imagePreviewModal")) closePreview();
};

// CAMERA MODEL
document.addEventListener("DOMContentLoaded", function () {
    const radios = document.querySelectorAll('input[name="camera_choice"]');
    const modelBox = document.getElementById("cameraModelBox");
    const modelInput = document.getElementById("camera_model");

    radios.forEach(radio => {
        radio.addEventListener("change", function () {
            if (this.value === "not_borrowed") {
                modelBox.classList.remove("d-none");
                modelInput.required = true;
            } else {
                modelBox.classList.add("d-none");
                modelInput.value = "";
                modelInput.required = false;
            }
        });
    });
});