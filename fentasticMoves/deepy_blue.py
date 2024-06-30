#!/usr/bin/env python3

import re
import signal
import socket
import multiprocessing

from typing import Tuple
from stockfish import Stockfish, StockfishException

SERVER = ''
PORT = 0
ENCODING = 'UTF-8'
ANSI_ESCAPE_PATTERN = re.compile(r'\x1b\[\d*(;\d*;\d*)?m')
BOARD_ROW_PATTERN = re.compile(r'^\s{2}(.*)\s\d$')
# Path to the stockfish executable: https://stockfishchess.org/download/
STOCKFISH_PATH = ''


class Board:
    _COLUMNS = {
        'a': 0,
        'b': 1,
        'c': 2,
        'd': 3,
        'e': 4,
        'f': 5,
        'g': 6,
        'h': 7
    }
    _PIECES = {
        # b = bishop, k = king, n = knight, p = pawn, q = queen, r = rook
        # uppercase = white pieces, lowercase = black pieces
        '♗': 'B',  # White bishop
        '♔': 'K',  # White king
        '♘': 'N',  # White knight
        '♙': 'P',  # White pawn
        '♕': 'Q',  # White queen
        '♖': 'R',  # White rook
        '♝': 'b',  # Black bishop
        '♚': 'k',  # Black king
        '♞': 'n',  # Black knight
        '♟': 'p',  # Black pawn
        '♛': 'q',  # Black queen
        '♜': 'r'  # Black rook
    }

    def __init__(self, board: list):
        self._board = []

        for row in board:
            fen_row = []

            for box in row:
                if box == ' ':
                    fen_row.append(box)
                else:
                    if not self._PIECES.get(box):
                        print(f'[D] Piece not found: [{box}]')

                    fen_row.append(self._PIECES.get(box))

            self._board.append(fen_row)

    # Returns the representation in FEN notation
    def __repr__(self) -> str:
        fen_board = []

        # FEN notation starts from the 8th row (blacks)
        for row in self._board:
            fen_row = []
            empty_boxes = 0

            for box in row:
                if box == ' ':
                    empty_boxes = empty_boxes + 1
                else:
                    if empty_boxes > 0:
                        fen_row.append(str(empty_boxes))
                        empty_boxes = 0

                    fen_row.append(box)

            if empty_boxes > 0:
                fen_row.append(str(empty_boxes))

            fen_row.append('/')
            fen_board.extend(fen_row)

        piece_positions = ''.join(fen_board)[:-1]
        active_color = 'w'
        castling = self._get_castling()
        en_passant = '-'
        halfmove_clock = '0'
        fullmove_number = '1'

        return f"{piece_positions} {active_color} {castling} {en_passant} {halfmove_clock} {fullmove_number}"

    def _get_castling(self) -> str:
        # FEN for the starting position; rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
        # https://chess.stackexchange.com/questions/1482/how-do-you-know-when-a-fen-position-is-legal
        # "If the king or rooks are not in their starting position; the castling ability for that side is lost (in the case of king, both are lost)."
        def get_color_castling(row: int, king: str, queen: str, rook: str) -> str:
            castling = ''

            if self._board[row][3] == king:
                castling = castling + king

                if self._board[row][0] == rook and self._board[row][7] == rook:
                    castling = castling + queen

        white_castling = get_color_castling(0, 'K', 'Q', 'R')
        black_castling = get_color_castling(7, 'k', 'q', 'r')

        if white_castling or black_castling:
            return f"{white_castling}{black_castling}".strip()
        else:
            return '-'


def _handle_sigint(signal, frame):
    print('\n[*] Stopped')
    exit(0)


def _read_info(data: list[bytes]) -> Tuple[list, str]:
    board = []

    for line in data:
        utf8_line = line.decode(ENCODING)
        utf8_line = ANSI_ESCAPE_PATTERN.sub('', utf8_line)  # Remove ANSI escape codes

        board_row_match = re.match(BOARD_ROW_PATTERN, utf8_line)

        if board_row_match:
            row = board_row_match.group(1)
            # On the board each square occupies two characters
            # Make each box occupy a single character by eliminating whitespaces
            row = row.replace('  ', '$')
            row = row.replace(' ', '')
            row = row.replace('$', ' ')

            board.append(row)

    return board


def _find_best_move(fen: str) -> str:
    try:
        if stockfish.is_fen_valid(fen):
            stockfish.set_fen_position(fen)
        else:
            print(f"[!]: Invalid fen: {fen}")

        return stockfish.get_best_move()
    except StockfishException:
        print('[!] Stockfish process has crashed')
        exit(-1)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, _handle_sigint)
    threads = multiprocessing.cpu_count()

    try:
        stockfish = Stockfish(STOCKFISH_PATH, depth=20)
    except StockfishException:
        print('[!] Stockfish process hash crashed')
        exit(-1)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print(f"[+] Connecting to {SERVER}:{PORT}...")

        try:
            s.connect((SERVER, PORT))
        except socket.error:
            print('[!] Could not connect to server.')
            exit(-1)

        puzzle_num = 1

        while True:
            buffer = b''

            while b'What\'s the best move?' not in buffer:
                buffer += s.recv(1024)

            # print(buffer.decode(ENCODING))  # Print all the data sent from server

            parsed_data = buffer.split(b'\n')
            remote_board = _read_info(parsed_data)
            # print(remote_board)
            local_board = Board(remote_board)

            best_move = _find_best_move(str(local_board))
            # print(f"[+] << {best_move}")
            best_move_line = best_move + '\n'
            s.sendall(bytes(best_move_line.encode(ENCODING)))

            result = s.recv(1024)

            if b'Wrong!' in result or b'Correct!' in result:
                print(f"[+] Puzzle {puzzle_num}: {result.decode(ENCODING)}", end='')
            else:
                print(f"[+] {result.decode(ENCODING)}", end='')

            if b'Wrong!' in result or b'Bye!' in result or b'flag' in result or b'slow' in result:
                exit(0)

            puzzle_num += 1
