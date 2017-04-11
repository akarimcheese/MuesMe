import json,requests,sys

def getArtistSpotifyInfo(artist_name):
    url = 'https://api.spotify.com/v1/search?'

    #query parameters
    params = dict(
        q = artist_name,
        type='artist',
        limit='1'
    )

    #calling API
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)

    #getting the artist's id from search
    if (len(data['artists']['items']) >= 1):
        if (len(data['artists']['items'][0]['images']) >= 1):
            return dict( id=data['artists']['items'][0]['id'],
                         name=artist_name,
                         img=data['artists']['items'][0]['images'][0]['url'])
        else:
            return dict( id=data['artists']['items'][0]['id'],
                         name=artist_name,
                         img="data:image/jpeg;base64,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")
    return None

def getSongUris(song_obj):
    return song_obj['uri']

def getSongUrisFromArtist(artist_id,auth):
    url = 'https://api.spotify.com/v1/artists/' + artist_id + '/top-tracks?'
    #query parameters
    params = dict(
        country = 'US'
    )

    headers = {"Authorization":"Bearer " + auth}

    #calling API
    resp = requests.get(url=url, params=params, headers=headers)
    data = json.loads(resp.text)

    song_uris = map(getSongUris,data['tracks'][:5])
    return song_uris

def makePlaylistFromSongs(username,song_uris,auth):
    url = 'https://api.spotify.com/v1/users/' + username + '/playlists'

    headers = {"Authorization":"Bearer " + auth}

    payload = {
        'description': 'Taste Test Created By TuneTown',
        'public': 'true',
        'name': 'Taste Test'
    }

    resp = requests.post(url=url, data=json.dumps(payload), headers=headers)
    data = json.loads(resp.text)

    playlist_id = data['id']
    playlist_url = data['external_urls']['spotify']

    for song_uri in song_uris:
        url = 'https://api.spotify.com/v1/users/' + username + '/playlists/' + playlist_id + '/tracks?'
        #query parameters
        params = dict(
            position = '0',
            uris = song_uri
        )

        headers = {"Authorization":"Bearer " + auth}

        resp = requests.post(url=url, params=params, headers=headers)

    return playlist_url
