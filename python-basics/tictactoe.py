import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 600
HEIGHT = 700
LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Neon Colors
BG_COLOR = (10, 14, 39)  # Dark blue background
LINE_COLOR = (0, 255, 255)  # Neon cyan
CIRCLE_COLOR = (0, 255, 0)  # Neon green
CROSS_COLOR = (255, 0, 255)  # Neon magenta
TEXT_COLOR = (0, 255, 255)  # Neon cyan
BUTTON_COLOR = (255, 0, 255)  # Neon magenta
WINNER_COLOR = (255, 255, 0)  # Neon yellow

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('NEON TIC TAC TOE')
screen.fill(BG_COLOR)

# Board
board = [[None, None, None] for _ in range(BOARD_ROWS)]

# Fonts
title_font = pygame.font.Font(None, 60)
font = pygame.font.Font(None, 40)
small_font = pygame.font.Font(None, 30)

# Game variables
player = 1  # Player 1: X, Player 2: O
game_over = False
winner = None
winning_line = None
scores = {'X': 0, 'O': 0, 'Draw': 0}

def draw_lines():
    """Draw the tic-tac-toe grid with neon glow effect"""
    # Horizontal lines
    for row in range(1, BOARD_ROWS):
        # Glow effect
        for thickness in range(5, 0, -1):
            alpha = 50 + (5 - thickness) * 40
            glow_surface = pygame.Surface((WIDTH, LINE_WIDTH + thickness * 2), pygame.SRCALPHA)
            glow_surface.fill((*LINE_COLOR, alpha))
            screen.blit(glow_surface, (0, row * SQUARE_SIZE - thickness))
        # Main line
        pygame.draw.line(screen, LINE_COLOR, (0, row * SQUARE_SIZE), 
                        (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
    
    # Vertical lines
    for col in range(1, BOARD_COLS):
        # Glow effect
        for thickness in range(5, 0, -1):
            alpha = 50 + (5 - thickness) * 40
            glow_surface = pygame.Surface((LINE_WIDTH + thickness * 2, WIDTH), pygame.SRCALPHA)
            glow_surface.fill((*LINE_COLOR, alpha))
            screen.blit(glow_surface, (col * SQUARE_SIZE - thickness, 0))
        # Main line
        pygame.draw.line(screen, LINE_COLOR, (col * SQUARE_SIZE, 0), 
                        (col * SQUARE_SIZE, WIDTH), LINE_WIDTH)

def draw_figures():
    """Draw X's and O's with neon glow effect"""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:  # Draw X
                # Glow effect
                for thickness in range(8, 0, -1):
                    alpha = 30 + (8 - thickness) * 25
                    glow_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                    # Line 1
                    pygame.draw.line(glow_surface, (*CROSS_COLOR, alpha),
                                   (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                   (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, 
                                    row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                   CROSS_WIDTH + thickness)
                    # Line 2
                    pygame.draw.line(glow_surface, (*CROSS_COLOR, alpha),
                                   (col * SQUARE_SIZE + SPACE, 
                                    row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                   (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, 
                                    row * SQUARE_SIZE + SPACE),
                                   CROSS_WIDTH + thickness)
                    screen.blit(glow_surface, (0, 0))
                
                # Main X
                pygame.draw.line(screen, CROSS_COLOR,
                               (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                               (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, 
                                row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                               CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR,
                               (col * SQUARE_SIZE + SPACE, 
                                row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                               (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, 
                                row * SQUARE_SIZE + SPACE),
                               CROSS_WIDTH)
                
            elif board[row][col] == 2:  # Draw O
                # Glow effect
                for thickness in range(8, 0, -1):
                    alpha = 30 + (8 - thickness) * 25
                    glow_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                    pygame.draw.circle(glow_surface, (*CIRCLE_COLOR, alpha),
                                     (int(col * SQUARE_SIZE + SQUARE_SIZE // 2),
                                      int(row * SQUARE_SIZE + SQUARE_SIZE // 2)),
                                     CIRCLE_RADIUS + thickness, CIRCLE_WIDTH + thickness)
                    screen.blit(glow_surface, (0, 0))
                
                # Main O
                pygame.draw.circle(screen, CIRCLE_COLOR,
                                 (int(col * SQUARE_SIZE + SQUARE_SIZE // 2),
                                  int(row * SQUARE_SIZE + SQUARE_SIZE // 2)),
                                 CIRCLE_RADIUS, CIRCLE_WIDTH)

def mark_square(row, col, player):
    """Mark a square with the current player"""
    board[row][col] = player

def available_square(row, col):
    """Check if a square is available"""
    return board[row][col] is None

def is_board_full():
    """Check if the board is full"""
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] is None:
                return False
    return True

def check_win(player):
    """Check if a player has won"""
    # Vertical wins
    for col in range(BOARD_COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True, 'vertical', col
    
    # Horizontal wins
    for row in range(BOARD_ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True, 'horizontal', row
    
    # Diagonal wins
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True, 'diagonal_desc', None
    
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True, 'diagonal_asc', None
    
    return False, None, None

def draw_winning_line(line_type, position):
    """Draw the winning line with neon glow"""
    if line_type == 'horizontal':
        y_pos = position * SQUARE_SIZE + SQUARE_SIZE // 2
        # Glow effect
        for thickness in range(10, 0, -1):
            alpha = 40 + (10 - thickness) * 20
            glow_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pygame.draw.line(glow_surface, (*WINNER_COLOR, alpha),
                           (15, y_pos), (WIDTH - 15, y_pos), 15 + thickness)
            screen.blit(glow_surface, (0, 0))
        # Main line
        pygame.draw.line(screen, WINNER_COLOR, (15, y_pos), (WIDTH - 15, y_pos), 15)
    
    elif line_type == 'vertical':
        x_pos = position * SQUARE_SIZE + SQUARE_SIZE // 2
        # Glow effect
        for thickness in range(10, 0, -1):
            alpha = 40 + (10 - thickness) * 20
            glow_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pygame.draw.line(glow_surface, (*WINNER_COLOR, alpha),
                           (x_pos, 15), (x_pos, WIDTH - 15), 15 + thickness)
            screen.blit(glow_surface, (0, 0))
        # Main line
        pygame.draw.line(screen, WINNER_COLOR, (x_pos, 15), (x_pos, WIDTH - 15), 15)
    
    elif line_type == 'diagonal_desc':
        # Glow effect
        for thickness in range(10, 0, -1):
            alpha = 40 + (10 - thickness) * 20
            glow_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pygame.draw.line(glow_surface, (*WINNER_COLOR, alpha),
                           (15, 15), (WIDTH - 15, WIDTH - 15), 15 + thickness)
            screen.blit(glow_surface, (0, 0))
        # Main line
        pygame.draw.line(screen, WINNER_COLOR, (15, 15), (WIDTH - 15, WIDTH - 15), 15)
    
    elif line_type == 'diagonal_asc':
        # Glow effect
        for thickness in range(10, 0, -1):
            alpha = 40 + (10 - thickness) * 20
            glow_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            pygame.draw.line(glow_surface, (*WINNER_COLOR, alpha),
                           (15, WIDTH - 15), (WIDTH - 15, 15), 15 + thickness)
            screen.blit(glow_surface, (0, 0))
        # Main line
        pygame.draw.line(screen, WINNER_COLOR, (15, WIDTH - 15), (WIDTH - 15, 15), 15)

def restart():
    """Restart the game"""
    global board, player, game_over, winner, winning_line
    screen.fill(BG_COLOR)
    draw_lines()
    board = [[None, None, None] for _ in range(BOARD_ROWS)]
    player = 1
    game_over = False
    winner = None
    winning_line = None

def draw_status():
    """Draw status bar and buttons"""
    # Status bar background
    pygame.draw.rect(screen, BG_COLOR, (0, WIDTH, WIDTH, HEIGHT - WIDTH))
    
    # Status text
    if game_over:
        if winner:
            status_text = f"Player {'X' if winner == 1 else 'O'} WINS!"
            color = CROSS_COLOR if winner == 1 else CIRCLE_COLOR
        else:
            status_text = "IT'S A DRAW!"
            color = WINNER_COLOR
    else:
        status_text = f"Player {'X' if player == 1 else 'O'}'s Turn"
        color = CROSS_COLOR if player == 1 else CIRCLE_COLOR
    
    # Draw status text with glow
    text = font.render(status_text, True, color)
    text_rect = text.get_rect(center=(WIDTH // 2, WIDTH + 30))
    # Glow effect
    for size in range(5, 0, -1):
        glow_surface = pygame.Surface((WIDTH, HEIGHT - WIDTH), pygame.SRCALPHA)
        alpha = 30 + (5 - size) * 40
        glow_text = font.render(status_text, True, (*color, alpha))
        glow_rect = glow_text.get_rect(center=(WIDTH // 2, WIDTH + 30))
        glow_surface.blit(glow_text, glow_rect)
        screen.blit(glow_surface, (0, WIDTH))
    screen.blit(text, text_rect)
    
    # Draw buttons
    reset_button = pygame.Rect(WIDTH // 2 - 100, WIDTH + 70, 200, 50)
    pygame.draw.rect(screen, BUTTON_COLOR, reset_button, 3, border_radius=10)
    reset_text = small_font.render("RESTART", True, BUTTON_COLOR)
    reset_text_rect = reset_text.get_rect(center=reset_button.center)
    screen.blit(reset_text, reset_text_rect)
    
    # Draw scores
    score_y = WIDTH + 140
    
    # Player X score
    x_text = small_font.render(f"Player X: {scores['X']}", True, CROSS_COLOR)
    screen.blit(x_text, (50, score_y))
    
    # Draw score
    draw_text = small_font.render(f"Draws: {scores['Draw']}", True, WINNER_COLOR)
    draw_rect = draw_text.get_rect(center=(WIDTH // 2, score_y + 15))
    screen.blit(draw_text, draw_rect)
    
    # Player O score
    o_text = small_font.render(f"Player O: {scores['O']}", True, CIRCLE_COLOR)
    o_rect = o_text.get_rect(right=WIDTH - 50, top=score_y)
    screen.blit(o_text, o_rect)
    
    return reset_button

# Draw initial board
draw_lines()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]
            mouseY = event.pos[1]
            
            # Check if click is on the board
            if mouseY < WIDTH:
                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE
                
                if available_square(clicked_row, clicked_col):
                    mark_square(clicked_row, clicked_col, player)
                    
                    # Check for win
                    won, line_type, position = check_win(player)
                    if won:
                        game_over = True
                        winner = player
                        winning_line = (line_type, position)
                        if player == 1:
                            scores['X'] += 1
                        else:
                            scores['O'] += 1
                    elif is_board_full():
                        game_over = True
                        scores['Draw'] += 1
                    else:
                        player = 2 if player == 1 else 1
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX = event.pos[0]
            mouseY = event.pos[1]
            
            # Check if restart button is clicked
            if WIDTH + 70 <= mouseY <= WIDTH + 120:
                if WIDTH // 2 - 100 <= mouseX <= WIDTH // 2 + 100:
                    restart()
    
    # Draw everything
    draw_figures()
    
    if game_over and winning_line:
        draw_winning_line(winning_line[0], winning_line[1])
    
    reset_button = draw_status()
    
    pygame.display.update()

pygame.quit()
