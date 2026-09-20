function showForm() {
    const form = document.getElementById("application-form");

    if (form.style.display === "block") {
        form.style.display = "none";
    } else {
        form.style.display = "block";
    }
}

function filterApplications(status) {
    const applications = document.querySelectorAll(".application-card");

    applications.forEach(function(application) {
        const applicationStatus = application.querySelector(".status").textContent.trim();

        if (status === "All" || applicationStatus === status) {
            application.style.display = "block";
        } else {
            application.style.display = "none";
        }
    });
}