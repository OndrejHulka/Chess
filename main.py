import pygame

#ui design
pygame.init()

#sound
pygame.mixer.init()
#screen
screen = pygame.display.set_mode((800,800))

#caption
pygame.display.set_caption("Chess")

#background color
screen.fill((230, 194, 139))
#draw board
def draw_board():
    a = (100, 800, 200)
    b = (0, 700, 200)

    for i in range(0, 800, 100):
        if i == 0 or i == 200 or i == 400 or i == 600:
            for j in range(a[0], a[1], a[2]):
                pygame.draw.rect(screen, (139, 90, 43), (i, j, 100, 100), 0)
        else:
            for j in range(b[0], b[1], b[2]):
                pygame.draw.rect(screen, (139, 90, 43), (i, j, 100, 100), 0)
    

#update
pygame.display.flip() 

class Piece:
    def __init__(self, color, type, position):
        self.color = color
        self.type = type
        self.position = position
        shortcut = f"{self.color[0]}{self.type}"
        self.image = pygame.image.load(f"chess/image/{shortcut}.png")
        self.image = pygame.transform.scale(self.image, (60, 60))

    def draw(self, screen):
        x, y = self.position
        screen.blit(self.image, (x*100, y*100))

    def move(self, new_position):
        self.position = new_position

class Board:
    def __init__(self):
        self.grid = {}
        self.setup_pieces()

    def draw(self, screen):
        for piece in self.grid.values():
            if piece is not None:
                piece.draw(screen)

    def move_pieces(self, old_pos, new_pos):
        if old_pos in self.grid and self.grid[old_pos] is not None:
            piece = self.grid.pop(old_pos)
        
            self.grid[new_pos] = piece
            piece.move(new_pos)
            self.grid[old_pos] = None

    def setup_pieces(self):
        for i in range(8):
            for j in range(8):
                self.grid[(i, j)] = None
    
        self.grid[(0, 0)] = Piece("black", "rook", (0,0))
        self.grid[(1, 0)] = Piece("black", "horse", (1,0))
        self.grid[(2, 0)] = Piece("black", "bishop", (2,0))
        self.grid[(3, 0)] = Piece("black", "queen", (3,0))
        self.grid[(4, 0)] = Piece("black", "king", (4,0))
        self.grid[(5, 0)] = Piece("black", "bishop", (5,0))
        self.grid[(6, 0)] = Piece("black", "horse", (6,0))
        self.grid[(7, 0)] = Piece("black", "rook", (7,0))

        for i in range(8):
            self.grid[(i, 1)] = Piece("black", "pawn", (i, 1))
            self.grid[(i, 6)] = Piece("white", "pawn", (i, 6))

        self.grid[(0, 7)] = Piece("white", "rook", (0,7))
        self.grid[(1, 7)] = Piece("white", "horse", (1,7))
        self.grid[(2, 7)] = Piece("white", "bishop", (2,7))
        self.grid[(3, 7)] = Piece("white", "queen", (3,7))
        self.grid[(4, 7)] = Piece("white", "king", (4,7))
        self.grid[(5, 7)] = Piece("white", "bishop", (5,7))
        self.grid[(6, 7)] = Piece("white", "horse", (6,7))
        self.grid[(7, 7)] = Piece("white", "rook", (7,7))


        self.draw(screen)

#will be returning True or False
def valid_moves(piece, old_pos, new_pos, board):
    if piece is None:
        return False

    if piece.type == "pawn":
        return valid_pawn_move(piece, old_pos, new_pos, board)
    elif piece.type == "rook":
        return valid_rook_move(piece, old_pos, new_pos, board)
    elif piece.type == "bishop":
        return valid_bishop_move(piece, old_pos, new_pos, board)
    elif piece.type == "horse":
        return valid_horse_move(piece, old_pos, new_pos, board)
    elif piece.type == "queen":
        return valid_queen_move(piece, old_pos, new_pos, board)
    elif piece.type == "king":
        return valid_king_move(piece, old_pos, new_pos, board)

#check moves of pawn - working
def valid_pawn_move(piece, old_pos, new_pos, board):
    x1, y1 = old_pos
    x2, y2 = (new_pos)
    valid_moves = set()

    direction = -1 if piece.color == "white" else 1
    start_row = 6 if piece.color == "white" else 1

    if board.grid.get((x1, y1 + direction)) is None:
        valid_moves.add((x1, y1 + direction))

        if y1 == start_row and board.grid.get((x1, y1 + 2 * direction)) is None:
            valid_moves.add((x1, y1 + 2 * direction))


    right_attack = (x1 + 1, y1 + direction)
    if board.grid.get(right_attack) and board.grid[right_attack].color != piece.color:
        valid_moves.add(right_attack)

    left_attack = (x1 - 1, y1 + direction)
    if board.grid.get(left_attack) and board.grid[left_attack].color != piece.color:
        valid_moves.add(left_attack)
    
    return new_pos in valid_moves

#working
def valid_rook_move(piece, old_pos, new_pos, board):
    x1, y1 = old_pos
    x2, y2 = new_pos
    valid_moves = []

    #doprava
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for dx, dy in directions:
        nx, ny = x1, y1

        while True:
            nx += dx
            ny += dy

            if not (0 <= nx < 8 and 0 <= ny < 8):
                break

            val = board.grid.get((nx, ny))

            if val is None:  
                valid_moves.append((nx, ny))
            else:
                if val.color != piece.color: 
                    valid_moves.append((nx, ny))
                break  

    return new_pos in valid_moves  


def valid_bishop_move(piece, old_pos, new_pos, board):
    x1, y1 = old_pos
    x2, y2 = new_pos
    valid_moves = []
    #levy horni roh matrixu, pravy horni roh
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    for dx, dy in directions:
        nx, ny = x1, y1

        while True:
            nx += dx
            ny += dy

            if not(0 <= nx < 8 and 0 <= ny < 8):
                break

            val = board.grid.get((nx, ny))

            if val is None:
                valid_moves.append((nx, ny))
            else:
                if val.color != piece.color:
                    valid_moves.append((nx, ny))
                break
    return new_pos in valid_moves


def valid_queen_move(piece, old_pos, new_pos, board):
    if valid_bishop_move(piece, old_pos, new_pos, board) or valid_rook_move(piece, old_pos, new_pos, board):
        return True
    else:
        return False

def valid_horse_move(piece, old_pos, new_pos, board):
    x1, y1 = old_pos
    x2, y2 = new_pos

    possible_moves = [
        (x1 - 2, y1 - 1), (x1 - 2, y1 + 1),
        (x1 + 2, y1 - 1), (x1 + 2, y1 + 1),
        (x1 - 1, y1 - 2), (x1 - 1, y1 + 2),
        (x1 + 1, y1 - 2), (x1 + 1, y1 + 2)
    ]


    if new_pos in possible_moves and 0 <= x2 < 8 and 0 <= y2 < 8:

        if board.grid.get(new_pos) is None or board.grid[new_pos].color != piece.color:
            return True
    return False

def valid_king_move(piece, old_pos, new_pos, board):
    x1, y1 = old_pos
    x2, y2 = new_pos
    valid_moves = [
        (x1 - 1, y1 - 1), (x1, y1 - 1), (x1 + 1, y1 - 1),
        (x1 - 1, y1), (x1 + 1, y1),
        (x1 - 1, y1 + 1), (x1, y1 + 1), (x1 + 1, y1 + 1)
    ]

    if new_pos in valid_moves and 0 <= x2 <8 and 0 <= y2 < 8:
        if board.grid.get(new_pos) is None or board.grid[new_pos].color != piece.color:
            
            if is_square_atacked(new_pos, board, piece.color):
                return False
            
            return True
    return False


def is_square_atacked(pos, board, color):
    for piece_pos, piece in board.grid.items():
        if piece is not None and piece.color != color:
            if valid_moves(piece, piece_pos, pos, board):
                return True
    return False

def is_king_in_check(board, color):
    king_pos = None
    for pos, piece in board.grid.items():
        if piece and piece.color == color and piece.type == "king":
            king_pos = pos
            break
    return king_pos, is_square_atacked(king_pos, board, color) 

#current player
current_player = "white"
board = Board()
selected_pos = None
running = True
#main cycle of pygame
while running:
    screen.fill((230, 194, 139))
    draw_board()

    board.draw(screen)

    if selected_pos is not None and selected_pos in board.grid and board.grid[selected_pos] is not None:
        x, y = selected_pos
        pygame.draw.rect(screen, (255, 255, 0, 128), (x*100, y*100, 100, 100), 2)
        

    king_pos, in_check = is_king_in_check(board, current_player)
    if in_check:
        x, y = king_pos
        move_sound = pygame.mixer.Sound("chess/image/move-check.mp3")
        pygame.draw.rect(screen, (255, 255, 140, 200), (x*100, y*100, 100, 100), 2)
        

    pygame.display.flip()  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            row = x // 100
            col = y // 100
            start_pos = (row, col)

            if start_pos in board.grid and board.grid[start_pos] is not None:
                piece = board.grid[start_pos]

                if piece.color == current_player:
                    selected_pos = start_pos

        if event.type == pygame.MOUSEBUTTONUP:
            if selected_pos is not None:
                x, y = pygame.mouse.get_pos()
                row = x // 100
                col = y // 100
                end_pos = (row, col)

                piece = board.grid[start_pos]

                if selected_pos != end_pos and (board.grid[end_pos] is None or board.grid[end_pos].color != piece.color) and valid_moves(piece, start_pos, end_pos, board):
                    board.move_pieces(old_pos=selected_pos, new_pos=end_pos)

                    if current_player == "white":
                        current_player = "black"
                    else:
                        current_player = "white"
     
            selected_pos = None
    


    


                
        

        
