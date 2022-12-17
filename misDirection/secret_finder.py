# /!/usr/bin/env python3
import os
import base64

if __name__ == '__main__':
    base_dir = "secret"
    dictionary_tmp = {}
    b64secret = ""

    for d in os.listdir(base_dir):
        files = os.listdir(os.path.join(base_dir, d))

        # We create a dictionary for the not empty subfolders
        if files:
            for f in files:
                # The key will be the position and the value will be the character
                dictionary_tmp[f"{int(f):02}"] = d

    # As the dictionary key are the positions on the flag string we will sort the dictionary entries by key
    sorted_dictionary = sorted(dictionary_tmp.items())

    # Once the dictionary is sorted we will iterate the dictionary
    # We will store the dictionary values on the flag string
    for key, value in sorted_dictionary:
        b64secret = b64secret + value

    # The result flag is encoded in base64, so we will decode it
    secret = base64.b64decode(b64secret)

    print(f"flag: {str(secret.decode())}")
