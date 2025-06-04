var redirect_uri = "https://johrikeshav.github.io/statify/stats.html";
var client_id = "e25a9541103b4281965e723111e57950";
var client_secret = "7bba00da10c4459e8887c29f5ce034ba";

const authorize = "https://accounts.spotify.com/authorize";

function on_page_load() {}

function request_authorization() {
  let url = authorize;
  url += "?client_id=" + client_id;
  url += "&response_type=code";
  url += "&redirect_uri=" + encodeURI(redirect_uri);
  url += "&show_dialog=true";
  url +=
    "&scope=playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public user-read-playback-position user-top-read user-read-recently-played user-library-read user-library-modify user-read-email user-read-private";
  window.location.href = url;
}

document.addEventListener("DOMContentLoaded", () => {
  const button = document.getElementById("login_button");
  button.addEventListener("click", () => {
    console.log("Button was clicked!");
    request_authorization();
  });
});
