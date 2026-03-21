let selectedBackground = "";

function selectBackground(bg) {
  selectedBackground = bg;

  document.getElementById("background-section").style.display = "none";
  document.getElementById("domain-section").style.display = "block";

  showDomains(bg);
}

function showDomains(bg) {
  const domainDiv = document.getElementById("domain-options");
  domainDiv.innerHTML = "";

  let domains = [];

  if (bg === "Computer Science") {
    domains = ["Data Science", "Web Development", "AI/ML", "Cybersecurity"];
  } else if (bg === "Mechanical") {
    domains = ["Automobile", "Design", "Manufacturing"];
  } else {
    domains = ["Finance", "Marketing"];
  }

  domains.forEach(domain => {
    const btn = document.createElement("button");
    btn.innerText = domain;
    btn.onclick = () => showResult(domain);
    domainDiv.appendChild(btn);
  });
}

function showResult(domain) {
  document.getElementById("domain-section").style.display = "none";
  document.getElementById("result-section").style.display = "block";

  // Replace this with backend API call later
  const dummyResult = {
    jobs: 15000,
    salary: "10-20 LPA",
    companies: ["Google", "Amazon", "TCS", "Accenture"]
  };

  const resultText = `
    <p><b>Background:</b> ${selectedBackground}</p>
    <p><b>Domain:</b> ${domain}</p>
    <p><b>Job Openings:</b> ${dummyResult.jobs}</p>
    <p><b>Salary Range:</b> ${dummyResult.salary}</p>
    <p><b>Top Companies:</b> ${dummyResult.companies.join(", ")}</p>
  `;

  document.getElementById("result-text").innerHTML = resultText;
}