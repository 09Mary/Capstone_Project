const baseURL = "http://127.0.0.1:8000"; // Django API base URL
const user = JSON.parse(localStorage.getItem("user"));

function toggleMenu() {
  document.querySelector(".navbar").classList.toggle("active");
}


document.addEventListener("DOMContentLoaded", () => {
  if (!user) {
    window.location.href = "login.html";
    return;
  }

  document.getElementById("userName").textContent = user.username || "User";
  loadDashboard();
});

async function loadDashboard() {
  const role = user.role;
  const dashboard = document.getElementById("dashboardContent");

  if (role === "driver") {
    dashboard.innerHTML = `
      <h4>Your Vehicle</h4>
      <div id="vehicleDetails">Loading...</div>

      <h4>Incoming Trip Requests</h4>
      <div id="tripRequests">Loading...</div>

      <h4>Your Ratings</h4>
      <div id="ratings">Loading...</div>
    `;
    loadDriverData();
  } else {
    dashboard.innerHTML = `
      <h4>Book a Trip</h4>
      <button onclick="createTrip()">Request Trip</button>

      <h4>Your Trips</h4>
      <div id="clientTrips">Loading...</div>
    `;
    loadClientData();
  }
}

// Load Driver Data
async function loadDriverData() {
  try {
    const resVehicle = await fetch(`${baseURL}/vehicles/${user.id}/`);
    const vehicle = await resVehicle.json();
    document.getElementById("vehicleDetails").innerHTML = `
      <p>Model: ${vehicle.model || "N/A"}</p>
      <p>Plate: ${vehicle.plate_number || "N/A"}</p>
    `;

    const resTrips = await fetch(`${baseURL}/trips/driver/${user.id}/`);
    const trips = await resTrips.json();
    document.getElementById("tripRequests").innerHTML = trips.length
      ? trips.map(t => `<p>Trip #${t.id}: ${t.status}</p>`).join("")
      : "No trips yet.";

    const resRatings = await fetch(`${baseURL}/ratings/driver/${user.id}/`);
    const ratings = await resRatings.json();
    document.getElementById("ratings").innerHTML = ratings.length
      ? ratings.map(r => `<p>⭐ ${r.score}: ${r.comment}</p>`).join("")
      : "No ratings yet.";
  } catch (err) {
    console.error(err);
  }
}

// Load Client Data
async function loadClientData() {
  try {
    const resTrips = await fetch(`${baseURL}/trips/user/${user.id}/`);
    const trips = await resTrips.json();
    document.getElementById("clientTrips").innerHTML = trips.length
      ? trips.map(t => `<p>Trip to ${t.destination}: ${t.status}</p>`).join("")
      : "No trips yet.";
  } catch (err) {
    console.error(err);
  }
}

// Logout
document.getElementById("logoutBtn")?.addEventListener("click", () => {
  localStorage.removeItem("user");
  window.location.href = "login.html";
});
