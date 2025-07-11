#!/usr/bin/env python3

FILE_STATES = 'deterministic.txt'
FIRST_STATE = '69420'
LAST_STATE = '999'


def _get_states() -> dict:
    states = {}  # {state: (value, next_state)}

    with open(FILE_STATES, 'r', ) as reader:
        line = reader.readline()

        while line != '':  # EOF
            data = line.strip().split()  # sate, value, next_state
            states[data[0]] = (data[1], data[2])
            line = reader.readline()

    return states


def _get_xored_password(states: dict) -> list:
    current_state = FIRST_STATE
    xored_password = []

    while current_state != LAST_STATE:
        xored_password.append(states[current_state][0])
        current_state = states[current_state][1]

    # xored_password.append(states[current_state][0])  # State 999 is not in the file

    return xored_password


def _get_passphrase(xored_password: list) -> None:
    # Each character of the password is XORed with key of length one.
    # Brute-force attack
    for i in range(128):  # ASCII range
        char = chr(i)
        passphrase = []

        if char.isalnum():
            for j in xored_password:
                key_char = chr(i ^ int(j)).replace('\n', '')

                if key_char.isprintable():
                    passphrase.append(key_char)

            print(f"Key: '{char}' -> '{''.join(passphrase)}'")


if __name__ == '__main__':
    states = _get_states()
    xored_password = _get_xored_password(states)
    _get_passphrase(xored_password)
