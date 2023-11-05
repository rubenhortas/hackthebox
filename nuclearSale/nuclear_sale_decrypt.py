#!/usr/bin/env python3

"""
Script to solve the crypto challenge "Nuclear Sale" from https://app.hackthebox.com
"""

# Mail ciphertexts are hex strings of the same length

# He is a high profile individual. His information is encrypted below -> pt ^ k
CT1_HEX = '6b65813f4fe991efe2042f79988a3b2f2559d358e55f2fa373e53b1965b5bb2b175cf039'

# Here is the ciphertext encrypted with our key -> pt ^ k ^ k1
CT2_HEX = 'fd034c32294bfa6ab44a28892e75c4f24d8e71b41cfb9a81a634b90e6238443a813a3d34'

# Encrypting again with our key... -> pt ^ k1
CT3_HEX = 'de328f76159108f7653a5883decb8dec06b0fd9bc8d0dd7dade1f04836b8a07da20bfe70'

if __name__ == '__main__':
    # CT1_HEX = pt ^ k
    # CT2_HEX = pt ^ k ^ k1
    # CT3_HEX = pt ^ k1

    #   CT1_HEX ^ CT2_HEX =
    # = pt ^ k ^ pt ^ k ^ k1 =
    # = ((pt ^ k ) ^ (pt ^ k)) ^ k1 =
    # = 0 ^ k1 =
    # = k1

    #   CT1_HEX ^ CT2_HEX ^ CT3_HEX =
    # = (CT1_HEX ^ CT2_HEX) ^ CT3_HEX =
    # = k1 ^ CT3_HEX =
    # = k1 ^ pt ^ k1 =
    # = (k1 ^ k1) ^ pt =
    # = 0 ^ pt =
    # = pt
    ct1_bytes = bytes.fromhex(CT1_HEX)
    ct2_bytes = bytes.fromhex(CT2_HEX)
    ct3_bytes = bytes.fromhex(CT3_HEX)
    pt_list = []

    for i in range(0, len(ct1_bytes)):
        pt_list.append(ct1_bytes[i] ^ ct2_bytes[i] ^ ct3_bytes[i])

    pt_bytes = bytes(pt_list)
    pt = pt_bytes.decode()
    print(pt)
