import pygame

# pygame module initiolization
pygame.init()

sound = pygame.mixer.Sound("chess_move.wav")
# make 800 * 800 window
screen = pygame.display.set_mode((800, 800))
# make window caption
pygame.display.set_caption("Chess Game")


# main chess board 
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

# colors used to draw the board
white = (235, 236, 208)
black = (115, 149, 82)
dots = (202, 203, 179)
dots_attack = (255, 0, 0)

move_history = []
legal_moves = []
cur_piece = ()
turn = True
is_short_white_castling_valid = True
is_long_white_castling_valid = True
is_short_black_castling_valid = True
is_long_black_castling_valid = True


def draw_board():
    """
    Draws the chess board, pieces, and legal move indicators on the screen.
    """
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
    """
    Returns the current player's color: 'w' for white, 'b' for black.
    """
    if turn:
        return 'w'
    else:
        return 'b'

def opponent():
    """
    Returns the opponent's color: 'b' if white's turn, 'w' if black's turn.
    """
    if turn:
        return 'b'
    else:
        return 'w'

def pown_move(pos):
    """
    Returns all legal moves for a pawn at the given position.
    Handles first move, captures, and forward movement.
    
    Args:
        pos (tuple): The (row, col) position of the pawn.

    Returns:
        list of tuple: Legal move positions.
    """
    def is_pawn_first_move(row):
        if me() == 'w' and row == 6:
            return True
        elif me() == 'b' and row == 1:
            return True
        return False
    
    x, y = pos
    moves = []
    if me() == 'w':
        direction = -1 
    else:
        direction = 1

    if 0 <= x + direction <= 7 and board[x + direction][y] == "  ":
        moves.append((x + direction, y))
    if is_pawn_first_move(x) and board[x + 2 * direction][y] == "  " and board[x + direction][y] == "  ":
        moves.append((x + 2 * direction, y))
    if 0 <= x + direction <= 7 and 0 <= y - 1 <= 7 and board[x + direction][y - 1].startswith(opponent()):
        moves.append((x + direction, y - 1))
    if 0 <= x + direction <= 7 and 0 <= y + 1 <= 7 and board[x + direction][y + 1].startswith(opponent()):
        moves.append((x + direction, y + 1))
    
    return moves

def rook_move(pos):
    """
    Returns all legal moves for a rook at the given position.
    
    Args:
        pos (tuple): The (row, col) position of the rook.

    Returns:
        list of tuple: Legal move positions.
    """
    moves = []
    x, y = pos
    rook_moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for i, j in rook_moves: 
        nx = x + i
        ny = y + j
        while 0 <= nx <= 7 and 0 <= ny <= 7:
            if board[nx][ny].startswith(me()):
                break
            elif board[nx][ny].startswith(opponent()):
                moves.append((nx, ny))
                break
            else:
                moves.append((nx, ny))
                nx += i
                ny += j
    return moves

def knight_move(pos):
    """
    Returns all legal moves for a knight at the given position.
    
    Args:
        pos (tuple): The (row, col) position of the knight.

    Returns:
        list of tuple: Legal move positions.
    """
    moves = []
    knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
    
    for i, j in knight_moves:
        x = pos[0] + i
        y = pos[1] + j 
        if 0 <= x <= 7 and 0 <= y <= 7: 
            if not board[x][y].startswith(me()):
                moves.append((x, y))
    
    return moves

def bishop_move(pos):
    """
    Returns all legal moves for a bishop at the given position.
    
    Args:
        pos (tuple): The (row, col) position of the bishop.

    Returns:
        list of tuple: Legal move positions.
    """
    moves = []
    x, y = pos
    bishop_moves = [(1, 1), (-1, -1), (-1, 1), (1, -1)]

    for i, j in bishop_moves: 
        nx = x + i
        ny = y + j
        while 0 <= nx <= 7 and 0 <= ny <= 7:
            if board[nx][ny].startswith(me()):
                break
            elif board[nx][ny].startswith(opponent()):
                moves.append((nx, ny))
                break
            else:
                moves.append((nx, ny))
                nx += i
                ny += j
    return moves

def queen_move(pos):
    """
    Returns all legal moves for a queen at the given position.
    Combines rook and bishop moves.
    
    Args:
        pos (tuple): The (row, col) position of the queen.

    Returns:
        list of tuple: Legal move positions.
    """
    return rook_move(pos) + bishop_move(pos)

def king_move(pos):    
    """
    Returns all legal moves for a king at the given position, including castling if available.
    
    Args:
        pos (tuple): The (row, col) position of the king.

    Returns:
        list of tuple: Legal move positions.
    """    
    moves = []
    king_moves =[(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

    
    for i, j in king_moves:
        x = pos[0] + i
        y = pos[1] + j
        if 0 <= x <= 7 and 0 <= y <= 7:
            if board[x][y] == '  ' or not board[x][y].startswith(me()):
                moves.append((x, y))

    if me() == 'w' and pos == (7, 4):
        if board[7][0] == 'wr' and board[7][1] == board[7][2] == board[7][3] == '  ' and is_long_white_castling_valid:
            moves.append((7, 2))
        if board[7][7] == 'wr' and board[7][5] == board[7][6] == '  ' and is_short_white_castling_valid:
            moves.append((7, 6))
    elif me() == 'b' and pos == (0, 4):
        if board[0][0] == 'br' and board[0][1] == board[0][2] == board[0][3] == '  ' and is_long_black_castling_valid:
            moves.append((0, 2))
        if board[0][7] == 'br' and board[0][5] == board[0][6] == '  ' and is_short_black_castling_valid:
            moves.append((0, 6))
    return moves

def castling(pos, type):
    """
    Executes castling move for the king and rook.

    Args:
        pos (tuple): King's starting position.
        type (str): Either 'short' or 'long' for castling side.
    """
    global legal_moves, turn
    x = pos[0]
    if type == 'short':
        board[x][6] = board[x][4]
        board[x][4] = '  '
        board[x][5] = board[x][7]
        board[x][7] = '  '
    else:
        board[x][2] = board[x][4]
        board[x][4] = '  '
        board[x][3] = board[x][0]
        board[x][0] = '  '
    legal_moves = [] 
    turn = not turn  

def move(start_pos, end_pos):
    """
    Moves a piece from start_pos to end_pos and handles pawn promotion.

    Args:
        start_pos (tuple): Starting square.
        end_pos (tuple): Target square.
    """
    global legal_moves, turn
    if board[start_pos[0]][start_pos[1]] == 'wp' and end_pos[0] == 0:  
        board[end_pos[0]][end_pos[1]] = 'wq'
    elif board[start_pos[0]][start_pos[1]] == 'bp' and end_pos[0] == 7:  
        board[end_pos[0]][end_pos[1]] = 'bq' 
    else:
        board[end_pos[0]][end_pos[1]] = board[start_pos[0]][start_pos[1]]  
    board[start_pos[0]][start_pos[1]] = '  '
    legal_moves = [] 
    turn = not turn  

def make_legal_moves(pos):
    """
    Dispatches move generation for the selected piece.

    Args:
        pos (tuple): Position of the selected piece.

    Returns:
        list of tuple: Legal moves.
    """
    x, y = pos
    if board[x][y] == me() + 'p':
        return pown_move(cur_piece)
    elif board[x][y] == me() + 'r':
        return rook_move(cur_piece)
    elif board[x][y] == me() + 'q':
        return queen_move(cur_piece)
    elif board[x][y] == me() + 'k':
        return king_move(cur_piece)
    elif board[x][y] == me() + 'b':
        return bishop_move(cur_piece)
    elif board[x][y] == me() + 'n':
        return knight_move(cur_piece)

def undo():
    """
    Undoes the last move by restoring the previous board state.
    """
    global turn, board
    if move_history:
        turn = not turn
        board = move_history.pop()  

def copy_board():
    """
    Copies the current board state and appends it to move history.
    """
    global board, move_history
    new_board = []
    for i in board:
        new_board.append(i.copy())
    move_history.append(new_board)


# main gui loop
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            quit()
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_UP:
            undo()
        elif e.type == pygame.MOUSEBUTTONDOWN:
            y ,x = e.pos
            x //= 100
            y //= 100
            if board[x][y].startswith(me()):
                cur_piece = (x, y)
                legal_moves = make_legal_moves((x,y))
            else: 
                if (x, y) in legal_moves:
                    sound.play()
                    copy_board()
                    if board[cur_piece[0]][cur_piece[1]] in ('wk', 'bk'):
                        if (x, y) in [(7, 2), (0, 2)]:
                            castling(cur_piece, 'long')
                        elif (x, y) in [(7, 6), (0, 6)]:
                            castling(cur_piece, 'short')
                        else:
                            move(cur_piece, (x, y))
                        if me() == 'b':
                            is_long_white_castling_valid = False
                            is_short_white_castling_valid = False
                        else:
                            is_long_black_castling_valid = False
                            is_short_black_castling_valid = False
                    else: 
                        if board[cur_piece[0]][cur_piece[1]] == 'wr':
                            if cur_piece == (7, 7):
                                is_short_white_castling_valid = False
                            elif cur_piece == (7, 0):
                                is_long_white_castling_valid = False
                        elif board[cur_piece[0]][cur_piece[1]] == 'br':
                            if cur_piece == (0, 7):
                                is_short_black_castling_valid = False
                            elif cur_piece == (0, 0):
                                is_long_black_castling_valid = False
                        move(cur_piece, (x, y))
                else:
                    legal_moves = []   
                cur_piece = ()
    draw_board()
    pygame.display.flip()

pygame.quit()