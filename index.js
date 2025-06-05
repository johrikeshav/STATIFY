// Spotify Authorization Details
const AUTHORIZE_URL = "https://accounts.spotify.com/authorize";
const CLIENT_ID = "e25a9541103b4281965e723111e57950"; // Replace with your Spotify app's client ID
const REDIRECT_URI = "http://127.0.0.1:5500/stats.html"; // Replace with your redirect URI
const SCOPES = "user-read-private user-read-email"; // Add more scopes as needed

console.log("Client ID:", CLIENT_ID);

// Function to redirect the user to Spotify's authorization page
function requestAuthorization() {
  const authUrl = `${AUTHORIZE_URL}?client_id=${CLIENT_ID}&response_type=token&redirect_uri=${encodeURIComponent(
    REDIRECT_URI
  )}&scope=${encodeURIComponent(SCOPES)}`;
  console.log("Authorization URL:", authUrl); // Log the full URL
  window
