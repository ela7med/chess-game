import pygame

# pygame module initiolization
pygame.init()

# make 800 * 800 window
screen = pygame.display.set_mode((800, 800))


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

# list contail all legal moves availabile for the selected peice
legal_moves = []
# currunt selected peice possion
cur_piece = ()
# True => white to play | False => Black to play
turn = True

def draw_board():
    # drow the background of the board
    for i in range(8):
        for j in range(8):
            if ((i + j) % 2 != 0):
                pygame.draw.rect(screen, black, (i * 100, j * 100 , 100, 100))
            else:
                pygame.draw.rect(screen, white, (i * 100, j * 100 , 100, 100))
    # add the pieces to the board according to the board  2D array
    for i, rank in enumerate(board):
        for j, file in enumerate(rank):
            if file != '  ':
                p = pygame.image.load(f"images/{file}.png")
                p = pygame.transform.scale(p, (100, 100))
                screen.blit(p, (j * 100, i * 100))
    # add the legal moves dots on the board
    for i in legal_moves:
        if board[i[0]][i[1]] == '  ':
            pygame.draw.circle(screen, dots, (i[1] * 100 + 50, i[0] * 100 + 50), 12)
        else:
            pygame.draw.circle(screen, dots_attack, (i[1] * 100 + 50, i[0] * 100 + 50), 12)

def me():
    if turn:
        return 'w'
    else:
        return 'b'

def opponent():
    if turn:
        return 'b'
    else:
        return 'w'


'''
    pown_move function
    input: pos => tuple represent the possion of the current pown
    output: list represent all the legal moves for the current pown
'''
def pown_move(pos):
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

'''
    rook_move function
    input: pos => tuple represent the possion of the current rook
    output: list represent all the legal moves for the current rook
'''
def rook_move(pos):
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

'''
    knight_move function
    input: pos => tuple represent the possion of the current knight
    output: list represent all the legal moves for the current knight
'''
def knight_move(pos):
    moves = []
    knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
    
    for i, j in knight_moves:
        x = pos[0] + i
        y = pos[1] + j 
        if 0 <= x <= 7 and 0 <= y <= 7: 
            if not board[x][y].startswith(me()):
                moves.append((x, y))
    
    return moves

'''
    bishop_move function
    input: pos => tuple represent the possion of the current bishop
    output: list represent all the legal moves for the current bishop
'''
def bishop_move(pos):
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

'''
    queen_move function
    input: pos => tuple represent the possion of the current queen
    output: list represent all the legal moves for the current queen
'''
def queen_move(pos):
    return rook_move(pos) + bishop_move(pos)

'''
    king_move function
    input: pos => tuple represent the possion of the current king
    output: list represent all the legal moves for the current king
'''
def king_move(pos):        
    moves = []
    king_moves =[(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    
    for i, j in king_moves:
        x = pos[0] + i
        y = pos[1] + j
        if 0 <= x <= 7 and 0 <= y <= 7:
            if board[x][y] == '  ' or not board[x][y].startswith(me()):
                moves.append((x, y))

    if me() == 'w' and pos == (7, 4):
        if board[7][0] == 'wr' and board[7][1] == board[7][2] == board[7][3] == '  ':
            moves.append((7, 2))
        if board[7][7] == 'wr' and board[7][5] == board[7][6] == '  ':
            moves.append((7, 6))
    elif me() == 'b' and pos == (0, 4):
        if board[0][0] == 'br' and board[0][1] == board[0][2] == board[0][3] == '  ':
            moves.append((0, 2))
        if board[0][7] == 'br' and board[0][5] == board[0][6] == '  ':
            moves.append((0, 6))

    return moves

def castling(pos, type):
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
    
# main gui loop
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            quit()
        if e.type == pygame.MOUSEBUTTONDOWN:
            y ,x = e.pos
            x //= 100
            y //= 100
            if board[x][y].startswith(me()):
                cur_piece = (x, y)
                legal_moves = make_legal_moves((x,y))
            else: 
                if (x, y) in legal_moves:
                    if board[cur_piece[0]][cur_piece[1]] in ('wk', 'bk'):
                        if (x, y) in [(7, 2), (0, 2)]:
                            castling(cur_piece, 'long')
                            continue
                        elif (x, y) in [(7, 6), (0, 6)]:
                            castling(cur_piece, 'short')
                        else:
                            move(cur_piece, (x, y))
                    else:
                        move(cur_piece, (x, y))
                else:
                    legal_moves = []   
                cur_piece = ()
    draw_board()
    pygame.display.flip()

pygame.quit()