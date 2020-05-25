import sys
import random
import copy

def abstract(board, pattern):
    '''
      retorna la versión abstracta de board según pattern
    '''
    abstract_board = []
    for x in board:
        if x in pattern or x == 0:
            abstract_board.append(x)
        else:
            abstract_board.append(-1)
    return abstract_board

class Puzzle:
    goal15 = list(range(16))  # objetivo del 15-puzzle
    goal8 = list(range(9))    # objetivo del 8-puzzle
    MaxPDB = 5
    pdb = []           ## en mí código, yo usé estas líneas, si te hacen sentido, úsalas
    pdb_pattern = [[1, 4, 5], [2, 3, 6, 7], [8, 9, 12, 13], [10, 11, 14, 15]]
    #pdb_pattern = [[2, 3, 7, 11], [1, 3, 12, 15], [10, 11, 14, 15], [12, 9, 6, 3], [4, 5, 1]]   # si no te hacen sentido, haz lo que tú quieras
    for i in range(MaxPDB):
        pdb.append({})
        pdb_pattern.append(None)

    def __init__(self, board=None, blank=-1):
        if not board:
            self.x = 3
            self.size = 9
            self.board = [i for i in range(0, self.size)]
            self.blank = 0
        else:
            self.board = board
            if len(self.board) == 9:
                self.x = 3
                self.size = 9
            elif len(self.board) == 16:
                self.x = 4
                self.size = 16
            else:
                print('puzzle size not supported')
                sys.exit(1)
            if blank == -1:
                self.blank = board.index(0)

    def initialize_pdb(id):
        for i in range(id):
            filename = "pdba" + str(i+1) + ".txt"
            with open(filename, 'r', encoding='utf8') as file:
                for line in file:
                    line = line.rstrip("\n").split(" ")
                    Puzzle.pdb[i][" ".join(line[:-1])] = int(line[-1])

    def pdb_heuristic(self, id):
        board = [str(x) for x in abstract(self.board, Puzzle.pdb_pattern[id-1])]
        board = " ".join(board)
        cost = Puzzle.pdb[id - 1][board]
        return cost

    def pdb_1(self):
        return self.pdb_heuristic(1)

    def pdb_2(self):
        return self.pdb_heuristic(2)

    def pdb_3(self):
        return self.pdb_heuristic(3)

    def pdb_4(self):
        return self.pdb_heuristic(4)
    
    def pdb_5(self):
        return self.pdb_heuristic(5)

    ## acá, agrega más llamados si lo deseas!

    def pdb_final(self):
        return max(self.pdb_1(), self.pdb_2(), self.pdb_3(), self.pdb_4(), self.manhattan())

    def __hash__(self):
        return hash(tuple(self.board))

    def __eq__(self, other):
        return self.board == other.board

    def __repr__(self):
        def tostr(d):
            if d > 0:
                return "%2d" % (d)
            else:
                return "  "

        s = '\n'
        for i in range(0, self.x):
            s += "|"
            s += "|".join([tostr(d) for d in self.board[i*self.x:i*self.x+self.x]])
            s += "|\n"
        return s

    def zero_heuristic(self):
        return 0

    def incorrect_tiles(self):
        '''
            retorna el numero de piezas que no estan en la posicion correcta
        '''
        num = 0
        for i in range(0, self.size):
            if self.board[i] == 0:
                continue
            else:
                if self.board[i] != i:
                    num += 1
        return num

    def manhattan(self):
        '''
            retorna la suma de distancias manhattan de cada pieza a su
            posicion final
        '''
        num = 0
        for i in range(0, self.size):
            if self.board[i] == 0:
                continue
            else:
                num += abs(i % self.x - self.board[i] % self.x)
                num += abs(i // self.x - self.board[i] // self.x)
        return num

    def successors(self):
        '''
            Crea una lista de tuplas de la forma (estado, accion, costo)
            donde estado es el estado sucesor de self que se genera al ejecutar
            accion (un string) y costo (un numero real) es el costo de accion
        '''
        def create_child(newblank):
            child = copy.deepcopy(self)
            child.blank = newblank
            child.board[child.blank] = 0
            child.board[self.blank] = self.board[newblank]
            return child

        succ = []
        if self.blank > self.x - 1:
            c = create_child(self.blank-self.x)
            succ.append((c, 'up', 1))
        if self.blank % self.x > 0:
            c = create_child(self.blank-1)
            succ.append((c, 'left', 1))
        if self.blank % self.x < self.x - 1:
            c = create_child(self.blank+1)
            succ.append((c, 'right', 1))
        if self.blank < self.size - self.x:
            c = create_child(self.blank+self.x)
            succ.append((c, 'down', 1))
        return succ

    def is_goal(self):
        return self.size == 16 and Puzzle.goal15 == self.board or \
               self.size == 9 and Puzzle.goal8 == self.board
