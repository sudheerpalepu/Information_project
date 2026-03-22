const background = localStorage.getItem("background");
const domain = localStorage.getItem("domain");

async function getPrediction() {
    document.getElementById("result-text").innerHTML = "Loading...";

    try {
        const response = await fetch("http://127.0.0.1:8000/predict", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({background, domain})
        });

        const data = await response.json();

        // Show textual results
        const resultDiv = document.getElementById("result-text");
        resultDiv.innerHTML = `
            <p><b>Background:</b> ${background}</p>
            <p><b>Domain:</b> ${domain}</p>
            <p><b>Job Openings:</b> ${data.jobs}</p>
            <p><b>Salary Range:</b> ${data.salary}</p>
            <p><b>Top Companies:</b> ${data.companies.join(", ")}</p>
        `;

        // Job Openings Chart
        new Chart(document.getElementById("jobsChart"), {
            type: 'bar',
            data: {
                labels: data.companies,
                datasets: [{
                    label: 'Job Openings',
                    data: [data.jobs, data.jobs*0.8, data.jobs*0.6, data.jobs*0.4], // dummy for 4 companies
                    backgroundColor: 'rgba(54, 162, 235, 0.7)'
                }]
            },
            options: { responsive: true }
        });

        // Salary Chart
        new Chart(document.getElementById("salaryChart"), {
            type: 'bar',
            data: {
                labels: data.companies,
                datasets: [{
                    label: 'Salary in LPA',
                    data: data.salary.split('-').map(s => parseInt(s)), // convert "10-20" -> [10,20]
                    backgroundColor: 'rgba(255, 99, 132, 0.7)'
                }]
            },
            options: { responsive: true }
        });

    } catch(err) {
        document.getElementById("result-text").innerHTML = "Error fetching prediction.";
        console.error(err);
    }
}

getPrediction();