import pygame

pygame.init()

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Chess Game")
sound = pygame.mixer.Sound("chess_move.wav")

board = [
    ['br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'],
    ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  '],
    ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
    ['wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr']
]

white = (235, 236, 208)
black = (115, 149, 82)
dots = (202, 203, 179)
dots_attack = (255, 0, 0)

move_history = []
legal_moves = []
cur_piece = ()
turn = True

def draw_board():
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                pygame.draw.rect(screen, white, (i * 100, j * 100, 100, 100))
            else:
                pygame.draw.rect(screen, black, (i * 100, j * 100, 100, 100))
    for i in range(8):
        font = pygame.font.SysFont('arial', 18)
        num = font.render(f"{8 - i}", True, (0, 0, 0))
        screen.blit(num, (5, i * 100 + 5))
    
    for i, j in enumerate('abcdefgh'):
        font = pygame.font.SysFont('arial', 18)
        letter = font.render(f"{j}", True, (0, 0, 0))
        screen.blit(letter, (i * 100 + 5, 795 - 18))

    for i, rank in enumerate(board):
        for j, peice in enumerate(rank):
            if peice != '  ':
                img = pygame.image.load(f'images/{peice}.png')
                img = pygame.transform.scale(img, (100, 100))
                screen.blit(img, (j * 100, i * 100))

    for i ,j in legal_moves:
        if board[i][j] == '  ':
            pygame.draw.circle(screen, dots, (j * 100 + 50, i * 100 + 50), 12)
        else:
            pygame.draw.circle(screen, dots_attack, (j * 100 + 50, i * 100 + 50), 12)

def me():
    if turn:
        return 'w'
    return 'b'

def opponent():
    if turn:
        return 'b'
    return 'w'

def pawn_move(pos):
    x, y = pos
    moves = []
    def is_first_move(row):
        if (me() == 'w' and row == 6) or (me() == 'b' and row == 1):
            return True
        return False
    
    if turn:
        direction = -1
    else:
        direction = 1

    if 0 <= x + direction <= 7 and board[x + direction][y] == '  ':
        moves.append((x + direction, y))

    if is_first_move(x) and board[x + direction][y] == '  ' and board[x + 2 * direction][y] == '  ':
        moves.append((x + 2 * direction, y))
    
    if 0 <= x + direction <= 7 and 0 <= y + 1 <= 7 and board[x + direction][y + 1].startswith(opponent()):
        moves.append((x + direction, y + 1))
    
    if 0 <= x + direction <= 7 and 0 <= y - 1 <= 7 and board[x + direction][y - 1].startswith(opponent()):
        moves.append((x + direction, y - 1))
    
    return moves


def rook_move(pos):
    rook_moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    moves = []
    for dx, dy in rook_moves:
        x, y = pos
        x += dx
        y += dy
        while True:
            if board[x][y] == '  ':
                moves.append((x, y))
                x += dx
                y += dy
            elif board[x][y].statswith(opponent()):
                moves.append((x, y))
                break
            else:
                break
    return moves

    
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            quit()
    
    draw_board()
    pygame.display.flip()
