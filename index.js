const client_id = "326a535358834e489bf67c1033cae264";
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
    window.location = `https://accounts.spotify.com/authorize?client_id=326a535358834e489bf67c1033cae264&redirect_uri=https://johrikeshav.github.io/statify/stats.html&scope=${scopes_uri_param}&response_type=token&show_dialog=true`;
    console.log("clicked");
  });
});
