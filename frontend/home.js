function goToDomain(background) {
    localStorage.setItem("background", background); // store for next page
    window.location.href = "domain.html"; // go to next page
}