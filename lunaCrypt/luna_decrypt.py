#!/usr/bin/env python3

import math

strchr = lambda x: chr(x)
strbyt = lambda x, y=0: ord(x[y])
bitlst = lambda x, y: x << y
bitrst = lambda x, y: x >> y
bitext = lambda x, y, z=1: bitrst(x, y) & int(math.pow(2, z) - 1)
bitxor = lambda x, y: x ^ y
bitbor = lambda x, y: x | y
btest = lambda x, y: (x & y) != 0

FL_NEGATE = bitlst(1, 1)
FL_XORBY6B = bitlst(1, 3)
FL_XORBY3E = bitlst(1, 4)
FL_SWAPBYTES = bitlst(1, 6)


def DecryptCharacter(char, flag):
    char = ValidateChar(char)

    if CheckFlag(flag, FL_XORBY3E):
        char = XorBy3E(char)
    if CheckFlag(flag, FL_XORBY6B):
        char = XorBy6B(char)
    if CheckFlag(flag, FL_NEGATE):
        char = NegateChar(char)
    if CheckFlag(flag, FL_SWAPBYTES):
        char = InvertESwapChar(char)

    if type(char) is int:
        char = strchr(char)
    return char


def ValidateChar(char):
    if type(char) is str and len(char) == 1:
        char = strbyt(char)
    return char


def CheckFlag(f, flag):
    return btest(f, flag)


def XorBy6B(char):
    char = ValidateChar(char)

    return strchr(bitxor(char, 0x6B))


def XorBy3E(char):
    char = ValidateChar(char)

    return strchr(bitxor(char, 0x3E))


def NegateChar(char):
    char = ValidateChar(char)

    return strchr(255 - char)


def InvertESwapChar(ct):
    # Left side -> Revert (THIS_MSB xor 0x0D)
    pt_upper = ValidateChar(ct)

    # Convert 4 upper bits to 0 (Masking pt_upper)
    for i in range(4, 8):
        pt_upper = pt_upper & ~(1 << i)

    pt_upper = pt_upper ^ 0x0D
    pt_upper = pt_upper << 4

    # Right side -> Revert (bitlst(THIS_LSB, 4) xor 0xB0)
    pt_lower = ValidateChar(ct)

    # Convert 4 lower bits to 0 (Masking pt_lower)
    for i in range(4):
        pt_lower = pt_lower & ~(1 << i)

    pt_lower = pt_lower ^ 0xB0  # = bitlst
    pt_lower = pt_lower >> 4  # bitlst >> 4

    pt = pt_upper | pt_lower

    return chr(pt)


if __name__ == '__main__':
    plaintext = []
    flag = []

    with open('output.txt', 'rb') as f:
        ciphertext = f.read().strip().split()

    encrypted_chars = ciphertext[0::2]
    encrypted_flags = ciphertext[1::2]  # xored flags
    unxored_flags = list(map(lambda x: int(x) ^ 0x4A, encrypted_flags))

    for i in range(len(encrypted_chars)):
        pt_char = DecryptCharacter(int(encrypted_chars[i]), unxored_flags[i])
        plaintext.append(pt_char)

    print(''.join(plaintext))