import python_wrapper_template as ayman
import spotify_playlist_creation as sp
import events_from_artist as vik
import sys, json
from dateutil.parser import parse
from StringIO import StringIO

io = StringIO()


artist_ids = sys.argv[1].split(',')
song_uris = []

# FIX AUTHORIZATION
for artist in artist_ids:
    uris = sp.getSongUrisFromArtist(artist,sys.argv[2])
    song_uris.extend(uris)
    
url = sp.makePlaylistFromSongs(sys.argv[3],song_uris,sys.argv[2])
print(url)
sys.stdout.flush()