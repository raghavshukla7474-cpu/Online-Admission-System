document.addEventListener('DOMContentLoaded', function () {
    // Self-dismissing alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) {
                bsAlert.close();
            }
        }, 5000);
    });
    // Custom client-side file-size validator
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(function (input) {
        input.addEventListener('change', function () {
            if (this.files.length > 0) {
                const fileSize = this.files[0].size / 1024 / 1024; // size in MB
                if (fileSize > 5) {
                    alert('Warning: File size exceeds 5MB limit. Please upload a smaller compressed file.');
                    this.value = ''; // Clear value
                }
            }
        });
    });
});
