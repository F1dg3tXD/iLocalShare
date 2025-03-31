async function checkAuth() {
    try {
        const response = await fetch("/requires-auth");
        const data = await response.json();

        if (!data.requiresAuth) {
            document.getElementById("authSection").style.display = "none";
            document.getElementById("fileSection").style.display = "block";
            fetchFiles();
        }
    } catch (error) {
        console.error("Error checking authentication:", error);
    }
}

checkAuth();

async function login() {
    const password = document.getElementById("passwordInput").value;

    const response = await fetch("/", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `password=${password}`
    });

    if (response.ok) {
        document.getElementById("authSection").style.display = "none";
        document.getElementById("fileSection").style.display = "block";
        fetchFiles();
    } else {
        alert("Wrong password!");
    }
}

async function fetchFiles() {
    const response = await fetch("/files");
    const files = await response.json();
    
    let fileList = document.getElementById("fileList");
    fileList.innerHTML = "";
    
    files.forEach(file => {
        let listItem = document.createElement("li");
        listItem.innerHTML = `<a href="/download/${file}">${file}</a>`;
        fileList.appendChild(listItem);
    });
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
    
    // Enable dark mode by default
    if (!localStorage.getItem("theme")) {
        localStorage.setItem("theme", "dark");
    }

    // Apply saved theme
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

        // Generate QR code
        document.getElementById("qrcode").innerHTML = ""; // Clear previous QR code
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

function logout() {
    fetch("/logout").then(() => {
        location.reload();
    });
}
