import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

client_id = "49d80436e9ca445c8560d005108b0a36"
client_secret = os.environ['CLISEC']


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri="http://example.com",
                                               scope='playlist-modify-public'))

# user_id = "31iak5juofovz6ucx47opualkm6u"
user_id = sp.current_user()['id']

date = input("Which year do you want to travel to? Type the date in the format YYYY-MM-DD: ")
response = requests.get("https://www.billboard.com/charts/hot-100/"+date)
data = response.text
soup = BeautifulSoup(data, 'html.parser')
# print(soup.prettify())
titles = soup.select(selector="li ul li h3")
artists = soup.select(selector="li ul li span")[::7]
title_list= [title.getText().strip() for title in titles]
artists_list = [artist.getText().strip() for artist in artists]
print(title_list)
# print(artists_list)
# year = date.split("-")[0]
# print(year)
song_uris = []
for i in range(len(title_list)):
    result = sp.search(q=f"{title_list[i]} {artists_list[i]}", type="track")
    # print(result)
    try:
        song_id = result['tracks']['items'][0]['uri']
        song_uris.append(song_id)
    except IndexError:
        print(f"{title_list[i]} doesnt exist on spotify. skipped.")

# print(song_uris)
new_playlist = sp.user_playlist_create(user=user_id, name=f"Top100-{date}", public=True)
playlist_id = new_playlist['id']
add_tracks = sp.playlist_add_items(playlist_id=playlist_id, items=song_uris)




