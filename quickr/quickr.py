#!/usr/bin/env python3

# This script needs its own venv because issues with python3-opencv library.
# To create the venv:   $ python -m venv /path/to/quickr
# To activate the venv: $ source /path/to/quickr/bin/activate
# To install opencv:    $ pip3 install opencv-python
# To install pillow:    $ pip3 install pillow

import re
import cv2

from socket import socket, AF_INET, SOCK_STREAM
from PIL import Image

SERVER = ''
PORT = 0
ENCODING = 'UTF-8'
QR_BG_COLOR = bytes('(255, 255, 255)', ENCODING)  # White
QR_FG_COLOR = bytes('(0, 0, 0)', ENCODING)  # Black
QR_IMAGE = 'qr.png'
RGB_PATTERN = re.compile(bytes(r'\(\d*, \d*, \d*\)', ENCODING))


def _read_data() -> list:
    with open('response.txt', 'r') as output:
        return output.readlines()


def _get_qr(lines: list) -> list:
    qr = []

    for line in lines:
        if line and len(line) > 1 and line[0] == 9:  # 9 is \t in this context
            qr.append(line)

    return qr


def _generate_qr_image(console_qr: list) -> None:
    # If the qr image exists it will be overwritten
    image_qr_pixels = []

    for line in console_qr:
        # Convert QR byte color to black (QR_FG_COLOR) and white (QR_BG_COLOR) byte colors
        image_qr_line = line
        image_qr_line = re.sub(b'\\t', b'', image_qr_line)
        image_qr_line = re.sub(b'\\x1b\\[7m {2}\\x1b\\[0m', QR_BG_COLOR, image_qr_line)
        image_qr_line = re.sub(b'\\x1b\\[41m {2}\\x1b\\[0m', QR_FG_COLOR, image_qr_line)

        # Get the byte colors of the line as list
        image_qr_line_pixels = re.findall(RGB_PATTERN, image_qr_line)

        # Convert all the byte colors to string colors and store them
        image_qr_pixels.extend(list(map(eval, image_qr_line_pixels)))  # eval to convert from bytes to tuple directly

    image_size = len(console_qr)  # Same width as height
    image = Image.new('RGB', (image_size, image_size))
    image.putdata(image_qr_pixels)
    image.save(QR_IMAGE)


def _get_qr_equation() -> str:
    image = cv2.imread(QR_IMAGE)
    qr_code_detector = cv2.QRCodeDetector()
    data, bbox, straight_qrcode = qr_code_detector.detectAndDecode(image)

    equation = re.sub('=', '', data)
    equation = re.sub(' ', '', equation)
    equation = re.sub('x', '*', equation)

    return equation


if __name__ == '__main__':
    with socket(AF_INET, SOCK_STREAM) as s:
        s.connect((SERVER, PORT))
        data = b''

        while b'Decoded string:' not in data:
            data = data + s.recv(1024)

        qr_data = _get_qr(data.splitlines())
        _generate_qr_image(qr_data)
        equation = _get_qr_equation()
        result = f'{eval(equation)}\n'
        s.send(bytes(result.encode(ENCODING)))
        print(f"[<] {result}", end='')

        response = s.recv(1024)
        response = re.sub(b'\\x1b\\[1m\\x1b\\[92m', b'', response)
        response = re.sub(b'\\x1b\\[0m', b'', response)
        response = response.decode(ENCODING)
        response = f'[>] {response}'
        print(response, end='')

        s.close()
        exit(0)

