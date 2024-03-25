import json


my_data = json.loads(input())
errors = dict.fromkeys(['bus_id', 'stop_id', 'stop_name', 'next_stop', 'stop_type', 'a_time'], 0)
model = {'bus_id': int, 'stop_id': int, 'stop_name': str, 'next_stop': int, 'stop_type': str, 'a_time': str}
my_data = json.loads(ddd)
# print(json.dumps(my_data, indent=2))
for stop_data in my_data:
    for key, value in stop_data.items():
        if (not isinstance(value, model[key])) or (not value):
            errors[key] += 1
print(errors)