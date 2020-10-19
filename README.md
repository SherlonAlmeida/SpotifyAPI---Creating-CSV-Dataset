# SpotifyAPI---Creating-CSV-Dataset
This program will get data directly from Spotify using Spotipy and export in CSV format.

Description: <br>
    This program get tracks information directly from Spotify API using Spotipy. <br>
    1) The first step is to set up your own credentials (Client_id, Client_Secret), in the connectSpotifyAPI() function. <br>
    2) After that you just need to write the name of the artists you want to collect data from. So, replace the names in the artists list in main() function. <br>
    3) That's it! Run the program and enjoy your music Dataset. :) <br>

Output: <br>
    Will be created a CSV file containg the attributes below: <br>
    ['track_name', 'track_id', 'album_name', 'album_id', 'artist_name', 'artist_id', 'release_date', 'length', 'popularity', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature']
    
