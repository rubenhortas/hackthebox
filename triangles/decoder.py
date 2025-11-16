#!/usr/bin/env python3

import csv
import math

from typing import Tuple

OUT_FILE = 'out.csv'
COORDINATE_MATRIX_FILE = 'grid.csv'


class Coordinate:
    def __init__(self, num, distances):
        self.num = num  # Coordinate position. Just an ordinal to keep track of the position in the flag.
        self.val1 = distances[0][0]
        self.distance_xy_p1 = float(distances[0][1])
        self.val2 = distances[1][0]
        self.distance_xy_p2 = float(distances[1][1])
        self.val3 = distances[2][0]
        self.distance_xy_p3 = float(distances[2][1])
        self.distance_p1_p2 = float(distances[3][1])
        self.distance_p2_p3 = float(distances[4][1])
        self.distance_p1_p3 = float(distances[5][1])
        self.distances = distances

    def __str__(self):
        info = [f"[*] Coordinate {self.num}:\n", f"[*] \tval1: {self.val1}\n",
                f"[*] \tdistance_xy_p1: {self.distance_xy_p1}\n", f"[*] \tval2: {self.val2}\n",
                f"[*] \tdistance_xy_p2: {self.distance_xy_p2}\n", f"[*] \tval3: {self.val3}\n",
                f"[*] \tdistance_xy_p3: {self.distance_xy_p3}\n", f"[*] \tdistance_p1_p2: {self.distance_p1_p2}\n",
                f"[*] \tdistance_p2_p3: {self.distance_p2_p3}\n", f"[*] \tdistance_p1_p3: {self.distance_p1_p3}\n"
                                                                  f"[*] \traw values: {self.distances}\n"]
        return ''.join(info)


def _get_coordinate_matrix() -> list:
    """
    Reads the coordinate matrix from the csv file.
    :return: 100x100 coordinate matrix.
    """
    matrix = []

    with open(COORDINATE_MATRIX_FILE) as f:
        for line in csv.reader(f):
            matrix.append(line)

    return matrix


# noinspection PyShadowingNames
def _get_grid_positions(grid: list, val1: list, val2: list, val3: list) -> Tuple[list, list, list]:
    """
    Gets all the positions of certain values in the grid.
    """
    val1_positions = []
    val2_positions = []
    val3_positions = []

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == val1:
                val1_positions.append((i, j))
            if grid[i][j] == val2:
                val2_positions.append((i, j))
            if grid[i][j] == val3:
                val3_positions.append((i, j))

    return val1_positions, val2_positions, val3_positions


def _get_distance(x: float, y: float, x2: float, y2: float) -> float:
    """
    Calculates the Euclidean distance between two points in a 2D space.
    This distance is the straight line distance between the points (x, y) and (x2, y2).
    """
    return math.sqrt(math.pow(x - x2, 2) + math.pow(y - y2, 2))


def _get_matching_distance_points(p1_list: list, p2_list: list, distance: float) -> Tuple[list, list]:
    """
    Gets all the points (from two point lists) that matches a certain distance.
    :return:
    list(p1_matching): List of points from p1_list that matches the distance.
    list(p2_matching): List of points from p2_list that matches the distance.
    """
    p1_matching = set()
    p2_matching = set()

    for p1 in p1_list:
        for p2 in p2_list:
            distance_p1p2 = _get_distance(p1[0], p1[1], p2[0], p2[1])

            if distance_p1p2 == distance:
                p1_matching.add(p1)
                p2_matching.add(p2)

    return list(p1_matching), list(p2_matching)


def _get_cap_points(p1_positions: list, p2_positions: list, p3_positions: list, distance_p1_p2: float,
                    distance_p2_p3: float, distance_p1_p3: float) -> Tuple[list, list, list]:
    """
    Gets the points that matches the distance between p1 and p2.
    """
    p1_candidates, p2_candidates = _get_matching_distance_points(p1_positions, p2_positions, distance_p1_p2)
    p1_candidates, p3_candidates = _get_matching_distance_points(p1_candidates, p3_positions, distance_p1_p3)
    p2_candidates, p3_candidates = _get_matching_distance_points(p2_candidates, p3_candidates, distance_p2_p3)

    return p1_candidates, p2_candidates, p3_candidates


# noinspection PyShadowingNames
def _uncap(num: int) -> list:
    """
    Undoes the cap() function operations.
    """
    result = []

    for i in range(-7, 8):  # [-7,7]
        p = num + i

        if p <= 0:
            if 0 not in result:
                result.append(0)
        elif p >= 99:
            if 99 not in result:
                result.append(99)
        else:
            result.append(p)

    return result


# noinspection PyShadowingNames
def _get_uncapped_candidates(points: list) -> list:
    """
    Gets the original points candidates.
    """
    candidates = set()

    for p in points:
        uncapped_x = _uncap(p[0])
        uncapped_y = _uncap(p[1])

        for x in uncapped_x:
            for y in uncapped_y:
                candidates.add((x, y))

    return list(candidates)


# noinspection PyShadowingNames
def _get_point(p1: list, p2: list, p3: list, distance_xy_p1: float, distance_xy_p2: float,
               distance_xy_p3: float) -> list:
    p = []

    p1_candidates = _get_uncapped_candidates(p1)
    p2_candidates = _get_uncapped_candidates(p2)
    p3_candidates = _get_uncapped_candidates(p3)

    p1_candidates, _ = _get_matching_distance_points(p1_candidates, p1, distance_xy_p1)
    p2_candidates, _ = _get_matching_distance_points(p2_candidates, p2, distance_xy_p2)
    p3_candidates, _ = _get_matching_distance_points(p3_candidates, p3, distance_xy_p3)

    for candidate in p1_candidates:
        if candidate in p2_candidates:
            if candidate in p3_candidates:
                p.append(candidate)

    if len(p) == 1:  # Only one point found
        return p[0]
    else:  # zero or many points found
        return p  # []


# noinspection PyShadowingNames
def _get_original_point(coordinate: Coordinate, coordinate_matrix: list) -> list:
    # Find all possible "capped" point positions
    val1_positions, val2_positions, val3_positions = _get_grid_positions(coordinate_matrix, coordinate.val1,
                                                                         coordinate.val2, coordinate.val3)
    # Find the "capped" points
    p1, p2, p3 = _get_cap_points(val1_positions, val2_positions, val3_positions, coordinate.distance_p1_p2,
                                 coordinate.distance_p2_p3, coordinate.distance_p1_p3)

    # Find the original points
    return _get_point(p1, p2, p3, coordinate.distance_xy_p1, coordinate.distance_xy_p2, coordinate.distance_xy_p3)


# noinspection PyShadowingNames
def _get_flag(coordinates: list) -> str:
    flag = []

    for p in coordinates:
        if p:
            flag.append(coordinate_matrix[p[0]][p[1]])
        else:
            flag.append('?')

    return ''.join(flag)


# noinspection PyShadowingNames
def _get_coordinates() -> list:
    """
    Gets the encrypted coordinates info.
    """
    coordinates = []

    # The information of each coordinate takes six lines
    with open(OUT_FILE) as f:
        lines = f.read().splitlines()
        num_coordinates = len(lines) // 6

    for i in range(1, num_coordinates + 1):
        coordinate_values = []

        for j in range(6, 0, -1):
            coordinate_values.append((lines[(i * 6) - j]).split(','))

        coordinate = Coordinate(i, coordinate_values)
        coordinates.append(coordinate)

    return coordinates


if __name__ == '__main__':
    print('[*] Decoding...')
    coordinate_matrix = _get_coordinate_matrix()  # 100x100 grid
    coordinates = _get_coordinates()
    flag_coordinates = []

    for coordinate in coordinates:
        p = _get_original_point(coordinate, coordinate_matrix)
        flag_coordinates.append(p)

    flag = _get_flag(flag_coordinates)
    print(f"[!] Flag: {flag}")
