import copy
from Chess_5.constants import king_table,queen_table,rook_table,bishop_table,knight_table,pawn_table


class Board:
    def __init__(self,positions = None,color=1,history = None):
        # it is considered king is on right side of queen
        if not positions:
            self.positions = [
                ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
                ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                ['', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', ''],
                ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']]
        else:
            self.positions = positions

        # if color:
        self.color = color
        # else:
        #     self.color = 1

        self.all_positions = []
        if history:
            self.history = history
        else:
            self.history = []
        self.chess_notation = ''

        for y in range(8):
            for x in range(8):
                self.all_positions.append([self.positions[y][x],x,y])

        if self.color == 1:
            self.ally_team = [i for i in self.all_positions if i[0].isupper()]
            self.enemy_team = [i for i in self.all_positions if i[0].islower()]
        else:
            self.ally_team = [i for i in self.all_positions if i[0].islower()]
            self.enemy_team = [i for i in self.all_positions if i[0].isupper()]

        self.ally_peices = [i[0] for i in self.ally_team]
        self.enemy_peices = [i[0] for i in self.enemy_team]

        self.ally_queen = []
        self.ally_rook = []
        self.ally_bishop = []
        self.ally_knight = []
        self.ally_pawn = []

        self.enemy_queen = []
        self.enemy_rook = []
        self.enemy_bishop = []
        self.enemy_knight = []
        self.enemy_pawn = []

        for i in self.ally_team:
            if i[0].lower() == 'k':
                self.ally_king = i
            if i[0].lower() == 'q':
                self.ally_queen.append(i)
            if i[0].lower() == 'r':
                self.ally_rook.append(i)
            if i[0].lower() == 'b':
                self.ally_bishop.append(i)
            if i[0].lower() == 'n':
                self.ally_knight.append(i)
            if i[0].lower() == 'p':
                self.ally_pawn.append(i)

        for i in self.enemy_team:
            if i[0].lower() == 'k':
                self.enemy_king = i
            if i[0].lower() == 'q':
                self.enemy_queen.append(i)
            if i[0].lower() == 'r':
                self.enemy_rook.append(i)
            if i[0].lower() == 'b':
                self.enemy_bishop.append(i)
            if i[0].lower() == 'n':
                self.enemy_knight.append(i)
            if i[0].lower() == 'p':
                self.enemy_pawn.append(i)

        if not self.ally_king:
            print('No Ally King')
            exit()

        if not self.enemy_king:
            print('No Enemy King')
            exit()

        self.en_passant = False
        self.castling_k = False
        self.castling_q = False

        self.check_attackers = self.Check()
        if self.check_attackers:
            self.check = True
        else:
            self.check = False
        self.no_of_check = len(self.check_attackers)

        self.king_table = king_table
        self.queen_table = queen_table
        self.rook_table = rook_table
        self.bishop_table = bishop_table
        self.knight_table = knight_table
        self.pawn_table = pawn_table

        if self.color == 2:
            self.king_table = self.king_table[::-1]
            self.queen_table = self.queen_table[::-1]
            self.rook_table = self.rook_table[::-1]
            self.bishop_table = self.bishop_table[::1]
            self.knight_table = self.knight_table[::-1]
            self.pawn_table = self.pawn_table[::-1]

        x = self.ally_king[1]
        x1 = self.enemy_king[1]
        y = self.ally_king[2]
        y1 = self.enemy_king[2]
        self.ally_king_moves = [[x+1,y],[x,y+1],[x+1,y+1],[x-1,y],[x,y-1],[x-1,y-1],[x-1,y+1],[x+1,y-1]]
        self.enemy_king_moves = [[x1+1,y1],[x1,y1+1],[x1+1,y1+1],[x1-1,y1],[x1,y1-1],[x1-1,y1-1],[x1-1,y1+1],[x1+1,y1-1]]
        self.ally_king_moves = [i for i in self.ally_king_moves if i[0] >= 0 and i[1] >= 0 and i[0] < 8 and i[1] < 8]
        self.enemy_king_moves = [i for i in self.enemy_king_moves if i[0] >= 0 and i[1] >= 0 and i[0] < 8 and i[1] < 8]

        self.peice_value = {'k':20000,'q':900,'r':500,'b':350,'n':300,'p':100}

    def Teams(self,color):
        if color == 1:
            return [self.all_positions[i] for i in range(64) if self.all_positions[i][0].isupper()]
        else:
            return [self.all_positions[i] for i in range(64) if self.all_positions[i][0].islower()]

    # @property
    # def color(self):
    #     return self._color
    #
    # @color.setter
    # def color(self,value):
    #     self._color = value
    def Update(self,color):
        if color == 1:
            color = 2
        else:
            color = 1
        new_class = Board(self.positions,color)
        self.__dict__.update(new_class.__dict__)

    def Convert_String_To_Notation(self,move):
        old = move[0]
        new = move[1]
        x = move[1][0]
        y = move[1][1]
        x_coor = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
        k = ''
        if self.check:
            k = '+'

        if old[0].lower() == 'p':
            if old[1] == new[0]:
                return x_coor[x] + str(y+1)+k
            else:
                return x_coor[old[1]] + 'x' + x_coor[x] + str(y+1)+k
        else:
            if len(new) != 4:
                attack = self.positions[y][x]
                if attack == '' or self.ally_enemy_string(attack):
                    return old[0].upper() + x_coor[x] + str(y+1)+k
                else:
                    return old[0].upper() + 'x' + x_coor[x] + str(y+1)+k
            else:
                if x == 3:
                    return '0-0'
                else:
                    return '0-0-0'

    def Move(self,move,copy_ = False):
        old = move[0]
        new = move[1]

        if copy_ == False:
            self.history.append(move)
            if len(self.history) % 2 == 0:
                black = self.history[-1]
                self.chess_notation += ' ' + self.Convert_String_To_Notation(black)
            else:
                white = self.history[-1]
                index = int(len(self.history) // 2) + 1
                if index != 1:
                    index = ' ' + str(index)
                self.chess_notation += str(index) + '. ' + self.Convert_String_To_Notation(white)

            if self.color == 1:
                color = 2
                self.color = 2
            else:
                color = 1
                self.color = 1
            if len(move) == 4:
                self.positions[move[0][2]][move[0][1]] = ''
                self.positions[move[1][1]][move[1][0]] = move[0][0]
                self.positions[move[2][2]][move[2][1]] = ''
                self.positions[move[3][1]][move[3][0]] = move[2][0]

            elif len(move[1]) == 4:
                king_ = new[0]
                king_m = new[1]
                rook_ = new[2]
                rook_m = new[3]
                self.positions[king_[2]][king_[1]] = ''
                self.positions[king_m[1]][king_m[0]] = king_[0]
                self.positions[rook_[2]][rook_[1]] = ''
                self.positions[rook_m[1]][rook_m[0]] = rook_[0]
                # self.Move(move[2:])
            else:
                self.positions[old[2]][old[1]] = ''
                self.positions[new[1]][new[0]] = old[0]

            new_class = Board(self.positions,color)
            h = self.history.copy()
            n = copy.copy(self.chess_notation)
            self.__dict__.update(new_class.__dict__)
            self.history = h
            self.chess_notation = n

            return self.positions
        else:
            # if self.color == 1:
            #     self.color = 2
            # else:
            #     self.color = 1
            positions = copy.deepcopy(self.positions)
            if len(move[1]) == 4:
                king_ = new[0]
                king_m = new[1]
                rook_ = new[2]
                rook_m = new[3]
                positions[king_[2]][king_[1]] = ''
                positions[king_m[1]][king_m[0]] = king_[0]
                positions[rook_[2]][rook_[1]] = ''
                positions[rook_m[1]][rook_m[0]] = rook_[0]
            # if len(move) == 4:
            #     positions = self.Move(move[2:], True)
            else:
                positions[old[2]][old[1]] = ''
                positions[new[1]][new[0]] = old[0]
            return positions

    def ally_enemy_string(self,string):
        if self.color == 1:
            if string.isupper():
                return True
            else:
                return False
        else:
            if string.islower():
                return True
            else:
                return False

    def Rook_Bishop_legal(self,positions,peice):
        index = positions.index(peice)
        p_left = positions[:index][::-1]
        p_right = positions[index+1:]

        moves = []
        for i in p_left:
            if self.positions[i[1]][i[0]] == '' or self.positions[i[1]][0] == ' ':
                moves.append(i)
            elif self.ally_enemy_string(self.positions[i[1]][i[0]]):
                break
            elif not self.ally_enemy_string(self.positions[i[1]][i[0]]):
                moves.append(i)
                break
        moves = moves[::-1]

        for i in p_right:
            if self.positions[i[1]][i[0]] == '' or self.positions[i[1]][0] == ' ':
                moves.append(i)
            elif self.ally_enemy_string(self.positions[i[1]][i[0]]):
                break
            elif not self.ally_enemy_string(self.positions[i[1]][i[0]]):
                moves.append(i)
                break
        return moves

    def Move_Rook(self,peice):
        x = peice[1]
        y = peice[2]

        x_axis = [[i,y] for i in range(8)]
        y_axis = [[x,i] for i in range(8)]

        return self.Rook_Bishop_legal(x_axis,[x,y]) + self.Rook_Bishop_legal(y_axis,[x,y])

    def Move_Bishop(self,peice):
        x = peice[1]
        y = peice[2]

        diff1 = y - x
        diff2 = y + x
        x_coor = [[i, i + diff1] for i in range(8) if (i + diff1 >= 0 and i + diff1 < 8)]
        y_coor = [[i, -i + diff2] for i in range(8) if (-i + diff2 < 8 and - i + diff2 >= 0)]

        return self.Rook_Bishop_legal(x_coor,[x,y]) + self.Rook_Bishop_legal(y_coor,[x,y])

    def Move_Queen(self,peice):
        a = self.Move_Rook(peice)
        b = self.Move_Bishop(peice)
        if a and not b:
            return a
        elif not a and b:
            return b
        else:
            return a + b
        # if a and b:
        #     return a + b

    def Move_Knight(self,peice):
        moves = [[peice[1] + 1, peice[2] + 2], [peice[1] + 2, peice[2] + 1], [peice[1] - 1, peice[2] - 2],
                 [peice[1] - 2, peice[2] - 1], [peice[1] - 1, peice[2] + 2], [peice[1] + 1, peice[2] - 2],
                 [peice[1] - 2, peice[2] + 1], [peice[1] + 2, peice[2] - 1]]
        ally = [i[1:] for i in self.ally_team]
        moves = [i for i in moves if i[0] >= 0 and i[1] >= 0 and i[1] < 8 and i[0] < 8]
        moves = [i for i in moves if i not in ally]

        return moves

    def Move_Pawn(self,peice):
        x = peice[1]
        y = peice[2]
        a = [x,y+1]
        b = [x,y+2]
        c = [x+1,y+1]
        d = [x-1,y+1]
        e = [x+1,4] #c
        f = [x-1,4] #d
        k = 1
        l = 4

        enemy = [i[1:] for i in self.enemy_team]

        if self.color == 2:
            # a[1] = 7 - a[1]
            # b[1] = 7 - b[1]
            # c[1] = 7 - c[1]
            # d[1] = 7 - d[1]
            # e[1] = 7 - e[1]
            # f[1] = 7 - f[1]
            # k = 7 - k
            # l = 7 - l
            a[1] = a[1] - 2
            # b[1] = b[1] - 3
            b[1] = y - 2
            c[1] = c[1] - 2
            d[1] = d[1] - 2
            e[1] = 7 - e[1]
            f[1] = 7 - f[1]
            k = 7-k
            l = l - 2

        moves = []

        if a[0] >= 0 and a[1] < 8:
            if self.positions[a[1]][a[0]] == '' and a[1] < 8 and a[1] >= 0:
                moves.append(a)

        if b[0] >= 0 and b[1] < 8:
            if self.positions[b[1]][b[0]] == '' and y == k:
                moves.append(b)

        if c in enemy:
            moves.append(c)

        if d in enemy:
            moves.append(d)

        if self.history:
            if self.history[-1][-1] == e and y == l:
                self.en_passant = True
                moves.append(c)

            if self.history[-1][-1] == f and y == l:
                self.en_passant = True
                moves.append(d)

        return moves

    def Move_King(self,peice):
        x = peice[1]
        y = peice[2]
        ally = [i[1:] for i in self.ally_team]
        moves = [[x, y + 1], [x + 1, y], [x + 1, y + 1], [x - 1, y], [x, y - 1], [x + 1, y - 1], [x - 1, y + 1],
                 [x - 1, y - 1]]
        moves = [i for i in moves if i[0] >= 0 and i[1] >= 0 and i[0] < 8 and i[1] < 8]
        moves = [i for i in moves if i not in ally]

        a = [x-2,0]
        b = [x+2,0]
        c = [0,0]
        d = [7,0]
        e = [5,0]
        f = [6,0]
        g = [3,0]
        h = [2,0]
        i = [1,0]
        if self.color == 2:
            a[1] = 7-a[1]
            b[1] = 7-b[1]
            c[1] = 7-c[1]
            d[1] = 7-d[1]
            e[1] = 7-e[1]
            f[1] = 7-f[1]
            g[1] = 7-g[1]
            h[1] = 7-h[1]
            i[1] = 7-i[1]

        if self.history:
            x_ = [i[0][0] for i in self.history]
            y_ = [i[0] for i in self.history]
        else:
            x_ = []
            y_ = []

        if self.color == 1:
            if 'K' not in x_:
                if ['R'] + c not in y_ and not self.check and self.positions[g[1]][g[0]] == '' and self.positions[h[1]][h[0]] == '' and self.positions[i[1]][i[0]] == '' and self.positions[c[1]][c[0]] == 'R':
                    moves.append([peice,a,['R']+c,[x-1,a[1]]])
                    self.castling_q = True

                if ['R'] + d not in y_ and not self.check and self.positions[e[1]][e[0]] == '' and self.positions[f[1]][f[0]] == '' and self.positions[d[1]][d[0]] == 'R':
                    moves.append([peice,b,['R']+d,[x+1,b[1]]])
                    self.castling_k = True
        else:
            if 'k' not in x_:
                if ['r'] + c not in y_ and not self.check and self.positions[g[1]][g[0]] == '' and self.positions[h[1]][h[0]] == '' and self.positions[i[1]][i[0]] == '' and self.positions[c[1]][c[0]] == 'r':
                    moves.append([peice, a, ['r'] + c, [x - 1, a[1]]])
                    self.castling_q = True

                if ['r'] + d not in y_ and not self.check and self.positions[e[1]][e[0]] == '' and self.positions[f[1]][f[0]] == '' and self.positions[c[1]][c[0]] == 'r':
                    moves.append([peice, b, ['r'] + d, [x + 1, b[1]]])
                    self.castling_k = True

        return moves

    def Moves_Between_Peices(self,p1,p2):
        if p1[0] == p2[0]:
            positions = [[p1[0],i] for i in range(min(p1[1],p2[1])+1,max(p1[1],p2[1]))]
        else:
            m = int((p2[1] - p1[1]) / (p2[0] - p1[0]))
            positions = [[i,p1[1] + m*i] for i in range(min(p1[0],p2[0])+1,max(p1[0],p2[0]))]
        positions = [i for i in positions if i[1] >= 0 and i[0] >= 0 and i[1] < 8 and i[1] < 8]
        return positions

    def Pseudo_Move(self):
        moves = []
        king_move = self.Move_King(self.ally_king)
        moves.append([self.ally_king] + king_move)

        for i in self.ally_rook:
            k = self.Move_Rook(i)
            if k:
                moves.append([i] + k)
        for i in self.ally_bishop:
            k = self.Move_Bishop(i)
            if k:
                moves.append([i]+k)
        for i in self.ally_queen:
            k = self.Move_Queen(i)
            if k:
                moves.append([i]+k)
        for i in self.ally_knight:
            k = self.Move_Knight(i)
            if k:
                moves.append([i]+k)

        for i in self.ally_pawn:
            k = self.Move_Pawn(i)
            if k:
                moves.append([i]+k)

        moves = [i for i in moves if len(i) > 1]
        return moves

    def Is_Pinned(self,king,enemy_peice):
        b_moves = self.Moves_Between_Peices(king[1:],enemy_peice[1:])
        k = 0
        s = None
        if b_moves:
            for i in b_moves:
                if self.ally_enemy_string(self.positions[i[1]][i[0]]):
                    k+=1
                    s = i
                else:
                    if self.color == 1:
                        if self.positions[i[1]][i[0]].islower():
                            return None
                    elif self.color == 2:
                        if self.positions[i[1]][i[0]].isupper():
                            return None
                if k == 2:
                    break
            if k == 1:
                return [[self.positions[s[1]][s[0]],s[0],s[1]],enemy_peice[1:]] + b_moves
            else:
                return None
        else:
            return None

    def Pinned_Peice(self):
        pinned = []
        for i in self.enemy_rook:
            k = self.Is_Pinned(self.ally_king,i)
            if k:
                pinned.append(k)

        for i in self.enemy_queen:
            k = self.Is_Pinned(self.ally_king,i)
            if k:
                pinned.append(k)

        for i in self.enemy_bishop:
            k = self.Is_Pinned(self.ally_king,i)
            if k:
                pinned.append(k)

        return pinned

    def Check(self):
        peices = []

        rook = self.Move_Rook(self.ally_king)
        bishop = self.Move_Bishop(self.ally_king)
        knight = self.Move_Knight(self.ally_king)

        rook_e = [i[1:] for i in self.enemy_rook]
        bishop_e = [i[1:] for i in self.enemy_bishop]
        queen_e = [i[1:] for i in self.enemy_queen]
        knight_e = [i[1:] for i in self.enemy_knight]
        pawn_e = [i[1:] for i in self.enemy_pawn]

        for i in rook:
            if i in rook_e:
               peices.append(i)

            if i in queen_e:
                peices.append(i)

        for i in bishop:
            if i in bishop_e:
                peices.append(i)

            if i in queen_e:
                peices.append(i)

        for i in knight_e:
            if i in knight:
                peices.append(i)
                break

        if self.color == 1:
            x = self.ally_king[1]
            y = self.ally_king[2]
            a = [x+1,y+1]
            b = [x-1,y+1]
            if a in pawn_e:
                peices.append(a)
            if b in pawn_e:
                peices.append(b)
        else:
            x = self.ally_king[1]
            y = self.ally_king[2]
            a = [x+1, y-1]
            b = [x-1, y-1]
            if a in pawn_e:
                peices.append(a)
            if b in pawn_e:
                peices.append(b)

        return peices

    def Legal_Moves(self):
        check_attackers = self.check_attackers
        n = self.no_of_check
        pinned_peice = self.Pinned_Peice()
        pseudo_moves = self.Pseudo_Move()
        legal_moves = []
        king_moves = [i for i in pseudo_moves if i[0][0].lower() == 'k']

        if pinned_peice:
            for i in pinned_peice:
                if i[0][0].lower() != 'k':
                    a = self.positions[i[1][1]][i[1][0]]
                    if a.lower() in ['r','q']:
                        # try:
                        k = [j for j in pseudo_moves if j[0] == i[0]]
                        if k:
                            k = k[0]

                            if i[0][0].lower() in ['p','r','q']:

                                if i[0][0].lower() != 'p':
                                    legal_moves.append(i)
                                    pseudo_moves.remove(k)
                                else:
                                    s = []
                                    for x in k:
                                        if x in i[2:]:
                                            s.append(x)
                                    legal_moves.append([k[0]] + s)
                                    pseudo_moves.remove(k)
                            else:
                                pseudo_moves.remove(k)

        if n == 0:
            if king_moves:
                k = [self.ally_king]
                for i in king_moves[0][1:]:
                    new_board = self.Move([self.ally_king,i],True)
                    b = Board(new_board,self.color)

                    if not b.Check():
                        k.append(i)
                if len(k) > 1:
                    legal_moves.append(k)
                pseudo_moves.remove(king_moves[0])
            return legal_moves + pseudo_moves,pinned_peice
        elif n == 1:
            between = self.Moves_Between_Peices(self.ally_king[1:],check_attackers[0])
            # ss = pseudo_moves[1:] + legal_moves
            ss = pseudo_moves + legal_moves
            for i in ss:
                if check_attackers[0] in i:
                    legal_moves.append([i[0],check_attackers[0]])
                    # pseudo_moves.remove([j for j in pseudo_moves if j[0] == i[0]][0])
                t = []
                for j in between:
                    if j in i:
                        t.append(j)
                if t:
                    legal_moves.append([i[0]] + t)
            if king_moves:
                k = [self.ally_king]
                for i in king_moves[0][1:]:
                    new_board = self.Move([self.ally_king,i],True)
                    b = Board(new_board,self.color)

                    if not b.Check():
                        k.append(i)
                if len(k) > 1:
                    legal_moves.append(k)
        else:
            if king_moves:
                k = [self.ally_king]
                for i in king_moves[0][1:]:
                    new_board = self.Move([self.ally_king,i],True)
                    b = Board(new_board)
                    if b.color == 1:
                        b.color = 2
                    else:
                        b.color = 1
                    if not b.Check():
                        k.append(i)
                if len(k) >1:
                    legal_moves.append(k)
            return []
        legal_moves = [i for i in legal_moves if i]
        return legal_moves,pinned_peice

    def Check_Mate(self,legal_moves):
        if not legal_moves and self.check:
            return True

        return False

    def StaleMate(self,legal_moves):
        if not legal_moves and not self.check:
            return True
        return False
positions = [
            ['', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
            ['P', 'P', 'n', 'P', 'P', 'P', 'P', 'P'],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', 'P', '', '', ''],
            ['', '', '', '', '', '', 'p', ''],
            ['', '', '', '', '', '', '', ''],
            ['p', 'p', 'p', 'p', 'p', 'p', '', 'p'],
            ['r', 'n', 'b', 'q', '', 'r', 'k', '']]
import time
t1 = time.time()
a = Board(positions,1)
print(a.Legal_Moves())
print(time.time()-t1)
