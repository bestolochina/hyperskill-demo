import json
import re


def validate_stop_name(stop_name: str) -> bool:
    suffixes = ['Road', 'Avenue', 'Boulevard', 'Street']
    try:
        name, suffix = stop_name.rsplit(maxsplit=1)
    except ValueError:
        return False
    if suffix not in suffixes or not name[0].isupper():
        return False
    return True


def validate_stop_type(stop_type: str) -> bool:
    if stop_type not in ['', 'S', 'O', 'F']:
        return False
    return True


def validate_a_time(a_time: str) -> bool:
    if not re.match(r'^(2[0-3]|[01]\d):[0-5]\d$', a_time):
        return False
    return True


my_data: dict = json.loads(input())
format_errors: dict = dict.fromkeys(['stop_name', 'stop_type', 'a_time'], 0)
for stop_data in my_data:
    if validate_stop_name(stop_data['stop_name']) is False:
        format_errors['stop_name'] += 1
    if validate_stop_type(stop_data['stop_type']) is False:
        format_errors['stop_type'] += 1
    if validate_a_time(stop_data['a_time']) is False:
        format_errors['a_time'] += 1

all_errors = sum(format_errors.values())

print(f'Format validation: {all_errors} errors')
for key, value in format_errors.items():
    print(f'{key}: {value}')
