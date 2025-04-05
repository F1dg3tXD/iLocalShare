// Redirect to login.html if not authenticated
async function checkAuth() {
    try {
        const response = await fetch("/requires-auth");
        const data = await response.json();

        if (data.requiresAuth || data.secureServerRunning) {
            // If we're not already on the login page, redirect
            if (!window.location.pathname.includes("login.html")) {
                window.location.href = "/static/login.html";
            }
        } else {
            // Show the main file section
            document.getElementById("authSection").style.display = "none";
            document.getElementById("fileSection").style.display = "block";
            fetchFiles();
        }
    } catch (error) {
        console.error("Error checking authentication:", error);
    }
}

// Only used if you're still keeping a login form on this page (optional)
async function login() {
    const password = document.getElementById("passwordInput").value;

    const response = await fetch("/static/login", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `password=${encodeURIComponent(password)}`
    });

    if (response.ok) {
        const data = await response.json();
        if (data.success) {
            window.location.href = "/static/index.html";
        } else {
            alert("Wrong password!");
            document.getElementById("passwordInput").value = "";
        }
    } else {
        alert("Login failed!");
    }
}

async function fetchFiles() {
    try {
        const response = await fetch("/files");

        if (response.status === 403) {
            window.location.href = "/static/login.html";
            return;
        }

        const files = await response.json();
        let fileList = document.getElementById("fileList");
        fileList.innerHTML = "";

        files.forEach(file => {
            let listItem = document.createElement("li");
            listItem.innerHTML = `<a href="/download/${file}">${file}</a>`;
            fileList.appendChild(listItem);
        });
    } catch (error) {
        console.error("Error fetching files:", error);
    }
}

document.getElementById("uploadForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    let fileInput = document.getElementById("fileInput");
    let files = fileInput.files;

    if (files.length === 0) {
        alert("No files selected");
        return;
    }

    let formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append("files", files[i]);
    }

    await fetch("/upload", {
        method: "POST",
        body: formData
    });

    fileInput.value = "";
    fetchFiles();
});

document.addEventListener("DOMContentLoaded", function () {
    const themeToggle = document.getElementById("theme-toggle");

    if (!localStorage.getItem("theme")) {
        localStorage.setItem("theme", "dark");
    }

    if (localStorage.getItem("theme") === "light") {
        document.body.classList.add("light-mode");
        themeToggle.innerText = "🌙 Dark Mode";
    } else {
        document.body.classList.remove("light-mode");
        themeToggle.innerText = "☀️ Light Mode";
    }

    themeToggle.addEventListener("click", function () {
        document.body.classList.toggle("light-mode");
        if (document.body.classList.contains("light-mode")) {
            localStorage.setItem("theme", "light");
            themeToggle.innerText = "🌙 Dark Mode";
        } else {
            localStorage.setItem("theme", "dark");
            themeToggle.innerText = "☀️ Light Mode";
        }
    });

    // Optional: Handle login form if it exists on this page
    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", function (e) {
            e.preventDefault();
            login();
        });
    }
});

async function fetchServerInfo() {
    try {
        const response = await fetch("/server-info");

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        document.getElementById("localhost-info").innerText = `http://127.0.0.1:${data.port}`;
        document.getElementById("ip-info").innerText = `http://${data.ip}:${data.port}`;

        document.getElementById("qrcode").innerHTML = "";
        new QRCode(document.getElementById("qrcode"), {
            text: `http://${data.ip}:${data.port}`,
            width: 128,
            height: 128
        });

    } catch (error) {
        console.error("Error fetching server info:", error);
    }
}

fetchServerInfo();
checkAuth();

function logout() {
    fetch("/logout").then(() => {
        window.location.href = "/static/login.html";
    });
}