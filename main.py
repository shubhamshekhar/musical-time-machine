import spotipy
from spotipy.oauth2 import SpotifyOAuth
import web_scraping

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id="",
        client_secret="",
        show_dialog=True,
        cache_path="token.txt"
    )
)
date = input("Which year do you want to travel to? Type the date in YYYY-MM-DD format.")
scrap = web_scraping.Scrapping(date, sp)
scrap.find_songs()
scrap.get_song_uri()
scrap.create_playlist()

