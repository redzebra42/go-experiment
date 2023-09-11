class Game_archive():

    def __init__(self) -> None:
        pass

    def sfg_to_move_list():
        file = open("Game_1.sgf", "r")
        line = file.readline()
        while line != ";":
            print(line)
            line = file.readline()
        print(line)

Game_archive.sfg_to_move_list()