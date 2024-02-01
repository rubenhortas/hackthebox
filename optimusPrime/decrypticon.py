#!/usr/bin/env python3

"""
Script to solve the crypto challenge "Optimus Prime" from https://app.hackthebox.com
"""

import sys

from gmpy2 import gcd
from Crypto.Util.number import inverse, long_to_bytes

E_VALUES = [3, 65537]


def _are_coprimes(a, b):
    return gcd(a, b) == 1


def _get_integer(name):
    n = 0

    while n == 0:
        try:
            n = int(input(f"Enter {name}: "))
        except:
            pass

    return n


def _decrypt(n1, n2, c2):
    # n1 = p1 * q1
    # n2 = p2 * q2
    # If n1 and n2 are not coprimes we can find a common prime and
    # n1 = p * q1
    # n2 = p * q2
    p = int(gcd(n1, n2))

    # n2 = p * q2 -> q2 = n2 / p
    q2 = n2 // p

    # phi2 = (p - 1) * (q2 - 1)
    phi2 = (p - 1) * (q2 - 1)

    for e in E_VALUES:
        # d2 = e^-1 mod(phi2)
        d2 = inverse(e, phi2)

        # p2 = c2^d2 mod(n2)
        p2 = pow(c2, d2, n2)

        p2_bytes = long_to_bytes(p2)

        try:
            pt2 = p2_bytes.decode()
            print('e: ', e)
            print('private key (int): ', p2)
            print('private key (plaintext): ', pt2)
            exit()
        except:
            pass


if __name__ == '__main__':
    print('Get the first public key and encrypted password and close the connection')
    print('Get the second public key and encrypted password and let open the connection to input the private key')

    n1 = _get_integer('Public key 1')
    c1 = _get_integer('Encrypted password 1')
    n2 = _get_integer('Public key 2')
    c2 = _get_integer('Encrypted password 2')

    if not _are_coprimes(n1, n2):
        _decrypt(n1, n2, c2)
    else:
        print('n1 and n2 are coprimes. Unable to decrypt message.')
        print('Try again')
