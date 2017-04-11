import python_wrapper_template as ayman
import spotify_playlist_creation as sp
import events_from_artist as vik
import sys, json
from dateutil.parser import parse
from StringIO import StringIO

io = StringIO()


venue = ayman.getVenues(sys.argv[1])[0]
concerts = ayman.getEvents(venue)

def eventsInRange(events,startDate,endDate):
    start = parse(startDate)
    end = parse(endDate)
    result = []
    for event in events:
        date = parse(event[3])
        if (date >= start) & (date <= end):
            result.append(dict(
                    name=event[0],
                    id=event[1],
                    performance=event[2],
                    date=event[3]
                    )
                )
    return result

concertsInRange = eventsInRange(concerts,sys.argv[2],sys.argv[3])
json.dump(concertsInRange[:10], io)

print(io.getvalue())

sys.stdout.flush()