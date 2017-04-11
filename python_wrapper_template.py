import json, requests, sys, os

# Get venue list

# Given a venue JSON object, return
# a tuple of the venue name, id, and metro id
def stripData(venue):
    return (venue['displayName'],venue['id'],venue['metroArea']['id'])

# Given a venue search query, return a list of
# venue tuples for all possible matches
def getVenues(query):
    url = 'http://api.songkick.com/api/3.0/search/venues.json?'

    params = dict(
        query=query, # Query
        apikey=os.environ['SONGKICK_API_KEY'],
    )

    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)

    venue_list = map(stripData,data['resultsPage']['results']['venue'])
    return venue_list

# We have the venue list, show it to user through frontend and have them
# choose the correct venue
# For the purpose of prototyping, assume they chose the first result

venue = getVenues('930+Club')[0]

# Now, get the events at this venue

# Given a venue id and a list of events, return the
# concerts at this venue
def getConcertsAtVenue(venue_id, events):
    result = []
    for event in events:
        if ((event['type'] == "Concert")):
            result.append((event['displayName'],event['id'],event['performance'],event['start']['date']))
    return result

# For the venue, get a list of events
def getEvents(venue):
    url = 'http://api.songkick.com/api/3.0/venues/' + str(venue[1]) + '/calendar.json?'

    # Max query of 50 events at a time, but
    # let's try to look at all possible events
    page = 1

    params = dict(
        apikey=os.environ['SONGKICK_API_KEY'],
        page=str(page)
    )

    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)

    events = getConcertsAtVenue(venue[1],data['resultsPage']['results']['event'])

    # While there are more events to see,
    # see em
    while (page * 50 < data['resultsPage']['totalEntries']):
        page = page + 1
        params = dict(
            location='sk:' + str(venue[2]), # Query
            apikey=os.environ['SONGKICK_API_KEY'],
            page=str(page)
        )
        resp = requests.get(url=url, params=params)
        data = json.loads(resp.text)

        events.extend(getConcertsAtVenue(venue[1],data['resultsPage']['results']['event']))
    return events

# events is now the events at this venue
# show the events at this venue
# for purposes of this prototype, assume the user wants all events at the venue

concerts = getEvents(venue)


def getArtists(obj):
    return obj['artist']['displayName']

# now find the artists playing at these events

# Get the artists at these concerts
def getArtistsFromConcerts(concerts):
    artists = []


    for concert in concerts:
        artists.extend(map(getArtists,concert[2]))

    return artists

def getArtistsFromEventIds(event_ids):
    artists = []

    for event_id in event_ids:
        url = "http://api.songkick.com/api/3.0/events/" + str(event_id) + ".json?"
        params = dict(
            apikey=os.environ['SONGKICK_API_KEY'],
        )
        resp = requests.get(url=url, params=params)
        data = json.loads(resp.text)

        artists.extend(map(getArtists,data['resultsPage']['results']['event']['performance']))

    return artists


artists = getArtistsFromConcerts(concerts)
