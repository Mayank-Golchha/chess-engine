from Chess_5.Board import Board
from copy import deepcopy
from Chess_5.constants import king_table,queen_table,rook_table,bishop_table,knight_table,pawn_table
import random

#     def Mini_Max(self,board,N):
#         moves = self.Legal_Moves_To_List(self.legal_moves)
#         score = []
#         for move in moves:
#             temp = deepcopy(board)
#             temp.Move(move)
#             legal,pinned = temp.Legal_Moves()
#             check_mate = temp.Check_Mate(legal)
#             stale_mate = temp.StaleMate(legal)
#
#             if check_mate:
#                 return move
#             elif stale_mate:
#                 value = 1000
#                 if self.color != temp.color:
#                     score.append(-value)
#                 else:
#                     score.append(value)
#             else:
#                 if N > 1:
#                     temp_best_move = self.Mini_Max(temp,N-1)
#                     temp.Move(temp_best_move)
#                 e = temp.Evaluation()
#                 if temp.color != self.color:
#                     e = -1*e
#                 score.append(e)
#         # for i in range(len(score)):
#         #     print(moves[i])
#         #     print(score[i])
#         #     print()
#         if board.color == self.color:
#             best_move = moves[score.index(max(score))]
#         else:
#             best_move = moves[score.index(min(score))]
#         return best_move
#
#
#
# a = Engine(1)
# print(a.Legal_Moves_To_List(a.legal_moves))
# print(a.Mini_Max(a.board,3))
#


class Engine:
    def __init__(self,positions,color,chess_notations_history = None,move_index=0):
        self.all_positions = []
        self.color = color
        self.positions = positions
        self.chess_notations_history = chess_notations_history
        self.move_index = move_index

        for y in range(8):
            for x in range(8):
                self.all_positions.append([self.positions[y][x], x, y])

        self.white_team = [i for i in self.all_positions if i[0].isupper()]
        self.black_team = [i for i in self.all_positions if i[0].islower()]

        self.white_king = [i for i in self.white_team if i[0] == 'K'][0]
        self.black_king = [i for i in self.black_team if i[0] == 'k'][0]
        if self.color == 1:
            self.ally_king = self.white_king
            self.enemy_king = self.black_king
        else:
            self.ally_king = self.black_king
            self.enemy_king = self.white_king

        self.king_table = king_table
        self.queen_table = queen_table
        self.rook_table = rook_table
        self.bishop_table = bishop_table
        self.knight_table = knight_table
        self.pawn_table = pawn_table

        self.tempoerary = []

        self.peice_value = {'k':30000,'q':900,'r':500,'b':350,'n':300,'p':100}

        self.chess_notation = ''

    def All_Legal_Move(self,legal_moves):
        moves = []
        for i in legal_moves:
            for j in i[1:]:
                moves.append([i[0],j])
        return moves

    def Read_Game(self):
        if self.chess_notations_history:
            s = self.chess_notations_history
            kk = [i for i in s.split() if '.' not in s]
            # j = len(s)//2
            length = len(self.chess_notations_history)
            f = open('D:/Project/Chess_4/Data/openings.txt').read()
            f = f.split('\n')
            # good = [i for i in f if i[:length] == s]
            good = [i for i in f if s in i]

            if good:
                choice = random.choice(good).split()
                choice = [i for i in choice if '.' not in i]
                return choice[self.move_index]
                # return choice[j]
            else:
                return None
        else:
            f = open('D:/Project/Chess_4/Data/openings.txt').read()
            f = f.split('\n')
            g = [i for i in f]
            choice = random.choice(g).split()
            return choice[1]

    def Convert_Back(self,move, legal_moves,color):
        t = ['R', 'B', 'N', 'Q', 'K']
        x_coor = {
            'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7
        }
        if 'x' not in move:
            p = move[0]
            if p not in t:
                r = [i for i in legal_moves if i[0][0].lower() == 'p']
                k = [x_coor[p], int(move[1]) - 1]
                ss = [i for i in r if k in i][0]
                return [ss[0], [x_coor[p], int(move[1]) - 1]]
            else:
                r = [i for i in legal_moves if i[0][0].lower() == p.lower()]
                m = [x_coor[move[1]], int(move[2]) - 1]
                f = [i for i in r if m in i][0]
                return [f[0], [x_coor[move[1]], int(move[2]) - 1]]
        elif 'x' in move:
            if 'P' in move:
                r = [i for i in legal_moves if i[0][0].lower() == 'p' and i[0][1] == move[0]]
                k = [x_coor[move[2]], int(move[3]) - 1]
                t = [i for i in r if k in i][0]
                return [t[0], k]
            else:
                r = [i for i in legal_moves if i[0][0].lower() == move[0]]
                k = [x_coor[move[2]], int(move[3]) - 1]
                t = [i for i in r if k in i][0]
                return [t[0], k]
        elif 'o' in move:
            if 'o-o' in move:
                if color == 1:
                    return [['K',4,0],[6,0],['R',7,0],[5,0]]
                else:
                    return [['k',4,7],[6,7],['r',7,7],[5,7]]
            else:
                if color == 1:
                    return [['K',4,0],[2,0],['R',0,0],[3,0]]
                else:
                    return [['k',4,7],[2,7],['r',0,7],[3,7]]

    def Position_Value(self,peice,color):
        a = peice[0]
        b = peice[1]
        c = peice[2]
        if peice[0].isupper():
            if a == 'K':
                return self.king_table[c][b]
            elif a == "Q":
                return self.queen_table[c][b]
            elif a == "R":
                return self.rook_table[c][b]
            elif a == "B":
                return self.bishop_table[c][b]
            elif a == "N":
                return self.knight_table[c][b]
            elif a == "P":
                return self.pawn_table[c][b]
        else:
            if a == 'k':
                return self.king_table[::-1][c][b]
            if a == 'q':
                return self.queen_table[::-1][c][b]
            if a == 'r':
                return self.rook_table[::-1][c][b]
            if a == 'b':
                return self.bishop_table[::-1][c][b]
            if a == 'n':
                return self.knight_table[::-1][c][b]
            if a == 'p':
                return self.pawn_table[::-1][c][b]

    def Stacked_Pawns(self,color):
        l = zip(i for i in self.positions)
        if color == 1:
            stacked = [i.count('P') for i in l]
        else:
            stacked = [i.count('p') for i in l]
        score = 0
        for i in stacked:
            if i > 1:
                score += 5 * i
        return -score

    def Evaluation(self,positions_,color):
        positions_all = []
        for y in range(8):
            for x in range(8):
                positions_all.append([positions_[y][x], x, y])
        white_team = [i for i in positions_all if i[0].isupper()]
        black_team = [i for i in positions_all if i[0].islower()]
        white_board = Board(positions_,1)
        black_board = Board(positions_,2)
        try:
            white_legal,white_pinned = white_board.Legal_Moves()

        except:
            # print(Exception)
            if white_board.Check_Mate([]):
                if color == self.color:
                    return -30000
                else:
                    return 30000
        try:
            black_legal,black_pinned = black_board.Legal_Moves()

        except:
            if black_board.Check_Mate([]):
                if color == self.color:
                    return -30000
                else:
                    return 30000


        white_peice_value = [self.peice_value[i[0].lower()] for i in white_team]
        black_peice_value = [self.peice_value[i[0].lower()] for i in black_team]

        white_position_value = sum([self.Position_Value(i,1) for i in white_team])
        black_position_value = sum([self.Position_Value(i,2) for i in black_team])

        white_check = white_board.no_of_check
        black_check = black_board.no_of_check

        white_stacked_pawn = self.Stacked_Pawns(1)
        black_stacked_pawn = self.Stacked_Pawns(2)

        length_moves = (len(white_legal) - len(black_legal))*5
        peice_value = sum(white_peice_value) - sum(black_peice_value)
        pinned_peice_value = -(len(white_pinned)-len(black_pinned))*10
        checks = (white_check-black_check)*25
        positions_value = (white_position_value-black_position_value)
        stacked_pawns = white_stacked_pawn - black_stacked_pawn

        evaluation = length_moves + peice_value + pinned_peice_value + checks + positions_value + stacked_pawns

        if color == 1:
            return evaluation
        else:
            return -1*evaluation

    def MiniMax(self,board,depth,is_maximizing):
        if depth == 0:
            return self.Evaluation(board.positions,self.color)

        moves = self.All_Legal_Move(board.Legal_Moves()[0])

        if is_maximizing:
            best_move = -9999
            for move in moves:
                if move[1] == board.ally_king[1:]:
                    return -30000
                elif move[1] == board.enemy_king[1:]:
                    return 30000
                else:
                    temp = deepcopy(board)
                    temp.Move(move)
                    best_move = max(best_move,self.MiniMax(temp,depth-1,not is_maximizing))
            return best_move
        else:
            best_move = 9999
            for move in moves:
                if move[1] == board.ally_king[1:]:
                    return -30000
                elif move[1] == board.enemy_king[1:]:
                    return 30000
                else:
                    temp = deepcopy(board)
                    temp.Move(move)
                    best_move = min(best_move,self.MiniMax(temp,depth-1,not is_maximizing))
            return best_move

    def Best_Move(self,board,depth,is_maximizing):
        legal_moves = self.All_Legal_Move(board.Legal_Moves()[0])
        try:
            m = self.Read_Game()
            if m:
                return self.Convert_Back(m,legal_moves,self.color)
        except:
            pass
        best_value = -9999
        final_move = None
        for move in legal_moves:
            if move[1] == board.ally_king[1:]:
                best_value = -30000

                # final_move = None
            elif move[1] == board.enemy_king[1:]:
                return move
            else:
                temp = deepcopy(board)
                temp.Move(move)
                value = max(best_value,self.MiniMax(temp,depth-1,not is_maximizing))
                if value > best_value:
                    best_value = value
                    final_move = move
        return final_move

# positions = [
#     ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
#     ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
#     ['', '', '', '', '', '', '', ''],
#     ['', '', '', '', '', '', '', ''],
#     ['', '', '', '', '', '', '', ''],
#     ['', '', '', '', '', '', '', ''],
#     ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
#     ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']]
# a = Engine(positions,1).Best_Move(Board(positions),3,True)
# print(a)
#
#

