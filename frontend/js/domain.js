const background = localStorage.getItem("background");
const domainDiv = document.getElementById("domain-options");
const bgText = document.getElementById("selected-bg");

if (!background) {
    alert("Please select a background first!");
    window.location.href = "home.html";
}

bgText.innerText = `Background: ${background}`;

let domains = [];
if (background === "Computer Science") domains = ["Data Science", "AIML", "Web Development", "Cybersecurity"];
else if (background === "Mechanical") domains = ["Automobile", "Design", "Manufacturing"];
else if (background === "Finance") domains = ["Investment Banking", "Accounting"];
else if (background === "Marketing") domains = ["Digital Marketing", "Brand Management"];

let selectedDomain = null;
let selectionConfirmed = false; // prevents repeated clicks

domains.forEach(domain => {
    const card = document.createElement("div");
    card.className = "card";
    card.innerHTML = `<h3>${domain}</h3><p>Explore jobs in this domain</p>`;

    card.onclick = () => {
        if (selectionConfirmed) return;
        selectedDomain = domain;
        showPopup(domain);
    };

    domainDiv.appendChild(card);
});

function showPopup(domain) {
    document.getElementById("popupTitle").innerText = `Proceed with ${domain}?`;
    document.getElementById("popup").classList.remove("hidden");
}

function closePopup() {
    document.getElementById("popup").classList.add("hidden");
}

function confirmSelection() {
    if (!selectedDomain || selectionConfirmed) return;
    selectionConfirmed = true;
    localStorage.setItem("domain", selectedDomain);
    window.location.href = "result.html";
}