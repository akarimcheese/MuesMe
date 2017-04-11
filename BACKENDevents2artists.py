import python_wrapper_template as ayman
import spotify_playlist_creation as sp
import events_from_artist as vik
import sys, json
from dateutil.parser import parse
from StringIO import StringIO

io = StringIO()


events = sys.argv[1].split(',')

artists = ayman.getArtistsFromEventIds(events)
artistSpotifyInfo = map(sp.getArtistSpotifyInfo,artists)
artists = []
for artist in artistSpotifyInfo:
    if artist != None:
        artists.append(artist)
        

json.dump(artistSpotifyInfo, io)

print(io.getvalue())
sys.stdout.flush()