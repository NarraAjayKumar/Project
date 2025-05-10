document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('fileInput');
    const fileNameDisplay = document.getElementById('fileName');
    const uploadArea = document.getElementById('uploadArea');
    const scanForm = document.getElementById('scanForm');

    if (fileInput && uploadArea && scanForm) {
        // Handle file selection
        fileInput.addEventListener('change', function() {
            if (this.files.length) {
                fileNameDisplay.textContent = this.files[0].name;
                scanForm.submit();
            }
        });

        // Drag and drop functionality
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, preventDefaults, false);
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            uploadArea.addEventListener(eventName, highlight, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, unhighlight, false);
        });

        uploadArea.addEventListener('drop', handleDrop, false);
    }

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    function highlight() {
        this.classList.add('highlight');
    }

    function unhighlight() {
        this.classList.remove('highlight');
    }

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length) {
            fileInput.files = files;
            fileNameDisplay.textContent = files[0].name;
            scanForm.submit();
        }
    }
});