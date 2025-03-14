import pygame

#ui design
pygame.init()
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

board = Board()

running = True
#main cycle of pygame
while running:
    screen.fill((230, 194, 139))
    draw_board()

    board.draw(screen)
    pygame.display.flip()  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            row = x // 100
            col = y // 100
            start_pos = (row, col)

            if board.grid[start_pos] != None:
                selected_pos = start_pos
            else:
                selected_pos = None

        if event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            row = x // 100
            col = y // 100
            end_pos = (row, col)

            board.move_pieces(old_pos=selected_pos, new_pos=end_pos)
            selected_pos = None

