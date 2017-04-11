import json,requests, os
from datetime import datetime as dt

#getting the artist's songkick ID:

#given an artist's nwame as a string,
#search for the artist's ID and return it
def get_artist_id(artistName):
    #base URL
    url = 'http://api.songkick.com/api/3.0/search/artists.json?'

    #query parameters
    params = dict(
            query = artistName,
    	    apikey=os.environ['SONGKICK_API_KEY']
    )

    #calling the SongKick API
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)

    #getting the artist's id from the returned JSON object
    artist_id = data['resultsPage']['results']['artist'][0]['id']
    return artist_id


# getting an artist's event calendar:

# given an artist's songkick ID,
# make a dict/hash of data for each event
# that the artist is playing at,
# and return a list of those dicts/hashes.
def get_events_for_artist(artistid,start_date = 'empty',end_date = 'empty'):
    #base URL
    url = 'http://api.songkick.com/api/3.0/artists/' + str(artistid) + '/calendar.json?apikey=s9TgD3sUNEyDRjbc'
    #Calling SongKick API
    resp = requests.get(url=url)
    data = json.loads(resp.text)

    #list to store events
    events_arr = []

    #variables to store the start/end date
    start_datetime = 'empty'
    end_datetime = 'empty'

    # if start and end date provided, convert to datetime objects.
    # Provided date strings must be in format YYY-MM-DD
    if start_date != 'empty' and end_date != 'empty':
        start_datetime = dt.strptime(start_date, '%Y-%m-%d')
        end_datetime = dt.strptime(end_date,'%Y-%m-%d')

    #looping through the events the artist is playing at
    for event in data['resultsPage']['results']['event']:
        #if event is a concert, store the event's data in a dict
        if event['type'] == "Concert":
            date = event['start']['time']
            displayName = event['displayName']
            location = event['location']['city']
            venue = event['venue']['displayName']
            date = event['start']['date']
            event_datetime = dt.strptime(date,'%Y-%m-%d')
            start_time = event['start']['time']

            artist = event['performance'][0]['artist']['displayName']

            event_dict = {
                'Loc' : location,
                'Venue': venue,
                'Event Name': displayName,
                'Date': date,
                'Start Time': start_time,
                'Artist': artist
            }
            #if start/end date provided, check if event is between those dates
            #and only add if between them. Otherwise, always add the event
            if start_datetime != 'empty' and end_datetime != 'empty':
                if is_between_dates(event_datetime,start_datetime,end_datetime):
                    events_arr.append(event_dict)
            else: #if empty, add all
                print('entered else')
                print('\n')
                events_arr.append(event_dict)

    return events_arr


def is_between_dates(eventdate,startdate,enddate):
    return eventdate >= startdate and eventdate <= enddate
