import os
user = os.getenv("SUDO_USER")
if user is None:
    print ("This program need 'sudo'")
    exit()
else:
    print('ok')
