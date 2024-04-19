import hashlib
import requests
import argparse


def check_password(password: str, show_hash: bool) -> None:
    sha1_hash: str = hashlib.sha1(password.encode()).hexdigest().upper()
    print(f'Your hashed password is: {sha1_hash}\nChecking...') if show_hash else print('Checking...')
    hash_prefix: str = sha1_hash[:5]
    url: str = f"https://api.pwnedpasswords.com/range/{hash_prefix}"
    response: requests.Response = requests.get(url=url)
    print(f'A request was sent to "{url}" endpoint, awaiting response...')
    if response.status_code == 200:
        for suffix, num in [line.split(':') for line in response.text.splitlines()]:
            if suffix == sha1_hash[5:]:
                print(f'Your password has been pwned! The password "{password}" appears {num} times in data breaches.')
                break
        else:
            print("Good news! Your password hasn't been pwned.")
    else:
        print('Failed to check password.')


def main() -> None:
    parser = argparse.ArgumentParser(description='Check whether the password has been pwned')
    parser.add_argument('--show-hash', action='store_true', default=False)
    args = parser.parse_args()
    while (password := input("Enter your password (or 'exit' to quit): ")) != 'exit':
        check_password(password, args.show_hash)
    print('Goodbye!')


if __name__ == '__main__':
    main()
