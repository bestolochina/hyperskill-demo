import hashlib
import requests


password = input('Enter your password: ')
sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
print(f'Your hashed password is: {sha1_hash}')
print('Checking...')
hash_prefix = sha1_hash[:5]
url = f"https://api.pwnedpasswords.com/range/{hash_prefix}"
response = requests.get(url=url)
print(f'A request was sent to "{url}" endpoint, awaiting response...')
if response.status_code == 200:
    suffixes: list[str] = [line.split(':')[0] for line in response.text.splitlines()]
    if sha1_hash[5:] in suffixes:
        pass
        # print('The password has been compromised!')
    else:
        pass
        # print('The password has not been compromised.')
else:
    pass
    # print('Failed to check password.')
