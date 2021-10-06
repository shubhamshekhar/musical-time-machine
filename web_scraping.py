from bs4 import BeautifulSoup
import requests
URL = "https://www.billboard.com/charts/hot-100/"


class Scrapping:
    def __init__(self, date, sp):
        self.url = URL + date
        self.songs = []
        self.date = date
        self.song_uris = []
        self.sp = sp
        self.user_id = sp.current_user()["id"]

    def find_songs(self):
        response = requests.get(url=self.url)
        response.raise_for_status()
        data = response.text

        soup = BeautifulSoup(data, "html.parser")
        song_list = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
        self.songs = [song.getText() for song in song_list]
        self.songs = self.songs[:10]
        print(self.songs)

    def get_song_uri(self):
        year = self.date.split("-")[0]
        for song in self.songs:
            result = self.sp.search(q=f"track:{song} year:{year}", type="track")
            print(result)
            try:
                uri = result["tracks"]["items"][0]["uri"]
                self.song_uris.append(uri)
            except IndexError:
                print(f"{song} doesn't exist in Spotify. Skipped.")

    def create_playlist(self):
        playlist = self.sp.user_playlist_create(user=self.user_id, name=f"{self.date} Billboard 100", public=False)
        self.sp.playlist_add_items(playlist_id=playlist["id"], items=self.song_uris)
        print(playlist["external_urls"]["spotify"])

