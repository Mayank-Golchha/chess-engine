from Chess_5.Board import Board
from Chess_5.Engine import Engine
import pygame

pygame.init()
screen = pygame.display.set_mode((400,400))
pygame.display.set_caption('Chess Board')


class Game:
    def __init__(self,engine_color):
        self.piece_images = {
        "wking": pygame.image.load("Data/White_King.svg"),
        "bking": pygame.image.load("Data/Black_King.svg"),
        "wqueen": pygame.image.load("Data/White_Queen.svg"),
        "bqueen": pygame.image.load("Data/Black_Queen.svg"),
        "wrook": pygame.image.load("Data/White_Rook.svg"),
        "brook": pygame.image.load("Data/Black_Rook.svg"),
        "wbishop": pygame.image.load("Data/White_Bishop.svg"),
        "bbishop": pygame.image.load("Data/Black_Bishop.svg"),
        "wknight": pygame.image.load("Data/White_Knight.svg"),
        "bknight": pygame.image.load("Data/Black_Knight.svg"),
        "wpawn": pygame.image.load("Data/White_Pawn.svg"),
        "bpawn": pygame.image.load("Data/Black_Pawn.svg"),
        }
        self.selected_piece = None

        self.engine_color = engine_color
        self.move_index = 0

        positions = [
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']]
        # positions = [
        #     ['R','N','','Q','K','B','N','R'],
        #     ['P','P','P','P','P','P','P','P'],
        #     ['', '', '', '', '', '', '', ''],
        #     ['', '', 'B', '', '', '', '', ''],
        #     ['', '', '', '', '', '', '', ''],
        #     ['', '', '', '', '', '', '', ''],
        #     ['p','p','p','','p','p','p','p'],
        #     ['r','n','n','q','k','b','n','r']
        #
        # ]
        self.board = Board(positions)

        self.constant = []

        self.turn = 1

        self.history = []

    def Draw_Board(self):
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 0:
                    color = (255, 206, 158)  # Light color for white squares
                else:
                    color = (209, 139, 71)  # Dark color for black squares
                pygame.draw.rect(screen, color, (col * 50, row * 50, 50, 50))

        for i in self.board.all_positions:
            self.Draw_Piece(i)

        if self.constant:
            surface = pygame.Surface((50, 50))
            surface.fill(pygame.Color('red'))
            for i in self.constant[-1][1:]:
                if not len(i) == 4:
                    screen.blit(surface, (i[0] * 50, i[1] * 50))
                else:
                    screen.blit(surface,(i[1][0]*50,i[1][1]*50))
            pygame.display.flip()

    def Draw_Piece(self,piece):
        if piece[0] != '':
            if piece[0].isupper():
                if piece[0].lower() == 'k':
                    piece_image = self.piece_images['wking']
                elif piece[0].lower() == 'q':
                    piece_image = self.piece_images['wqueen']
                elif piece[0].lower() == 'r':
                    piece_image = self.piece_images['wrook']
                elif piece[0].lower() == 'b':
                    piece_image = self.piece_images['wbishop']
                elif piece[0].lower() == 'n':
                    piece_image = self.piece_images['wknight']
                elif piece[0].lower() == 'p':
                    piece_image = self.piece_images['wpawn']
            else:
                if piece[0].lower() == 'k':
                    piece_image = self.piece_images['bking']
                elif piece[0].lower() == 'q':
                    piece_image = self.piece_images['bqueen']
                elif piece[0].lower() == 'r':
                    piece_image = self.piece_images['brook']
                elif piece[0].lower() == 'b':
                    piece_image = self.piece_images['bbishop']
                elif piece[0].lower() == 'n':
                    piece_image = self.piece_images['bknight']
                elif piece[0].lower() == 'p':
                    piece_image = self.piece_images['bpawn']
            screen.blit(piece_image, (piece[1] * 50, piece[2] * 50))

    def erase_piece(self, position):
        if len(position) != 4:
            row, col = position[0],position[1]
            if (row + col) % 2 == 0:
                color = (255, 0, 0)  # Light color for white squares
            else:
                color = (209, 139, 71)  # Dark color for black squares

            pygame.draw.rect(screen, color, (row * 50, col * 50, 50, 50))
        else:
            self.erase_piece(position[1])
            self.erase_piece(position[3])

    def Move(self,move):
        old = move[0]
        new = move[1]
        self.erase_piece(old[1:])
        self.erase_piece(new)
        # self.history.append(move)
        self.board.Move(move)
        pygame.display.flip()
        if self.turn == 1:
            self.turn = 2
        else:
            self.turn = 1

        self.move_index += 1

    def Write_Game(self):
        file = open('Data/game_data.txt','a')
        g = ''
        for y in self.board.positions:
            k = ''
            for x in y:
                if x == '':
                    k += '.'
                else:
                    k += x
            g += k + ' '
        file.write(g[:-1] + '\n')
        file.close()

    def Three_Fold_Repition(self):
        file = open('Data/game_data.txt','r')
        f = file.read().split('\n')
        current = f[-1]
        if current == '' or current == '\n':
            current = f[-2]
        if f.count(current) == 3:
            print('THREE FOLD REPITITION')
            file.close()
            exit()
        file.close()

    def Game(self):
        file = open('Data/game_data.txt','w')
        file.close()
        while True:
            l = self.board.Legal_Moves()
            if l:
                l = l[0]

            if self.board.Check_Mate(l):
                if self.board.color == 1:
                    print("Winner is White!!")
                else:
                    print("Winner is Black!!")
                exit()
            elif self.board.StaleMate(l):
                print('DRAW BY STALEMATE')
                exit()
            self.Draw_Board()
            pygame.display.flip()

            if self.engine_color == self.turn:
                move = Engine(self.board.positions, self.engine_color,self.board.chess_notation,self.move_index).Best_Move(
                    Board(self.board.positions, self.engine_color), 2, True)
                self.Move(move)

            else:
                if self.turn == 1:
                    kk = 7
                else:
                     kk = 0
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        x,y = event.pos
                        x,y = x//50,y//50

                        if self.selected_piece == None:
                            moves = self.board.Legal_Moves()[0]
                            print(moves)
                            self.selected_piece = [self.board.positions[y][x],x,y]
                            valid = [i for i in moves if i[0] == self.selected_piece]
                            if valid:
                                valid = valid[0]
                                surface = pygame.Surface((50, 50))
                                surface.fill(pygame.Color('red'))
                                for i in valid[1:]:
                                    if not len(i) == 4:
                                        screen.blit(surface, (i[0] * 50, i[1] * 50))
                                    else:
                                        screen.blit(surface, (i[1][0] * 50, i[1][1] * 50))

                                pygame.display.flip()
                            else:
                                valid = []
                            self.constant = [valid]
                        else:
                            if self.constant[-1]:
                                move = [self.constant[-1][0],[x,y]]
                                a = [x,y]
                                if a not in [i[1:] for i in self.board.ally_team]:
                                    if a in self.constant[-1]:
                                        self.Move(move)
                                        if a[1] == kk and self.constant[-1][0][0].lower() == 'p':
                                            pp = input('Which Peice Queen(1),Rook(2),Bishop(3),Knight(4) : ')
                                            if pp.isdigit():
                                                pp = int(pp)
                                            else:
                                                pp = input('Which Peice Queen(1),Rook(2),Bishop(3),Knight(4) in integers : ')
                                            if self.turn == 1:
                                                if pp == 1:
                                                    self.board.positions[move[1][1]][move[1][0]] = 'q'
                                                elif pp == 2:
                                                    self.board.positions[move[1][1]][move[1][0]] = 'r'
                                                elif pp == 3:
                                                    self.board.positions[move[1][1]][move[1][0]] = 'b'
                                                elif pp == 4:
                                                    self.board.positions[move[1][1]][move[1][0]] = 'n'

                                            else:
                                                if pp == 1:
                                                    self.board.positions[move[1][1]][move[1][0]] = 'Q'
                                                elif pp == 2:
                                                    self.board.positions[move[1][1]][move[1][0]] = 'R'
                                                elif pp == 3:
                                                    self.board.positions[move[1][1]][move[1][0]] = 'B'
                                                elif pp == 4:
                                                    self.board.positions[move[1][1]][move[1][0]] = 'N'

                                    else:
                                        if len(self.constant[-1]) > 2:
                                            for j in self.constant[-1][1:]:
                                                if a in j:
                                                    self.Move(j)
                                self.selected_piece = None
                                self.constant = []

                    elif event.type == pygame.MOUSEMOTION:
                        pass


a = Game(1).Game()
# a = Game(1).Three_Fold_Repition()




