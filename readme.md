# Windows Credential Updater

Searches the windows credential store for all entries with an old password and replaces it with an updated password.

Wraps %windir%\system32\cmdkey.exe to get a list of locally stored credentials, and uses the python [keyring](https://pypi.org/project/keyring/) package to match and update passwords.


Example:

```
python3 wincredupdate.py
Please type OLD password:
Please type NEW password:
Please retype NEW password: 
Skipped XboxLive
Match! Updating password for: git:https://bitbucket.intranet.testlab (testuser)
Match! Updating password for: 10.10.10.50 (testuser)
Match! Updating password for: proxy.intranet.testsite (testuser)
Matched 3 entries
```
