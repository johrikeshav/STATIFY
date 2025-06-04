import { access_token } from ".";
import { get_user_profile } from ".";

document.addEventListener("DOMContentLoaded", async () => {
  const token = localStorage.getItem("access_token") || access_token;
  if (token) {
    try {
      const username = await get_user_profile(token);
      console.log("Username:", username);
      // Use `username` in your UI
    } catch (err) {
      console.error(err);
    }
  }
});
