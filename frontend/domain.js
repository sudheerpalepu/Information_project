const background = localStorage.getItem("background");
const domainDiv = document.getElementById("domain-options");

let domains = [];
if(background === "Computer Science") domains = ["Data Science", "AI/ML", "Web Development", "Cybersecurity"];
else if(background === "Mechanical") domains = ["Automobile", "Design", "Manufacturing"];
else domains = ["Finance", "Marketing"];

domains.forEach(domain => {
    const btn = document.createElement("button");
    btn.innerText = domain;
    btn.onclick = () => {
        localStorage.setItem("domain", domain);
        window.location.href = "result.html";
    };
    domainDiv.appendChild(btn);
});