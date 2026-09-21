/**
 * Main Client-Side JavaScript
 * AI Resume Analyzer & Job Recommendation System
 */

document.addEventListener("DOMContentLoaded", function () {
    // Auto-dismiss alert messages after 5 seconds
    const alerts = document.querySelectorAll(".alert-dismissible");
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Form submission loading state
    const uploadForm = document.getElementById("uploadForm");
    if (uploadForm) {
        uploadForm.addEventListener("submit", function () {
            const submitBtn = document.getElementById("submitBtn");
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = `
                    <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                    Running NLP Extraction & Machine Learning Matching...
                `;
            }
        });
    }
});
