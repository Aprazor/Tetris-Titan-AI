import numpy as np
import random
import copy

class Tetrino:
    TETRINOS = {
        1: {
            'shape': np.array([[1, 1], [1, 1]]),
            'color': (0, 255, 255),
            'num_rotations': 1
        },  # O
        2: {
            'shape': np.array([[0, 0, 0, 0], [2, 2, 2, 2]]),
            'color': (255, 255, 0),
            'num_rotations': 2
        },  # I
        3: {
            'shape': np.array([[3, 3, 0], [0, 3, 3]]),
            'color': (0, 0, 255),
            'num_rotations': 2
        },  # Z
        4: {
            'shape': np.array([[0, 4, 4], [4, 4, 0]]),
            'color': (0, 255, 0),
            'num_rotations': 2
        },  # S
        5: {
            'shape': np.array([[0, 0, 5], [5, 5, 5]]),
            'color': (0, 127, 255),
            'num_rotations': 4
        },  # L
        6: {
            'shape': np.array([[6, 0, 0], [6, 6, 6]]),
            'color': (255, 0, 0),
            'num_rotations': 4
        },  # J
        7: {
            'shape': np.array([[0, 7, 0], [7, 7, 7]]),
            'color': (255, 0, 255),
            'num_rotations': 4
        }  # T
    }

    def __init__(self, id):
        self.rotation = 0
        self.ref_point = np.array([0, 3])
        self.id = id
        self.shape = self.TETRINOS.get(id, {}).get('shape')
        self.color = self.TETRINOS.get(id, {}).get('color')
        self.num_unique_rotations = self.TETRINOS.get(id, {}).get('num_rotations')
        self.dim = [self.shape.shape[0], self.shape.shape[1]]

    def reset(self):
        self.rotation = 0
        self.ref_point = np.array([0, 3])

    def move(self, direction):
        self.ref_point += direction

    def rotate_right(self):
        self.shape = np.rot90(self.shape)
        self.dim = [self.shape.shape[0], self.shape.shape[1]]
        self.rotation = (self.rotation + 1) % self.num_unique_rotations


class Tetris:
    BOARD_DIMS = (24, 10)

    def __init__(self):
        self.score = 0
        self.level = 0
        self.lines_cleared = 0
        self.playing = True
        self.can_store = True
        self.bag = list(range(1, 8))
        self.game_board = np.zeros(shape=self.BOARD_DIMS, dtype=int)
        self.active_piece = self._get_next_piece()
        self.next_piece = self._get_next_piece()

    def reset(self):
        self.score = 0
        self.level = 0
        self.lines_cleared = 0
        self.playing = True
        self.can_store = True
        self.bag = list(range(1, 8))
        self.game_board = np.zeros(shape=self.BOARD_DIMS, dtype=int)
        self.active_piece = self._get_next_piece()
        self.next_piece = self._get_next_piece()

    def _get_next_piece(self):
        if len(self.bag) == 0:
            self.bag = list(range(1, 8))
            random.shuffle(self.bag)
        piece_id = self.bag.pop(0)
        return Tetrino(piece_id)

    def _is_valid_position(self, piece):
        shape = piece.shape
        ref_point = piece.ref_point

        # Check if piece is inside the game board
        if (
            ref_point[0] < 0
            or ref_point[0] + piece.dim[0] > self.BOARD_DIMS[0]
            or ref_point[1] < 0
            or ref_point[1] + piece.dim[1] > self.BOARD_DIMS[1]
        ):
            return False

        # Check if piece collides with existing blocks on the board
        for row in range(shape.shape[0]):
            for col in range(shape.shape[1]):
                if shape[row][col] != 0 and self.game_board[ref_point[0] + row][ref_point[1] + col] != 0:
                    return False
        return True

    def _place_piece(self, piece):
        shape = piece.shape
        ref_point = piece.ref_point

        for row in range(shape.shape[0]):
            for col in range(shape.shape[1]):
                if shape[row][col] != 0:
                    self.game_board[ref_point[0] + row][ref_point[1] + col] = shape[row][col]

    def _check_lines(self):
        lines_to_clear = []

        for row in range(self.BOARD_DIMS[0]):
            if np.all(self.game_board[row, :] != 0):
                lines_to_clear.append(row)

        lines_cleared = len(lines_to_clear)
        self.score += 100 * lines_cleared
        self.lines_cleared += lines_cleared

        # Increase level every 10 lines cleared
        self.level = self.lines_cleared // 10

        # Clear lines
        for line in lines_to_clear:
            self.game_board[1:line+1, :] = self.game_board[:line, :]

        return lines_cleared

    def _is_game_over(self):
        return np.any(self.game_board[0, :] != 0)

    def _update(self):
        # Move active piece down
        self.active_piece.move((1, 0))

        if not self._is_valid_position(self.active_piece):
            # Undo last move if position is invalid
            self.active_piece.move((-1, 0))

            # Place piece on the board
            self._place_piece(self.active_piece)

            # Check for cleared lines
            lines_cleared = self._check_lines()

            # Update score and level based on cleared lines
            self.score += (lines_cleared ** 2) * 10
            self.level = self.lines_cleared // 10

            # Check if the game is over
            if self._is_game_over():
                self.playing = False
            else:
                # Get next piece
                self.active_piece = self.next_piece
                self.next_piece = self._get_next_piece()

    def move_left(self):
        self.active_piece.move((0, -1))
        if not self._is_valid_position(self.active_piece):
            self.active_piece.move((0, 1))

    def move_right(self):
        self.active_piece.move((0, 1))
        if not self._is_valid_position(self.active_piece):
            self.active_piece.move((0, -1))

    def rotate_piece(self):
        self.active_piece.rotate_right()
        if not self._is_valid_position(self.active_piece):
            self.active_piece.rotate_right()
            self.active_piece.rotate_right()
            self.active_piece.rotate_right()

    def drop_piece(self):
        while self._is_valid_position(self.active_piece):
            self.active_piece.move((1, 0))
        self.active_piece.move((-1, 0))
        self._update()

    def get_game_board(self):
        return copy.deepcopy(self.game_board)

    def get_active_piece_shape(self):
        return copy.deepcopy(self.active_piece.shape)

    def get_next_piece_shape(self):
        return copy.deepcopy(self.next_piece.shape)

    def get_score(self):
        return self.score

    def get_level(self):
        return self.level

    def is_playing(self):
        return self.playing

    def can_store_piece(self):
        return self.can_store

    def store_piece(self):
        if self.can_store:
            self.can_store = False
            stored_piece = self.active_piece
            stored_piece.reset()
            self.active_piece = self.next_piece
            self.next_piece = stored_piece

    def update(self):
        if self.playing:
            self._update()
   

