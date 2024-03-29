#!/usr/bin/env python3

"""
Script to solve the misc challenge "RLotto" from https://app.hackthebox.com
"""

from time import time
from random import seed, randint


def _generate_combination():
    combination = []

    while len(combination) < 5:
        number = randint(1, 90)

        if number not in combination:
            combination.append(number)

    return combination


def _guess_next_numbers(start_time, lotto_numbers):
    time_seed = start_time
    combination = []

    while lotto_numbers != combination:
        # Go back in time until the second where the lotto combination was generated
        time_seed -= 1

        # Initialize the (pseudo) random number generator
        seed(time_seed)  # random seed

        combination = _generate_combination()

    next_combination = _generate_combination()

    print(next_combination)


if __name__ == '__main__':
    lotto_numbers = input('Lotto numbers: ')
    numbers = [int(n) for n in lotto_numbers.split()]

    if len(numbers) == 5:
        print('Guessing...')

        now = int(time())
        _guess_next_numbers(now, numbers)
