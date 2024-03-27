import json
from collections import defaultdict

my_data: dict = json.loads(input())
lines: dict[int: list[tuple[str, str]]] = defaultdict(list)
print('Arrival time test:')
for stop in my_data:
    lines[stop['bus_id']].append((stop['stop_name'], stop['a_time']))

ok = True
for line, stops in lines.items():
    prev_time = stops[0][1]
    for i in range(1, len(stops)):
        if stops[i][1] <= prev_time:
            print(f'bus_id line {line}: wrong time on station {stops[i][0]}')
            ok = False
            break
        prev_time = stops[i][1]
if ok is True:
    print('OK')
