import json
import sys

my_data: dict = json.loads(input())
stops: dict[int: dict[str: set[str]]] = {}

# Find start and finish stops for each bus line
for stop_data in my_data:
    if stop_data['bus_id'] not in stops.keys():
        stops[stop_data['bus_id']] = {'Start stops': set(),
                                      'Transfer stops': set(),
                                      'Finish stops': set(),
                                      'All stops': set()}
    stops[stop_data['bus_id']]['All stops'].add(stop_data['stop_name'])
    if stop_data['stop_type'] == 'S':
        stops[stop_data['bus_id']]['Start stops'].add(stop_data['stop_name'])
    if stop_data['stop_type'] == 'F':
        stops[stop_data['bus_id']]['Finish stops'].add(stop_data['stop_name'])

# Find transfer stops
for my_bus_id, my_bus_stops in stops.items():
    for bus_id, bus_stops in stops.items():
        if bus_id == my_bus_id:
            continue
        my_bus_stops['Transfer stops'].update(my_bus_stops['All stops'] & bus_stops['All stops'])

# Aggregating all start, finish and transfer stops
stf_stops = set()
for bus_stops in stops.values():
    stf_stops.update(bus_stops['Start stops'] | bus_stops['Finish stops'] | bus_stops['Transfer stops'])

wrong_stops = set()
for stop_data in my_data:
    if stop_data['stop_type'] == 'O' and stop_data['stop_name'] in stf_stops:
        wrong_stops.add(stop_data['stop_name'])

print('On demand stops test:')
if len(wrong_stops) == 0:
    print('OK')
else:
    print(f'Wrong stop type: {sorted(list(wrong_stops))}')
