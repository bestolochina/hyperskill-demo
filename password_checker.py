import hashlib
import requests


password: str = input('Enter your password: ')
sha1_hash: str = hashlib.sha1(password.encode()).hexdigest().upper()
print(f'Your hashed password is: {sha1_hash}')
print('Checking...')
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
