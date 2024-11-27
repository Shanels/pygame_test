import pygame
import random

pygame.init()

WIDTH, HEIGHT = 300, 600
GRID_SIZE = 30
COLUMNS, ROWS = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
COLORS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (0, 255, 255),
    (255, 0, 255),
    (128, 0, 128),
]

SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
]

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.grid = [[0] * COLUMNS for _ in range(ROWS)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.game_over = False
        self.score = 0

    def new_piece(self):
        shape = random.choice(SHAPES)
        color = random.choice(COLORS)
        return {"shape": shape, "color": color, "x": COLUMNS // 2 - len(shape[0]) // 2, "y": 0}

    def rotate_piece(self):
        original_shape = self.current_piece["shape"]
        rotated_shape = [
            [original_shape[y][x] for y in range(len(original_shape))][::-1]
            for x in range(len(original_shape[0]))
        ]
        original_x = self.current_piece["x"]
        self.current_piece["shape"] = rotated_shape
        if self.can_move(0, 0):
            return
        for dx in range(-len(rotated_shape[0]), len(rotated_shape[0]) + 1):
            self.current_piece["x"] = original_x + dx
            if self.can_move(0, 0):
                return
        self.current_piece["shape"] = original_shape
        self.current_piece["x"] = original_x

    def can_move(self, dx, dy):
        shape = self.current_piece["shape"]
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.current_piece["x"] + x + dx
                    new_y = self.current_piece["y"] + y + dy
                    if new_x < 0 or new_x >= COLUMNS or new_y >= ROWS or (new_y >= 0 and self.grid[new_y][new_x]):
                        return False
        return True

    def merge_piece(self):
        shape = self.current_piece["shape"]
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current_piece["y"] + y][self.current_piece["x"] + x] = self.current_piece["color"]

    def clear_lines(self):
        new_grid = [row for row in self.grid if any(cell == 0 for cell in row)]
        cleared_lines = ROWS - len(new_grid)
        self.score += cleared_lines
        self.grid = [[0] * COLUMNS for _ in range(cleared_lines)] + new_grid

    def draw_grid(self):
        for y in range(ROWS):
            for x in range(COLUMNS):
                if self.grid[y][x] != 0:
                    rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                    pygame.draw.rect(self.screen, self.grid[y][x], rect)
                    pygame.draw.rect(self.screen, GRAY, rect, 1)

    def draw_piece(self, piece):
        shape = piece["shape"]
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect((piece["x"] + x) * GRID_SIZE, (piece["y"] + y) * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                    pygame.draw.rect(self.screen, piece["color"], rect)
                    pygame.draw.rect(self.screen, GRAY, rect, 1)

    def draw_background_grid(self):
        for y in range(ROWS):
            for x in range(COLUMNS):
                rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(self.screen, GRAY, rect, 1)

    def run(self):
        while not self.game_over:
            self.screen.fill(BLACK)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and self.can_move(-1, 0):
                        self.current_piece["x"] -= 1
                    elif event.key == pygame.K_RIGHT and self.can_move(1, 0):
                        self.current_piece["x"] += 1
                    elif event.key == pygame.K_DOWN and self.can_move(0, 1):
                        self.current_piece["y"] += 1
                    elif event.key == pygame.K_UP:
                        self.rotate_piece()
            if self.can_move(0, 1):
                self.current_piece["y"] += 1
            else:
                self.merge_piece()
                self.clear_lines()
                self.current_piece = self.next_piece
                self.next_piece = self.new_piece()
                if not self.can_move(0, 0):
                    self.game_over = True
            self.draw_background_grid()
            self.draw_grid()
            self.draw_piece(self.current_piece)
            pygame.display.flip()
            self.clock.tick(7)
        pygame.quit()

if __name__ == "__main__":
    Tetris().run()
