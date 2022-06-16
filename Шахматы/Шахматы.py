import os
import sys
import pygame
import time

WHITE = 1
BLACK = 2
Time_black = 30 * 60
Time_white = 30 * 60


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def draw():
    h = 480 // 8
    for i in range(8):
        if i % 2 == 0:
            perenency = 0
        else:
            perenency = h
        for j in range(8):
            if j % 2 == 0:
                screen.blit(image_black, (h * j + perenency, h * i))
                screen.blit(image_white, (h * j + perenency - h, h * i))
                if perenency == 0:
                    screen.blit(image_white, (h * j + perenency + h, h * i))


class MyTimer:
    def __init__(self, color):
        self.running = False
        if color == 'white':
            self.last_start_time = Time_white
            self.elapsed = Time_white

        else:
            self.last_start_time = Time_black
            self.elapsed = Time_black

    def start(self):
        if not self.running:
            self.running = True
            self.last_start_time = time.time()

    def switched(self):
        return self.running

    def pause(self):
        if self.running:
            self.running = False
            self.elapsed -= int(time.time() - self.last_start_time)

    def get_elapsed(self):
        elapsed = self.elapsed
        if self.running:
            elapsed -= int(time.time() - self.last_start_time)
            return elapsed


class Board:
    # создание поля

    def __init__(self, width, height):
        self.x1 = -1
        self.y1 = -1
        self.x2 = -1
        self.y2 = -1
        self.width = width
        self.height = height
        self.board = [[-1] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 50
        self.move = 1
        self.action = None
        self.stop = False
        self.pawn = 'Q'
    # настройка внешнего вида

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def end(self):
        return self.stop

    def render(self):
        screen.fill((0, 0, 0))
        draw()
        stalemate_black = True
        stalemate_white = True
        for row in range(7, -1, -1):
            for col in range(8):
                f1 = pygame.font.Font(None, 36)
                text1 = f1.render(chessboard.cell(row, col), 1, (180, 0, 0))
                if chessboard.cell(row, col) == "wP":
                    screen.blit(image_pawnW, (60 * col, 10 * row * 6))
                elif chessboard.cell(row, col) == "bP":
                    screen.blit(image_pawnB, (60 * col, 10 * row * 6))
                elif chessboard.cell(row, col) == "bR":
                    screen.blit(image_rookB, (60 * col, 10 * row * 6))
                elif chessboard.cell(row, col) == "wR":
                    screen.blit(image_rookW, (60 * col, 10 * row * 6))
                elif chessboard.cell(row, col) == "bN":
                    screen.blit(image_knightB, (60 * col, 10 * row * 6))
                elif chessboard.cell(row, col) == "wN":
                    screen.blit(image_knightW, (60 * col, 10 * row * 6))
                elif chessboard.cell(row, col) == "wK":
                    screen.blit(image_kingW, (60 * col, 10 * row * 6))
                    stalemate_white = False
                elif chessboard.cell(row, col) == "bK":
                    stalemate_black = False
                    screen.blit(image_kingB, (60 * col, 10 * row * 6))
                elif chessboard.cell(row, col) == "wQ":
                    screen.blit(image_queenW, (60 * col, 10 * row * 6))
                elif chessboard.cell(row, col) == "bQ":
                    screen.blit(image_queenB, (60 * col, 10 * row * 6))
                elif chessboard.cell(row, col) == "bB":
                    screen.blit(image_bishopB, (60 * col, 10 * row * 6))
                elif chessboard.cell(row, col) == "wB":
                    screen.blit(image_bishopW, (60 * col, 10 * row * 6))
        screen.blit(image_queenW, (60*10, 0))            
        screen.blit(image_bishopW, (60*11, 0))
        screen.blit(image_rookW, (60*9, 0))
        screen.blit(image_knightW, (60*8, 0))
            
        if stalemate_black or stalemate_white:
            f1 = pygame.font.Font(None, 20)
            if stalemate_black:
                text1 = f1.render("Белые поставили мат чёрным!", 1, (220, 0, 0))
                self.stop = True

            else:
                text1 = f1.render("Чёрные поставили мат белым!", 1, (220, 0, 0))
                self.stop = True

            screen.blit(text1, (490, 110))
        else:
            f1 = pygame.font.Font(None, 40)
            if chessboard.color == 1:
                text2 = f1.render("Ход белых", 1, (0, 255, 200))
                timer_white.start()
                timer_black.pause()
                Time_white = timer_white.get_elapsed()
                f1 = pygame.font.Font(None, 40)
                text1 = f1.render('{} min {} s'.format(str(Time_white // 60),
                                                       str(Time_white % 60)), 1, (255, 0, 250))
                pygame.draw.rect(screen, 'black', ((490, 90), (200, 60)))
                screen.blit(text1, (490, 90))

            else:
                text2 = f1.render("Ход чёрных", 1, (0, 255, 200))
                timer_white.pause()
                timer_black.start()
                Time_black = timer_black.get_elapsed()
                f1 = pygame.font.Font(None, 40)
                text1 = f1.render('{} min {} s'.format(str(Time_black // 60),
                                                       str(Time_black % 60)), 1, (255, 0, 250))
                pygame.draw.rect(screen, 'black', ((490, 400), (200, 60)))
                screen.blit(text1, (490, 400))

            if self.action:
                text1 = f1.render("Ход успешен", 1, (0, 255, 0))
            elif self.action is None:
                text1 = f1.render("", 1, (255, 0, 0))
            else:
                text1 = f1.render("Ошибка!", 1, (255, 0, 0))
            pygame.draw.rect(screen, 'white', ((490, 170), (200, 60)), 1)
            screen.blit(text1, (490, 180))
            screen.blit(text2, (490, 270))
        pygame.display.flip()

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def on_click(self, cell_coords):
        if cell_coords is None:
            return cell_coords
        if self.x1 == -1 and self.y1 == -1:
            self.x1, self.y1 = cell_coords
        else:
            self.x2, self.y2 = cell_coords
            if self.x1 == 4 and self.y1 == 7 and self.x2 == 7 and self.y1 == 7:
                if not chessboard.castling7():
                    self.action = False
                else:
                    self.action = True
                self.render()
                self.x2, self.y2, self.x1, self.y1 = -1, -1, -1, -1
            elif self.x1 == 4 and self.y1 == 7 and self.x2 == 0 and self.y1 == 7:
                if not chessboard.castling0():
                    self.action = False
                else:
                    self.action = True

                self.render()
                self.x2, self.y2, self.x1, self.y1 = -1, -1, -1, -1
            elif self.x1 == 4 and self.y1 == 0 and self.x2 == 7 and self.y1 == 0:
                if not chessboard.castling7():
                    self.action = False
                else:
                    self.action = True
                self.render()
                self.x2, self.y2, self.x1, self.y1 = -1, -1, -1, -1
            elif self.x1 == 4 and self.y1 == 0 and self.x2 == 0 and self.y1 == 0:
                if not chessboard.castling0():
                    self.action = False
                else:
                    self.action = True
                self.render()
                self.x2, self.y2, self.x1, self.y1 = -1, -1, -1, -1

            elif chessboard.move_piece(self.y1, self.x1, self.y2, self.x2):
                self.x2, self.y2, self.x1, self.y1 = -1, -1, -1, -1
                self.action = True
                self.render()

            else:
                self.x2, self.y2, self.x1, self.y1 = -1, -1, -1, -1
                self.action = False
                self.render()

    def get_cell(self, mouse_pos):
        new_x = (mouse_pos[0] - self.left) // self.cell_size
        new_y = (mouse_pos[1] - self.top) // self.cell_size
        if new_x > self.width - 1 or new_x < 0 or new_y > self.height - 1 or new_y < 0:
            if new_x == 8 and new_y == 0:
                self.pawn = 'N'
                
            if new_x == 9 and new_y == 0:
                self.pawn = 'R'
            if new_x == 10 and new_y == 0:
                self.pawn = 'Q'
            if new_x == 11 and new_y == 0:
                self.pawn = 'B'
            return None
        return new_x, new_y

    def transformation(char, color):
        if char == 'Q':
            return Queen(color)
        if char == 'R':
            return Rook(color)
        if char == 'B':
            return Bishop(color)
        if char == 'N':
            return Knight(color)

    def opponent(color):
        if color == WHITE:
            return BLACK
        else:
            return WHITE

    def correct_coords(row, col):
        return 0 <= row < 8 and 0 <= col < 8


class Pieces:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color


class Сhessboard:
    def __init__(self):
        self.color = WHITE
        self.field = []
        for row in range(8):
            self.field.append([None] * 8)
        self.field[0] = [
            Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE),
            King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)
        ]
        self.field[1] = [
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE),
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)
        ]
        self.field[6] = [
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK),
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)
        ]
        self.field[7] = [
            Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK),
            King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)
        ]

    def current_player_color(self):
        return self.color

    def cell(self, row, col):
        piece = self.field[row][col]
        if piece is None:
            return '  '
        color = piece.get_color()
        c = 'w' if color == WHITE else 'b'
        return c + piece.char()

    def get_piece(self, row, col):
        if correct_coords(row, col):
            return self.field[row][col]
        else:
            return None

    def move_piece(self, row, col, row1, col1):
        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False
        piece = self.field[row][col]
        if piece is None:
            return False
        if piece.get_color() != self.color:
            return False
        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):
                return False
        elif self.field[row1][col1].get_color() == opponent(piece.get_color()):
            if not piece.can_attack(self, row, col, row1, col1):
                return False
        else:
            return False
        if piece.char() == 'P':
            if row1 == 0 or row1 == 7:
                board.change = True
                board.render()
                self.field[row][col] = None
                if board.pawn != '':
                    self.move_and_promote_pawn(row, col, row1, col1, board.pawn)
                    return True
        self.field[row][col] = None
        self.field[row1][col1] = piece
        self.color = opponent(self.color)
        return True

    def move_and_promote_pawn(self, row, col, row1, col1, char):
        if char == 'R':
            self.field[row1][col1] = Rook(self.color)
            self.color = opponent(self.color)
            return True
        if char == 'Q':
            self.field[row1][col1] = Queen(self.color)
            self.color = opponent(self.color)
            return True
        if char == 'B':
            self.field[row1][col1] = Bishop(self.color)
            self.color = opponent(self.color)
            return True
        if char == 'N':
            self.field[row1][col1] = Knight(self.color)
            self.color = opponent(self.color)
            return True
        return False

    def castling0(self):
        if self.current_player_color() == WHITE:
            if isinstance(self.field[0][0], Rook) and isinstance(self.field[0][4], King):
                if not self.field[0][0].move and not self.field[0][4].move:
                    if (self.field[0][1] is None and self.field[0][2] is None
                            and self.field[0][3] is None):
                        self.field[0][0] = None
                        self.field[0][3] = Rook(self.color)
                        self.field[0][4] = None
                        self.field[0][2] = King(self.color)
                        self.color = opponent(self.color)
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False

        else:
            if isinstance(self.field[7][0], Rook) and isinstance(self.field[7][4], King):
                if not self.field[7][0].move and not self.field[7][4].move:
                    if (self.field[7][1] is None and self.field[7][2] is None
                            and self.field[7][3] is None):
                        self.field[7][0] = None
                        self.field[7][3] = Rook(self.color)
                        self.field[7][4] = None
                        self.field[7][2] = King(self.color)
                        self.color = opponent(self.color)
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False

    def castling7(self):
        if self.current_player_color() == WHITE:
            if isinstance(self.field[0][7], Rook) and isinstance(self.field[0][4], King):
                if not self.field[0][7].move and not self.field[0][4].move:
                    if self.field[0][5] is None and self.field[0][6] is None:
                        self.field[0][7] = None
                        self.field[0][5] = Rook(self.color)
                        self.field[0][4] = None
                        self.field[0][6] = King(self.color)
                        self.color = opponent(self.color)
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            if isinstance(self.field[7][7], Rook) and isinstance(self.field[7][4], King):
                if not self.field[7][7].move and not self.field[7][4].move:
                    if self.field[7][5] is None and self.field[7][6] is None:
                        self.field[7][7] = None
                        self.field[7][5] = Rook(self.color)
                        self.field[7][4] = None
                        self.field[7][6] = King(self.color)
                        self.color = opponent(self.color)
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False


class Rook(Pieces):
    def __init__(self, color):
        super().__init__(color)
        self.move = False

    def char(self):
        return 'R'

    def moved(self, move):
        self.move = move
        return self.move

    def can_move(self, board, row, col, row1, col1):
        if row != row1 and col != col1:
            return False

        step = 1 if (row1 >= row) else -1
        for r in range(row + step, row1, step):
            if not (board.get_piece(r, col) is None):
                return False

        step = 1 if (col1 >= col) else -1
        for c in range(col + step, col1, step):
            if not (board.get_piece(row, c) is None):
                return False
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Pawn(Pieces):
    def __init__(self, color):
        super().__init__(color)
        self.move = False

    def char(self):
        return 'P'

    def moved(self, move):
        self.move = move
        return self.move

    def can_move(self, board, row, col, row1, col1):

        if col != col1:
            return False

        if self.color == WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6

        if row + direction == row1:
            return True

        if (row == start_row
                and row + 2 * direction == row1
                and board.field[row + direction][col] is None):
            return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        if self.color == WHITE:
            direction = 1
        else:
            direction = -1
        return (row + direction == row1
                and (col + 1 == col1 or col - 1 == col1))


class Bishop(Pieces):
    def __init__(self, color):
        super().__init__(color)
        self.move = False

    def can_move(self, board, row, col, row1, col1):
        if abs(row1 - row) == abs(col1 - col):
            return True
        return False

    def moved(self, move):
        self.move = move
        return self.move

    def char(self):
        return 'B'

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Knight(Pieces):
    def __init__(self, color):
        super().__init__(color)
        self.moved = False

    def can_move(self, board, row, col, row1, col1):
        if abs(col - col1) * abs(row - row1) == 2:
            return True
        return False

    def moved(self, move):
        self.move = move
        return self.move

    def char(self):
        return 'N'

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Queen(Pieces):
    def __init__(self, color):
        super().__init__(color)
        self.move = False

    def can_move(self, board, row, col, row1, col1):
        piece = board.get_piece(row1, col1)
        if not (piece is None) and piece.get_color() == self.color:
            return False

        if row == row1 or col == col1:

            if (row1 >= row):
                step = 1
            else:
                step = -1
            for r in range(row + step, row1, step):
                if not (board.get_piece(r, col) is None):
                    return False

            if (col1 >= col):
                step = 1
            else:
                step = -1
            for c in range(col + step, col1, step):
                if not (board.get_piece(row, c) is None):
                    return False

            return True

        if row - col == row1 - col1:
            if (row1 >= row):
                step = 1
            else:
                step = -1
            for r in range(row + step, row1, step):
                c = col - row + r
                if not (board.get_piece(r, c) is None):
                    return False
            return True

        if row + col == row1 + col1:
            if (row1 >= row):
                step = 1
            else:
                step = -1
            for r in range(row + step, row1, step):
                c = row + col - r
                if not (board.get_piece(r, c) is None):
                    return False
            return True

        return False

    def moved(self, move):
        self.move = move
        return self.move

    def char(self):
        return 'Q'

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class King(Pieces):
    def __init__(self, color):
        super().__init__(color)
        self.move = False

    def can_move(self, board, row, col, row1, col1):
        piece = board.get_piece(row1, col1)
        if not (piece is None) and piece.get_color() == self.color:
            return False
        if abs(row - row1) <= 1 and abs(col - col1) <= 1:
            return True
        return False

    def char(self):
        return 'K'

    def moved(self, move):
        self.move = move
        return self.move

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


def opponent(color):
    if color == WHITE:
        return BLACK
    else:
        return WHITE


def correct_coords(row, col):
    return 0 <= row < 8 and 0 <= col < 8


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Шахматы')
    chessboard = Сhessboard()
    timer_white = MyTimer('white')
    timer_black = MyTimer('black')
    size = width, height = 700, 480
    running = True
    screen = pygame.display.set_mode(size)
    board = Board(8, 8)
    board.set_view(0, 0, 60)  # изменение координат положения и размера клетки
    image_rookB = pygame.transform.scale(load_image('rookB.png'), (60, 60))
    image_rookW = pygame.transform.scale(load_image('rookW.png'), (60, 60))
    image_knightB = pygame.transform.scale(load_image('knightB.png'), (60, 60))
    image_knightW = pygame.transform.scale(load_image('knightW.png'), (60, 60))
    image_pawnW = pygame.transform.scale(load_image('pawnW.png'), (60, 60))
    image_pawnB = pygame.transform.scale(load_image('pawnB.png'), (60, 60))
    image_kingW = pygame.transform.scale(load_image('kingW.png'), (60, 60))
    image_kingB = pygame.transform.scale(load_image('kingB.png'), (60, 60))
    image_queenW = pygame.transform.scale(load_image('queenW.png'), (60, 60))
    image_queenB = pygame.transform.scale(load_image('queenB.png'), (60, 60))
    image_bishopB = pygame.transform.scale(load_image('bishopB.png'), (60, 60))
    image_bishopW = pygame.transform.scale(load_image('bishopW.png'), (60, 60))
    image_black = pygame.transform.scale(load_image('black2.png'), (60, 60))
    image_white = pygame.transform.scale(load_image('white2.png'), (60, 60))
    image_end = pygame.transform.scale(load_image('game-over-chessBlack.png'), (700, 480))
    board.render()
    timer_white.start()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        if timer_white.switched() and chessboard.color == 1:
            if timer_white.get_elapsed() < Time_white:
                Time_white = timer_white.get_elapsed()
                f1 = pygame.font.Font(None, 40)
                text1 = f1.render('{} min {} s'.format(str(Time_white // 60), str(Time_white % 60)), 1, (255, 0, 250))
                pygame.draw.rect(screen, 'black', ((490, 90), (200, 60)))
                screen.blit(text1, (490, 90))

                if Time_white == 0:
                    running = False

        elif timer_black.switched() and chessboard.color == 2:
            if timer_black.get_elapsed() < Time_black:
                Time_black = timer_black.get_elapsed()
                f1 = pygame.font.Font(None, 40)
                text1 = f1.render('{} min {} s'.format(str(Time_black // 60), str(Time_black % 60)), 1, (255, 0, 250))
                pygame.draw.rect(screen, 'black', ((490, 400), (200, 60)))
                screen.blit(text1, (490, 400))
                if Time_black == 0:
                    running = False
        if board.end():
            time.sleep(3)
            running = False

        pygame.display.flip()

    x_pos = -700
    v = 200  # пикселей в секунду
    running = True
    pygame.display.flip()
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if x_pos < 0:
            x_pos += v * clock.tick() / 1000  # v * t в секундах
        screen.blit(image_end, (x_pos, 0))
        pygame.display.flip()
    pygame.quit()
