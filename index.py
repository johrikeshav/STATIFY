import base64
import urllib.parse
import requests
import string
import random
import json
from urllib.parse import urlparse
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from scipy.special import softmax
from flask import Flask, request, redirect, session, url_for, render_template # type:ignore

app = Flask(__name__)
app.secret_key = '457878f51e8b4ddba3b4df5be79af8e9' # Needed for session management

CLIENT_ID = "e25a9541103b4281965e723111e57950"
CLIENT_SECRET = "7bba00da10c4459e8887c29f5ce034ba"
REDIRECT_URI = "http://127.0.0.1:5000/callback" 

AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1/"

SCOPE = "user-read-private user-read-email playlist-read-private user-top-read"

def generate_random_string(length):
    """Generates a random string for the state parameter."""
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login")
def login():
    state = generate_random_string(16)
    session['spotify_auth_state'] = state # Store state in session

    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': SCOPE,
        'state': state,
        # 'show_dialog': 'true' # Optional: forces the user to re-approve
    }
    auth_url_with_params = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    return redirect(auth_url_with_params)

@app.route("/callback")
def callback():
    error = request.args.get('error')
    code = request.args.get('code')
    state = request.args.get('state')
    stored_state =   session.pop('spotify_auth_state', None)

    if error:
        return f"Error during Spotify authorization: {error}"

    if state is None or state != stored_state:
        # State mismatch, potential CSRF attack
        return "Error: State mismatch. Please try logging in again."

    if code:
        # --- Exchange authorization code for access token ---
        auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
        payload = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URI,
        }
        headers = {
            'Authorization': f'Basic {auth_header}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post(TOKEN_URL, data=payload, headers=headers)
        token_info = response.json()

        if response.status_code == 200:
            session['access_token'] = token_info.get('access_token')
            session['refresh_token'] = token_info.get('refresh_token')
            session['expires_in'] = token_info.get('expires_in')
            # You would typically store these tokens securely (e.g., in a database associated with the user)
            print("Access Token:", session.get('access_token'))
            print("Refresh Token:", session.get('refresh_token'))
            return redirect(url_for('stats'))
        else:
            return f"Error getting token: {token_info.get('error_description', response.text)}"
    else:
        return "Error: No code received from Spotify."
    
@app.route("/stats", methods=['GET', 'POST'])
def stats():
    access_token = session.get('access_token')
    if not access_token:
        return redirect(url_for('login'))

    # --- 1. Get User's Display Name (First API Call) ---
    headers = {'Authorization': f'Bearer {access_token}'}
    profile_response = requests.get(f"{API_BASE_URL}me", headers=headers)
    
    # Check for errors on the first call
    if profile_response.status_code != 200:
        return redirect(url_for('login')) # Or handle the error appropriately
    

    display_name = profile_response.json().get('display_name')

    # --- 2. Get User's Top Artists (Second API Call) ---
    selected_time_range = request.args.get('time_range', 'short_term')
    
    # These params are for the /me/top/artists endpoint
    params = {
        'limit': 5,  # Get the top 5 artists
        'time_range': selected_time_range
    }
    
    # Make the CORRECT API call to the /top/artists endpoint
    artists_response = requests.get(f"{API_BASE_URL}me/top/artists", headers=headers, params=params)

    # Making the API call for top tracks

    params = {
        'type' : 'tracks',
        'limit': 5,  # Get the top 5 tracks
        'time_range': selected_time_range
    }

    tracks_response = requests.get(f"{API_BASE_URL}me/top/tracks", headers=headers, params=params)

    # Check for errors on the second call
    if artists_response.status_code != 200:
        return redirect(url_for('login')) 

    # Use a list comprehension to create a simple list of just the artist names.
    # This is the "nice array" you want!
    full_artist_list = artists_response.json().get('items', [])

    # parsing json data

    full_tracks_list = tracks_response.json().get('items', [])

    # handling popularity and genres with a larger api call

    params = {
        'type' : 'artists',
        'limit': 50,  # Get the top 50 artists
        'time_range': selected_time_range
    }

    complete_artist_response = requests.get(f"{API_BASE_URL}me/top/artists", headers=headers, params=params)
    complete_artist_list = complete_artist_response.json().get('items', [])
    genre_list = []

    for artist in complete_artist_list:
        genre_list.extend(artist['genres'])

    genre_counts = Counter(genre_list)
    top_genres = genre_counts.most_common(5)

    top_genre_img = None
    top_genre_name = None

    if top_genres:
    # Get the name of the top genre, e.g., 'pop'
        top_genre_name = top_genres[0][0]

        # Find the first artist that matches the genre and has an image
        for artist in complete_artist_list:
            if top_genre_name in artist.get('genres', []):
                
                # **FIX for Bug #2: Check if the images list exists and is not empty**
                if artist.get('images'):
                    top_genre_img = artist['images'][0]['url']
                    
                    # **FIX for Logic Flaw: Stop looking once we've found our image**
                    break

    # Assume most_popular and least_popular are initialized before the loop, for example:
    # name, popularity, image_url
    most_popular = [None, -1, None]  # Initialize with a value lower than any possible popularity
    least_popular = [None, 101, None] # Initialize with a value higher than any possible popularity

    if complete_artist_list:
        # The loop iterates through each artist one by one
        for artist in complete_artist_list:
            popularity = artist.get('popularity', 50) # Default to 50 if no popularity key

            # --- Check for Most Popular ---
            # THIS BLOCK IS NOW INDENTED TO BE INSIDE THE FOR LOOP
            if popularity > most_popular[1]:
                most_popular[0] = artist.get('name')
                most_popular[1] = popularity
                # Your safety check for the image is correct!
                if artist.get('images'):
                    most_popular[2] = artist['images'][0]['url']
                else:
                    most_popular[2] = None

            # --- Check for Least Popular ---
            # THIS BLOCK IS ALSO INDENTED TO BE INSIDE THE FOR LOOP
            if popularity < least_popular[1]:
                least_popular[0] = artist.get('name')
                least_popular[1] = popularity
                # Your safety check for the image is correct here too!
                if artist.get('images'):
                    least_popular[2] = artist['images'][0]['url']
                else:
                    least_popular[2] = None
    
    #print(most_popular)
    #print(least_popular)

    # getting the url from spotify and doing neural network stuff

    song_url = request.form.get('song') # this will give us a string which has the url, need to parse the track id
    print(f"song url is :{song_url}")

    predicted_value_raw = None
    final_match = None
    
    # parsing the to get the track id
    # urlparse breaks the URL into its components
    if song_url:
        parsed_url = urlparse(song_url)

        # The path will be '/track/11dFghVXANMlKmJXsNCbNl'
        path_parts = parsed_url.path.split('/')

            # The parts will be: ['', 'track', '11dFghVXANMlKmJXsNCbNl']
            # The ID is the last element.
        spotify_id = None
        
        if len(path_parts) > 2 and path_parts[1] == 'track':
            spotify_id = path_parts[2]
            #print(f"Successfully extracted Spotify ID from URL: {spotify_id}")
        else:
            print("This is not a valid Spotify track URL.")

        # now that we have the spotify id, its time we use it to create the model input

        #print(f"DEBUG: spotify_id is type: {type(spotify_id)}")
        #print(f"DEBUG: spotify_id with repr: {repr(spotify_id)}")
        #print(f"{API_BASE_URL}/tracks/{spotify_id}")

        headers = {'Authorization': f'Bearer {access_token}'}

        user_track_response = requests.get(f"{API_BASE_URL}tracks/{spotify_id}", headers=headers)
        user_track_data = user_track_response.json()

        """ if user_track_data:
            print(user_track_data)
        else:
            print("sadness") """

        model_input = []

        #print(user_track_data['duration_ms']/1000)
        model_input.append(user_track_data['duration_ms']/1000)
        #print(user_track_data['explicit'])
        model_input.append(int(user_track_data['explicit']))
        #print(user_track_data['popularity'])
        model_input.append(user_track_data['popularity'])
        
        album_release_year = user_track_data['album']['release_date'][0:4]
        #print(album_release_year)
        model_input.append(int(album_release_year)) 
        album_id = user_track_data['album']['id']
        user_album_response = requests.get(f"{API_BASE_URL}albums/{album_id}", headers=headers)
        user_album_data = user_album_response.json()
        album_popularity = user_album_data['popularity']
        model_input.append(album_popularity)

        artist_id = user_track_data['artists'][0]['id']
        user_artist_response = requests.get(f"{API_BASE_URL}artists/{artist_id}", headers=headers)
        user_artist_data = user_artist_response.json()
        artist_followers = user_artist_data['followers']['total']
        artist_popularity = user_artist_data['popularity']
        model_input.append(artist_followers/1000)
        model_input.append(artist_popularity)

        print(model_input)

        # now we have the input to our model in a list, which should look like : 
        # [duration, 
        # explicitness, 
        # track_popularity, 
        # release_date, 
        # album_popularity, 
        # artist_followers, 
        # artist_popularity]

        # now we will go through the user's top 50 tracks to train a Linear Regression Model

        params = {
            'type' : 'tracks',
            'limit': 50,  # Get the top 50 tracks
            'time_range': selected_time_range
        }

        complete_track_response = requests.get(f"{API_BASE_URL}me/top/tracks", headers=headers, params=params)
        complete_track_list = complete_track_response.json().get('items', [])

        model_training_data = []
        max_score = 100
        scores = []

        while max_score > 65:
            scores.append(max_score)
            max_score -= (35/49)

        for track in complete_track_list:
            example = []
            
            duration = track.get('duration_ms')
            example.append(duration/1000)
            
            explicit = track.get('explicit', 0)
            example.append(int(explicit))
            
            track_pop = track.get('popularity', 50)
            example.append(track_pop)
            
            album = track.get('album')
            album_id = album.get('id')
            album_response = requests.get(f"{API_BASE_URL}albums/{album_id}", headers=headers)
            album = album_response.json()

            album_release_year = int(album['release_date'][0:4])
            example.append(album_release_year)

            album_popularity = album['popularity']
            example.append(album_popularity)

            artist = track.get('artists')[0]
            artist_id = artist.get('id')
            artist_response = requests.get(f"{API_BASE_URL}artists/{artist_id}", headers=headers)
            artist = artist_response.json()

            artist_followers = artist['followers']['total']
            example.append(artist_followers/1000)

            artist_popularity = artist['popularity']
            example.append(artist_popularity)

            model_training_data.append(example)

        #print(model_training_data)

        # and now we train a ML model

        X_train_np = np.array(model_training_data)
        Y_train_np = np.array(scores).reshape(-1,1)

        model_input_np = np.array(model_input).reshape(1,-1)

        model = LinearRegression()
        model.fit(X_train_np,Y_train_np)

        print("--- Model Training Complete ---")
        # You can inspect the learned coefficients and intercept
        # Note: For multiple features, coef_ will be an array of coefficients
        #print(f"Model coefficients: {model.coef_}")
        probabilities = softmax(model.coef_)
        #print(probabilities)
        #print(f"Model intercept: {model.intercept_}\n")

        predicted_value_raw = model.predict(model_input_np)[0][0]
        final_match = int(predicted_value_raw)
        print(predicted_value_raw)

    # --- 4. Pass everything to the template ---
    return render_template('stats.html', 
                           name=display_name, 
                           artists=full_artist_list, # Pass the list of names
                           tracks = full_tracks_list,
                           complete_artist_list = complete_artist_list,
                           top_genres = top_genres,
                           top_genre_img = top_genre_img,
                           most_popular = most_popular,
                           least_popular = least_popular,
                           predicted_value_raw = final_match,
                           selected_range=selected_time_range) # For highlighting the active nav link

    
       