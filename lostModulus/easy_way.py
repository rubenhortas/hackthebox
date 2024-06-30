#!/usr/bin/env python3

"""
Script to solve the crypto challenge "LostModulus" from https://app.hackthebox.com
"""

# Requires pycryptodome
from Crypto.Util.number import getPrime, long_to_bytes, inverse


class RSA:
    def __init__(self):
        self.p = getPrime(512)  # 512 bits length
        self.q = getPrime(512)
        self.e = 3  # public exponent
        self.n = self.p * self.q  # modulus (Public by construction)
        self.phi = (self.p - 1) * (self.q - 1)
        self.d = inverse(self.e, self.phi)  # private exponent

    def encrypt(self, data: bytes) -> bytes:
        pt = int(data.hex(), 16)  # plaintext
        ct = pow(pt, self.e, self.n)  # ciphertext

        return long_to_bytes(ct)

    def decrypt(self, data: bytes) -> bytes:
        ct = int(data.hex(), 16)  # ciphertext
        pt = pow(ct, self.d, self.n)  # plaintext

        return long_to_bytes(pt)


def decrypt_flag(crypto):
    flag = open('flag.txt', 'r').read().strip().encode()
    encrypted_flag_hex = flag.decode()
    encrypted_flag_bytes = bytes.fromhex(encrypted_flag_hex)
    decrypted_flag_bytes = b''

    while b'HTB{' not in decrypted_flag_bytes:
        decrypted_flag_bytes = crypto.decrypt(encrypted_flag_bytes)

    print('Decrypted flag bytes: ', decrypted_flag_bytes)


if __name__ == '__main__':
    crypto = RSA()
    decrypt_flag(crypto)
