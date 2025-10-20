const API_BASE = "http://127.0.0.1:8000"; // your Django backend

// Helper function to send API requests
async function apiRequest(endpoint, method = "GET", data = null, token = null) {
  const options = {
    method,
    headers: { "Content-Type": "application/json" },
  };
  if (data) options.body = JSON.stringify(data);
  if (token) options.headers["Authorization"] = `Bearer ${token}`;

  const response = await fetch(`${API_BASE}${endpoint}`, options);
  if (!response.ok) throw new Error(`API error: ${response.status}`);
  return await response.json();
}

// AUTH endpoints
async function registerClient(data) {
  return apiRequest("/auth/register/client/", "POST", data);
}
async function registerDriver(data) {
  return apiRequest("/auth/register/driver/", "POST", data);
}
async function login(data) {
  return apiRequest("/auth/login/", "POST", data);
}

// Example usage — fetch a driver profile
async function getDriverProfile(id, token) {
  return apiRequest(`/profile/driver/${id}/`, "GET", null, token);
}
