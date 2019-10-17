import requests
import hashlib
import sys

def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching {res.status_code}, check the api and try again.')
    return res

def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)

def main(args):
    open_text_file = open('checkpass.txt', 'r')
    my_pass = open_text_file.read()
    for _ in args:
        count = pwned_api_check(my_pass)
        if count:
            print(f'The Password \'{my_pass}\' WAS Found {count} Times... You Should Probably Change Your Password!')
            open_text_file.close() 
        else:
            print(f'The Password \'{my_pass}\' Was NOT found!\nYour Password Is Currently Safe.\nCheck It Here Often To Check If It Is Ever Compromised.')
            open_text_file.close() 
    return 'You Can Edit The \'checkpass.txt\' File In The Main Folder To Check Another Password Or Quit Terminal To End The Programme.\nDelete The Password You Checked From The \'checkpass.txt\' File So You Don\'t Keep Your Passwords Saved In The File.'  

if __name__ == '__main__':    
    sys.exit(main(sys.argv[1:]))

