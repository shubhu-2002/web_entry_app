document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("loginForm");
    const registerForm = document.getElementById("registerForm");
    const logoutBtn = document.getElementById("logoutBtn");

    if (loginForm) {
        loginForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            let email = document.getElementById("loginEmail").value;
            let password = document.getElementById("loginPassword").value;

            let response = await fetch("/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password }),
            });

            if (response.ok) {
                window.location.href = "/dashboard.html";
            } else {
                alert("Invalid credentials");
            }
        });
    }

    if (registerForm) {
        registerForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            let email = document.getElementById("registerEmail").value;
            let password = document.getElementById("registerPassword").value;

            let response = await fetch("/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password }),
            });

            if (response.ok) {
                alert("Registration successful, please login!");
                document.getElementById("showLogin").click();
            } else {
                alert("User already exists");
            }
        });
    }

    if (logoutBtn) {
        logoutBtn.addEventListener("click", async () => {
            await fetch("/logout", { method: "POST" });
            window.location.href = "/";
        });
    }
});

async function uploadFile() {
    let fileInput = document.getElementById("fileInput").files[0];
    let formData = new FormData();
    formData.append("file", fileInput);

    let response = await fetch("/upload", {
        method: "POST",
        body: formData,
    });

    if (response.ok) {
        alert("File uploaded successfully");
        loadFiles();
    }
}

async function loadFiles() {
    let response = await fetch("/files");
    let files = await response.json();

    let table = document.getElementById("fileTable");
    table.innerHTML = "";

    files.forEach((file) => {
        table.innerHTML += `<tr>
            <td><a href="/download/${file.name}">${file.name}</a></td>
            <td>${file.type}</td>
            <td>${file.date}</td>
        </tr>`;
    });
}
