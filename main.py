from go import *

if __name__ == "__main__":
    go = Go()
    go.board.print_board()
    

    while True:
        hand = input(str(go.current_player) + " to move: ")

        if hand == None:
            continue
        coord = go.hand_to_coord(hand)
        go.move(coord)
        go.capture(coord)
        go.next_turn(hand)

        print(go.territory('w'))
        go.board.print_board()
