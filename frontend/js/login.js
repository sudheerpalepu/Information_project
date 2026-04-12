const API = "/api";
async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const res = await fetch(`${API}/login`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ username, password })
    });

    if (res.ok) {
        // 🔥 Save login
        localStorage.setItem("loggedIn", "true");

        // redirect
        window.location.href = "home.html";
    } else {
        document.getElementById("error").innerText = "Invalid credentials";
    }
}