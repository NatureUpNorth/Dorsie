// page elements
const dropArea = document.getElementById('drop-area');
const fileList = document.getElementById('file-list');
const folderInput = document.getElementById('fileElemFolder');
let filesToUpload = [];

// drag and drop elements
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

// folder button input
folderInput.addEventListener('change', e => {
  handleFiles(e.target.files);
});

// recursive folder reading
function traverseFileTree(entry, path = "") {
  if (entry.isFile) {
    entry.file(file => {
      // ignore hidden files
      if (file.name.startsWith('.')) return;
      // continue
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

// display and manage file list
function renderFileList() {
  fileList.innerHTML = '';
  filesToUpload.forEach((f, idx) => {
    const row = document.createElement('div');
    const name = document.createElement('span');
    name.textContent = f.relativePath || f.webkitRelativePath || f.name;

    // create preview button
    //const previewBtn = document.createElement('button');
    //previewBtn.type = 'type'
    //previewBtn.textContent = "Preview"
    //previewBtn.className = 'btn btn-sm btn-outline-danger ms-2'

    // create remove button
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
    //row.appendChild(previewBtn);
    row.appendChild(removeBtn);
    fileList.appendChild(row);
  });
}

// sync files with hidden inputs
function syncInputFiles() {
  const dt = new DataTransfer();
  filesToUpload.forEach(f => dt.items.add(f));
  folderInput.files = dt.files;
}

// for manuel folder selection
function handleFiles(files) {
  filesToUpload = Array.from(files).filter(f => !f.name.startsWith('.'));
  renderFileList();
  syncInputFiles();
}
