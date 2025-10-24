const baseURL = "http://127.0.0.1:8000";

// ----- LOGIN -----
document.getElementById("loginForm")?.addEventListener("submit", async (e) => {
  e.preventDefault();
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  try {
    const res = await fetch(`${baseURL}/auth/login/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    if (!res.ok) {
      alert("Invalid credentials");
      return;
    }

    const data = await res.json();
    console.log("Login success:", data);

    // Save JWT tokens + email locally
    localStorage.setItem("access", data.access);
    localStorage.setItem("refresh", data.refresh);
    localStorage.setItem("email", email);

    // Redirect to dashboard
    window.location.href = "dashboard.html";
  } catch (err) {
    console.error(err);
    alert("Login failed — check server");
  }
});

// ----- REGISTER CLIENT -----
document.getElementById("registerFormClient")?.addEventListener("submit", async (e) => {
  e.preventDefault();
  const form = e.target;
  const payload = {
    email: form.email.value,
    password: form.password.value,
    username: form.username.value,
  };

  const res = await fetch(`${baseURL}/auth/register/client/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (res.ok) {
    alert("Client registered! You can now log in.");
    window.location.href = "login.html";
  } else {
    alert("Registration failed.");
  }
});
