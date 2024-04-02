import socket
import sys
from itertools import product


assert len(sys.argv) == 3
hostname = sys.argv[1]
port = int(sys.argv[2])
address = (hostname, port)
symbols = 'abcdefghijklmnopqrstuvwxyz0123456789'
password = ''

with socket.socket() as my_socket:
    my_socket.connect(address)

    repeat = 1
    while not password:
        for passw in product(symbols, repeat=repeat):
            my_socket.send(''.join(passw).encode())
            response = my_socket.recv(1024).decode()

            if response == 'Wrong password!':
                continue
            elif response == 'Connection success!':
                password = ''.join(passw)
                break
            elif response == 'Too many attempts':
                sys.exit('--- Game over ---')
        repeat += 1

print(password)
