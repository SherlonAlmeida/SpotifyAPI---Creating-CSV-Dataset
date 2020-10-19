# -*- coding: utf-8 -*-

"""
Author: Sherlon Almeida
University of São Paulo

Description:
	This program get tracks information directly from Spotify API using Spotipy.
	1) The first step is to set up your own credentials (Client_id, Client_Secret) below, in the connectSpotifyAPI() function.
	2) Now you just need to write the name of the artists you want to collect data from. So, replace the names in the artists list in main() function.
	3) That's it! Run the program and enjoy your music Dataset. :)
"""

"""Import libraries"""
import spotipy, time, codecs, json
from spotipy.oauth2 import SpotifyClientCredentials
from cleantext import clean

""" Description:
        This function removes all NON-ASCII characters
    Parameters:
        input_str    ->  String to be fixed
    Return:
        result       ->  The generated string
"""
def data_preprocessing(input_str):
    #Remove only pontuation
    #result = input_str.translate(str.maketrans('', '', string.punctuation))
    
    #Remove Non-Printable characteres
    #printable = set(string.printable)
    #result = ''.join(filter(lambda x: x in printable, input_str))
    
    result = clean(input_str,
        fix_unicode=True,               # fix various unicode errors
        to_ascii=True,                  # transliterate to closest ASCII representation
        lower=False,                    # lowercase text
        no_line_breaks=False,           # fully strip line breaks as opposed to only normalizing them
        no_urls=False,                  # replace all URLs with a special token
        no_emails=False,                # replace all email addresses with a special token
        no_phone_numbers=False,         # replace all phone numbers with a special token
        no_numbers=False,               # replace all numbers with a special token
        no_digits=False,                # replace all digits with a special token
        no_currency_symbols=False,      # replace all currency symbols with a special token
        no_punct=False,                 # fully remove punctuation
        replace_with_url="<URL>",
        replace_with_email="<EMAIL>",
        replace_with_phone_number="<PHONE>",
        replace_with_number="<NUMBER>",
        replace_with_digit="0",
        replace_with_currency_symbol="<CUR>",
        lang="en"                       # set to 'de' for German special handling
    )
    return result


""" Description:
        This function connects to the Spotify API
    Parameters:
        It is not required, but you need to set up your own credentials (client_id, client_secret)
    Return:
        sp -> Spotipy object generated
"""
def connectSpotifyAPI():
    client_id = ''     #You need to put your own credentials here
    client_secret = '' #... and here
    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp


""" Description:
        This function returns the JSON formatted
    Parameters:
        data      -> A JSON file to be formatted
    Return:
        formatted -> A JSON file formatted
"""
def showInformation(data):
    formatted = json.dumps(data, indent=4, sort_keys=True)
    return formatted


""" Description:
        Given a track id, returns the metadata and features related
    Parameters:
        id      -> The Identification of the Track
    Return:
        This function returns a list of metadata and features
"""
def getTrackData(sp, track_id, csv_file):
    meta = sp.track(track_id)
    features = sp.audio_features(track_id)
    
    # meta
    track_name = meta['name'] #Remove Non-Ascii Characters
    track_id = meta['id']
    album_name = meta['album']['name'] #Remove Non-Ascii Characters
    album_id = meta['album']['id']
    artist_name = meta['album']['artists'][0]['name'] #Remove Non-Ascii Characters
    artist_id = meta['album']['artists'][0]['id']
    release_date = meta['album']['release_date']
    length = meta['duration_ms']
    popularity = meta['popularity']
    
    # features
    acousticness = features[0]['acousticness']
    danceability = features[0]['danceability']
    energy = features[0]['energy']
    instrumentalness = features[0]['instrumentalness']
    liveness = features[0]['liveness']
    loudness = features[0]['loudness']
    speechiness = features[0]['speechiness']
    tempo = features[0]['tempo']
    time_signature = features[0]['time_signature']
    
    track = [track_name, track_id, album_name, album_id, artist_name, artist_id, release_date, length, popularity,
             acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, tempo, time_signature]
    
    print("Getting track data: " + str(artist_name) + " - " + str(track_name))
    for column in track:
        csv_file.write(str(column) + "; ")
    csv_file.write("\n")
    
    time.sleep(.5) #This waiting time is necessary to avoid Spotify denial of service identification


""" Description:
        Retrieve the information of all Tracks inside an album by Album_ID 
    Parameters:
        sp       -> Spotipy object
        album_id -> Album's identification to Spotify API
    Return:
        It is not Required
"""
def getAlbumsTracks(sp, album_id, csv_file):
    track_data = []
    results = sp.album_tracks(album_id)
    for track in results['items']:
        #Get track information
        track_id = track['id']
        getTrackData(sp, track_id, csv_file)

""" Description: 
        Retrieve albums of an artist using artist URI
    Parameters:
        sp         -> Spotipy object
        artist_uri -> Artist identification to Spotify API
    Return:
        It is not Required
"""
def getAlbums(sp, artist_uri, csv_file):
    albums_data = []
    #Get Albums
    albums = sp.artist_albums(artist_uri, album_type='album')
    albums_names = albums['items']
    while albums['next']:
        albums = sp.next(albums)
        albums_names.extend(albums['items'])
    for album in albums_names:
        albums_data.append({'id': album['id'], 'name': album['name']})
    
    #Get Album tracks
    for album in albums_data:
        getAlbumsTracks(sp, album['id'], csv_file)


""" Description: 
        Retrieve information of a list of Artists by Name
    Parameters:
        sp      -> Spotipy object
        artists -> A string list of artists
    Return:
        artists_data -> Some attributes of artist
            'artist' -> Name of artist
            'uri'    -> Artist identification to Spotify API
            'genres' -> Genres of artist
"""
def getArtistsInformation(sp, artists):
    print("Getting Artist's information...")
    artists_data = []
    for name in artists:
        #Get artist information by Name (Query)
        results = sp.search(q='artist:' + name, type='artist')
        #Get and store URI
        uri = results['artists']['items'][0]['uri']
        #Get and store Genres
        genres = results['artists']['items'][0]['genres']
        #Save information
        artists_data.append({'artist': name, 'uri': uri, 'genres': genres})
    return artists_data


""" Description: 
        Insert the headers in csv
    Parameters:
        csv_file     -> File to be written
    Return:
        It is not Required
"""
def insert_csv_headers(csv_file):
    columns = ['track_name', 'track_id', 'album_name', 'album_id', 'artist_name', 'artist_id', 'release_date', 'length', 
               'popularity', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness',
               'speechiness', 'tempo', 'time_signature']
    
    for column in columns:
        csv_file.write(str(column) + "; ")
    csv_file.write("\n")

"""Main Function"""
def main():
    """Connect to the API"""
    sp = connectSpotifyAPI()
    
    """Define Artists by Name to Search"""
    artists = ["Coldplay", "Green Day", "JP Cooper", "The Beatles",
               "Europe", "Firehouse", "The Outfield", "Scorpions", "Oasis",
               "Megadeth", "Metallica", "Iron Maiden", "Lynyrd Skynyrd", "Kansas"] #Define here the artists you want data from
    
    """Retrieve information of a list of Artists by Name"""
    artists_data = getArtistsInformation(sp, artists)
    
    """Retrieve albums, tracks and track features of each artist and store it in a CSV file"""
    csv_file = codecs.open("Dataset.csv", "w", "utf-8")
    insert_csv_headers(csv_file)
    for artist in artists_data:
        getAlbums(sp, artist['uri'], csv_file)
    csv_file.close()
    
#Call the main function
main()