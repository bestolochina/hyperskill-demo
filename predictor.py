def enter_0_1() -> str:
    user_input = input('Print a random string containing 0 or 1:\n\n')
    string_0_1 = ''
    for char in user_input:
        if char in '01':
            string_0_1 += char
    return string_0_1


min_length = 100

my_string = ''

while True:
    my_string += enter_0_1()
    length = len(my_string)

    if length >= min_length:
        break
    print(f'Current data length is {length}, {min_length - length} symbols left')

print('Final data string:')
print(my_string)
