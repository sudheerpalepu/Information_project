const API = "http://127.0.0.1:8000";

function loadJobs() {
    fetch(`${API}/jobs`)
    .then(res=>res.json())
    .then(data=>{
        const table = document.getElementById("jobTable");
        table.innerHTML="";
        data.forEach(job=>{
            table.innerHTML+=`
                <tr>
                    <td>${job.title}</td>
                    <td>${job.company}</td>
                    <td><span class="chip">${job.domain}</span></td>
                    <td>
                        <button class="btn-warning" onclick="editJob(${job.id})">Edit</button>
                        <button class="btn-danger" onclick="deleteJob(${job.id})">Delete</button>
                    </td>
                </tr>
            `;
        });
    });
}

function addJob() {
    const job={
        title: document.getElementById("title").value,
        company: document.getElementById("company").value,
        domain: document.getElementById("domain").value,
        location: document.getElementById("location").value,
        salary: parseFloat(document.getElementById("salary").value)||null
    };
    fetch(`${API}/jobs`, { method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(job) })
    .then(()=>loadJobs());
}

function deleteJob(id){ fetch(`${API}/jobs/${id}`,{method:"DELETE"}).then(()=>loadJobs()); }

function editJob(id){
    const title=prompt("New title:"), company=prompt("New company:"), domain=prompt("New domain:"), location=prompt("New location:");
    fetch(`${API}/jobs/${id}`,{ method:"PUT", headers:{"Content-Type":"application/json"}, body:JSON.stringify({title, company, domain, location, salary:null}) })
    .then(()=>loadJobs());
}

loadJobs();