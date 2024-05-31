import copy
import random
from MCT import *
import MinMax
import matplotlib.pyplot as plt
import operator

def init_board(board):
    "initialize the board to the starting position"
    board[3][3], board[4][4], board[3][4], board[4][3] = 1, 1, 2, 2

class Oboard():

    def __init__(self, board=None, player=2, size=8, prev_move=None) -> None:
        self.board = copy.deepcopy(board)        #(0: empty, 1: white, 2: black, 3: legal move)
        if self.board == None:
            self.board = [[0 for i in range(8)] for j in range(8)]
            init_board(self.board)
        self.current_player = player
        self.size = size
        self.prev_move = prev_move
        self.sec_prev_move = None
        self.legal_moves()
        self.nb_coups = 0

    def curr_player(self):
        return self.current_player
    
    def clone(self):
        new_child = Oboard(self.board, self.current_player, self.size, self.prev_move)
        return new_child

    def int_to_player(self, n):
        if n == 0:
            return " "
        elif n == 1:
            return "O"
        elif n == 2:
            return "#"
        elif n == 3:
            return "."
        else:
            raise RuntimeError("n should be 0, 1 or 2")

    def print_board(self):
        print("  a b c d e f g h")
        for i in range(len(self.board)):
            print(i + 1, ("|".join(self.int_to_player(self.board[i][j]) for j in range(len(self.board)))))
    
    def neighbours(self, coord):
        '''Returns an array of neighbouring coordinates, of length 2 to 4.'''
        if coord[0] == 0:
            if coord[1] == 0:
                return [(0,1), (1,0)]
            elif coord[1] == self.size - 1:
                return [(0,self.size - 2), (1,self.size - 1)]
            else:
                return [(0, coord[1]-1),
                        (0, coord[1]+1),
                        (1, coord[1])]
        elif coord[0] == self.size - 1:
            if coord[1] == 0:
                return [(self.size - 1, 1), (self.size - 2, 0)]
            elif coord[1] == self.size - 1:
                return [(self.size - 1, self.size - 2), (self.size - 2, self.size - 1)]
            else:
                return [(self.size - 1, coord[1]-1),
                        (self.size - 1, coord[1]+1),
                        (self.size - 2, coord[1])]
        else:
            if coord[1] == 0:
                return [(coord[0]-1, 0), (coord[0]+1, 0), (coord[0], 1)]
            elif coord[1] == self.size - 1:
                return [(coord[0]-1, self.size - 1), (coord[0]+1, self.size - 1), (coord[0], self.size - 2)]
            else:
                return [(coord[0]-1, coord[1]),
                        (coord[0]+1, coord[1]),
                        (coord[0], coord[1]-1),
                        (coord[0], coord[1]+1)]
            
    def occupied_tiles(self):
        """retunrs dictionnary with 1: [list of white coords], 2: [list of black coords]"""
        occ_tiles = {1: [], 2: []}
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 1:
                    occ_tiles[1].append((i,j))
                elif self.board[i][j] == 2:
                    occ_tiles[2].append((i,j))
        return occ_tiles
    
    def opp_player(self):
        if self.current_player == 1:
            return 2
        else:
            return 1

    def legal_dirs(self, move):
        if self.board[move[0]][move[1]] in (0, 3):   #si la case est vide
            leg_directions = []
            if move[0] < self.size - 1:
                i = move[0] + 1
                while i < self.size - 1 and self.board[i][move[1]] == self.opp_player():
                    i += 1
                if (i != move[0] + 1) and (self.board[i][move[1]] == self.current_player):
                    leg_directions.append('U')
            if move[0] > 0:
                i = move[0] - 1
                while i > 0 and self.board[i][move[1]] == self.opp_player():
                    i -= 1
                if (i != move[0] - 1) and (self.board[i][move[1]] == self.current_player):
                    leg_directions.append('D')
            if move[1] < self.size - 1:
                j = move[1] + 1
                while j < self.size - 1 and self.board[move[0]][j] == self.opp_player():
                    j += 1
                if (j != move[1] + 1) and (self.board[move[0]][j] == self.current_player):
                    leg_directions.append('R')
            if move[1] > 0:
                j = move[1] - 1
                while j > 0 and self.board[move[0]][j] == self.opp_player():
                    j -= 1
                if (j != move[1] - 1) and (self.board[move[0]][j] == self.current_player):
                    leg_directions.append('L')
            if move[0] < self.size - 1 and move[1] < self.size - 1:
                i,j = move[0] + 1, move[1] + 1
                while i < self.size - 1 and j < self.size - 1 and self.board[i][j] == self.opp_player():
                    i += 1
                    j += 1
                if (i != move[0] + 1) and (self.board[i][j] == self.current_player):
                    leg_directions.append('DR')
            if move[0] < self.size - 1 and move[1] > 0:
                i,j = move[0] + 1, move[1] - 1
                while i < self.size - 1 and j > 0 and self.board[i][j] == self.opp_player():
                    i += 1
                    j -= 1
                if (i != move[0] + 1) and (self.board[i][j] == self.current_player):
                    leg_directions.append('DL')
            if move[0] > 0 and move[1] > 0:
                i,j = move[0] - 1, move[1] - 1
                while i > 0 and  j > 0 and self.board[i][j] == self.opp_player():
                    i -= 1
                    j -= 1
                if (i != move[0] - 1) and (self.board[i][j] == self.current_player):
                    leg_directions.append('UL')
            if move[0] > 0 and move[1] < self.size - 1:
                i,j = move[0] - 1, move[1] + 1
                while i > 0 and j < self.size - 1 and self.board[i][j] == self.opp_player():
                    i -= 1
                    j += 1
                if (i != move[0] - 1) and (self.board[i][j] == self.current_player):
                    leg_directions.append('UR')
            return leg_directions
        else:
            return []
    
    def is_legal(self, move):
        return move == "pass" or (len(self.legal_dirs(move)) != 0)
    
    def reverse(self, move, dir) -> list:
        reversed = []
        if dir == 'R':
            i = move[1] + 1
            while self.board[move[0]][i] == self.opp_player():
                reversed.append((move[0], i))
                self.board[move[0]][i] = self.current_player
                i += 1
        elif dir == 'L':
            i = move[1] - 1
            while self.board[move[0]][i] == self.opp_player():
                reversed.append((move[0], i))
                self.board[move[0]][i] = self.current_player
                i -= 1
        elif dir == 'U':
            i = move[0] + 1
            while self.board[i][move[1]] == self.opp_player():
                reversed.append((i, move[1]))
                self.board[i][move[1]] = self.current_player
                i += 1
        elif dir == 'D':
            i = move[0] - 1
            while self.board[i][move[1]] == self.opp_player():
                reversed.append((i, move[1]))
                self.board[i][move[1]] = self.current_player
                i -= 1
        elif dir == 'DR':
            i = move[0] + 1
            j = move[1] + 1
            while self.board[i][j] == self.opp_player():
                reversed.append((i, j))
                self.board[i][j] = self.current_player
                i += 1
                j += 1
        elif dir == 'UR':
            i = move[0] - 1
            j = move[1] + 1
            while self.board[i][j] == self.opp_player():
                reversed.append((i, j))
                self.board[i][j] = self.current_player
                i -= 1
                j += 1
        elif dir == 'DL':
            i = move[0] + 1
            j = move[1] - 1
            while self.board[i][j] == self.opp_player():
                reversed.append((i, j))
                self.board[i][j] = self.current_player
                i += 1
                j -= 1
        elif dir == 'UL':
            i = move[0] - 1
            j = move[1] - 1
            while self.board[i][j] == self.opp_player():
                reversed.append((i, j))
                self.board[i][j] = self.current_player
                i -= 1
                j -= 1 
        return reversed
    
    def legal_moves(self):
        leg_moves = []
        for i in range(self.size):
            for j in range(self.size):
                move = (i, j)
                if self.is_legal(move):
                    self.board[move[0]][move[1]] = 3
                    leg_moves.append(move)
                elif self.board[move[0]][move[1]] == 3:
                    self.board[move[0]][move[1]] = 0
        leg_moves.append('pass')
        return leg_moves
    
    def is_over(self):
        if self.prev_move == 'pass' and self.sec_prev_move == 'pass':
            return True
        elif len(self.legal_moves()) == 1:
            new_state = self.clone()
            new_state.play_at('pass')
            if len(new_state.legal_moves()) == 1:
                return True
        return False
    
    def score(self):
        b = 0
        w = 0
        for line in self.board:
            for stone in line:
                if stone == 1:
                    w += 1
                elif stone == 2:
                    b += 1
        return w - b
    
    def winner(self):
        '''return 1 for white, 2 for black, 0 for equal scores'''
        if self.is_over():
            score = self.score()
            if score > 0:
                return 1
            elif score < 0:
                return 2
            else:
                return 0
            
    def play_random(self):
        leg_moves = self.legal_moves()
        i = random.randint(0, len(leg_moves) - 1)
        self.play_at(leg_moves[i])

    def rand_simulation(self):
        while not self.is_over():
            self.play_random()

    def play_at(self, move):
        #modifie le state et renvois le sec_prev_move
        reversed = []
        if move == 'pass':
            self.current_player = self.opp_player()
            sec_move = self.sec_prev_move
            self.sec_prev_move = self.prev_move
            self.prev_move = move
            self.legal_moves()
            return sec_move, reversed
        else:
            leg_directions = self.legal_dirs(move)
            if len(leg_directions) != 0:
                for legal_dir in leg_directions:
                    reversed += self.reverse(move, legal_dir)
                self.board[move[0]][move[1]] = self.current_player
                self.nb_coups += 1
                self.current_player = self.opp_player()
                sec_move = self.sec_prev_move
                self.sec_prev_move = self.prev_move
                self.prev_move = move
                self.legal_moves()
                return sec_move, reversed
            else:
                print("illegal move from state")
                raise RuntimeError

    def unplay_at(self, move, sec_move, reversed):
        self.current_player = self.opp_player()
        self.prev_move = self.sec_prev_move
        self.sec_prev_move = sec_move
        for rev_move in reversed:
            self.board[rev_move[0]][rev_move[1]] = 3 - self.board[rev_move[0]][rev_move[1]]
        if move != 'pass':
            self.board[move[0]][move[1]] = 0
            self.nb_coups -= 1
        self.legal_moves()
    
    def play_at_and_print(self, move):
        self.play_at(move)
        self.print_board()

    def corners(self, max_player):
        corner_min = 0
        corner_max = 0
        for corner in [(0, 0), (0, 7), (7, 0), (7, 7)]:
            if self.board[corner[0]][corner[1]] == max_player:
                corner_max += 1
            elif self.board[corner[0]][corner[1]] == 3 - max_player:
                corner_min += 1
        if corner_max + corner_min != 0:
            return (corner_max - corner_min) / (corner_min + corner_max)
        else:
            return 0
    
    def mobility(self, max_player):
        mob_curr_player = len(self.legal_moves())
        tmp_state = self.clone()
        tmp_state.play_at('pass')
        mob_opp_player = len(tmp_state.legal_moves())
        if mob_curr_player + mob_opp_player == 0:
            return 0
        else:
            if self.current_player == max_player:     #if currnet player is MAX
                return (mob_curr_player - mob_opp_player) / (mob_curr_player + mob_opp_player)
            else:
                return (mob_opp_player - mob_curr_player) / (mob_curr_player + mob_opp_player)

    def parity(self):
        return self.nb_coups % 2
    
    def evaluation(self, max_player):
        corner_bias = 2
        mobility_bias = 1
        parity_bias = 1
        return (corner_bias * self.corners(max_player) + mobility_bias * self.mobility(max_player) + parity_bias * self.parity())
    
class Ogame():

    def __init__(self) -> None:
        self.state = Oboard()

        '''
        game class that has the following functions:
        X legal_moves(state) 
        X play_at(state, move)
        X is_over(state)
        X winner(state)
        X rand_simulation(state)
        X play_mct()
        state class with the following funcyions:
        X curr_player()
        X clone()
        '''
    
    def txt_move_to_coord(self, move):
        if move == 'pass':
            return move
        '''Convert a textual hand like c12 into coordinates like (2, 12).'''
        L = ['a','b','c','d','e','f','g','h']
        return (int(move[1:])-1, L.index(move[0]))
    
    def legal_moves(self, state):
        return state.legal_moves()
    
    def play_at(self, state, move):
        state.play_at(move)

    def is_over(self, state):
        return state.is_over()

    def winner(self, state):
        return state.winner()

    def rand_simulation(self, state):
        state.rand_simulation()
        return state
    
    def biased_minmax_simulation(self, state, bias, eval):
        MinMax.MinMaxNode(self, state).biased_minmax_simulation(bias, eval)
        return state

    def play_mct(self, state, coord, player):
        res = Oboard(state.board, player, state.size, state.prev_move)
        res.play_at(coord)
        return res
    
    def _mct_move(self, state, move):
        new_state = state.clone()
        new_state.curr_player = new_state.opp_player()
        new_state.prev_move = move
        new_state.legal_moves()
    
    def biased_rand_simulation(self, state, bias):
        #TODO extremement lent, voir pour enlever clone -> stocker l'état précédent ?
        while not state.is_over():
            moves = []
            for move in state.legal_moves():
                sec_move, reversed = state.play_at(move)
                moves.append((state.evaluation(state.current_player), move))
                state.unplay_at(move, sec_move, reversed)
            moves = sorted(moves, reverse=True, key=operator.itemgetter(0))
            moves = moves[:int(bias*len(moves))+1]
            move = random.choice(moves)[1]
            state.play_at(move)
        return state.winner()

def is_legal_test(board1):
    legal_board = [[None for i in range(board1.size)] for j in range(board1.size)]
    for i in range(board1.size):
        for j in range(board1.size):
            legal_board[i][j] = board1.is_legal((i, j))
    for i in range(len(legal_board)):
        for j in range(len(legal_board)):
            if legal_board[i][j]:
                board1.board[i][j] = 3


if __name__ == "__main__":
    game = Ogame()
    state = game.state
    mct = MCT(state, game)

    def play_at(coord, state=state):
        if state.is_legal(coord):
            game.play_at(state, coord)
            #state.print_board()
        else:
            print("illegal move from main")

    def tree_search(search_depth):
        mct.new_move(search_depth)
        #mct.state.print_board()

    def time_tree_search(sec, tree):
        tree.new_move_time(sec)
        #tree.root.state.print_board()

    def rand_vs_mct(n, time):
        mct_wins = 0
        j = 0
        k = 0
        while j < n:
            j += 1
            tree = MCT(Oboard(), Ogame())
            print("new game\n\n\n")
            while not tree.current_node.state.is_over():
                k += 1
                print("MCT move: ")
                chosen_node, chosen_move = tree.tree_search(tree.current_node, time)
                state = tree.current_node.state
                play_at(chosen_move, state)
                tree.current_node = chosen_node
                if not(tree.current_node.state.is_over()): 
                    leg_moves = tree.current_node.state.legal_moves()
                    i = random.randint(0, len(leg_moves)-1)
                    print("random move: ")
                    play_at(leg_moves[i], state)
                    tree.current_node = tree.current_node.enfants[leg_moves[i]]
                    print(leg_moves[i], " ", k)
            tree.state.print_board()
            if game.winner(tree.state) == 0:
                print("win")
                mct_wins += 1
        return mct_wins

    def graph_vs(from_itt, to_itt, incr_itt, nb_parties, minmax_level, eval_bias=False, bias=1):
        itt = from_itt
        x = []
        y = []
        while itt <= to_itt:

            mct_victories = 0

            for i in range(nb_parties):

                game = Ogame()
                state = game.state
                mct = MCT(state.clone(), game)
                minmax = MinMax.MinMaxNode(game, state)

                #randomly starts with mct or minmax
                if random.randint(0,1) == 0:
                    #minmax starts black
                    mct_player = 1
                    max_player = 2
                    move = minmax.minimax(state, max_player, minmax_level)[0]
                    play_at(move, state)
                    if move in mct.current_node.enfants.keys():
                        mct.current_node = mct.current_node.enfants[move]
                    else:
                        mct.current_node = mct.current_node.node_from_move(move)
                else:
                    #mct starts black
                    mct_player = 2
                    max_player = 1
                
                print("mct is ", mct_player)
                print("minmax is ", max_player)

                while not state.is_over():

                    #mct's turn
                    chosen_node, chosen_move = mct.tree_search(mct.current_node, itt, False, itt, eval_bias, state.evaluation, bias)
                    state = mct.current_node.state
                    play_at(chosen_move, state)
                    mct.current_node = chosen_node
                    if state.is_over():
                        break

                    #minmax's turn
                    move = minmax.minimax(state, max_player, minmax_level)[0]
                    play_at(move, state)
                    if move in mct.current_node.enfants.keys():
                        mct.current_node = mct.current_node.enfants[move]
                    else:
                        mct.current_node = mct.current_node.node_from_move(move)
                
                state.print_board()
                if state.winner() == mct_player:
                    print("winner is mct")
                    mct_victories += 1
                else:
                    print("winner is minmax")
            
            x.append(itt)
            y.append(100*mct_victories/nb_parties)
            print(x)
            print(y)
            itt += incr_itt

        return x, y

    def biased_graph(i_depart, i_arrive, incr, nb_parties, temps_parties, minmax_level):
        x, y = [], []
        i = i_depart
        while i <= i_arrive:
            i += incr
            mct_victories = 0
            for j in range(nb_parties):
                #initialisation des classes
                game = Ogame()
                state = game.state
                mct = MCT(state.clone(), game)
                minmax = MinMax.MinMaxNode(game, state)
                #alterne le premier joueur
                if i % 2 == 0:
                    #minmax starts black
                    mct_player = 1
                    max_player = 2
                    move = minmax.minimax(state, max_player, minmax_level)[0]
                    play_at(move, state)
                    if move in mct.current_node.enfants.keys():
                        mct.current_node = mct.current_node.enfants[move]
                    else:
                        mct.current_node = mct.current_node.node_from_move(move)
                else:
                    #mct starts black
                    mct_player = 2
                    max_player = 1
                #boucle pour une partie
                while not state.is_over():
                    #tour de mct
                    chosen_node, chosen_move = mct.biased_tree_search(mct.current_node, temps_parties, i)
                    state = mct.current_node.state
                    play_at(chosen_move, state)
                    mct.current_node = chosen_node
                    #state.print_board()
                    if state.is_over():
                        break
                    #tour de minmax
                    move = minmax.minimax(state, max_player, minmax_level)[0]
                    play_at(move, state)
                    if move in mct.current_node.enfants.keys():
                        mct.current_node = mct.current_node.enfants[move]
                    else:
                        mct.current_node = mct.current_node.node_from_move(move)

                state.print_board()
                if state.winner() == mct_player:
                    print("winner is MCT")
                    mct_victories += 1
                else:
                    print("winner is minmax")
            x.append(i)
            y.append(100*mct_victories/nb_parties)
            print(x)
            print(y)
        plt.plot(x ,y)
        plt.show()


    what_to_play = input(str("what do you want to play ? (mct/minmax/vs/graph)\n"))
    mct.state.print_board()

    if what_to_play == 'mct':

        while True:
            
            print(rand_vs_mct(4, 1))

            chosen_node, chosen_move = mct.tree_search(mct.current_node, 2)
            state = mct.current_node.state
            play_at(chosen_move, state)
            mct.current_node = chosen_node

            move = input(str('next move: '))

            if move == None:
                continue
            
            coord = game.txt_move_to_coord(move)
            play_at(coord, state)
            mct.current_node = mct.current_node.enfants[coord]
    
    elif what_to_play == 'biased mct':

        while True:
            
            print(rand_vs_mct(4, 1))

            def eval(state):
                return state.eval

            chosen_node, chosen_move = mct.tree_search(mct.current_node, 2, False, 100, True, eval, 1)
            state = mct.current_node.state
            play_at(chosen_move, state)
            mct.current_node = chosen_node

            move = input(str('next move: '))

            if move == None:
                continue
            
            coord = game.txt_move_to_coord(move)
            play_at(coord, state)
            mct.current_node = mct.current_node.enfants[coord]

    elif what_to_play == 'minmax':

        while True:
            max_player = 2

            minmax = MinMax.MinMaxNode(game, state)
            play_at(minmax.minimax(state, max_player, 3)[0])

            #Debug
            print(minmax.file)
            print("corners: ", state.corners())
            print("mobility: ", state.mobility())
            print("parity: ", state.parity())
            print("evaluation: ", state.evaluation())

            move = input(str('next move: '))
            if move == None:
                continue
            coord = game.txt_move_to_coord(move)
            play_at(coord, state)

            #Debug
            print("corners: ", state.corners())
            print("mobility: ", state.mobility())
            print("parity: ", state.parity())
            print("evaluation: ", state.evaluation())

    elif what_to_play == 'biased minmax':

        max_player = 2
         
        while True:

            minmax = MinMax.MinMaxNode(game, state)
            play_at(minmax.minimax(state, max_player, 1)[0])

            minmax = MinMax.MinMaxNode(game, state)
            coord = minmax.biased_minmax_simulation(state, 1, 0.5, state.evaluation)[0]
            play_at(coord, state)

    elif what_to_play == 'vs':

        #une partie (mct iter 2000 minmax 3) ~ 5 minutes
        
        while True:
            minmax = MinMax.MinMaxNode(game, state)

            #mct's turn
            chosen_node, chosen_move = mct.tree_search(mct.current_node, 2, True, 100)
            state = mct.current_node.state
            play_at(chosen_move, state)
            print(chosen_move)
            mct.current_node = chosen_node
            mct.pretty_print()
            
            #minmax's turn
            move = minmax.minimax(state, 2, 3)[0]
            play_at(move, state)
            print(move)
            if move in mct.current_node.enfants.keys():
                mct.current_node = mct.current_node.enfants[move]
            else:
                mct.current_node = mct.current_node.node_from_move(move)

    elif what_to_play == 'graph':

        minmax_level = 3
        x, y = graph_vs(4, 6, 1, 20, minmax_level)
        plt.plot(x, y)
        plt.xlabel("nombre d'itérations de MCT")
        plt.ylabel(f"{'%'} de victoires")
        plt.title(f"pourcentage de victoires de MCT contre minmax de profondeur {minmax_level}")
        plt.show()
    
    elif what_to_play == 'bias_graph':
        x, y = biased_graph(i_depart=0, i_arrive=0.8, incr=0.2, nb_parties=20, temps_parties=4, minmax_level=3)

    else:
            raise RuntimeError

