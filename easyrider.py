import json
import sys

# my_data: dict = json.loads(input())
my_data: dict = json.loads('''[{"bus_id" : 128, "stop_id" : 1, "stop_name" : "Prospekt Avenue", "next_stop" : 3, "stop_type" : "S", "a_time" : "08:12"}, {"bus_id" : 128, "stop_id" : 3, "stop_name" : "Elm Street", "next_stop" : 5, "stop_type" : "", "a_time" : "08:19"}, {"bus_id" : 128, "stop_id" : 5, "stop_name" : "Fifth Avenue", "next_stop" : 7, "stop_type" : "O", "a_time" : "08:25"}, {"bus_id" : 128, "stop_id" : 7, "stop_name" : "Sesame Street", "next_stop" : 0, "stop_type" : "F", "a_time" : "08:37"}, {"bus_id" : 512, "stop_id" : 4, "stop_name" : "Bourbon Street", "next_stop" : 6, "stop_type" : "", "a_time" : "08:13"}, {"bus_id" : 512, "stop_id" : 6, "stop_name" : "Sunset Boulevard", "next_stop" : 0, "stop_type" : "F", "a_time" : "08:16"}]''')
stops: dict[int: dict[str: set[str]]] = {}

# Find start and finish stops for each bus line
for stop_data in my_data:
    if stop_data['bus_id'] not in stops.keys():
        stops[stop_data['bus_id']] = {'Start stops': set(), 'Transfer stops': set(), 'Finish stops': set(), 'All stops': set()}
    stops[stop_data['bus_id']]['All stops'].add(stop_data['stop_name'])
    if stop_data['stop_type'] == 'S':
        stops[stop_data['bus_id']]['Start stops'].add(stop_data['stop_name'])
    if stop_data['stop_type'] == 'F':
        stops[stop_data['bus_id']]['Finish stops'].add(stop_data['stop_name'])

# Validate the number of start and finish stops for each bus line
for bus_id, bus_stops in stops.items():
    if len(bus_stops['Start stops']) == 0 or len(bus_stops['Finish stops']) == 0:
        print(f'There is no start or end stop for the line: {bus_id}.')
        sys.exit()
    if len(bus_stops['Start stops']) > 1 or len(bus_stops['Finish stops']) > 1:
        print(f'There is more than 1 start or end stop for the line: {bus_id}.')
        sys.exit()

# Start stops: 3 ['Bourbon Street', 'Pilotow Street', 'Prospekt Avenue']
# Transfer stops: 3 ['Elm Street', 'Sesame Street', 'Sunset Boulevard']
# Finish stops: 2 ['Sesame Street', 'Sunset Boulevard']
