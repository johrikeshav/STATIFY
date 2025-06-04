var redirect_uri = "https://johrikeshav.github.io/statify/stats.html";
var client_id = "e25a9541103b4281965e723111e57950";
var client_secret = "";

const authorize = "https://accounts.spotify.com/authorize";

function on_page_load() {
  if (window.location.search.length > 0) {
    handle_redirect();
  }
}

function handle_redirect() {
  let code = get_code();
}

function get_code() {
  let code = null;
  const query_string = window.location.search;
  if (query_string.length > 0) {
    const url_params = new URLSearchParams(query_string);
    code = url_params.get_code("code");
  }
}

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
