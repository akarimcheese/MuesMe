import events_from_artist as efa
import json
import sys

#getting the correct arguments from command line
artist_name = sys.argv[1]
start_date = sys.argv[2]
end_date = sys.argv[3]

#getting songkick ID for artist
artist_id = efa.get_artist_id(artist_name)

# getting a list of dictionaries
# where each dict is a concert
concert_dict = efa.get_events_for_artist(artist_id,start_date,end_date)

print(json.dumps(concert_dict))