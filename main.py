from go import *
from tkinter import *
from tkinter import ttk

if __name__ == "__main__":
    go = Go()
    go.board.print_board()
    
    root = Tk()
    root.geometry("1100x800")
    frm = ttk.Frame(root, padding=10)
    my_canvas = Canvas(root, width=1200, height= 800)

    def play():
        hand = text_box.get()
        coord = go.hand_to_coord(hand)
        go.move(coord)
        go.capture(coord)
        go.next_turn(hand)
        go.board.print_tkinter_board(my_canvas)

    text_box = Entry(my_canvas)
    text_box.place(x=810, y=120)

    pos_button = ttk.Button(my_canvas, text= "play", command = lambda: play())
    pos_button.place(x=850, y=165)

    go.board.print_tkinter_board(my_canvas)

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
        root.mainloop()

