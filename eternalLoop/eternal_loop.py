#!/usr/bin/env python3

"""
Script to solve the misc challenge "Eternal Loop" from https://app.hackthebox.com

You can read the full walkthrough here: https://rubenhortas.github.io/posts/htb-eternal-loop
"""

import os

from zipfile import ZipFile


def _unzip(counter, f, files):
    print(f"{counter} {f}")

    zf = ZipFile(f)
    zf_inner = zf.namelist()[0]

    if zf_inner != '':
        if zf_inner.endswith('.zip'):
            files.append(f)
            zf_password = zf_inner.split('.')[0]

            print(f"\tpassword: {zf_password}")
            print(f"\tinner zip: {zf_inner}")

            zf.extractall(pwd=bytes(zf_password, 'UTF-8'))

            counter = counter + 1
            _unzip(counter, str(zf_inner), files)
        else:
            print(f"\tinner file: {zf_inner}")
            print(f"total files: {counter}")


def _delete(files):
    for f in files:
        os.remove(f)


if __name__ == '__main__':
    zip_files = []
    _unzip(1, '37366.zip', zip_files)
    _delete(zip_files)
