function showForm() {
    const form = document.getElementById("application-form");

    if (form.style.display === "block") {
        form.style.display = "none";
    } else {
        form.style.display = "block";
    }
}

let currentFilter = "All";

function filterApplications(status) {
    currentFilter = status;
    applyFilters();
}

function searchApplications() {
    applyFilters();
}

function applyFilters() {
    const searchText = document.getElementById("searchInput").value.toLowerCase();
    const applications = document.querySelectorAll(".application-card");

    applications.forEach(function(application) {
        const applicationStatus = application.querySelector(".status").textContent.trim();
        const applicationText = application.textContent.toLowerCase();

        const matchesStatus =
            currentFilter === "All" || applicationStatus === currentFilter;

        const matchesSearch =
            applicationText.includes(searchText);

        if (matchesStatus && matchesSearch) {
            application.style.display = "";
        } else {
            application.style.display = "none";
        }
    });
}

function sortApplications() {
    const sortOrder = document.getElementById("sortSelect").value;
    const list = document.querySelector(".application-list");
    const applications = Array.from(document.querySelectorAll(".application-card"));

    applications.sort(function(a, b) {
        const dateA = a.querySelector("p:nth-of-type(3)").textContent.trim();
        const dateB = b.querySelector("p:nth-of-type(3)").textContent.trim();

        const dateValueA = new Date(dateA.replace("Date Applied:", "").trim());
        const dateValueB = new Date(dateB.replace("Date Applied:", "").trim());

        if (sortOrder === "newest") {
            return dateValueB - dateValueA;
        } else {
            return dateValueA - dateValueB;
        }
    });

    applications.forEach(function(application) {
        list.appendChild(application);
    });
}

function confirmDelete() {
    return confirm("Are you sure you want to delete this application?");
}