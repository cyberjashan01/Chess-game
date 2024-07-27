import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load images
def load_images():
    pieces = ['bB', 'bK', 'bN', 'bP', 'bQ', 'bR', 'wB', 'wK', 'wN', 'wP', 'wQ', 'wR']
    images = {}
    for piece in pieces:
        images[piece] = pygame.transform.scale(pygame.image.load(f'images/{piece}.jpg'), (SQUARE_SIZE, SQUARE_SIZE))
    return images

# Draw the chessboard
def draw_board(win):
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for r in range(ROWS):
        for c in range(COLS):
            color = colors[(r+c) % 2]
            pygame.draw.rect(win, color, pygame.Rect(c*SQUARE_SIZE, r*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Draw pieces on the board
def draw_pieces(win, board, images):
    for r in range(ROWS):
        for c in range(COLS):
            piece = board[r][c]
            if piece != "--":
                win.blit(images[piece], (c*SQUARE_SIZE, r*SQUARE_SIZE))

# Get row and col from mouse position
def get_square_under_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

# Validate moves for each piece type
def is_valid_move(board, start_pos, end_pos, turn):
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    piece = board[start_row][start_col]
    target = board[end_row][end_col]

    if piece == "--" or piece[0] != turn:
        return False

    if target != "--" and target[0] == turn:
        return False

    piece_type = piece[1]

    if piece_type == 'P':
        direction = -1 if turn == 'w' else 1
        start_row_for_pawn = 6 if turn == 'w' else 1
        if start_col == end_col and target == "--":
            if end_row == start_row + direction:
                return True
            if start_row == start_row_for_pawn and end_row == start_row + 2 * direction and board[start_row + direction][start_col] == "--":
                return True
        if abs(start_col - end_col) == 1 and end_row == start_row + direction and target != "--":
            return True

    elif piece_type == 'R':
        if start_row == end_row or start_col == end_col:
            if is_clear_path(board, start_pos, end_pos):
                return True

    elif piece_type == 'N':
        if (abs(start_row - end_row), abs(start_col - end_col)) in [(2, 1), (1, 2)]:
            return True

    elif piece_type == 'B':
        if abs(start_row - end_row) == abs(start_col - end_col):
            if is_clear_path(board, start_pos, end_pos):
                return True

    elif piece_type == 'Q':
        if start_row == end_row or start_col == end_col or abs(start_row - end_row) == abs(start_col - end_col):
            if is_clear_path(board, start_pos, end_pos):
                return True

    elif piece_type == 'K':
        if abs(start_row - end_row) <= 1 and abs(start_col - end_col) <= 1:
            return True

    return False

# Check if the path is clear for rook, bishop, and queen moves
def is_clear_path(board, start_pos, end_pos):
    start_row, start_col = start_pos
    end_row, end_col = end_pos

    row_step = (end_row - start_row) // max(1, abs(end_row - start_row)) if start_row != end_row else 0
    col_step = (end_col - start_col) // max(1, abs(end_col - start_col)) if start_col != end_col else 0

    current_row, current_col = start_row + row_step, start_col + col_step

    while (current_row, current_col) != (end_row, end_col):
        if board[current_row][current_col] != "--":
            return False
        current_row += row_step
        current_col += col_step

    return True

# Main game loop
def main():
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Chess')
    images = load_images()
    
    # Sample board state
    board = [
        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
        ["wR", "wN", "wB", "wK", "wQ", "wB", "wN", "wR"]
    ]

    turn = 'w'
    selected_piece = None
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_square_under_mouse(pos)
                if selected_piece:
                    start_row, start_col = selected_piece
                    if is_valid_move(board, (start_row, start_col), (row, col), turn):
                        board[row][col] = board[start_row][start_col]
                        board[start_row][start_col] = "--"
                        turn = 'b' if turn == 'w' else 'w'
                    selected_piece = None
                else:
                    if board[row][col][0] == turn:
                        selected_piece = (row, col)

        draw_board(win)
        draw_pieces(win, board, images)
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
