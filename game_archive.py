from board import Board
class Game_archive():

    def __init__(self) -> None:
        self.SZ = None
        self.EV = None
        self.RO = None
        self.PB = None
        self.PW = None
        self.KM = None
        self.DT = None
        self.PC = None
        self.RE = None
        self.C = None
        self.board = Board([['0','0','0','0','0','0','0','0','0'],
                              ['0','0','0','0','0','0','0','0','0'],
                              ['0','0','0','0','0','0','0','0','0'],
                              ['0','0','0','0','0','0','0','0','0'],
                              ['0','0','0','0','0','0','0','0','0'],
                              ['0','0','0','0','0','0','0','0','0'],
                              ['0','0','0','0','0','0','w','0','0'],
                              ['0','0','0','0','0','0','0','0','0'],
                              ['0','0','0','0','0','0','0','0','0']], {'w': 0,'b': 0}, 'b')

    def sfg_to_move_list():
        file = open("Game_1.sgf", "r")
        line = file.readline()
        prev_line = None
        for line in file.readlines():
            pass
            

Game_archive.sfg_to_move_list()