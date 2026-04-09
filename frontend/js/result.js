const API = "http://127.0.0.1:8000";

const domain = localStorage.getItem("domain") || "Data Science";
const background = localStorage.getItem("background") || "Computer Science";

const summaryDiv = document.getElementById("summary");
const tableBody = document.querySelector("#jobTable tbody");

let companyChart, locationChart, salaryChart, domainScopeChart;
let editId = null;

// ---------------- LOAD ----------------
async function loadJobs() {
    const res = await fetch(`${API}/predict`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ domain, background })
    });

    const data = await res.json();

    renderSummary(data);
    renderTable(data.jobs);
    renderCompanyChart(data.top_companies);
    renderLocationChart(data.jobs);
    renderSalaryChart(data.jobs);
    renderDomainScopeChart(data.jobs); // NEW
}

// ---------------- SUMMARY ----------------
function renderSummary(data) {
    const topCompanies = (data.top_companies || [])
        .map(c => `${c[0]} (${c[1]})`).join(", ");

    summaryDiv.innerHTML = `
        <h3>Results</h3>
        <p><b>Domain:</b> ${domain}</p>
        <p><b>Total Jobs:</b> ${data.total_jobs}</p>
        <p><b>Total Companies:</b> ${data.total_companies}</p>
        <p><b>Top Companies:</b> ${topCompanies || "None"}</p>
    `;
}

// ---------------- TABLE ----------------
function renderTable(jobs) {
    tableBody.innerHTML = "";

    if (!jobs.length) {
        tableBody.innerHTML = `<tr><td colspan="7">No jobs found</td></tr>`;
        return;
    }

    jobs.forEach(job => {
        tableBody.innerHTML += `
        <tr>
            <td>${job.id}</td>
            <td>${job.title}</td>
            <td>${job.company}</td>
            <td>${job.domain}</td>
            <td>${job.location}</td>
            <td>${job.salary ?? "NA"}</td>
            <td>
                <button onclick="viewJob('${job.title}')">View</button>
                <button onclick="editJob(${job.id}, '${job.title}', '${job.company}', '${job.location}', ${job.salary})">Edit</button>
                <button onclick="deleteJob(${job.id})">Delete</button>
            </td>
        </tr>`;
    });
}

// ---------------- VIEW ----------------
function viewJob(title) {
    alert("Job Title: " + title);
}

// ---------------- ADD / UPDATE ----------------
async function saveJob() {
    const job = {
        title: document.getElementById("title").value,
        company: document.getElementById("company").value,
        location: document.getElementById("location").value,
        salary: parseFloat(document.getElementById("salary").value),
        domain,
        background
    };

    if (editId) {
        await fetch(`${API}/delete-job/${editId}`, { method: "DELETE" });
        await fetch(`${API}/add-job`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(job)
        });
        editId = null;
    } else {
        await fetch(`${API}/add-job`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(job)
        });
    }

    clearForm();
    loadJobs();
}

// ---------------- EDIT ----------------
function editJob(id, title, company, location, salary) {
    editId = id;
    document.getElementById("title").value = title;
    document.getElementById("company").value = company;
    document.getElementById("location").value = location;
    document.getElementById("salary").value = salary;
}

// ---------------- DELETE ----------------
async function deleteJob(id) {
    if (!confirm("Delete this job?")) return;
    await fetch(`${API}/delete-job/${id}`, { method: "DELETE" });
    loadJobs();
}

// ---------------- CLEAR FORM ----------------
function clearForm() {
    document.getElementById("title").value = "";
    document.getElementById("company").value = "";
    document.getElementById("location").value = "";
    document.getElementById("salary").value = "";
}

// ---------------- CHARTS ----------------
function renderCompanyChart(data) {
    if (companyChart) companyChart.destroy();
    companyChart = new Chart(document.getElementById("companyChart"), {
        type: "doughnut",
        data: {
            labels: data.map(c => c[0]),
            datasets: [{ data: data.map(c => c[1]), backgroundColor: generateColors(data.length) }]
        }
    });
}

function renderLocationChart(jobs) {
    if (locationChart) locationChart.destroy();
    const count = {};
    jobs.forEach(j => count[j.location] = (count[j.location] || 0) + 1);

    locationChart = new Chart(document.getElementById("locationChart"), {
        type: "bar",
        data: {
            labels: Object.keys(count),
            datasets: [{ data: Object.values(count), backgroundColor: generateColors(Object.keys(count).length) }]
        }
    });
}

// ✅ SALARY CHART
function renderSalaryChart(jobs) {
    if (salaryChart) salaryChart.destroy();
    const ranges = { "0-3":0, "3-6":0, "6-10":0, "10+":0 };
    jobs.forEach(j => {
        const s = parseFloat(j.salary) || 0;
        if(s<3) ranges["0-3"]++;
        else if(s<6) ranges["3-6"]++;
        else if(s<10) ranges["6-10"]++;
        else ranges["10+"]++;
    });

    salaryChart = new Chart(document.getElementById("salaryChart"), {
        type: "bar",
        data: {
            labels: Object.keys(ranges),
            datasets: [{ data: Object.values(ranges), backgroundColor: generateColors(4) }]
        }
    });
}

// ---------------- DOMAIN SCOPE CHART (NEW) ----------------
function renderDomainScopeChart(jobs) {
    if(domainScopeChart) domainScopeChart.destroy();

    // Count jobs per domain
    const domainCounts = {};
    jobs.forEach(j => domainCounts[j.domain] = (domainCounts[j.domain] || 0) + 1);

    // Convert to chart
    domainScopeChart = new Chart(document.getElementById("domainScopeChart") || createDomainChartCanvas(), {
        type: "bar",
        data: {
            labels: Object.keys(domainCounts),
            datasets: [{
                label: "Job Opportunities",
                data: Object.values(domainCounts),
                backgroundColor: generateColors(Object.keys(domainCounts).length)
            }]
        },
        options: {
            plugins: { legend: { display: false } },
            responsive: true,
            maintainAspectRatio: false
        }
    });
}

// Helper to create canvas if not exists
function createDomainChartCanvas() {
    const canvas = document.createElement("canvas");
    canvas.id = "domainScopeChart";
    canvas.style.height = "300px";
    document.querySelector(".charts-container").prepend(canvas);
    return canvas;
}

// Helper: generate random colors
function generateColors(n) {
    const colors = [];
    for(let i=0;i<n;i++){
        colors.push(`hsl(${i*360/n},70%,60%)`);
    }
    return colors;
}

function logout() {
    localStorage.removeItem("loggedIn");
    window.location.href = "login.html";
}

// ---------------- INIT ----------------
loadJobs();