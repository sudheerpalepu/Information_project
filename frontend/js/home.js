// home.js
const container = document.getElementById("background-options");


const backgrounds = [
    "Computer Science",
    "Mechanical",
    "Finance",
    "Marketing"
];


container.innerHTML = "";


backgrounds.forEach(bg => {
    const btn = document.createElement("button");
    btn.innerText = bg;
    btn.className = "bg-btn"; // add class for styling
    btn.onclick = () => {
        localStorage.setItem("background", bg); // store selection
        window.location.href = "domain.html";   // navigate to domains
    };
    container.appendChild(btn);
});