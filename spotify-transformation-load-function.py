
import json
import boto3
from datetime import datetime
from io import StringIO
import pandas as pd

# -------- Album Function --------
def album(data):
    album_list = []
    for row in data['items']:
        album_id = row['track']['album']['id']
        album_name = row['track']['album']['name']
        album_release_date = row['track']['album']['release_date']
        album_total_tracks = row['track']['album']['total_tracks']
        album_url = row['track']['album']['external_urls']['spotify']

        album_element = {
            'album_id': album_id,
            'name': album_name,
            'release_date': album_release_date,
            'total_tracks': album_total_tracks,
            'url': album_url
        }

        album_list.append(album_element)  

    return album_list


# -------- Artist Function --------
def artist(data):
    artist_list = []
    for row in data['items']:
        for key, value in row.items():
            if key == "track":
                for artist in value['artists']:
                    artist_dict = {
                        'artist_id': artist['id'],
                        'artist_name': artist['name'],
                        'external_url': artist['href']
                    }
                    artist_list.append(artist_dict)

    return artist_list


# -------- Songs Function --------
def songs(data):
    songs_list = []
    for row in data['items']:
        song_element = {
            'song_id': row['track']['id'],
            'song_name': row['track']['name'],
            'duration_ms': row['track']['duration_ms'],
            'url': row['track']['external_urls']['spotify'],
            'popularity': row['track']['popularity'],
            'song_added': row['added_at'],
            'album_id': row['track']['album']['id'],
            'artist_id': row['track']['album']['artists'][0]['id']
        }

        songs_list.append(song_element)

    return songs_list


# -------- Lambda Handler --------
def lambda_handler(event, context):
    s3 = boto3.client('s3')

    Bucket = "spotify-etl-project-vinay9185"
    Prefix = "Raw_Data/to_processed/"

    spotify_data = []
    spotify_keys = []

    
    response = s3.list_objects_v2(Bucket=Bucket, Prefix=Prefix)

    if 'Contents' not in response:
        print("No files found")
        return

    for file in response['Contents']:
        file_key = file['Key']

        if file_key.endswith('.json'):
            obj = s3.get_object(Bucket=Bucket, Key=file_key)
            data = json.loads(obj['Body'].read())

            spotify_data.append(data)
            spotify_keys.append(file_key)

 
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    for data in spotify_data:
        album_list = album(data)
        artist_list = artist(data)
        songs_list = songs(data)

        # -------- DataFrames --------
        album_df = pd.DataFrame(album_list).drop_duplicates(subset=['album_id'])
        artist_df = pd.DataFrame(artist_list).drop_duplicates(subset=['artist_id'])
        song_df = pd.DataFrame(songs_list)

        # -------- Type conversions --------
        album_df['release_date'] = pd.to_datetime(album_df['release_date'])
        song_df['song_added'] = pd.to_datetime(song_df['song_added'])

        # -------- Upload to S3 --------
        def upload(df, key):
            buffer = StringIO()
            df.to_csv(buffer, index=False)

            s3.put_object(
                Bucket=Bucket,
                Key=key,
                Body=buffer.getvalue()
            )

        upload(song_df, f'transformed_data/songs_data/songs_{timestamp}.csv')
        upload(album_df, f'transformed_data/album_data/album_{timestamp}.csv')
        upload(artist_df, f'transformed_data/artist_data/artist_{timestamp}.csv')

    
    s3_resource = boto3.resource('s3')

    for key in spotify_keys:
        copy_source = {
            'Bucket': Bucket,
            'Key': key
        }

        s3_resource.meta.client.copy(
            copy_source,
            Bucket,
            'Raw_Data/processed/' + key.split('/')[-1]
        )

        s3_resource.Object(Bucket, key).delete()

    print("ETL process completed successfully ✅")
