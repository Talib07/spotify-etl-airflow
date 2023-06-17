import pandas as pd
from dotenv import load_dotenv
from requests import post, get
import os
import base64
import json
from google.cloud import storage

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
storage_client = storage.Client.from_service_account_json('key.json')

def get_token():
    # Encode the client ID and client secret in base64
    encoded_credentials = base64.b64encode((client_id + ':' + client_secret).encode()).decode('utf-8')

    url = "https://accounts.spotify.com/api/token"

    headers = {
        "Authorization" : "Basic " + encoded_credentials,
        "Content-Type" : "application/x-www-form-urlencoded"
    }

    data = {"grant_type":"client_credentials"}

    response = post(url,headers=headers,data=data)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the access token from the response
        access_token = response.json()['access_token']
    else:
        print('Failed to retrieve access token.')
        return None

    return access_token

def get_auth_header(token):
    return {"Authorization" : "Bearer " + token}

def get_artist_tracks(token, artist_id, limit=200):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
    headers = get_auth_header(token)
    params = {
        'country': 'US',
        'limit': limit
    }
    response = get(url, headers=headers, params=params)
    json_results = json.loads(response.content)
    return json_results.get('tracks', [])

def search_artist(token,artist):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist}&type=artist&limit=1"
    query_url = url + query
    response = get(query_url,headers=headers)
    json_results = json.loads(response.content)['artists']['items']
    if len(json_results)==0:
        print("No such artist found")
        return None
    else:
        return json_results[0]

def create_dataset(artist_id):
    token = get_token()
    tracks = get_artist_tracks(token, artist_id)

    dataset = []
    for track in tracks:
        track_data = {
            'Name': track['name'],
            'Duration (ms)': track['duration_ms'],
            'Popularity': track['popularity'],
            'Release Date': track['album']['release_date'],
            'Album': track['album']['name'],
            'Artist': track['artists'][0]['name'],
            'Artist ID': track['artists'][0]['id'],
            'Album Total Tracks': track['album']['total_tracks'],
            'Track Number': track["track_number"] 
            # Add more columns as per your requirements
        }
        
        dataset.append(track_data)

    return dataset

rock_bands = [
    "The Beatles",
    "Led Zeppelin",
    "The Rolling Stones",
    "Pink Floyd",
    "Queen",
    "AC/DC",
    "Guns N' Roses",
    "Nirvana",
    "The Who",
    "Metallica",
    "U2",
    "The Eagles",
    "Black Sabbath",
    "The Doors",
    "Rush",
    "The Jimi Hendrix Experience",
    "Deep Purple",
    "Fleetwood Mac",
    "Radiohead",
    "Pearl Jam",
    "Foo Fighters",
    "The Clash",
    "Van Halen",
    "The Beach Boys",
    "Red Hot Chili Peppers",
    "Green Day",
    "Bon Jovi",
    "The Police",
    "Genesis",
    "Aerosmith",
    "Def Leppard",
    "R.E.M.",
    "Dire Straits",
    "The Ramones",
    "Kiss",
    "The Cure",
    "The Kinks",
    "The Smashing Pumpkins",
    "Oasis",
    "ZZ Top",
    "Journey",
    "Creedence Clearwater Revival",
    "Linkin Park",
    "Coldplay",
    "Eagles"
]

dfs = []
def populate_data():
    token = get_token()
    for band in rock_bands:
        artist = search_artist(token,band)
        artist_id = artist['id']
        dataset = create_dataset(artist_id)
        df = pd.DataFrame(dataset)
        dfs.append(df)

    # Concatenate all dataframes into a single DataFrame
    df = pd.concat(dfs, ignore_index=True)

    # Save dataset as CSV
    temp_csv_path = 'spotify_dataset.csv'
    df.to_csv(temp_csv_path, index=False)

    # Upload the file to Google Cloud Storage
    bucket_name = 'spotify_etl_bucket'
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob('spotify_dataset.csv')
    blob.upload_from_filename(temp_csv_path)

    # Remove the temporary CSV file
    os.remove(temp_csv_path)

populate_data()
