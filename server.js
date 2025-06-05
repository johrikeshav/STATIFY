const express = require("express");
const bodyParser = require("body-parser");
const axios = require("axios");

const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

const CLIENT_ID = "e25a9541103b4281965e723111e57950";
const CLIENT_SECRET = "7bba00da10c4459e8887c29f5ce034ba";
const TOKEN_URL = "https://accounts.spotify.com/api/token";

app.post("/get-token", async (req, res) => {
  const { code, redirect_uri } = req.body;

  try {
    const response = await axios.post(
      TOKEN_URL,
      new URLSearchParams({
        grant_type: "authorization_code",
        code: code,
        redirect_uri: redirect_uri,
        client_id: CLIENT_ID,
        client_secret: CLIENT_SECRET,
      }),
      { headers: { "Content-Type": "application/x-www-form-urlencoded" } }
    );

    res.json(response.data); // Send the token back to the frontend
  } catch (error) {
    console.error("Error fetching token:", error.response.data);
    res.status(400).json(error.response.data);
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
