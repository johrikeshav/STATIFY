const client_id = "e25a9541103b4281965e723111e57950";
const spotify_endpoint = "https://accounts.spotify.com/authorize";
const redirect_uri = "https://johrikeshav.github.io/statify/stats.html";
const space_delimiter = "%20";
const scopes = [
  "playlist-read-private",
  "playlist-read-collaborative",
  "user-read-playback-position",
  "user-top-read",
  "user-read-recently-played",
  "user-library-read",
  "user-read-email",
  "user-read-private",
];
const scopes_uri_param = scopes.join(space_delimiter);

window.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("login_button");
  btn.addEventListener("click", () => {
    const authUrl = `${spotify_endpoint}?client_id=${client_id}&response_type=token&redirect_uri=${encodeURIComponent(
      redirect_uri
    )}&scope=${scopes_uri_param}&show_dialog=true`;
    window.location = authUrl;
    console.log("clicked");
  });
});
