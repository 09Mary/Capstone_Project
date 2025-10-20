const baseURL = "http://127.0.0.1:8000"; // Change if using different port

// LOGIN
document.getElementById("loginForm")?.addEventListener("submit", async (e) => {
  e.preventDefault();

  const data = {
    email: document.getElementById("email").value,
    password: document.getElementById("password").value,
  };

  const res = await fetch(baseURL + "/auth/login/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (res.ok) {
    const user = await res.json();
    console.log("Login success:", user);

    // Save user data
    localStorage.setItem("user", JSON.stringify(user));

    // Redirect to dashboard
    window.location.href = "dashboard.html";
  } else {
    alert("Invalid credentials");
  }
});
