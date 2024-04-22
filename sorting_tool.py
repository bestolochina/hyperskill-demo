my_list = []
while True:
    try:
        data = input()
        my_list.extend([int(_) for _ in data.split()])
    except EOFError:
        break

length = len(my_list)
greatest = max(my_list)
num = my_list.count(greatest)
print(f'Total numbers: {length}.')
print(f'The greatest number: {greatest} ({num} time(s)).')
