document.addEventListener("DOMContentLoaded", () => {
  if (!document.getElementById("map")) return;

  const map = L.map("map").setView([-1.286389, 36.817223], 13); // Default: Nairobi

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
  }).addTo(map);

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition((pos) => {
      const lat = pos.coords.latitude;
      const lon = pos.coords.longitude;
      L.marker([lat, lon])
        .addTo(map)
        .bindPopup("You are here!")
        .openPopup();
      map.setView([lat, lon], 14);
    });
  }
});
