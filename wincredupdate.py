import keyring
import subprocess
from getpass import getpass
from sys import exit
from os import environ


def main():
    '''
wincredupdate.py - search and replace old password to new password in the windows credential store
https://github.com/glens/wincredupdate
Author: Glen Scott (glenscott.net)
    '''

    print(main.__doc__)

    times_to_ask_for_new_password = 3

    process = subprocess.Popen([environ['windir'] + '\\system32\\cmdkey.exe', '/list'],
                        stdout = subprocess.PIPE, 
                        stderr = subprocess.PIPE,
                        text = True,
                        shell = True)
    std_out, std_err = process.communicate()

    targets = []

    for entry in std_out.split("\n    \n    "):
        # parse output of cmdkey.exe to get credential entries into list
        tempdict={}
        for line in entry.splitlines():
            if 'Target:' in line:
                tempdict['label']=line.split('=')[1].strip()
            elif 'User' in line:
                tempdict['user']=line.split(':')[1].strip()
            elif 'Type' in line:
                tempdict['type']=line.split(':')[1].strip()
                
        targets.append(tempdict)

    oldpass = getpass("Please type OLD password:")
    newpass = getpass("Please type NEW password:")

    for n in range(times_to_ask_for_new_password):
        match = False
        newpass2 = getpass("Please retype NEW password:")
        if newpass == newpass2:
            match = True
            break
        else:
            if n < times_to_ask_for_new_password-1 :
                print("New passwords did not match, please try again")
            else:
                print("New passwords did not match ({} attempts), check your new password is entered correctly".format(n+1))
                exit()

    matches_found = 0

    for target in targets:
        # skip if credential entry is missing 'user' field as keyring requires it
        try:
            if keyring.get_password(target['label'], target['user']) == oldpass:
                print("Match! Updating password for: {} ({})".format(target['label'], target['user']))
                keyring.set_password(target['label'], target['user'], newpass)
                matches_found += 1

        except KeyError:
            print('No username field, skipping {}'.format(target['label']))

    if matches_found < 1:
        print("No Matches found (check password is entered correctly)")
    else:
        print("Matched {} entries".format(matches_found))


if (__name__ == "__main__"):
    main()
