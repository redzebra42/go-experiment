from go import *
from tkinter import *
from tkinter import ttk

if __name__ == "__main__":
    go = Go()
    root = Tk()
    root.geometry("1100x800")
    frm = ttk.Frame(root, padding=10)
    my_canvas = Canvas(root, width=1200, height= 800)

    def play():
        hand = text_box.get()
        coord = go.hand_to_coord(hand)
        if go.is_legal(coord):
            go.move(coord)
            go.capture(coord)
            go.next_turn(hand)
            go.board.print_tkinter_board(my_canvas)
        else:
            print("illegal move")

    text_box = Entry(my_canvas)
    text_box.place(x=810, y=120)

    pos_button = ttk.Button(my_canvas, text= "play", command = lambda: play())
    pos_button.place(x=850, y=165)

    go.board.print_tkinter_board(my_canvas)

    while True:
        root.mainloop()

