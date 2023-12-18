from MCT import *
from rand_game_trees import *
from matplotlib import pyplot as plt

if __name__ == "__main__":
    rgt = RGT()
    rgt_state = RGTstate()
    mct = MCT(rgt_state, rgt)
    #print(rgt_state.path(rgt_state.best_move)[0])
    #print(mct.tree_search(mct, 5))

    def test_graph_temps(board_size,val_up_to, t_up_to, nb_tests):
        #prend un peu plus de 5/2*nb_tests*(t_up_to²+t_up_to) secondes
        for i in range(1, val_up_to): #Boucle sur la valeur d'un bon coup
            y_list = []
            x_list = []
            for t in range(1, t_up_to): #Boucle sur la durée de chaque tests
                res = 0
                for k in range(nb_tests): #Boucle sur le nombre de tests par durées
                    best_move = random.randint(1, math.factorial(board_size))
                    state = RGTstate((0, 1), best_move, board_size, i)
                    game = RGT(state)
                    mct = MCT(state, game)
                    ts = mct.tree_search(mct, t)[1]
                    supp_move = state.path(best_move)[0]
                    print(i, t, k)
                    print(ts, supp_move)
                    if ts == supp_move:
                        res += 1
                x_list.append(t)
                y_list.append((res/nb_tests)*100)
            plt.plot(x_list, y_list)
        plt.show()

    def test_graph(board_size, val_up_to, parcour_up_to, nb_tests):
        for i in range(1, val_up_to): #Boucle sur la valeur d'un bon coup
            y_list = [0]
            x_list = [0]
            for t in range(100, parcour_up_to, 300): #Boucle sur le nombre de parours de l'arbre pour chaque tests
                clock = time.clock_gettime(0)
                res = 0
                for k in range(nb_tests - int(5*sqrt(t/100))): #Boucle sur le nombre de tests par parcours
                    if k%5 == 0:
                        print(k)
                    best_move = random.randint(1, math.factorial(board_size))
                    state = RGTstate((0, 1), best_move, board_size, i)
                    game = RGT(state)
                    mct = MCT(state, game)
                    ts = mct.tree_search(mct, None, True, t)[1]
                    supp_move = state.path(best_move)[0]
                    if ts == supp_move:
                        res += 1
                print(x_list)
                print(y_list)
                print(time.clock_gettime(0) - clock)
                print(nb_tests - int(5*sqrt(t/100)))
                clock = time.clock_gettime(0)
                x_list.append(t)
                y_list.append((res/(nb_tests - int(5*sqrt(t/100))))*100)
            plt.plot(x_list, y_list, label = str(i))
        plt.legend()
        plt.xlabel("nombre de parcours de l'arbre")
        plt.ylabel("pourcentage de bon coups")
        plt.title("Teste pour un plateau de taille " + str(board_size))
        plt.show()

    def test_win_rate(board_size, search_depth, nb_tests):
        nb_vict_1 = 0
        for i in range(nb_tests):
            best_move = random.randint(1, math.factorial(board_size))
            state = RGTstate((0, 1), best_move, board_size)
            game = RGT(state)
            mct = MCT(state, game)
            position = mct
            while not(state.is_over()):
                if state.current_player == 0:
                    position = mct.tree_search(position, None, True, search_depth)[0]
                    game.play_at(state, position.state.position)
                else:
                    move = random.choice(state.legal_moves())
                    game.play_at(state, move)
                    position = position.enfants[move]
                print(state.position)
            if state.winner() == 1:
                nb_vict_1 += 1
        return nb_vict_1/nb_tests

    print(test_win_rate(10, 3000, 100))
            



    #test_graph(81, 2, 5000, 54)
    #print(mct.tree_search(mct, None, True, 10000))

    #TODO graph ou autre pour mesurer l'accuracy en fonction de "l'étage" de l'arbre 
    #(pour voire si la recherche s'améliore significativement au fur et a mesure du temps)
    #en fait il suffit juste de faire des tests avec de tailles de plateaux différents sans doute (après ça test pas tout mais bon...)
'''
    plt.plot([0, 100, 400, 700, 1000, 1300, 1600, 1900, 2200, 2500, 2800, 3100, 3400, 3700, 4000, 4300, 4600], [0, 6.122448979591836, 22.727272727272727, 29.268292682926827, 43.58974358974359, 44.44444444444444, 50.0, 51.515151515151516, 54.83870967741935, 41.37931034482759, 53.57142857142857, 48.148148148148145, 44.0, 45.83333333333333, 43.47826086956522, 40.909090909090914, 38.095238095238095])
    plt.xlabel("nombre de parcours de l'arbre")
    plt.ylabel("pourcentage de bon coups")
    plt.title("Teste pour un plateau de taille 81")
    plt.show()'''

