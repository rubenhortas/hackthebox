#!/usr/bin/env python3

import os
import shutil
from zipfile import ZipFile

from PIL import Image

INITIAL_FILE = 'M0rsarchive.zip'
INITIAL_PASSWORD = 'hackthebox'
TMP_NAME = 'tmp'
MORSE = {  # International morse code
    '.-': 'A',
    '-...': 'B',
    '-.-.': 'C',
    '-..': 'D',
    '.': 'E',
    '..-.': 'F',
    '--.': 'G',
    '....': 'H',
    '..': 'I',
    '.---': 'J',
    '-.-': 'K',
    '.-..': 'L',
    '--': 'M',
    '-.': 'N',
    '---': 'O',
    '.--.': 'P',
    '--.-': 'Q',
    '.-.': 'R',
    '...': 'S',
    '-': 'T',
    '..-': 'U',
    '...-': 'V',
    '.--': 'W',
    '-..-': 'X',
    '-.--': 'Y',
    '--..': 'Z',
    '.----': '1',
    '..---': '2',
    '...--': '3',
    '....-': '4',
    '.....': '5',
    '-....': '6',
    '--...': '7',
    '---..': '8',
    '----.': '9',
    '-----': '0',
    '........': 'ERROR',
    '.-...': '&',
    '.----.': '\'',
    '.--.-.': '@',
    '-.--.-': ')',
    '-.--.': '(',
    '---...': ':',
    '--..--': ',',
    '-...-': '=',
    '-.-.--': '!',
    '.-.-.-': '.',
    '-....-': '-',
    '.-.-.': '+',
    '.-..-.': '"',
    '..--..': '?',
    '-..-.': '/'
}


def _unzip(file: str, password: str, unzip_path: str) -> (str, str):
    try:
        file_name = os.path.basename(file).split('.')[0]
        print(f"[*] Unzipping '{file_name}'...")

        with ZipFile(file, 'r') as zobject:
            zipped_files = zobject.namelist()
            zobject.extractall(unzip_path, pwd=password.encode('UTF-8'))

        next_zip = None
        next_img = None

        for f in zipped_files:
            if '.zip' in f:
                next_zip = f
            elif '.png' in f:
                next_img = f

        return next_zip, next_img
    except Exception as e:
        print(f"[!] Unzipping {file}: {e}")
        exit(0)


def _extract(zip_file: str, password: str, unzip_path: str) -> None:
    is_last = False
    next_zip, next_img = _unzip(zip_file, password, unzip_path)

    while not is_last:
        if next_zip and next_img:
            password = _get_password(os.path.join(unzip_path, next_img))
            next_zip, next_img = _unzip(os.path.join(unzip_path, next_zip), password, unzip_path)
        else:
            is_last = True

    print('[*] Done')


def _get_password(file: str) -> str:
    try:
        image = Image.open(file)
        width, height = image.size
        rgb_image = image.convert('RGB')
        image_color = rgb_image.getpixel((0, 0))
        img_morse = []
        prev_has_image_color = True

        for y in range(height):
            morse_line = ''

            for x in range(width):
                if rgb_image.getpixel((x, y)) != image_color:
                    morse_line = morse_line + 'X'
                    prev_has_image_color = False
                else:
                    if not prev_has_image_color:
                        morse_line = morse_line + ' '

                    prev_has_image_color = True

            if morse_line != '':
                morse_line = morse_line.replace('XXX', '-')
                morse_line = morse_line.replace('X', '.')
                morse_line = morse_line.replace(' ', '')
                img_morse.append(morse_line)

        password = _decode_morse(img_morse)

        if password is None:
            print(f"Password not found for: {file}")
            exit(0)

        print(f"[*] Password: {password}")

        return password
    except Exception as e:
        print(f"[!] Reading image '{file}': {e}")
        exit(0)


def _decode_morse(morse: list) -> str:
    try:
        plain_text = ''

        for item in morse:
            plain_text = plain_text + MORSE[item]

        return plain_text.lower()
    except Exception as e:
        print(f"[!] Decoding morse: {e}")
        exit(0)


if __name__ == '__main__':
    base_path = os.getcwd()
    initial_file = os.path.join(base_path, INITIAL_FILE)
    tmp_path = os.path.join(base_path, TMP_NAME)

    if os.path.exists(tmp_path):
        shutil.rmtree(tmp_path)

    os.makedirs(tmp_path, exist_ok=True)

    _extract(initial_file, INITIAL_PASSWORD, os.path.join(tmp_path))
