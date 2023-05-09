import pygame
import numpy as np
import random
import sys

# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Define the window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Define the Tetris board dimensions
BOARD_WIDTH = 10
BOARD_HEIGHT = 24
BLOCK_SIZE = WINDOW_HEIGHT // BOARD_HEIGHT

# Initialize the game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Tetris Titans')

# Load the Tetrimino shapes and colors
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

# Define the Tetrimino class
class Tetrimino:
    def __init__(self, id):
        self.rotation = 0
        self.ref_point = np.array([0, BOARD_WIDTH // 2 - 1])
        self.id = id
        self.shape = TETRINOS.get(id, {}).get('shape')
        self.color = TETRINOS.get(id, {}).get('color')
        self.num_unique_rotations = TETRINOS.get(id, {}).get('num_rotations')
        self.dim = [self.shape.shape[0], self.shape.shape[1]]

    def reset(self):
        self.rotation = 0
        self.ref_point = np.array([0, BOARD_WIDTH // 2 - 1])

    def move(self, direction):
        self.ref_point += direction

    def rotate_right(self):
        self.shape = np.rot90(self.shape)
        self.dim = [self.shape.shape[0], self.shape.shape[1]]
        self.rotation = (self.rotation + 1) % self.num_unique_rotations
# Define the Tetris game class
class Tetris:
    def __init__(self):
        self.score = 0
        self.level = 0
        self.lines_cleared = 0
        self.playing = True
        self.can_store = True
        self.bag = list(range(1, 8))
        self.game_board = np.zeros(shape=(BOARD_HEIGHT, BOARD_WIDTH), dtype=int)
        self.active_piece = self._get_next_piece()
        self.next_piece = self._get_next_piece()

    def reset(self):
        self.score = 0
        self.level = 0
        self.lines_cleared = 0
        self.playing = True
        self.can_store = True
        self.bag = list(range(1, 8))
        self.game_board = np.zeros(shape=(BOARD_HEIGHT, BOARD_WIDTH), dtype=int)
        self.active_piece = self._get_next_piece()
        self.next_piece = self._get_next_piece()

    def _get_next_piece(self):
        if len(self.bag) == 0:
            self.bag = list(range(1, 8))
            random.shuffle(self.bag)
        piece_id = self.bag.pop(0)
        return Tetrimino(piece_id)

    # Other methods...

    def draw_game_board(self):
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                pygame.draw.rect(window, GRAY, (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                if self.game_board[row][col] != 0:
                    pygame.draw.rect(window, TETRINOS[self.game_board[row][col]]['color'],
                                     (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    def draw_active_piece(self):
        shape = self.active_piece.shape
        ref_point = self.active_piece.ref_point

        for row in range(shape.shape[0]):
            for col in range(shape.shape[1]):
                if shape[row][col] != 0:
                    pygame.draw.rect(window, self.active_piece.color,
                                     ((ref_point[1] + col) * BLOCK_SIZE, (ref_point[0] + row) * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE))

    def draw_next_piece(self):
        shape = self.next_piece.shape
        offset_x = BOARD_WIDTH * BLOCK_SIZE + BLOCK_SIZE * 2
        offset_y = BLOCK_SIZE * 4

        for row in range(shape.shape[0]):
            for col in range(shape.shape[1]):
                if shape[row][col] != 0:
                    pygame.draw.rect(window, self.next_piece.color,
                                     (offset_x + col * BLOCK_SIZE, offset_y + row * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE))

    def draw_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        level_text = font.render(f"Level: {self.level}", True, WHITE)
        lines_cleared_text = font.render(f"Lines Cleared: {self.lines_cleared}", True, WHITE)
        window.blit(score_text, (BLOCK_SIZE, BLOCK_SIZE))
        window.blit(level_text, (BLOCK_SIZE, BLOCK_SIZE * 2))
        window.blit(lines_cleared_text, (BLOCK_SIZE, BLOCK_SIZE * 3))

    def draw(self, window):
        # Clear the window
        window.fill(BLACK)

    # Draw the game board
        self.draw_game_board()

        # Draw the active piece
        self.draw_active_piece()

        # Draw the next piece
        self.draw_next_piece()

        # Draw the score
        self.draw_score()

        # Update the display
        pygame.display.flip()

    def run_game(self):
        pygame.init()
        clock = pygame.time.Clock()

        # Set up the game window
        window_width = BOARD_WIDTH * BLOCK_SIZE + BLOCK_SIZE * 3
        window_height = BOARD_HEIGHT * BLOCK_SIZE
        window_size = (window_width, window_height)
        window = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Tetris")

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.move_left()
                    elif event.key == pygame.K_RIGHT:
                        self.move_right()
                    elif event.key == pygame.K_DOWN:
                        self.drop_piece()
                    elif event.key == pygame.K_UP:
                        self.rotate_piece()
                    elif event.key == pygame.K_SPACE:
                        self.store_piece()

            # Update the game state
        self.update()

            # Draw the game
        self.draw(window)

            # Limit the frame rate
        clock.tick(FPS)


# Create an instance of the Tetris game
tetris_game = Tetris()

# Run the game
tetris_game.run_game()