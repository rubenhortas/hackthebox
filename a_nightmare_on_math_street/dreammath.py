#!/usr/bin/env pyhon3

"""
Script to solve the misc challenge "A nightmare on math street" from https://app.hackthebox.com
"""

import re
import socket

SERVER = ''
PORT = 0
QUESTION_PATTERN = re.compile(r'\[\d+]:.*= \?')
PRECEDENCES = {  # Dream math precedences
    '**': 3,
    '+': 2,
    '/': 2,
    '*': 1,
    '-': 1,
}


def _get_question(data: str) -> str:
    match = QUESTION_PATTERN.search(data)

    if not match:
        print('[!] Question not found')
        exit(0)

    return match.group(0)


def _get_expression(question: str) -> list:
    return question.replace('(', '( ').replace(')', ' )').split()[1:-2]


def _get_rpn(expression: list) -> list:
    output_queue = []
    operator_stack = []

    for token in expression:
        if token == ' ':
            continue
        elif token in PRECEDENCES:
            while (operator_stack and operator_stack[-1] in PRECEDENCES and
                   PRECEDENCES[token] <= PRECEDENCES[operator_stack[-1]]):
                output_queue.append(operator_stack.pop())
            operator_stack.append(token)
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            while operator_stack and operator_stack[-1] != '(':
                output_queue.append(operator_stack.pop())
            operator_stack.pop()
        else:
            output_queue.append(int(token))

    while operator_stack:
        output_queue.append(operator_stack.pop())

    return output_queue


def _convert_rpn_to_infix(expression: list) -> str:
    output_queue = []

    for token in expression:
        if token in PRECEDENCES:
            b = output_queue.pop()
            a = output_queue.pop()
            output_queue.append(f"({a}{token}{b})")
        else:
            output_queue.append(token)

    return output_queue[0]


if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER, PORT))

        while True:
            data = s.recv(1024)
            utf8_data = data.decode('UTF-8')
            print(utf8_data)

            if data == b'\x1b[31mWrong Answer... Learn your math!\n\n':
                exit(0)

            question = _get_question(utf8_data)
            expression = _get_expression(question)
            rpn = _get_rpn(expression)
            infix = _convert_rpn_to_infix(rpn)
            result = eval(infix)
            print(f"<< {result}")

            str_result = str(result) + "\n"
            s.sendall(bytes(str_result.encode('UTF-8')))
