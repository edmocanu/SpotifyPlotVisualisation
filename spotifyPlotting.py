import spotipy
from spotipy.oauth2 import SpotifyOAuth
import matplotlib.pyplot as plt

# user variables
username = input("Enter your Spotify username:\n")
userID = input("Enter your Spotify user ID:\n")
clientID = input("Enter your Spotify client ID:\n")
clientSecret = input("Enter your Spotify secret client ID:\n")
playlistURL = input("All user information has been gathered. Enter the URL of the playlist you want to sort:\n")

# authorization variables
redirectURI = 'http://127.0.0.1:8080'
scope = 'playlist-modify-private','playlist-modify-public'
token = SpotifyOAuth(clientID,clientSecret,redirectURI,scope=scope,username=username)
sp = spotipy.Spotify(auth_manager = token)

# getting the playlist and its full length
playlist = sp.playlist(playlistURL)
results = playlist['tracks']
tracks = results['items']
while results['next']:
    results = sp.next(results)
    tracks.extend(results['items'])
length = len(tracks)

# setting up the x-axis
positions = []
for i in range(length):
    positions.append(i+1)

print("We are ready to generate a scatter plot now, where every point represents a different song from the playlist.")
print("The x-axis will be Position in the Playlist. Which attribute would you like the y-axis to be?")
print("You may choose from:\ndanceability\nenergy\nkey\nloudness\nmode\nspeechiness\nacousticness\ninstrumentalness")
print("liveness\nvalence\ntempo\ntype\nduration_ms\ntime_signature")

# input attributes
att1 = input()
att2 = input("Which attribute would you like to be represented in the sizes of the dots? Choose from the list above.\n")
att3 = input("Which attribute would you like to be represented in the colors of the dots? Choose from the list above.\n")

lst1 = []
lst2 = []
lst3 = []

# populating the arrays to store data for each song
for i in range(length):
    artist = playlist['tracks']['items'][i]['track']['album']['artists'][0]['name']
    song = playlist['tracks']['items'][i]['track']['name']
    songString = artist + " - " + song
    song = sp.search(q=songString,type='track',limit=1)['tracks']['items'][0]
    features = sp.audio_features(song['external_urls']['spotify'])[0]
    lst1.append(features[att1])
    lst2.append(features[att2])
    lst3.append(features[att3])

# the scatter plot is created
plt.scatter(positions,lst1,s=lst2,c=lst3)
plt.show()
