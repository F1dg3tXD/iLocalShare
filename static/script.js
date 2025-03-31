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

function logout() {
    fetch("/logout").then(() => {
        location.reload();
    });
}