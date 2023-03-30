from go import *
import tkinter as tk
from tkinter import ttk

if __name__ == "__main__":
    go = Go()
    go.board.print_board()
    go.print_tcltk()

    while True:
        go.root.mainloop()
        hand = input(str(go.current_player) + " to move: ")

        if hand == None:
            continue
        coord = go.hand_to_coord(hand)
        go.move(coord)
        go.capture(coord)
        go.next_turn(hand)

        print(go.territory('w'))
        go.board.print_board()
