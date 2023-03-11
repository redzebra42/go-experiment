import go

if __name__ == "__main__":
    go = go.Go()
    go.board.print_board()
    

    while True:
        hand = input(str(go.current_player) + " to move: ")

        if hand == None:
            continue

        go.move(hand)
        go.next_turn(go.current_player)
        

        go.board.print_board()
