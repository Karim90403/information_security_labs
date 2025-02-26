import sys
from typing import Optional

import getch


def mask_input(prompt: Optional[str] = None, mask: str = "*"):
    password = ''
    print(prompt or 'Enter your password: ')
    while True:
        pressedKey = getch.getch()
        if pressedKey == '\n':
            break
        elif pressedKey == "":
            sys.stdout.write("\b")
            sys.stdout.write(" ")
            sys.stdout.write("\b")
            password = password[:-1]
        else:
            password = password + pressedKey
            sys.stdout.write(mask)
    sys.stdout.write("\n")
    return password