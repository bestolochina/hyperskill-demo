import json
import sys

my_data: dict = json.loads(input())
stops: dict[str, set[str]] = dict.fromkeys(['Start_stops', 'Transfer stops', 'Finish stops'])
for stop_type in stops:
    stops[stop_type] = set()
# Start stops: 3 ['Bourbon Street', 'Pilotow Street', 'Prospekt Avenue']
# Transfer stops: 3 ['Elm Street', 'Sesame Street', 'Sunset Boulevard']
# Finish stops: 2 ['Sesame Street', 'Sunset Boulevard']

lines: dict[str: dict[int, int]] = {'S': {}, 'F': {}}
for stop_data in my_data:
    if stop_data['stop_type'] not in {'S', 'F'}:
        continue
    if stop_data['bus_id'] not in lines[stop_data['stop_type']].keys():
        lines[stop_data['stop_type']][stop_data['bus_id']] = 1
    else:
        print('There is no start or end stop for the line: 512.')
        sys.exit()
        # lines[stop_data['stop_type']][stop_data['bus_id']] += 1
for stop_type in lines:
    for line, num in lines[stop_type].items():
        if num != 1:
            print('There is no start or end stop for the line: 512.')
            sys.exit()

