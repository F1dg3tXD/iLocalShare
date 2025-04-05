document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("loginForm");
    const passwordInput = document.getElementById("passwordInput");
    const loginMessage = document.getElementById("loginMessage");

    // Automatically redirect if already authenticated
    async function checkAuth() {
        try {
            const response = await fetch("/requires-auth");
            const data = await response.json();

            if (!data.requiresAuth && !data.secureServerRunning) {
                window.location.href = "/static/index.html";
            }
        } catch (error) {
            console.error("Error checking auth status:", error);
        }
    }

    loginForm.addEventListener("submit", async function (e) {
        e.preventDefault();

        const password = passwordInput.value;

        const response = await fetch("/login", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: `password=${encodeURIComponent(password)}`
        });

        if (response.ok) {
            const data = await response.json();
            if (data.success) {
                window.location.href = "/static/index.html";
            } else {
                loginMessage.textContent = "Wrong password!";
                passwordInput.value = "";
            }
        } else {
            loginMessage.textContent = "Login failed. Try again.";
        }
    });

    checkAuth();
});