size = 9
goban_1 = [['0','0','0','0','0','0','0','0','0'],
         ['0','b','b','0','0','b','b','b','b'],
         ['b','b','w','b','b','w','b','w','w'],
         ['b','w','w','w','w','w','w','w','w'],
         ['w','0','0','w','w','w','b','b','w'],
         ['w','w','w','w','w','b','0','0','b'],
         ['b','b','b','w','b','b','0','b','0'],
         ['w','0','b','w','w','b','b','0','0'],
         ['0','w','b','0','w','w','b','0','0']] 
goban_3 = [['0','0','0','0','0','0','0','0','0'],
         ['0','b','b','0','0','b','b','b','b'],
         ['b','b','w','b','b','w','b','w','w'],
         ['b','w','w','w','w','w','w','w','w'],
         ['w','0','0','w','w','w','b','b','w'],
         ['w','w','w','w','w','b','b','0','b'],
         ['b','b','b','w','b','b','0','b','0'],
         ['w','b','b','w','w','b','b','0','b'],
         ['0','w','b','0','w','w','b','b','0']]
goban_4 = [['0','0','b','w','0','0','b','0','b'],
         ['0','0','b','w','b','b','w','b','0'],
         ['0','b','b','b','w','w','w','b','b'],
         ['0','w','w','w','w','0','w','w','b'],
         ['0','w','b','b','w','b','0','w','w'],
         ['w','w','w','b','b','b','b','0','0'],
         ['0','w','w','b','w','w','b','b','b'],
         ['w','0','0','w','0','w','b','0','b'],
         ['0','w','0','w','w','0','w','b','0']]
starting_board_4 = [['0','0','0','0','0','0','0','0','0'],
         ['0','b','b','0','0','b','b','b','b'],
         ['b','b','w','b','b','w','b','w','w'],
         ['b','w','w','w','w','w','w','w','w'],
         ['w','0','0','w','w','w','b','b','w'],
         ['w','w','w','w','w','b','b','0','b'],
         ['b','b','b','w','b','b','0','b','0'],
         ['w','b','b','w','w','b','b','0','b'],
         ['0','w','b','0','w','w','b','b','0']]
starting_board_5 = [['0','0','0','0','0','0','0','0','0'],
         ['0','b','b','0','0','b','b','b','b'],
         ['b','b','w','b','b','w','b','w','w'],
         ['b','w','w','w','w','w','w','w','w'],
         ['w','0','0','w','w','w','b','b','w'],
         ['w','w','w','w','w','b','b','0','b'],
         ['b','b','b','w','b','b','b','b','b'],
         ['w','b','b','w','w','b','b','0','b'],
         ['0','w','b','0','w','w','b','b','b']]
prev_move_4 = [(6, 8), (8, 0)]
goban_2 = [['0' for i in range(size)] for j in range(size)]

goban = starting_board_5
caps = {'w': 0,'b': 0}
player = 'b'
two_prev_moves = prev_move_4