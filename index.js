var redirect_uri = "https://johrikeshav.github.io/statify/stats.html";
var client_id = "e25a9541103b4281965e723111e57950";
var client_secret = "";

const authorize = "https://accounts.spotify.com/authorize";
const TOKEN = "https://accounts.spotify.com/token";

export let access_token, refresh_token;

function on_page_load() {
  if (window.location.search.length > 0) {
    handle_redirect();
  }
}

function handle_redirect() {
  let code = get_code();
  fetch_access_token(code);
}

function fetch_access_token(code) {
  let body = "grant_type=authorization_code";
  body += "&code=" + code;
  body += "&redirect_uri=" + encodeURI(redirect_uri);
  body += "&client_id=" + client_id;
  body += "&client_secret=" + client_secret;
  call_authorization_api(body);
}

function call_authorization_api(body) {
  let xhr = new XMLHttpRequest();
  xhr.open("POST", TOKEN, true);
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  xhr.setRequestHeader(
    "Authorization",
    "Basic " + btoa(client_id + ":" + client_secret)
  );
  xhr.send(body);
  xhr.onload = handle_authorization_response();
}

function handle_authorization_response() {
  if (this.status == 200) {
    var data = JSON.parse(this.responseText);
    console.log(data);
    var data = JSON.parse(this.responseText);
    if (data.access_token != undefined) {
      access_token = data.access_token;
      localStorage.setItem("access_token", access_token);
    }
    if (data.refresh_token != undefined) {
      refresh_token = data.refresh_token;
      localStorage.setItem("refresh_token", refresh_token);
    }
    on_page_load();
  } else {
    console.log(this.responseText);
    alert(this.responseText);
  }
}

function get_code() {
  let code = null;
  const query_string = window.location.search;
  if (query_string.length > 0) {
    const url_params = new URLSearchParams(query_string);
    code = url_params.get("code");
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

export async function get_user_profile(access_token) {
  const response = await fetch("https://api.spotify.com/v1/me", {
    headers: {
      Authorization: "Bearer " + access_token,
    },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch user profile");
  }

  const data = await response.json();
  console.log("User data:", data);
  return data.display_name; // or data.id, data.email etc.
}

document.addEventListener("DOMContentLoaded", () => {
  const button = document.getElementById("login_button");
  button.addEventListener("click", () => {
    console.log("Button was clicked!");
    request_authorization();
  });
});
