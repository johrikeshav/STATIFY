// Function to extract the access token from the URL
function getAccessTokenFromUrl() {
  const hash = window.location.hash.substring(1); // Get everything after the `#`
  const params = new URLSearchParams(hash); // Parse the hash into key-value pairs
  return params.get("access_token"); // Return the access token
}

// Function to fetch the user's Spotify profile
function fetchUserProfile(accessToken) {
  fetch("https://api.spotify.com/v1/me", {
    headers: {
      Authorization: `Bearer ${accessToken}`, // Add the access token to the request
    },
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to fetch user profile");
      }
      return response.json();
    })
    .then((data) => {
      console.log("User Profile:", data); // Log the user's profile data
      document.querySelector(
        ".greeting"
      ).textContent = `Hi, ${data.display_name}!`; // Update the greeting
    })
    .catch((error) => {
      console.error("Error fetching user profile:", error);
    });
}

// Function to request authorization
function requestAuthorization() {
  const authUrl = `${AUTHORIZE_URL}?client_id=${CLIENT_ID}&response_type=token&redirect_uri=${encodeURIComponent(
    REDIRECT_URI
  )}&scope=${encodeURIComponent(SCOPES)}`;
  console.log("Authorization URL:", authUrl); // Log the URL
  navigator.clipboard.writeText(authUrl).then(() => {
    console.log(
      "Authorization URL copied to clipboard. Paste it in your browser to test."
    );
  });
  // Comment out the redirect for debugging
  // window.location.href = authUrl;
}

// On page load, check if the access token is in the URL
document.addEventListener("DOMContentLoaded", () => {
  const accessToken = getAccessTokenFromUrl(); // Extract the access token
  if (accessToken) {
    console.log("Access Token:", accessToken); // Log the access token
    fetchUserProfile(accessToken); // Fetch the user's profile
  } else {
    console.log("No access token found. Please log in.");
  }

  const authUrl = "https://accounts.spotify.com/authorize"; // Example authorization URL
  console.log("Authorization URL:", authUrl); // Log the authorization URL
});
