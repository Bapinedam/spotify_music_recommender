import spotipy
from dotenv import dotenv_values
import pprint
import openai
import json
import argparse

# keys

config = dotenv_values(".env")

# Commands utilities

parser = argparse.ArgumentParser(description="Simple command line song utilities")
parser.add_argument("-p", type=str, help="The prompt to describe the playlist")
parser.add_argument("-n", type=int, default=8, help="The number of songs you want into the playlist")

args = parser.parse_args()



# OpenAI call

openai.api_key = config["OPENAI_API_KEY"]

def get_playlist(prompt, num_songs = 8):
    example_json = """
    [
    {"song": "Fix You", "artist": "Coldplay"},
    {"song": "Someone Like You", "artist": "Adele"},
    {"song": "Hurt", "artist": "Johnny Cash"},
    {"song": "Nothing Compares 2 U", "artist": "Sinead O'Connor"},
    {"song": "Yesterday", "artist": "The Beatles"},
    {"song": "Tears in Heaven", "artist": "Eric Clapton"},
    {"song": "Hallelujah", "artist": "Jeff Buckley"},
    {"song": "The Sound of Silence", "artist": "Simon & Garfunkel"},
    {"song": "All I Want", "artist": "Kodaline"},
    {"song": "Skinny Love", "artist": "Bon Iver"}
    ]

    """

    messages = [
        {"role": "system", "content": """
        You are a helpful playlist generating assistant. 
        You should generate a list of songs and their artist according to a text prompt.
        You should return a JSON array, where each element follows this format: {"song": <song_title>, "artist" : <artist_of_the_song>}
        """},
        {"role":"user","content":"Generate a playlist of 10 songs based on this prompt: susuper sad songs"},
        {"role":"assistant", "content":example_json},
        {"role":"user","content":f"Generate a playlist of {num_songs} songs based on this prompt: {prompt}"},

    ]

    response = openai.chat.completions.create(
        messages=messages,
        model="gpt-3.5-turbo",
        max_tokens=400
    )

    playlist = json.loads(response.choices[0].message.content)
    return playlist

playlist = get_playlist(prompt = args.p, num_songs = args.n)
#print(playlist)

# Spotify set up

sp = spotipy.Spotify(
        auth_manager=spotipy.SpotifyOAuth(
            client_id= config["SPOTIFY_CLIENT_ID"],
            client_secret= config["SPOTIFY_CLIENT_SECRET"],
            redirect_uri="http://localhost:9999",               # This has to be the same as in the dashboard on spotofy developers
            scope = "playlist-modify-private"
        )
    )

# Login validation
current_user = sp.current_user()
assert current_user is not None

# Searching
track_ids = []

for item in playlist:
    artist, song = item["artist"], item["song"]
    query = f"{song} {artist}"
    #print(query)

    search_results = sp.search(q=query, type="track", limit=1)
    track_ids.append(search_results["tracks"]["items"][0]["id"])

#print(track_ids)

# Creating the playlist

created_playlist= sp.user_playlist_create(
        current_user["id"],             # Validate the user
        public=False,                   # If I want to create a public list or not
        name="TESTING PLAYLIST FUN"     # The name of the new playlist
    )

sp.user_playlist_add_tracks(current_user["id"], created_playlist["id"], track_ids)